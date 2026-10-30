"""Check owned Markdown links/anchors and explicit docs/*.md references, offline."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit

EXCLUDED = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', 'backups',
            'deployments', 'artifacts', '.local'}


def owned(path, root):
    parts = path.relative_to(root).parts
    return not (set(parts) & EXCLUDED or parts[:3] == ('data', 'raw', 'player_save'))


def without_fences(text):
    return re.sub(r'^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$', '', text, flags=re.M | re.S)


def prose(text):
    text = without_fences(text)
    return re.sub(r'`[^`\n]+`', '', text)


def slug(text):
    text = re.sub(r'<[^>]*>', '', text).strip().lower()
    text = ''.join(c for c in text if c.isspace() or c in '-_' or unicodedata.category(c)[0] in 'LNM')
    return re.sub(r'\s', '-', text)


def anchors(text):
    result, counts = set(), Counter()
    for heading in re.findall(r'^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$', without_fences(text), re.M):
        key = slug(heading)
        count = counts[key]
        result.add(key + ('-' + str(count) if count else ''))
        counts[key] += 1
    result.update(re.findall(r'<a\s+(?:id|name)=[\"\']([^\"\']+)', text, re.I))
    return result


def check(root):
    root = Path(root).resolve()
    files = sorted(p for p in root.rglob('*') if p.is_file() and p.suffix.lower() == '.md' and owned(p, root))
    errors, checked, external, explicit = [], 0, 0, 0
    texts = {p: p.read_text(encoding='utf-8-sig') for p in files}
    anchor_cache = {p: anchors(t) for p, t in texts.items()}
    for source, text in texts.items():
        clean = prose(text)
        targets = re.findall(r'!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)(?:\s+[^)\n]*)?\)', clean)
        targets += re.findall(r'^\s*\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)', clean, re.M)
        for token in targets:
            raw = token[1:-1] if token.startswith('<') else token
            url = urlsplit(raw)
            if url.scheme or url.netloc:
                external += 1
                continue
            if not url.path and not url.fragment:
                continue
            checked += 1
            path = unquote(url.path)
            target = ((root / path.lstrip('/')) if path.startswith('/') else source.parent / path).resolve() if path else source
            label = source.relative_to(root).as_posix()
            if not target.is_relative_to(root):
                errors.append(f'{label}: local link escapes repository: {raw}')
            elif not target.exists():
                errors.append(f'{label}: missing target: {raw}')
            elif url.fragment and target.suffix.lower() == '.md' and owned(target, root):
                if target not in anchor_cache:
                    anchor_cache[target] = anchors(target.read_text(encoding='utf-8-sig'))
                if unquote(url.fragment) not in anchor_cache[target]:
                    errors.append(f'{label}: missing anchor: {raw}')
        # These paths explicitly declare repository-root context, including in code.
        for reference in set(re.findall(r'\bdocs/[A-Za-z0-9_./-]+\.md\b', text)):
            explicit += 1
            if not (root / reference).is_file():
                errors.append(f'{source.relative_to(root).as_posix()}: missing explicit doc reference: {reference}')
    return {'markdown_files': len(files), 'local_links_checked': checked,
            'explicit_doc_references_checked': explicit,
            'external_links_not_fetched': external, 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = check(args.root)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
