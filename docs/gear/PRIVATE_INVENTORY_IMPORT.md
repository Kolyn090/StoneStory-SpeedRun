# Private offline inventory importer

The standard-library Python importer in `tools/import_player_inventory.py` reads only an explicitly selected offline JSON export under `data/raw/player_save/`. It never discovers, reads or writes the active game save. It produces data, not Stonescript code, selectors or combat policy.

## Run after exporting a save

1. Finish exporting/decrypting a save and copy it into `data/raw/player_save/` as a new `.json` file. Keep the original export unchanged; do not use the active game's save path or a symlink to it.
2. From the repository root, run with Python 3.10+:

   ```powershell
   python -B tools/import_player_inventory.py --input data/raw/player_save/save-10-29.json
   ```

   Substitute your new export's filename on later runs. If Python is not on PATH, invoke your local Python executable using PowerShell's `& 'path-to-python.exe'` prefix. No pip packages or network connection are required. Git must be available on PATH for the privacy checks.

3. A successful run prints a sanitized JSON summary. Find detailed output under:

   ```text
   data/raw/player_save/derived/v1/<source-sha256>/inventory.json
   data/raw/player_save/derived/v1/<source-sha256>/summary.json
   ```

Both input and all generated files are private and Git-ignored. The importer rejects any tracked private file or unignored input/output path before reading the save. It does not run `git add` or edit the index. Do not force-add private files. Git ignoring is version-control protection, not encryption or access control; folder permissions/backups remain your responsibility.

The actual source hash and detailed raw item values are stored only inside the private inventory. No full source path, player profile, root authentication/account fields, timestamps, Mind Stone contents or loadout display names are copied into output. `raw_record` preserves all fields of each inventory item, including customization/unknown values; therefore **never publish `inventory.json`**. Unknown inventory-level fields are also retained privately. The summary includes no arbitrary raw IDs, ability strings, custom text or checksum.

## Normalized schema v1

| Output section | Meaning |
|---|---|
| `inventory_records` | All top-level `inventory_data.itms` records; current inspected export has 130. Do not hard-code that count for future exports |
| `raw_record` | Exact parsed record, preserving absent fields, values, duplicate types and variants |
| Raw convenience fields | Type ID, element, ability codes, upgrade value, both enchantment objects and quantity; no derived stars, rarity, stats or selectors |
| `stack_count_field_present` | Whether `co` was explicitly saved. Missing quantity is null in the convenience field, not guessed as one; the raw record distinguishes absence |
| `category_tentative` | Reviewed type-ID classification: weapon/shield families, tools, utilities, materials/consumables, unopened treasure, or unclassified. This is a heuristic, not an authoritative ownership/rarity schema |
| `resource_buckets_raw` | Separate inventory-level resource fields. `None` is preserved as an undecoded bucket |
| `unopened_contents` | Separate nested item-shaped records with parent/source pointers; excluded from direct top-level inventory counts. The raw parent also retains contents for lossless preservation |
| `seen_item_history_raw` | Separate seen-ID history; never merged into owned inventory |
| `equipment_references_raw` | Undecoded right/optional left references. No claim of exact equipped-instance resolution |
| `unmapped_inventory_fields` / `unknown_data_fields` | Future fields retained privately and flagged; not assigned guessed semantics |

The category dictionary describes record families, not individual-copy counts. A sword record can also be a stack. Quantity is never expanded into rows. The raw flag `hI` and raw randomization/signature fields are preserved without treating them as definitive ownership or unique instance keys.

### Determinism and comparisons

JSON keys are sorted and output has fixed formatting, with no generated time or absolute path. Records sort by type, canonical record hash and source pointer. Identical records remain separate with an occurrence counter. Each also retains its original source-array pointer.

Same input bytes and importer version produce the same files. Reimporting an intact existing snapshot is a no-op and does not rewrite timestamps. Different exports produce separate source-hash directories; existing differing/incomplete files are never overwritten. If interrupted output is incomplete, preserve it and investigate before manually choosing a recovery procedure; the importer will not delete it.

A content hash is **not** a stable game instance ID. A modified item changes hash, and an array reorder changes source pointers. Compare multisets of record hashes to identify unchanged records regardless of array order; inspect unmatched records as possible changed/added/removed items, not proof of unique-instance identity. No automated diff UI or watcher is implemented yet.

## Validation and schema evolution

- Accept strict UTF-8 (optional UTF-8 BOM), one complete JSON document, finite numbers and valid Unicode scalars. Reject duplicate keys anywhere, malformed/trailing JSON and excessive size/nesting.
- Require recorded save version `4.35.2`, inventory/list/reference fields, item `id`/`da` and required raw flags. Check known field types, positive saved quantity/upgrade values, enchantment structure and ability-code arrays.
- Unknown item types, elements or extra inventory/item fields are preserved and counted as warnings. No untrusted raw values or field names appear in CLI errors/summary. A warning is a review request, not a newly verified meaning.
- Changed known field types, missing required fields or another recorded version fail closed. Review the verification report and synthetic fixtures before deliberately updating the versioned schema/category dictionary. Do not merely bypass validation to import a new build.
- Root fields outside inventory are intentionally ignored for privacy; the importer is not a full game-save validator. Nested treasure records only receive dictionary/nonempty-ID checks because their detailed schema is not established.

No item counts, stat formulas or matching rules are inferred from catalog assumptions. `AEther` is preserved as raw text and summarized under a fixed `aether` label; this does not create a runtime equipment alias.

## Tests

```powershell
python -B -m unittest discover -s tests -p 'test_import_player_inventory.py' -v
```

Fixtures are synthetic and run in temporary folders. Tests cover malformed JSON, duplicate object keys, missing fields, changed types/version, unknown-field preservation, repeated types/exact duplicates, raw upgrade/enchantment retention, stack/content/history separation, sanitized summaries, deterministic snapshots, immutable reruns, input path boundaries and Git privacy rejection. They do not read the private real save or run the game.

## Initial local import

The verified `save-10-29.json` is imported separately from synthetic tests. Validate that the output has 130 top-level records, 2 nested content records and 281 seen entries; those are observations of this export, not future schema constraints. A second import must leave output bytes and timestamps unchanged. Original input and gameplay/deployment hashes are checked separately.

The initial local run produced all 130 records, 74 distinct type IDs, 37 explicitly counted stack records, 6 separate resource buckets, 2 nested contents, and 281 seen-history entries. It found 13 repeated-type groups and 25 repeated-type/element groups, with no identical complete records and no schema warnings. Modifier summary reports 69 primary and 67 secondary structures, including 67 pairs of raw level-21 values. These are successful data-import checks, not game/selector verification.

## Still needs in-game verification

Displayed star/rarity mapping from `lv`, meanings of `ra`/`sra` subfields, effect strength/chance/duration, exact duplicate discrimination, hand references and English selector aliases remain unresolved. The pipeline supplies raw evidence for future equipment selection but does not modify B2.1 or establish a successful equipment selector. See [PLAYER_SAVE_VERIFICATION.md](PLAYER_SAVE_VERIFICATION.md).

## Refresh after crafting, upgrading or renaming

Keep two layers separate:

| Layer | Meaning and maintenance |
|---|---|
| `data/gears/gear_attributes.csv` + `gear_effects.csv` | Configuration/display evidence, not owned-copy counts. Keep screenshot IDs, special-effect fragments and verification provenance. Do not duplicate a stat row merely because an identical copy is crafted. New/different upgrades, enchantments or abilities need separate evidence; never silently merge by name. |
| Private normalized `inventory.json` | Current export's owned records, exact duplicate occurrences, raw stack quantities, upgrades/enchantments/elements/ability structures and source references. Preserve all records, but do not equate record/stack counts with independently equippable copies. |

The existing importer already preserves multiple identical records and distinct raw variants. No CSV or normalized-output schema migration is needed. New synthetic tests cover crafting an identical record and renaming without losing its raw configuration or leaking names in summaries. The importer remains read-only and does not generate native selectors or displayed stats.

1. Export/decrypt a **new offline** JSON copy into ignored `data/raw/player_save/`, with a new filename, for example `save-2026-10-30.json`. Preserve older exports. Never point the importer at the active game save.
2. From the repository run `python -B tools/import_player_inventory.py --input data/raw/player_save/save-2026-10-30.json`. Existing privacy/schema checks apply; another save version requires review, not bypassing validation. The new source hash creates another immutable `derived/v1/<source-hash>/` snapshot. An identical rerun is a no-op. Do not edit the previous normalized inventory.
3. Compare records as multisets of content fingerprints and raw configuration fields; compare quantities separately. Content fingerprints change after renaming/upgrading and are **not permanent instance identities**. Source pointers/indices are snapshot-local references only. Unknown enchantment/signature fields must not be discarded to force a configuration merge. A repeated raw record is preserved evidence, not proof of two native hands.
4. Existing screenshot-derived records remain authoritative only for the displayed fields actually inspected. If crafting produces the same displayed configuration, reuse that configuration evidence for another owned record after review. If attributes differ, capture the new description and preserve the distinct configuration/provenance; do not invent new values from raw levels. No automatic save-to-screenshot instance join is claimed.
5. Restart the Rocky candidate so preparation rechecks **native** inventory counts. For two Vigor recovery items, distinguish selectors where possible and verify two physical copies can stay equipped simultaneously; identical-name allocation can also be supported after that observation. Only then set the scoped `dualVigorVerified` flag. Keep the conservative one-Vigor + offense fallback until confirmed; clear the flag when changing relevant gear/criteria. No broad selector campaign or runtime CSV parser is required.

No tool update is needed merely to add an owned copy: the existing normalized record list already supports this. Raw `co` quantities, duplicate records and seen history remain separate evidence classes. Do not multiply gear-stat rows or treat stacked units as individual equipment instances. All private inputs/outputs remain Git-ignored; no fresh personal export was generated by this implementation task.
