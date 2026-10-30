"""Read-only CSV audit. No game/save access, selectors, rankings or source edits."""
import argparse
import csv
import hashlib
import io
import json
import re
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path, PurePosixPath

SCHEMAS = {
    'gear_attributes.csv': 'gear_id,name,upgrade_display,damage,dps,range,armor_per_sec,armor,evade,source_image,review_status,notes',
    'gear_effects.csv': 'gear_id,effect_order,effect_text,source_image,review_status',
    'offensive.csv': 'name,element,damage,dps,range,crit,c_mul,ele_dmg,armor_mul',
    'defensive.csv': 'name,element,armor_gen,armor,can_dash,dash_cooldown,evade,engaging,note',
    'debuff.csv': 'name,debuff_type,strength,stack,duration,cooldown,chance',
}
NUMBERS = {
    'gear_attributes.csv': 'damage dps range armor_per_sec armor evade',
    'gear_effects.csv': 'effect_order',
    'offensive.csv': 'damage dps range crit c_mul ele_dmg armor_mul',
    'defensive.csv': 'armor_gen armor dash_cooldown evade engaging',
    'debuff.csv': 'strength stack duration cooldown chance',
}


def number(value, percent=False):
    """Blanks stay unknown. Only explicitly permitted '%' strings become fractions."""
    if value == '':
        return None
    is_percent = percent and value.endswith('%')
    token = value[:-1] if is_percent else value
    if not re.fullmatch(r'[0-9]+(?:\.[0-9]+)?', token):
        raise ValueError(f'invalid nonnegative decimal: {value!r}')
    try:
        result = Decimal(token)
    except InvalidOperation as exc:
        raise ValueError('invalid decimal') from exc
    return result / 100 if is_percent else result


def read_table(path, schema):
    raw = path.read_bytes()
    text = raw.decode('utf-8-sig', errors='strict')
    if '\x00' in text or '\ufffd' in text:
        raise ValueError(f'{path.name}: NUL or replacement character')
    reader = csv.reader(io.StringIO(text, newline=''), strict=True)
    header = next(reader, [])
    if header != schema.split(','):
        raise ValueError(f'{path.name}: schema changed: {header!r}')
    rows = []
    for row in reader:
        if len(row) != len(header):
            raise ValueError(f'{path.name}:{reader.line_num}: wrong column count')
        rows.append(dict(zip(header, row)))
    return rows, {
        'sha256': hashlib.sha256(raw).hexdigest(),
        'bytes': len(raw), 'encoding': 'UTF-8 BOM' if raw.startswith(b'\xef\xbb\xbf') else 'UTF-8',
        'rows': len(rows), 'columns': header,
    }


def family(name):
    # Comparison aliases only. Never Stonescript selectors or confirmed identities.
    name = name.casefold().replace('æ', 'ae').replace('tailsman', 'talisman')
    name = re.sub(r' [12]$', '', name)
    return {'quaterstaff': 'quarterstaff', 'dashstaff': 'quarterstaff',
            'fastgenshl': 'compound shield', 'bog': 'blade of the fallen god'}.get(name, name)


def comparisons(attributes, legacy, fields):
    """Many-to-many candidates. Never pick the first same-name variant."""
    result = []
    for index, old in enumerate(legacy, 2):
        candidates = []
        for new in attributes:
            if family(new['name']) != family(old['name']):
                continue
            differences, checked = {}, []
            for old_key, new_key in fields.items():
                a = number(old[old_key])
                b = number(new[new_key], percent=new_key == 'evade')
                if a is not None and b is not None:
                    checked.append(old_key)
                    if a != b:
                        differences[old_key] = {'legacy': old[old_key], 'screenshot_transcription': new[new_key]}
            candidates.append({'gear_id': new['gear_id'], 'checked_fields': checked, 'differences': differences})
        exact = [c['gear_id'] for c in candidates if c['checked_fields'] and not c['differences']]
        result.append({'legacy_row': index, 'name': old['name'], 'raw': old,
                       'status': 'numeric_profile_match' if exact else 'numeric_conflict' if candidates else 'no_family_candidate',
                       'matching_ids': exact, 'candidates': candidates})
    return result


def audit(root):
    root = Path(root)
    tables, files, errors, warnings = {}, {}, [], []
    for filename, schema in SCHEMAS.items():
        try:
            tables[filename], files[filename] = read_table(root / 'data/gears' / filename, schema)
        except (OSError, UnicodeError, csv.Error, ValueError) as exc:
            errors.append(str(exc))
    if errors:
        return {'errors': errors, 'warnings': warnings, 'files': files}
    for filename, rows in tables.items():
        for index, row in enumerate(rows, 2):
            for column in NUMBERS[filename].split():
                try:
                    number(row[column], percent=(filename == 'gear_attributes.csv' and column == 'evade'))
                except ValueError as exc:
                    errors.append(f'{filename}:{index}:{column}: {exc}')
            if not row.get('gear_id', row.get('name', '')):
                errors.append(f'{filename}:{index}: missing identifier/name')
            if filename == 'defensive.csv' and row['can_dash'] not in ('True', 'False'):
                errors.append(f'{filename}:{index}: invalid can_dash')
    if errors:
        return {'errors': errors, 'warnings': warnings, 'files': files}
    attrs, effects = tables['gear_attributes.csv'], tables['gear_effects.csv']
    by_id = {}
    for index, row in enumerate(attrs, 2):
        gid = row['gear_id']
        if not re.fullmatch(r'screenshot_[0-9]{4}', gid):
            errors.append(f'gear_attributes.csv:{index}: invalid gear_id')
        if gid in by_id:
            errors.append(f'duplicate gear_id: {gid}')
        by_id[gid] = row
        if not row['name'] or not row['upgrade_display'] or not row['review_status']:
            errors.append(f'{gid}: missing required metadata')
        if not re.fullmatch(r'\+[0-9]+/[0-9]+', row['upgrade_display']):
            warnings.append(f'{gid}: unfamiliar display upgrade; no star conversion')
        if row['evade'] and not row['evade'].endswith('%'):
            warnings.append(f'{gid}: evade has no explicit percent unit')
    grouped = defaultdict(list)
    keys = set()
    for index, row in enumerate(effects, 2):
        gid = row['gear_id']
        order = row['effect_order']
        if not re.fullmatch(r'[1-9][0-9]*', order):
            errors.append(f'gear_effects.csv:{index}: invalid effect_order')
            continue
        key = (gid, int(order))
        if key in keys:
            errors.append(f'duplicate effect key: {key}')
        keys.add(key)
        if gid not in by_id:
            errors.append(f'orphan effect: {gid}')
        elif row['source_image'] != by_id[gid]['source_image'] or row['review_status'] != by_id[gid]['review_status']:
            errors.append(f'{gid}: effect/image/status metadata mismatch')
        if not row['effect_text'] or not row['review_status']:
            errors.append(f'{gid}: empty effect text/status')
        grouped[gid].append(row)
    for gid in by_id:
        orders = sorted(int(r['effect_order']) for r in grouped[gid])
        if orders != list(range(1, len(orders) + 1)) or not orders:
            errors.append(f'{gid}: missing/noncontiguous effects')
    image_info = {}
    for row in attrs:
        relative = PurePosixPath(row['source_image'])
        if relative.is_absolute() or '..' in relative.parts or not relative.parts or relative.parts[0] != 'cropped' or '\\' in str(relative) or ':' in str(relative):
            errors.append(f'{row["gear_id"]}: unsafe/unrecognized image reference')
            continue
        path = root / 'photograph' / relative
        if not path.resolve().is_relative_to((root / 'photograph/cropped').resolve()):
            errors.append(f'{row["gear_id"]}: image escapes cropped directory')
            continue
        if path.is_file():
            raw = path.read_bytes()
            if not raw.startswith(b'\x89PNG\r\n\x1a\n'):
                errors.append(f'{row["gear_id"]}: not a PNG signature')
            image_info[str(relative)] = {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
        else:
            warnings.append(f'{row["gear_id"]}: image unavailable locally')
    repeated = {name: [r['gear_id'] for r in attrs if r['name'] == name]
                for name, count in Counter(r['name'] for r in attrs).items() if count > 1}
    for source, count in Counter(r['source_image'] for r in attrs).items():
        if count > 1:
            warnings.append(f'multiple equipment rows reference the same image: {source}')
    profiles = defaultdict(list)
    for row in attrs:
        profiles[tuple(row[k] for k in ('name', 'upgrade_display', 'damage', 'dps', 'range', 'armor_per_sec', 'armor', 'evade'))].append(row['gear_id'])
    offensive = comparisons(attrs, tables['offensive.csv'], {'damage': 'damage', 'dps': 'dps', 'range': 'range'})
    defensive = comparisons(attrs, tables['defensive.csv'], {'armor_gen': 'armor_per_sec', 'armor': 'armor', 'evade': 'evade'})
    debuffs = [{'legacy_row': i, 'raw': r, 'candidate_ids': [a['gear_id'] for a in attrs if family(a['name']) == family(r['name'])],
                'status': 'semantic_review_required'} for i, r in enumerate(tables['debuff.csv'], 2)]
    warnings.append('Numeric profile matches are not confirmed item identities or equivalent effect sets.')
    warnings.append('Effect prose, legacy ele_dmg/armor_mul/chance/duration units and variant bindings require semantic review.')
    return {
        'schema_version': 1, 'errors': errors, 'warnings': warnings, 'files': files,
        'summary': {'equipment_records': len(attrs), 'effect_fragments': len(effects), 'resolved_images': len(image_info),
                    'offensive': dict(Counter(r['status'] for r in offensive)), 'defensive': dict(Counter(r['status'] for r in defensive)),
                    'debuff_rows': len(debuffs), 'duplicate_names': repeated,
                    'identical_numeric_profile_groups': [g for g in profiles.values() if len(g) > 1],
                    'blank_numeric_fields': {k: sum(r[k] == '' for r in attrs) for k in NUMBERS['gear_attributes.csv'].split()}},
        'images': image_info,
        'equipment': [{'raw': r, 'effects': grouped[r['gear_id']], 'provenance': 'provisional_visual_transcription',
                       'owner_verified': False} for r in attrs],
        'comparisons': {'offensive': offensive, 'defensive': defensive, 'debuff': debuffs},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--write-audit', action='store_true', help='Write only artifacts/gear-reference-review/audit.json')
    args = parser.parse_args()
    result = audit(args.root)
    if args.write_audit:
        destination = args.root / 'artifacts/gear-reference-review/audit.json'
        if not destination.resolve().is_relative_to((args.root / 'artifacts').resolve()):
            parser.error('output escapes artifacts')
        if destination.exists() and destination.is_symlink():
            parser.error('refusing symlink output')
        # Source CSVs, screenshots and private inventories are never opened for writing.
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('summary', 'errors', 'warnings') if k in result}, indent=2))
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
