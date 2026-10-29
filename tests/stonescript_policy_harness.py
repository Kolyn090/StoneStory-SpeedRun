"""Test-only evaluator for this candidate's tiny syntax subset, NOT a game interpreter.

Runs the actual function source against fake native state. It cannot validate game
parsing, item search semantics, frame scheduling, real var lifetime or physics.
Local var declarations must have no initializer; our functions explicitly assign
before use. Unknown syntax fails rather than being silently ignored.
"""
import re
from types import SimpleNamespace


class Text(str):
    def __eq__(self, other):
        return str(other) in str(self)
    def __ne__(self, other):
        return not self == other
    def __add__(self, other):
        return Text(str(self) + str(other))
    __hash__ = str.__hash__


class Array(list):
    def Count(self): return len(self)
    def Add(self, value): self.append(value)
    def Clear(self): self.clear()


class Strings:
    calls = 0
    @staticmethod
    def Equals(a, b): return str(a) == str(b)
    @staticmethod
    def ToLower(value): return Text(str(value).lower())
    @staticmethod
    def IndexOf(value, part): return str(value).find(str(part))
    def Split(self, value, *separators):
        self.calls += 1
        discard = separators[-1] is True
        separators = separators[:-1] if type(separators[-1]) is bool else separators
        pieces = re.split("|".join(re.escape(str(x)) for x in separators), str(value))
        return Array(Text(x) for x in pieces if x or not discard)


def load_module(path, native):
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    fields, functions = set(), set()
    for line in lines:
        if line.startswith("var "): fields.add(line.split()[1])
        if line.startswith("func "): functions.add(line[5:].split("(")[0])
    names = fields | functions

    def expr(text):
        tokens = re.findall(r'"[^"\n]*"|>=|<=|[A-Za-z_]\w*|\s+|.', text)
        result = []
        previous = ""
        for token in tokens:
            original = token
            if token.startswith('"'):
                token = "Text(" + token + ")"
            elif token in ("true", "false"):
                token = token.capitalize()
            elif token in names and previous != ".":
                token = "self." + token
            elif token == "&": token = " and "
            elif token == "|": token = " or "
            elif token == "!":
                token = " not " if previous in ("", "(", "[", "&", "|", ",") else " != "
            elif token == "=": token = " == "
            result.append(token)
            if original.strip(): previous = original
        return "".join(result).strip()

    body = ["class Module:", " def __init__(self):"]
    for line in lines:
        if line.startswith("var "):
            name, value = line[4:].split(" = ", 1)
            value = expr(value)
            if value.startswith("["): value = "Array(" + value + ")"
            body.append("  self." + name + " = " + value)
    for line in lines:
        if not line.strip() or line.lstrip().startswith("//") or line.startswith("var "):
            continue
        indent = len(line) - len(line.lstrip())
        code = line.strip()
        prefix = " " * (indent + 1)
        if code.startswith("func "):
            signature = code[5:]
            name, params = signature[:-1].split("(")
            body.append(" def " + name + "(self" + (", " + params if params else "") + "):")
        elif code.startswith("var "):
            if "=" in code: raise ValueError("Local initializer lifetime is outside the test subset")
        elif code.startswith(":?"):
            body.append(prefix + "elif " + expr(code[2:]) + ":")
        elif code == ":": body.append(prefix + "else:")
        elif code.startswith("?"):
            body.append(prefix + "if " + expr(code[1:]) + ":")
        elif code.startswith("for "):
            match = re.fullmatch(r"for (\w+) = (.+)\.\.(.+)", code)
            if not match: raise ValueError("Loop outside test subset")
            var, begin, end = match.groups()
            body.append(prefix + f"for {var} in range({expr(begin)}, ({expr(end)}) + 1):")
        elif code.startswith("return"):
            body.append(prefix + "return " + (expr(code[7:]) if len(code) > 6 else "None"))
        elif code == "activate potion": body.append(prefix + "item.activations.append('potion')")
        elif " = " in code:
            left, right = code.split(" = ", 1)
            body.append(prefix + expr(left) + " = " + expr(right))
        elif re.fullmatch(r"[\w.]+\(.*\)", code): body.append(prefix + expr(code))
        else: raise ValueError("Unknown test subset statement: " + code)
    namespace = dict(native, Text=Text, Array=Array)
    exec("\n".join(body), namespace)
    return namespace["Module"]()


class Foe:
    def __init__(self, value="", buffs="", armor=0, hp=100):
        self.value = value
        self.buffs = SimpleNamespace(string=Text(buffs))
        self.armor, self.hp = armor, hp
    def __bool__(self): return bool(self.value)
    def __eq__(self, tag): return str(tag) in self.value


class Items:
    def __init__(self, counts):
        self.counts, self.queries, self.activations = counts, [], []
        self.potion = Text("empty")
    def GetCount(self, selector):
        self.queries.append(str(selector))
        return self.counts.get(str(selector), 0)
    def CanActivate(self): return True
