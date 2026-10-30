# Gear reference validation and integration review

**Owner correction (2026-10-29): FastGenShl is a Towering Shield nickname, not Compound Shield.** The owner also reports it can be used as an in-game name reference. Earlier Compound-to-0010 identity/probe suggestions in this historical review are superseded; do not use Compound queries to identify FastGenShl. Keep screenshot 0010 and 0065 stat/effect profiles separate. Existing private crosswalk files are preserved historical hypotheses and must not be treated as corrected exact-instance joins. See [current R15 selector policy](../rocky/ROCKY_PLATEAU_15.md).

Reviewed 2026-10-29. Scope: offline reference data only. No CSV corrections, gameplay changes, selector generation, deployment, staging, commits or pushes are part of this review.

## Result

The new tables contain **65 equipment-description records and 258 ordered effect fragments**. All 65 source references resolve beneath `photograph/cropped`. Both new CSVs are well-formed UTF-8 with BOM. The legacy tables are UTF-8: 46 offensive, 20 defensive and 30 debuff rows. These are overlapping views of equipment, not 96 distinct items.

All five tables were read completely. Automated structural validation found no malformed rows, invalid numeric tokens, duplicate primary/effect keys, orphan effects, missing required metadata, mismatched effect/image references or gaps in per-item effect ordering. The local PNG files have valid PNG signatures; that check alone is not a full image decode. Twenty-seven targeted screenshots were actually opened and visually inspected, as recorded below. The remaining 38 images were not visually rechecked in this review.

The structure is suitable as a **lossless provisional reference**, but it is not yet safe input to an equipment ranking or selector generator. The largest risks are legacy semantic column errors, variant binding, omitted effect qualifiers and unconfirmed identity links. No source wins automatically when records conflict.

## Inputs and reproducibility

| Source | Rows | SHA-256 |
|---|---:|---|
| `data/gears/gear_attributes.csv` | 65 | `1d516f4a353f487b2b86768f736adb834b171e51692e05fd0aa67d709f0a93db` |
| `data/gears/gear_effects.csv` | 258 | `0cbe6f8c50eebb23afbc421567449bc1213f2abdccdcf7cc475851e9c6574b86` |
| `data/gears/offensive.csv` | 46 | `841c93bd88887a3281845b6290f95c83ce3a8801e6080cc7782391ec6bc35f28` |
| `data/gears/defensive.csv` | 20 | `fa159f53da0ee23212ea0d549ebf07983f15258268da8881cd27856853e97c8c` |
| `data/gears/debuff.csv` | 30 | `9fb6f6523ccc5d3ff87f89a3fbdb02f91013fd85eb87bb3b333d34a79f84af72` |

From the repository root, using Python 3 (substitute a local Python executable if necessary):

```powershell
python -B tools/validate_gear_references.py
python -B tools/validate_gear_references.py --write-audit
python -B -m unittest discover -s tests -p test_gear_references.py -v
```

Default execution reads the five CSVs and their referenced cropped images, and prints counts/errors/warnings. `--write-audit` writes deterministic JSON only to `artifacts/gear-reference-review/audit.json`, already Git-ignored. It retains all raw rows/effect text, CSV row references for legacy comparisons, CSV/image hashes and many-to-many comparison candidates. It never reads a private inventory, active save or game installation. Re-running replaces this generated audit, not the inputs. Keep a copy of an audit outside that output filename if comparing revisions.

Exit 0 means structural checks passed, **not** that transcription, identity, effects or gameplay have been verified. Exit 1 reports structural errors. Missing local images are warnings so a source-only checkout can still be audited; inspect `resolved_images` before claiming screenshot availability. Unexpected columns fail closed rather than disappearing during import. All 30 debuff rows remain explicitly `semantic_review_required` in the machine audit; the human comparison is below.

## Schema, units and variant preservation

`gear_attributes.gear_id` is the primary key. `gear_effects.(gear_id,effect_order)` identifies ordered fragments. Each effect references the same source image/status as its equipment row. The IDs are screenshot references, not saved-instance IDs, Stonescript IDs or selectors. IDs 0010, 0011 and 0015–0077 are present; numbering gaps do not establish missing inventory records.

All 65 `upgrade_display` values are `+21/21`. Preserve this display string. It is not a derived star level or a raw-save upgrade conversion. Item rarity, base family, hand occupancy, capture build, screenshot date, account-wide modifiers and unique owned-instance identity are not explicit columns. Do not infer them from name color, MAX labels or equal stats. Screenshot records are not proof of 65 distinct physical inventory instances.

| Field | Interpretation and policy |
|---|---|
| `damage`, `dps` | Displayed Damage and Dmg/Sec values; do not assume DPS includes crit, weakness, splash, debuffs, buffs or activation damage |
| `range` | Displayed range; mapping to practical attack/engagement distance still needs game observation |
| `armor_per_sec`, `armor` | Displayed Armor/Sec and Armor, separate from conditional engaging armor and damage reduction |
| `evade` | Explicit percentage text in the new table (15%/30%); legacy defensive table uses fractions (.15/.3). Audit normalizes only for comparison and preserves raw strings |
| `effect_text` | Provisional transcription/paraphrase, not a complete executable rule or native filter string |
| blank numeric cells | Absent/unknown/not applicable; never silently zero |
| `notes`, `review_status` | Preserve verbatim, including clipping uncertainty; do not promote after a numeric match |

Blank numeric counts: damage/DPS/range each 17; armor generation/armor each 44; evade 55. These are not 17/44/55 corrupt items. Utility items can have effects without base combat stats. Eleven rows already flag potentially clipped lower text: 0034, 0035, 0047–0051, 0057, 0058, 0061, 0063.

There are nine repeated-name groups: Poison/Vigor/Fire/Ice Crossbows and all five elemental Shields. Three same-name groups also have identical displayed numerical profiles: Fire Crossbow 0020/0021, Ice Crossbow 0022/0023 and Vigor Shield 0038/0039. Their effect lists distinguish them. Never deduplicate by name, stats, family or upgrade string. Matching screenshot IDs must remain distinct until independent evidence proves duplication.

For comparison only, the tool folds `Æther`/`Aether`, `Tailsman`/`Talisman`, and legacy `Quaterstaff` spelling. It proposes `DashStaff` ↔ Quarterstaff and `BoG` ↔ Blade of the Fallen God as tentative aliases. FastGenShl ↔ Towering Shield is now owner-confirmed base-family information; the previous Compound association is superseded. Custom-name screenshots confirm the custom names and stats, not the underlying base-family identity. DashStaff and BoG remain hypotheses, even when numerical profiles match. The owner-confirmed FastGenShl family still does not identify a unique saved instance. None is a Stonescript selector.

## Comparison with the legacy tables

### Base numerical profiles

42/46 offensive rows have at least one same-family candidate matching **damage, DPS and range**. After the owner correction, 19/20 defensive rows have at least one candidate matching available **armor generation, armor and evade**. A blank new value is excluded from comparison, not treated as a match to legacy zero. These results include the explicit tentative aliases above. They do not compare effects, prove item identity, or certify 42/19 records as correct. The legacy Compound Shield row now has no family candidate. FastGenShl matches the Towering family but conflicts numerically with the legacy 14-armor profile; the separate 0065 profile still matches that legacy row. This replaces the earlier 20/20 result based on the incorrect alias.

The four offensive exceptions are:

| Legacy row | Screenshot-derived evidence | Disposition |
|---|---|---|
| Aether Crossbow 1: 80 damage, 88.89 DPS | 0019: 17 damage, 85 DPS, 33% crit, x6, +93 against Fire | Its high-physical profile is absent from this screenshot set. Do not replace legacy variant 1 with 0019 or claim the item is not owned |
| Fire Crossbow 1: 80 damage, 88.89 DPS | 0020 and 0021: 17 damage, 85 DPS | Two distinct low-physical variants. 0020 has +6 vs Ice and Burn; 0021 transcription has +93. High-physical profile not captured |
| Ice Crossbow 1: 80 damage, 88.89 DPS | 0022 and 0023: 17 damage, 85 DPS | 0022 has +6 vs Poison and Chill; 0023 transcription has +93. High-physical profile not captured |
| BoG: 500 damage, 275 DPS | 0058: 550 damage, 275 DPS | 550/275 visually confirmed. Legacy 500 remains preserved as conflicting evidence; no historical cause inferred |

Fire Crossbow 2 and Ice Crossbow 2 each have two base-profile matches, so base stats cannot select an exact variant. Both legacy Vigor Shield rows match both 0038/0039 numerically; their 1.8/7.2 conditional armor and healing distinguish them. The other shield pairs differ in evade (15% versus 30%) as well as conditional armor/effects.

Three new families have no counterpart in any of the old tables: Ice Staff 0046, Crossbow 0076, Stone Crossbow 0077. The legacy debuff-only Vigor Staff and Aether Staff have no same-family screenshot record. Do not relabel Big Swords, named staffs or other lifesteal/unmake items to fill these gaps. The Æther Crossbow high-physical configuration is missing, while Fire/Ice screenshot variants do not reproduce the legacy high-physical configurations. This is reference coverage, not an ownership audit.

### Incorrect classifications and effect differences

| Legacy field/records | New description | Assessment |
|---|---|---|
| `armor_mul`: all five elemental Swords | +85 or +9 damage against a named elemental foe | Flat conditional damage, not an armor multiplier. Poison and Fire sword screenshots directly confirm +85 |
| `armor_mul`: all five elemental Wands | +100 against a named elemental foe | Flat conditional damage. Poison Wand directly confirms +100 |
| `armor_mul`: Calamity/Explosive/Frost/Plague/Reset Wands | +6 against a named elemental foe | Flat conditional damage according to transcription; targeted confirmation still needed |
| `armor_mul`: Infernal/Eternity/Berserker/Prevention Staff | +9 against a named elemental foe | Flat conditional damage according to transcription; Infernal/Eternity screenshots confirm +9 |
| `ele_dmg=2.8`: Heavy Hammer | 2.8x damage to armored foes | Actual armor multiplier, misclassified as elemental damage; directly visible in 0061 |
| Hammer `armor_mul`: Poison/Æther/Fire/Ice 6.6, Vigor 2.4 | x damage to armored foes | Correct category according to transcription. Fire Hammer directly confirms 6.6x; not equivalent to elemental bonus |
| Aether Crossbow 2 `ele_dmg=6` | 0019: +93 against Fire | Directly confirmed conflict |
| Fire/Ice Crossbow 2 `ele_dmg=6` | One +6/status variant and one +93 variant per element | Legacy row may correspond to the status variant. Do not assign +93 solely from the numeric profile |
| Infernal Staff active legacy debuff row `strength=25,stack=5,duration=10,cooldown=30` | Gain 4 attack speed, self Burn 5 damage every 2 seconds, buff duration 10s, cooldown 30s | Different dimensions/target. 25 may be an old calculation but is undocumented; do not silently interpret as verified total damage or five stacks |
| Staff splash 50% | Ice/Grasping/Eternity/Berserker/Prevention transcriptions say 50%; Infernal also says 50% | Infernal screenshot 0048 does not visibly contain the claimed splash line. Preserve as unsupported transcription claim pending full description; absence in a crop does not establish false |
| Feeble/Weaken | Legacy labels several -4 effects `feeble`; new descriptions say Weaken | Do not merge status identities merely because both reduce damage. Cultist Mask explicitly describes Feeble separately |

The first four rows above cover **19 legacy weapon records** with elemental bonuses in `armor_mul`. Direct image confirmation covers named examples, not all 19. No numerical formula should consume that column as a uniform multiplier.

Crit fractions versus percentage prose are compatible for ordinary matching profiles (e.g. .75 ↔ 75%, .13 ↔ 13%, 1 ↔ 100%); critical multiplier `x12` is dimensionless, not twelve percentage points. The missing high-physical crossbow profiles also lack their corresponding 75%/x12 evidence. Base-DPS equality does not validate crit/effect equality. No DPS recomputation or ranking is produced.

### All 30 legacy debuff rows reviewed

This comparison preserves family candidates without forcing suffixes 1/2 onto screenshots. `999` durations have no screenshot support as seconds or infinity; keep them as legacy values with unknown meaning. `chance=0`, cooldown 0 and absent text must not be used as proof of no ability.

| Legacy records (row count) | Comparison / unresolved meaning |
|---|---|
| Cultist Mask Feeble (1) | 0059 transcription agrees with 6 applications, -2 damage, 1.5s and 20s. Also says lose 10 HP and extend debuffs by 150%, absent from legacy. Stack cap versus number of applied debuffs is not established |
| Poison Crossbow 2 (1) | Its -4/3s Weaken is visibly on **0015 high-physical**, not 0016 (+93). Legacy suffix binding conflicts with its offensive row. Do not rename Weaken to Feeble |
| Vigor Crossbow 2 (1) | 24% lifesteal is visibly on 0017 high-physical, absent from 0018 text. The variant-binding conflict is visually confirmed |
| Aether Crossbow 2 (1) | Legacy 34% unmake is not present in 0019's visible description. Different variant, omission or older data remains possible |
| Fire Crossbow 2 / Ice Crossbow 2 (2) | Burn 195 is visible on 0020, Chill 18.6s on 0022. Do not transfer to the +93 variants. Burn duration 999 not evidenced; Chill amount/attack-speed reduction not quantified |
| Five elemental Hammer Stuns (5) | Transcription agrees: 0.4s except Vigor 1.03s. Fire 0.4s visually confirmed. `strength=1` and single-stack assumptions are not separately supported |
| Big Vigor Sword / Big Aether Sword / Big Ice Sword (3) | Transcriptions agree with 109% lifesteal / 65% unmake / 18.6s Chill. **109% really is displayed on 0029**; retain above-100 value, do not clamp or infer runtime probability semantics |
| Bashing Shield (1) | 0032 transcription agrees 3.3s Stun/9s cooldown; 3.3 armor per stunned foe is a separate effect, not the Stun strength |
| Aether Tailsman (1) | 0034 visually confirms 20% Unstable-on-damage unmake, not an unconditional direct attack proc. Also summon/consume stages, 5s/90s cooldowns, 22 damage, armor cost/reward and Fire reduction |
| Fire Tailsman (1) | 0035 visually says **Ignition**, nearest foe every 0.5s, 4 damage/s, max 20; summon 5s and consume 90s with 40 damage per Ignition. Legacy generic Burn/999/0 is insufficient |
| Fire Shield / Ice Shield (2) | 0042/0044 transcription agrees Burn 260 / Chill 31.8s. Only one variant per family carries the status description. Burn 999 and unconditional application not established |
| Infernal Staff passive / active (2) | Passive attacker Burn 92 visually supported. Active self-Burn and attack-speed buff must remain a separate ability; see dimensional conflict above |
| Eternity Staff (1) | 0049 visually supports engaging Chill 15s and separately 0.2s immobilizing immunity/weapon-lock ability with 10s cooldown. Legacy covers only one effect |
| Berserker Staff (1) | 0050 transcription says attack-applied Weaken -4/3s, not Feeble; also separate bidirectional +30% damage active with 5s duration/30s cooldown |
| Vigor Staff / Aether Staff (2) | No screenshot family counterpart. Preserve legacy 109%/65% as legacy-only evidence; no automatic join |
| Calamity / Explosive / Frost / Plague / Reset Wands (5) | Passive transcriptions agree 13% unmake / 69 Burn / 6s Chill / -4 Weaken for 3s / 24% lifesteal. Separate active abilities are additional information, not replacements for passive effects. Legacy Plague Feeble and Burn 999 remain unresolved |

Counts in parentheses sum to 30. Numerical agreement is transcription-to-legacy agreement unless explicitly identified as visually checked. It is not an owner-confirmed runtime result.

## Targeted visual evidence ledger

Evidence base: `photograph/` plus each row's `source_image` (for example `photograph/cropped/page_004/item_0027.png`). The deterministic audit records each referenced PNG hash. Only the fields named below were checked. This is a **second model visual inspection**, without OCR, not owner/manual verification. No CSV `review_status` was changed.

| Screenshot IDs | Confirmed visible content / limits |
|---|---|
| 0010, 0011 | Custom displayed names FastGenShl/DashStaff; armor/sec 1.75; armor 35/13.4; stun 1.4s on shield; staff 16/34.29/range 5 and 4.4s mini-dash cooldown. FastGenShl base family is now owner-confirmed Towering; DashStaff alias remains inferred |
| 0015, 0016 | Poison variants 80/88.89/75%/x12/+6 with Weaken versus 17/85/33%/x6/+93 without visible Weaken |
| 0017, 0018 | Vigor variants 80/88.89/75%/x12/+6 with 24% lifesteal versus 17/85/33%/x6/+93 without visible lifesteal |
| 0019 | Æther Crossbow 17/85/33%/x6/+93 vs Fire; no 34% unmake in visible text |
| 0020, 0022 | Fire/Ice 17/85/33%/x6/+6, with Burn 195 / Chill 18.6s respectively |
| 0021, 0023 | Fire/Ice +93 counterpart images visibly show DPS 85, x6 critical multiplier and +93 against Ice/Poison. Damage, range and critical-chance fields are **not visible** in these crops, despite CSV values 17/22/33%. Those fields need a fuller capture; do not call them screenshot-confirmed |
| 0027 | Fire Hammer 28 damage, **84 DPS**, range 5, Stun 0.4s, 6.6x armor and +24 vs Ice. Unusual DPS relative to other hammers is not a transcription error here; cause unknown |
| 0029 | Big Vigor Sword 28/120/range 6, 100% splash, +9 vs Æther and **109% Lifesteal** |
| 0034, 0035 | Both talismans' separate 5s/90s cooldowns, summon/consume effects and costs/reductions. Fire text specifies nearest foe. Bottom power line clipped; no complete-description claim |
| 0038 | Vigor Shield 0.7 armor/s, 7 armor, **30% evade**, +1.8 engaging Æther armor, 70% chance to heal 2 HP when attacked. The 30% value is genuine, not an assumed 15% pairing |
| 0039 | Vigor Shield 0.7 armor/s, 7 armor, 30% evade and +7.2 engaging Æther armor; distinct from 0038 despite identical base stats |
| 0046, 0047 | Ice/Grasping Staff 78/167.14/range 20, 0.7 armor/s, 6 armor, 50% splash. Grasping: +10 range (22 max), 25s/30s, +0.75 engaging Fire armor, 39% attacker unmake. Active effect meaning/cap interaction not tested |
| 0048 | Infernal base stats 78/167.14/20/.7/6, active +4 attack speed and self Burn 5 every 2s, 10s buff/30s cooldown, +9 vs Ice, attacker Burn 92. Claimed splash not visible; no inference from another Staff |
| 0049 | Eternity base stats, 50% splash, +9 vs Poison, engaging Chill 15s; immunity with inability to move/change weapon/attack for 0.2s, cooldown 10s |
| 0052, 0055 | Poison/Fire Sword 18/108/range 5, 13% crit, x4, **flat +85 against Vigor/Ice** |
| 0058 | Blade damage **550**, displayed DPS 275, active 250/all foes, 4 Smite per hit, 155 per debuff, cap 93, cooldown 80s and 100% splash. Crop clips right/lower text; do not use this inspection to certify all text or range |
| 0061 | Heavy Hammer 69/69/range 7; 2.8x armored damage, Stun 0.4s, Armor Fatigue -75% armor gain/25s, cooldown 22s, 100% splash. Lower power line clipped |
| 0062 | Lollipop 20/28.57/range 19, 100% splash, 50% Trick/Treat, **Take 0 Damage** / gain 20 armor, 30s. Surprising zero is genuinely visible; effect behavior not inferred |
| 0066 | Poison Wand 20/100/range 20, 100% splash, **flat +100 against Vigor** |

Most lost-item actives and remaining elemental items still have only transcription evidence in this review. Even among inspected images, confirmation is field-specific: 0021/0023 do not visibly establish damage, range or critical chance. Request fuller captures for those fields and the uncertain Infernal splash claim before numerical optimization. No data is filled from a neighboring variant.

## Provenance and safe integration design

Retain the five original CSVs as separate immutable evidence sets. Add a derived comparison layer later, not an in-place merge. The current audit is that layer's minimal structural preparation, not a finalized inventory model.

For a future reviewed fact, record: screenshot ID + field/effect order, original text/value, typed value and explicit unit, affected entity, operation (flat addition, multiplier, probability, duration, interval, cap, resistance/reduction), condition, ability group, source path/hash, evidence class, reviewer and unresolved notes. Keep multiple competing claims when sources disagree. Values without established units remain raw text. Preserve unknown mechanics even if no numeric projection exists.

Evidence classes must remain separate:

1. **In-game screenshot evidence:** immutable local image/hash. No capture build/date supplied; do not infer 4.35.2 from this project's target version.
2. **Initial visual transcription:** owner-reported ChatGPT inspection without OCR. All CSV rows currently retain `visual_transcription_review_recommended`.
3. **Targeted model visual recheck:** only ledger fields above; useful corroboration, not human/manual verification or runtime validation.
4. **Owner/manual verification:** requires explicit owner confirmation of a specific value/variant; none recorded by this review.
5. **Community observation / official API documentation:** separate citations; neither proves ownership or current displayed stats.
6. **Calculation / interpretation:** formula, assumptions and inputs required. Never relabel a calculation as a displayed value.

Keep the **258 original fragments**, including overlapping duration/explanation lines. They are not 258 independent abilities. Group into abilities only with explicit reviewed linkage. Talismans require separate summon/consume groups; Infernal needs active self-effects and passive attacker effects; armor regeneration, engaging armor, evade and damage reduction are distinct. Resistances and elemental bonuses require explicit target elements. Costs, trigger conditions, stack caps and prohibited actions must survive normalization. Missing qualifiers (e.g. nearest target, rune/armor consumption, abbreviated status tokens) must be recorded as proposed additions with their image evidence, not silently inserted into the CSV.

Display aliases, effect codes in screenshots and private save ability codes are separate namespaces. The [official Stonescript manual](https://stonestoryrpg.com/stonescript/manual.html) documents inventory count queries and equipped-item state, but does not establish a unique saved-instance join from these CSVs. See `EQUIPMENT_SELECTOR_VALIDATION.md`; no new selectors or exact-instance claims are produced here. No private save/inventory was needed or accessed for this review.

## Rocky Plateau use and remaining gates

Use the data initially as evidence for **the existing R1 candidate's choices**, not as live CSV-driven combat. Keep boss-phase ownership and current travel/collection priorities unchanged. The review does not establish new boss resistances, attack timings or successful phase handling.

| Decision | Relevant reference data | Gate before automation use |
|---|---|---|
| Ordinary approach / Scout | Crossbow range/crit/pierce, wand splash, Chill, shield healing/evade | Exact variant and effective opening/attack behavior, Scout difficulty and status susceptibility |
| Boss ordinary/adaptive phases | Flat elemental bonuses on swords/wands; named target elements; status side effects | Current observed phase/defense, exact item binding, reflection/immunity/debuff effects. Highest sheet DPS does not account for those conditions |
| Armor counter | 6.6x/2.4x elemental Hammers; Heavy Hammer 2.8x and Armor Fatigue | Correct unit, actual armor response and two-handed/activation restrictions; compare whole-phase survival/time |
| Survival | Conditional engaging armor, regeneration, 30% evade, healing and stun effects | Trigger/target, real damage reduction, hand compatibility, and movement cost; no additive chance/armor stacking assumptions |
| Ability candidates | Grasping range, Eternity lock, lost wand actives, talisman costs/cooldowns | Confirm full text, activation eligibility, costs and ownership sequence before experimenting. No new active strategy authorized here |
| Travel / utility | DashStaff cooldown, Dashing/Towering shield descriptions | Keep current Triskelion travel priority. Triskelion, Star and Mind Stone are absent from these 65 records; their detailed properties are not filled by this dataset. No harvesting, waiting or collection detours |

Smallest safe next step: **owner-review a narrow evidence crosswalk** for the R1 baseline sword, shield and one armor-counter candidate. Start with Fire Sword 0055, the actually intended shield (do not assume FastGenShl's base identity), and Fire Hammer 0027 or another chosen armor counter. Confirm the displayed variant against a specific owned item and an already isolated selector test result. Keep links to private normalized inventory/source records in Git-ignored output only. Do not infer displayed stars or selectors from `+21/21`.

Resolve these questions before ranking: running build and screenshot capture modifiers, custom-name base identities, exact selector-to-owned-item binding, missing high-physical crossbows, unclear/clipped ability text, whether displayed DPS already incorporates speed/crit/element effects, actual boss defense/status interaction, costs/hand occupancy and first-attack/switching overhead. Record baseline difficulty, phase/Scout coverage, completion/deaths, intervention count and independently checked run/phase time. No predicted speed gain or supported-location status follows from this reference review.

## Checks and preservation

The validator checks exact schemas, strict UTF-8/CSV widths, decimal syntax, required metadata, unique IDs/effect keys, referential integrity, ordered fragments, safe image paths/signatures and hashes. It compares base numerical profiles only; prose semantics are reviewed in this document. Synthetic regression tests cover malformed CSV, schema change, ragged rows, invalid numbers, missing fields, duplicates, variant preservation, dangling references, ordering, metadata mismatch, unsafe paths, percent conversion, blank-versus-zero and deterministic output.

Executed checks: structural audit PASS (0 errors, 2 semantic-review warnings); 11 new CSV tests PASS; full suite 57 tests PASS. All 2,013 pre-existing protected files match their pre-review SHA-256 baseline, including source CSVs/images, scripts, existing tooling/tests/docs, offline private data, historical backups and both deployed observer/basic copies. These are preservation and static/synthetic checks, not in-game tests. Screenshot confirmation does not establish native API behavior, runtime probabilities, boss applicability, unique item identity or successful completion. Raw data and all combat/deployment/private tooling remain unchanged.

## Per-record legacy comparison index

Base profiles only. O = offensive damage/DPS/range; D = defensive armor/sec/armor/available evade. Numbers are CSV row numbers including the header. A match may be ambiguous or use a tentative alias. Effect agreement must be read separately above. A dash means no base-profile match in that table, not that equipment is absent or unusable. All raw candidates/differences are retained in the generated audit.

| Screenshot | Display name | O matching rows | D matching rows | Effect fragments |
|---|---|---|---|---:|
| screenshot_0010 | FastGenShl | — | — | 2 |
| screenshot_0011 | DashStaff | 2 | 3 | 3 |
| screenshot_0015 | Poison Crossbow | 3 | — | 6 |
| screenshot_0016 | Poison Crossbow | 4 | — | 4 |
| screenshot_0017 | Vigor Crossbow | 5 | — | 5 |
| screenshot_0018 | Vigor Crossbow | 6 | — | 4 |
| screenshot_0019 | Æther Crossbow | 8 | — | 4 |
| screenshot_0020 | Fire Crossbow | 10 | — | 6 |
| screenshot_0021 | Fire Crossbow | 10 | — | 4 |
| screenshot_0022 | Ice Crossbow | 12 | — | 6 |
| screenshot_0023 | Ice Crossbow | 12 | — | 4 |
| screenshot_0024 | Poison Hammer | 13 | — | 4 |
| screenshot_0025 | Vigor Hammer | 14 | — | 4 |
| screenshot_0026 | Æther Hammer | 15 | — | 4 |
| screenshot_0027 | Fire Hammer | 16 | — | 4 |
| screenshot_0028 | Ice Hammer | 17 | — | 4 |
| screenshot_0029 | Big Vigor Sword | 18 | — | 3 |
| screenshot_0030 | Big Æther Sword | 19 | — | 3 |
| screenshot_0031 | Big Ice Sword | 20 | — | 4 |
| screenshot_0032 | Bashing Shield | — | 4 | 4 |
| screenshot_0033 | Repeating Crossbow | 21 | — | 2 |
| screenshot_0034 | Æther Talisman | — | — | 8 |
| screenshot_0035 | Fire Talisman | — | — | 8 |
| screenshot_0036 | Poison Shield | — | 5 | 3 |
| screenshot_0037 | Poison Shield | — | 6 | 1 |
| screenshot_0038 | Vigor Shield | — | 7, 8 | 2 |
| screenshot_0039 | Vigor Shield | — | 7, 8 | 1 |
| screenshot_0040 | Æther Shield | — | 9 | 2 |
| screenshot_0041 | Æther Shield | — | 10 | 1 |
| screenshot_0042 | Fire Shield | — | 11 | 3 |
| screenshot_0043 | Fire Shield | — | 12 | 1 |
| screenshot_0044 | Ice Shield | — | 13 | 3 |
| screenshot_0045 | Ice Shield | — | 14 | 1 |
| screenshot_0046 | Ice Staff | — | — | 4 |
| screenshot_0047 | Grasping Staff | 22 | 15 | 6 |
| screenshot_0048 | Infernal Staff | 23 | 16 | 9 |
| screenshot_0049 | Eternity Staff | 24 | 17 | 6 |
| screenshot_0050 | Berserker Staff | 25 | 18 | 7 |
| screenshot_0051 | Prevention Staff | 26 | 19 | 5 |
| screenshot_0052 | Poison Sword | 27 | — | 3 |
| screenshot_0053 | Vigor Sword | 28 | — | 4 |
| screenshot_0054 | Æther Sword | 29 | — | 4 |
| screenshot_0055 | Fire Sword | 30 | — | 3 |
| screenshot_0056 | Ice Sword | 31 | — | 3 |
| screenshot_0057 | Bardiche | 32 | — | 5 |
| screenshot_0058 | Blade of the Fallen God | — | — | 6 |
| screenshot_0059 | Cultist Mask | — | — | 5 |
| screenshot_0060 | Dashing Shield | — | 20 | 1 |
| screenshot_0061 | Heavy Hammer | 34 | — | 8 |
| screenshot_0062 | Lollipop Wand | 35 | — | 6 |
| screenshot_0063 | Skeleton Arm | 36 | — | 7 |
| screenshot_0064 | Stone Sword | 37 | — | 2 |
| screenshot_0065 | Towering Shield | — | 21 | 2 |
| screenshot_0066 | Poison Wand | 38 | — | 2 |
| screenshot_0067 | Vigor Wand | 39 | — | 2 |
| screenshot_0068 | Æther Wand | 40 | — | 2 |
| screenshot_0069 | Fire Wand | 42 | — | 2 |
| screenshot_0070 | Ice Wand | 41 | — | 2 |
| screenshot_0071 | Calamity Wand | 43 | — | 5 |
| screenshot_0072 | Explosive Wand | 44 | — | 6 |
| screenshot_0073 | Frost Wand | 45 | — | 6 |
| screenshot_0074 | Plague Wand | 46 | — | 7 |
| screenshot_0075 | Reset Wand | 47 | — | 5 |
| screenshot_0076 | Crossbow | — | — | 2 |
| screenshot_0077 | Stone Crossbow | — | — | 3 |
