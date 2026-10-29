# Equipment selector validation

Status: source implemented and statically reviewed, **no in-game selector results yet**. Reviewed 2026-10-29 against the official manual displayed v4.35.2. B2.1, observer, Mind Stone text, gear CSVs, original export and normalized snapshot are unchanged. The diagnostic is prepared but has **not been installed into either game directory**.

## Evidence and boundaries

The [official manual](https://stonestoryrpg.com/stonescript/manual.html) documents `item.GetCount(criteria)` as inventory **copy count**, with zero for no match. It is not a list of matching instances or a count of normalized save records. `item.left` / `item.right` expose equipped descriptions; `.id` exposes item IDs and `.gp` gear power, neither documented as a unique saved-instance handle. Exact variant confirmation requires inventory inspection.

Official filters include elements, `*N` star level and `+N` enchantment bonus. Equip commands accept up to seven criteria, variable interpolation and exclusions. Examples demonstrate `-big`, `-socket`, `d_sword`, `dL` and `shiny`. Two-handed gear requires `equip`; `equipL` / `equipR` are one-handed commands. This is documented syntax, not evidence that each proposed item alias or combination matches this inventory. The manual does not provide an exhaustive mapping of internal save ability/enchantment codes, cosmetic fields or generated names to selectors. There is no documented arbitrary saved-record-ID selector or inventory-instance enumeration API used here. Native errors must be read in the game; this module cannot catch parser errors.

[Cobblestone's public source](https://github.com/alexbarker234/stonescript/blob/main/Cobblestone.txt) demonstrates narrowing duplicate gear using enchantment numbers, effect tokens (`D`, `dI`, `dU`, `dL`), and shiny/non-shiny filters. This is community implementation evidence, not a verified mapping from our `ra`, `sra` or `abs` fields. No code, timings or ranking policy were copied. Broad B2.1 criteria can select a low-quality duplicate; this milestone does not change B2.1.

## Inventory analysis and public matrix

All 130 top-level records were analyzed into 130 distinct raw-property profiles. Of 84 tentative equipment/tool records, 63 have explicit alias hypotheses and 21 remain deferred. Another 46 records are utility/material/consumable categories, with one unopened container kept separate. Nested treasure contents, resource buckets and seen history never create candidates; explicit stacks remain single records, not expanded copies.

The builder generated **94 queries**, of which **30** refer to multiple saved profiles. These are hypotheses associated with source evidence, not predicted native match counts. Profiles retain type, element, raw upgrade, both complete enchantment structures, abilities, shiny/appearance fields and source references privately. A shared profile would retain all duplicate source records. Tags, seeds, account fields and internal identifiers are never interpolated into generated Stonescript.

Matrix below is deliberately family-level and sanitized. `E` means a concrete documented element word (`poison`, `vigor`, `aether`, `fire`, `ice`); brackets and `N` are documentation placeholders, **not runnable selectors**. Exact per-case selectors, raw values, source pointers and test-result templates are in ignored private output. Primary/secondary counts refer to raw structures, not proven displayed enchantments. A raw `lv` is never converted into stars.

| Family (records) | Element scope | Observed raw upgrades | Primary/secondary structures | Proposed probe form | Static status | In-game matching | Exact item | Ambiguities |
|---|---|---|---|---|---|---|---|---|
| Sword (11) | Saved explicit element or absent | 1024,2048,4096,8192 | 9/9 | `[E] sword -big`; `[E] sword big`; `stone sword -big -socket` | Form reviewed; aliases unverified | NOT RUN | UNCONFIRMED | Large/basic/socketed variants; broad duplicates |
| Wand (15) | Saved explicit element or absent | 2,1024,2048 | 11/11 | `[E] wand` | Form reviewed; named/hidden aliases deferred | NOT RUN | UNCONFIRMED | Named variants may overlap broad wand filters |
| Crossbow (16) | Saved explicit element or absent | 4,1024,4096,8192 | 13/13 | `[E] crossbow`; `stone crossbow`; `repeating crossbow` | Form reviewed; aliases unverified | NOT RUN | UNCONFIRMED | Two-handed; broad overlaps |
| Hammer (6) | Saved explicit element or absent | 2048,8192 | 6/6 | `[E] hammer -heavy`; `heavy hammer` | Form reviewed; aliases unverified | NOT RUN | UNCONFIRMED | Heavy versus one-handed; variants |
| Shield (17) | Saved explicit element or absent | 2,1024,2048,4096 | 14/14 | `[E] shield`; `stone shield -socket`; `compound shield`; named shield probes | Form reviewed; English names unverified | NOT RUN | UNCONFIRMED | Same type/element duplicates; named aliases |
| Staff (8) | Saved explicit element or absent | 1024,4096 | 7/7 | `[E] staff`; `quarterstaff` | Form reviewed; hidden aliases deferred | NOT RUN | UNCONFIRMED | Two-handed; hidden variants |
| Special equipment (6) | No element inferred from internal name | 2048,4096 | 6/6 | Deferred | No generated aliases | NOT RUN | UNCONFIRMED | Need display names and hand behavior |
| Tools (5) | No element inferred | 2 where present | 0/0 | `shovel`; other aliases deferred | Shovel form reviewed | NOT RUN | UNCONFIRMED | Remaining tool semantics unresolved |
| Refinement probes | Explicit element only | Preserved privately | Both objects retained intact | Base plus `+N` from primary raw level; base plus `shiny` when raw flag true | Syntax documented; save-property translation **unverified** | NOT RUN | UNCONFIRMED | Secondary bonus/effect selection unknown; flag meaning unconfirmed |
| Future manual refinements | Confirmed display element | No raw conversion | Require displayed evidence | Base plus `*N`, `dL`, other verified effect tokens, exclusions | Templates only; not generated from raw codes | NOT RUN | UNCONFIRMED | Need displayed stars, enchantments/effects and duplicate comparison |

No star ranking, rarity, DPS, strongest-item decision or raw ability-to-modifier mapping is implemented. A +21 query is a test of a hypothesis, not proof that `ra.lv=21` maps to that native criterion. A count of one never automatically promotes exact-item status. A count greater than one may be identical copies or different variants.

## Generate/reproduce private probes

From the repository root, with Python 3.10+ (use your executable path if not on PATH):

```powershell
python -B tools/build_selector_candidates.py --inventory 'data/raw/player_save/derived/v1/<snapshot>/inventory.json'
python -B -m unittest discover -s tests -p 'test_*.py' -v
```

Choose the intended snapshot explicitly; do not automatically pick the newest export. Input must be an offline normalized snapshot inside the ignored private tree. Existing importer checks revalidate raw item fields; changed versions/schema, inconsistent identity/category, duplicate source references, unsafe strings and unignored/tracked private paths fail closed. Unknown aliases/elements are deferred. No active save is read and no normalized output is edited.

Output is deterministic under `data/raw/player_save/selector_validation/v1/<normalized-file-sha256>/`: `candidates.json` (private profiles/provenance and hypotheses), `Candidates.txt` (generated query/hand arrays), `summary.json` (fixed aggregate labels), and `results-template.json`. Same input reruns without rewriting intact outputs; changed/incomplete existing output is rejected. Keep all of these private. Copy the template to `results-local.json` in that same ignored directory before recording results; leave the generated template unchanged. Export array pointers and content hashes are evidence references, not stable game instance identifiers.

The existing `data/raw/player_save` ignore rule covers inputs, candidates and results; `/backups/` covers deployment backups. Do not force-add either tree. No ignore-rule change was necessary.

## Install the isolated diagnostic

The installer touches only the `EquipmentSelectorTest` namespace under the target Stonescript root. It requires count-only source, validates generated arrays, backs up and hash-checks any existing namespace before replacement, then verifies both installed files. It does not alter Mind Stone, SpeedRun or SpeedRunBasic. Existing unrelated files in that namespace are preserved. Backups have unique names under ignored `backups/selector-validation-*`.

```powershell
.\tools\Install-SelectorValidation.ps1 `
  -CandidatesDirectory 'data/raw/player_save/selector_validation/v1/<normalized-file-sha256>' `
  -StonescriptRoot 'E:\Steam\steamapps\common\Stone Story RPG\Stone Story_Data\StreamingAssets\Stonescript'
```

Use the same candidate directory and repeat for your existing save-folder Stonescript root if the Steam copy is not the one resolved by your game. Supply that root explicitly; the tool does not discover/read game saves. Both roots must use the same diagnostic files when testing. No actual game-root installation has been performed in this milestone.

## In-game acceptance sequence

1. Record installed build, commit, location/difficulty and candidate snapshot privately. Copy your entire current Mind Stone text to a safe local note before changing it. Begin with a safe Rocky Plateau difficulty you can survive with your existing loadout. Do not test unattended.
2. Temporarily replace Mind Stone text **yourself** with only `import EquipmentSelectorTest/main`. Never combine it with B2.1 or another equipment-writing script. Enable Mind Stone and enter a fresh run. Count-only overlay must appear, with `Allow equip: false`. No equipment change is expected from this module. Its first query runs once; no combat/survival policy is supplied.
3. Left/Right (default A/D or arrow keys) browse; Down (S/down arrow) recounts the selected query. Index is zero-based: index 0 is private case S001. Record selector and copy count for a broad query, its `+N` refinement and a shiny refinement where available. Compare to the inventory UI. Zero means absent or alias/filter mismatch; multiple means ambiguous copies/variants. Up then Enter in count-only mode must leave equipment unchanged. Record native errors (Tab) separately; zero count is not parser-error detection.
4. Only when ready for a supervised equip test, back up the installed diagnostic `main.txt` in each root. Set **only** `var allowEquip = true` in those diagnostic copies. Keep the repository default false. Reload in a fresh run; confirm overlay says true. This is the explicit controlled test mode. Native key bindings may also affect ordinary game controls; do not press potion/item-activation keys for this test.
5. Select a positive-count candidate. Press Up to arm, release, then press Enter once. One `equipL`, `equipR` or `equip` command is sent, with no ability activation. The overlay shows requested selector, live hands and samples taken on the following script frame. A new keypress sequence is needed for another test; browsing/recount/boundaries disarm it. Inspect the inventory's equipped item details manually: family, element, displayed stars, both enchantments, modifiers, appearance and distinguishing abilities. A description alone may omit distinguishing details. Two-handed candidates can clear/change both hands.
6. Test zero-match blocking, arrow cancellation after arming, repeated held Enter (no repeated command), and one-handed versus two-handed behavior. Compare broad and refined candidates against different known duplicate variants. If selection is wrong or descriptions are indistinguishable, report **unconfirmed/ambiguous**, not pass. Counts are cached until browse/recount; recount after inventory changes.
7. Stop on native errors or unexpected equipment changes. Capture the exact diagnostic file/line/message and last selector, action and hands; do not share save/profile/account fields. Leave the run or switch Mind Stone off if necessary. Native AI may continue attacking normally; the module does not disable AI or enforce a safe location. It never consumes potions or activates abilities.
8. When finished, restore `allowEquip = false` in diagnostic copies and your saved Mind Stone text. Restore your preferred loadout manually: equipment changes are not automatically rolled back. B2.1 may then be used unchanged; no candidate is integrated.

Report each case as: `case/index; selector; hand; count; before/after hands; displayed stars/enchantments/effects; intended variant; exact match yes/no/uncertain; errors/unexpected behavior`. Include build/commit, difficulty, manual changes and whether the request was armed/sent. Record results in the private JSON copy, and share only sanitized observations. Do not paste the save or entire candidates file. Tests do not require completing the map.

## Verification and next gate

23 automated Python tests pass, including the existing importer suite and synthetic candidate/schema/privacy/determinism checks, plus an actual PowerShell installer run against a temporary fake game directory proving backup preservation, hash-matched copying and untouched unrelated Mind Stone fixture. The existing B2 static checker passes. Private generation/repeat produced the same 94 probes. This is **not Stonescript interpreter execution**. Helper/import forms, indentation, key inputs and APIs were checked against documentation; game parsing, copy counts, hand selection, one-shot timing and exact variants remain untested.

Next gate: owner-confirmed import/count-only safety, then controlled exact-variant checks beginning with sword, wand and shield families used by B2.1. Collect displayed properties before introducing star/effect refinements. Integrate only individually confirmed selectors in a separate future milestone. Observer lifecycle, timing, completion, loops and location completion statuses remain unchanged.
