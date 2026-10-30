"""Check/package an offline Rocky candidate. Never installs, stages or edits game files."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

OWN = ["main.txt", "config/RockySettings.txt", "equipment/RockyGear.txt",
       "locations/RockyPlateau.txt"]
BASE = ["main.txt", "config/Settings.txt", "equipment/Catalog.txt",
        "combat/Generic.txt", "locations/Dispatcher.txt"]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def inspect(root):
    root = root.resolve()
    paths = {"SpeedRunRocky/" + p: root / "scripts/rocky" / p for p in OWN}
    paths.update({"SpeedRunBasic/" + p: root / "scripts/basic" / p for p in BASE})
    paths["SpeedRun/metrics/RunMetrics.txt"] = root / "scripts/metrics/RunMetrics.txt"
    data = {}
    for name, path in paths.items():
        require(path.resolve().is_relative_to(root), "Source escapes project.")
        data[name] = path.read_bytes()
    for name in ("SpeedRunRocky/" + p for p in OWN):
        text = data[name].decode("utf-8-sig")
        code = []
        for line in text.splitlines():
            require("\t" not in line and (len(line) - len(line.lstrip(" "))) % 2 == 0,
                    "Candidate indentation contract failed.")
            if line.lstrip().startswith(("//", ">")):
                continue
            code.append(re.sub(r'"[^"\n]*"', '""', line))
        cleaned = "\n".join(code)
        for left, right in (("(", ")"), ("[", "]")):
            require(cleaned.count(left) == cleaned.count(right), "Unbalanced candidate delimiter.")
        for module in re.findall(r"^\s*(?:var\s+\w+\s*=\s*)?(?:new|import)\s+([\w/]+)", text, re.M):
            require(module + ".txt" in paths, "Unresolved candidate import.")
    main = data["SpeedRunRocky/main.txt"].decode()
    handler = data["SpeedRunRocky/locations/RockyPlateau.txt"].decode()
    equipment = data["SpeedRunRocky/equipment/RockyGear.txt"].decode()
    tick = handler.split("func Tick(", 1)[1]
    require(re.search(r'\?string.Equals\(locations.handler, "rocky"\)\s+'
                      r'rockyHandled = rocky.Tick\([^\n]+\)\s+\?!rockyHandled\s+'
                      r'combat.Tick\(gear, config\)', main), "Rocky dispatch/ownership guard missing.")
    require(main.count("combat.Tick(") == 1 and main.count("metrics.Observe()") == 1,
            "Duplicate shared policy or observer call.")
    require(main.count("rocky.Reset()") == 3, "Entry/loop/attachment resets missing.")
    require(re.search(r'\?!initialized\s+rocky.Reset\(\)', main.split(":?loc.loop", 1)[0]),
            "Repeated begin must not erase the latched boss context.")
    require("return false" not in tick.split("gear.ClearRequest()", 1)[1],
            "Handled frame may fall through after equipment ownership.")
    require('bossLatched & !foe' in tick and 'phase = "transition-gap"' in tick and 'HoldTransition(gear, equipment)' in tick,
            "Missing-target boss transition guard missing.")
    require(not re.search(r"(?:^|\n)\s*(?:equip\w* |brew |loadout |activate (?!potion))", handler),
            "Unexpected native equipment/ability command in Rocky policy.")
    require(not re.search(r"foe\.(state|time)\s*[=<>!]|item.GetCount|\bharvest\b", handler),
            "Unverified timer, per-frame inventory query or harvesting policy.")
    require('string.Equals(tokens[n], "adaptive_defense_" + equipment.elements[i])' in handler,
            "Adaptive UID exact-token guard missing.")
    require('physicalOnly = unknownAdaptive | (phase = "unknown")' in handler,
            "Unknown-phase/adaptive fallback missing.")
    require("Available(" not in equipment.split("func FromChoices", 1)[1],
            "Selection must not search inventory every frame.")
    require('loc.stars ! profile.targetStars' in tick, "Target difficulty guard missing.")
    require('gear.Apply(' not in handler and 'gear.ApplyPair(weapon, equipment.shield)' in handler,
            "Specialized frame must retain the Rocky shield, not shared defaults.")
    profile = data["SpeedRunRocky/config/RockySettings.txt"].decode()
    require('var targetStars = 15' in profile and 'var useHealingSword = false' in profile,
            "R15 scope or stable damage defaults changed.")
    require('var fastGenShieldConfirmed = true' in profile and 'var preferredShield = "FastGenShl"' in profile
            and 'item.GetCount(selector) = 1' in equipment,
            "Owner-confirmed nickname or ambiguous gear guard missing.")
    return data


def prepare(root):
    data = inspect(root)
    manifest = {"format_version": 1, "candidate": "Rocky R15; NOT GAME VERIFIED",
                "files": {name: hashlib.sha256(value).hexdigest() for name, value in sorted(data.items())}}
    raw = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode()
    key = hashlib.sha256(raw).hexdigest()
    target = (root / "artifacts/rocky-r1" / key).resolve()
    require(target.is_relative_to(root.resolve()), "Artifact path escapes project.")
    files = {"manifest.json": raw}
    files.update({name: value for name, value in data.items() if name.startswith("SpeedRunRocky/")})
    if target.exists():
        require(all((target / name).is_file() and (target / name).read_bytes() == value
                    for name, value in files.items()), "Existing bundle differs; preserve it and review.")
    else:
        target.mkdir(parents=True)
        for name, value in files.items():
            path = target / name
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(value)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true", help="Build under ignored artifacts/, never game directories")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        inspect(root)
        if args.prepare:
            target = prepare(root)
            print("Prepared: " + str(target.relative_to(root)))
        print("PASS: source contracts/imports; shared dependencies included in manifest. No game parser or installation.")
        return 0
    except (ValueError, OSError, UnicodeError) as error:
        print("Candidate rejected: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
