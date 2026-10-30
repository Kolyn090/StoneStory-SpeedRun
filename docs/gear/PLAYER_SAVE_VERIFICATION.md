# Private player save verification

> Dated evidence report of the initial offline export, not a current directory listing or game-load certification. Use [the importer workflow](PRIVATE_INVENTORY_IMPORT.md) for regeneration; private original/derived data stays unchanged.

Inspection date: 2026-10-29. Scope: local, read-only structural and inventory analysis. No raw save upload, game import, active-save edit, selector generation, combat change, or deployment was performed. This report contains schema names, sanitized aggregates and generic item-type examples, not player names, account identifiers, custom tag text, random seeds, or embedded scripts.

## Input and privacy

| File under `data/raw/player_save/` | Size | Detected format |
|---|---|---|
| `save-10-29.json` | 138,428 bytes | One UTF-8 JSON document, no BOM; CRLF line endings |

One regular file was present; no additional files/subdirectories were found. The existing, locally modified `.gitignore` already contains `data/raw/player_save`, which excludes the directory and nested files. `git ls-files` returns no files in this directory; the available local Git history contains no matching path. No index cleanup or history rewrite is needed. This cannot establish what exists in inaccessible remote history or other clones.

The existing ignore rule was preserved without further edits. It can still be bypassed by `git add -f`; raw data must remain private. No commit or push was made. A private input checksum was retained for before/after verification, without publishing it here. The file bytes were unchanged after inspection.

## Structural validation

The local validation used strict UTF-8 decoding and JSON parsing with duplicate-key detection, nonstandard numeric-constant rejection, and additional type/finite-number checks. The entire document was consumed, not merely an initial readable fragment.

| Check | Result |
|---|---|
| Strict UTF-8 decoding | PASS; no UTF-8/UTF-16 BOM and no NUL bytes |
| JSON syntax / complete document | PASS; no syntax error, unterminated record or trailing document detected |
| Duplicate JSON object keys | 0 |
| Root | Object with 26 fields |
| Nested tree | 704 objects and 92 arrays |
| Invalid surrogate code units | 0 |
| Non-finite floats | 0 among 328 float values |
| Null values | 0; missing optional fields still occur |
| Main inventory | Array of 130 objects; all have nonempty string `id` and object `da` |
| Observed inventory field checks | No violations for positive integer `co`/`lv` when present, string ability-code lists, or integer `lv`/`ql`/`sSS` enchantment subfields |
| Nested treasure contents | Two additional item-shaped dictionaries with nonempty IDs; do not automatically count as unpacked owned gear |
| Exact duplicate top-level records | 0 |

The root `version` is the literal string **`4.35.2`**. Treat this as a recorded version, plausibly the writing game build; no separate, authoritative save-format revision was identified. It does not prove which build is currently installed or that the file has never been edited.

No structural sign of truncation/corruption was detected by these checks. There is no authoritative game-save schema or game loader test behind that statement. Omitted optional fields, encoded references, very high quantities and unknown field meanings are semantic uncertainties. Successful parsing does **not** establish authenticity, valid checksums, progression consistency, successful game loading, or compatibility with every game version. Do not replace the active save to test this report.

## Inventory: directly observed fields versus interpretation

The main collection is `inventory_data.itms`. It contains 130 records spanning 74 distinct `id` values. This is an inventory-record count, not 130 unique weapon instances: resources, stacks, utilities and a treasure container are included. `inventory_data.itmsSeen` contains 281 entries and must not be substituted for the owned collection.

| Field | Observed structure | Meaning / confidence |
|---|---|---|
| `id` | String on every record | Internal item-type identifier; repeated IDs prove it is not a universal unique instance ID |
| `da` | Object on every record | Nested saved item data |
| `co` | Positive integer on 37 records | Likely stack quantity; missing does not independently prove quantity one. Values reach hundreds of thousands, so never expand stacks into individual rows without a cap |
| `da.hI` | Boolean, true on all 130 records | Undecoded flag; its name is not sufficient evidence for rarity, ownership rules, or equip state |
| `da.rng` | Integer on every record | Likely randomization/seed input; not an account ID, but preserve privately and do not treat as damage or a stable unique key |
| `da.lv` | Positive integer on 84 records | Raw level/upgrade representation. All observed values are powers of two, ranging from 2 to 8192; **not validated as displayed star counts** |
| `da.ra`, `da.sra` | Objects on 69 and 67 records | Each has integer `lv`, `ql`, `sSS`; likely primary/secondary enchantment data. Meaning/formulas of `ql` and `sSS` are not established |
| `da.el` | String on 65 records | Explicit saved element labels: Poison, Vigor, AEther, Fire, Ice |
| `da.abs` | String array on 51 records; 23 distinct codes | Internal effect/variant identifiers, including lifesteal, chill, burn-like and elemental-damage names; names alone do not quantify mechanics |
| `da.hidAb` | True on 15 records | Likely hidden-ability flag; exact gameplay meaning unverified |
| `da.sh` | True on 17 records | Likely shiny marker; confirm in item UI/native matching |
| `da.c` | Present on 5 records, including golden/prismatic values | Appearance/customization metadata, not proven rarity |
| `da.tag` | String on 2 records | Potential user customization text; deliberately withheld |
| `da.sig` | String on 15 records | Undecoded signature/discriminator; not assumed globally unique or accepted as a selector |
| `da.lC`, `da.lBU` | Integer on 7 records each | Undecoded counters; retained as unknowns rather than renamed as stats |

There is no explicit field named `rarity`, `stars`, `star_level`, `damage`, `dps`, `armor`, `range`, `duration`, or `cooldown` in the inventory `da` records. Those values may be derived from type metadata, upgrade state, abilities and game formulas. This inspection did not decode them. Cosmetic appearance and raw upgrade/enchantment fields must not be relabeled as rarity.

67 records have **both** `ra.lv = 21` and `sra.lv = 21`. Two additional `ra` objects contain other levels. That supports the existence of a substantial dual-level-21 equipment collection, but does not validate a universal +21/21 assumption or establish every item's displayed modifier.

### Equipment families and variants

Observed internal families include socketed crossbows, one-handed swords, long swords, hammers and shields; ordinary/hidden wands and staves; compound, bashing, dashing and tower shields; quarterstaff, heavy hammer, Bardiche, Skeleton Arm, talismans, a cult mask and a blade item. Utility/tool records include a shovel, Mind Stone, Triskelion Stone and other game objects. This is class-level evidence of equipment in the collection, not proof that a proposed English selector matches it.

Examples of variant evidence: socketed crossbows carry different `abs` combinations, including an `_2` elemental-damage code versus elemental-damage plus an on-hit effect; elemental shields likewise have alternative ability-code sets. Hidden-wand/staff families have IDs different from their likely displayed names. Keep these records distinct.

13 type-ID groups and 25 type-plus-element groups have multiple top-level records. None of the complete records is byte-content-equivalent after canonical JSON comparison. Repeated types/elements are expected duplicate/variant candidates, not malformed duplicate keys. Retain raw record identity plus modifiers and quantities; do not collapse by family/element or assume catalog labels “1”/“2” identify the corresponding records.

### Equipped items and loadouts

- `inventory_data.rightH` is present as a string reference. It is **not** an exact match to any top-level `id` or `da.sig` alone. A known shovel-type prefix is present, suggesting a shovel-family right-hand reference, but the encoded-reference format and exact instance remain unresolved.
- No `leftH` field is present in this snapshot's `inventory_data`. This alone does not prove an empty left hand or two-handed mode.
- `utility_belt.loadouts` has six unique loadout indexes; `utility_belt.sel` points to an existing index. Entries use `rightHand`/`leftHand` and display-name fields, with some omitted/empty slots.
- Some loadout references directly match known type IDs, while others are composite references. Display-name fields may contain user customization and were not published.
- A selected saved loadout is not proof that its equipment was actually active at save time. Exact hand/instance reconstruction needs validated reference decoding plus a game UI cross-check.

## Comparison with the existing catalogs

Reviewed: `data/gears/offensive.csv` (46 rows), `defensive.csv` (20), `debuff.csv` (30), and the inventory note's +21/21 assumption. These files remain unchanged.

A local, **tentative** family/element alias comparison found counterparts for all 46 offensive and 20 defensive rows. This is not a verified one-to-one import: 14 offensive and 12 defensive rows had multiple possible saved records under that coarse mapping. The mapping was used for analysis only; no normalized inventory or selector file was generated.

| Catalog concept | Save comparison / limit |
|---|---|
| Five elemental sword/wand/hammer/crossbow/shield families | Family/element records are present; modifiers, levels and duplicate identity must refine the match |
| “Big” swords and special named staves/wands | Long-sword and hidden-family IDs are plausible counterparts; English display-name aliases remain unvalidated |
| `Quaterstaff`, `Tailsman`, `BoG` and other shorthand | Catalog spelling/abbreviations are not authoritative internal IDs or native query terms |
| +21/21 baseline | 67 records have both saved level fields at 21; other records differ or omit those fields |
| DPS, damage, armor, evade, cooldown and effect strength | No directly corresponding expanded stat table exists in the inspected item records. Numeric CSV values cannot be independently verified from this export alone |
| Debuff rows | Ability-code names provide qualitative counterparts for effects such as lifesteal/chill/burn-like effects; strength, chance, stacks and duration are not independently validated |

## Stonescript compatibility and B2.1

The [official manual](https://stonestoryrpg.com/stonescript/manual.html) documents criteria-based `equip`, `equipL`, `equipR`, variable interpolation, negative criteria, star/enchantment filters and `item.GetCount`. It does not document this decrypted-save schema or promise that an internal ID is a valid equipment query. `item.left`/`item.right` and loadout queries can help inspect actual equipped identities during a separately authorized validation step.

B2.1 uses English criteria such as family/element terms, excludes big/heavy variants where intended, checks availability at initialization, and falls back to broad defaults. The save provides promising counterparts for its core weapon/shield families and optional utilities. However:

- Internal IDs such as `socketed_crossbow`, `blade_of_god`, `cult_mask`, `tower_shield`, `wand_hidden_*` and `shovel_lv1` require a reviewed alias layer; replacing underscores with spaces is not a validated translator.
- Saved `AEther` and runtime/user-facing spelling need explicit normalization rather than blind string reuse.
- Effects in `abs` are internal codes, not automatically native enchantment/modifier criteria.
- `da.lv` cannot yet produce a trustworthy `*N` filter; saved `ra`/`sra` numbers cannot yet produce a fully verified modifier expression.
- Signature/name/skin/shiny metadata might distinguish variants, but must be tested for native matching. Broad B2.1 defaults can still choose a different duplicate than intended.

**No selectors were generated or installed.** Static save analysis does not establish native selector acceptance, successful equipment switching, or game completion.

## Suitability and next steps

**Suitable now:** a private normalized representation of observed item types, elements, raw upgrades/enchantments, ability codes, quantities and unknown fields, with provenance and uncertainty labels.

**Not yet suitable:** authoritative computed stats, displayed rarity/stars, exact equipped-instance recovery, automatic selector generation, or replacing the current gear catalogs without further validation.

Recommended reproducible pipeline, to implement in a later milestone:

1. Take an explicitly chosen offline export; never read/write the active game save automatically. Keep originals under the ignored private directory.
2. Run a local read-only importer with strict encoding/JSON/schema checks and a private source checksum. Reject/flag duplicate keys, changed shapes and unresolved required data; never log arbitrary raw payloads or user tags.
3. Extract an allowlisted inventory schema only. Keep raw type, element, level/enchantment structures, ability codes, quantity presence and source record path. Distinguish owned top-level records, stacks, unopened contents and seen-item history. Preserve unknowns; do not silently default quantity, star levels, or rarity.
4. Use a versioned, reviewed alias/field dictionary. Separate observed values, inferred meanings, derived stats and validated runtime matching. Keep source checksums and potentially identifying metadata in ignored private output, not public reports.
5. Generate deterministic private output under `data/raw/player_save/derived/` (already ignored), with stable ordering and explicit duplicate handling. Do not use randomization fields as universal instance IDs; retain snapshot-local row identity until a stable reference format is validated.
6. Compare a few representative items against the game UI: ordinary and socketed weapons, a hidden variant, two near-duplicates, shield, tool, raw `lv`, both enchantments and current hands. Record exact build and observations without changing the active save.
7. Only after separate authorization, validate a reviewed alias through native availability counts and controlled equip/hand inspection. Counts establish matching presence, not exact intended identity; actual item verification is required. Promote selectors only after evidence, keeping generated output separate from combat policy.
8. On future exports, rerun the same versioned importer and produce a sanitized added/removed/changed summary. A changed recorded version or field shape should trigger review before regeneration proceeds. Never auto-deploy regenerated gear data to a live script.

No importer, normalized inventory, watcher, or selector generator was implemented by this verification task. Game loading, save authenticity, semantic field mappings and runtime selector behavior remain separate validation work.
