# B2.1-TS live baseline

**Current installed baseline: B2.1-TS (`SpeedRunBasic/main`).** Its deployed files are preserved. Automated completion, exact gear selection and movement benefit remain unverified; installed does not mean successfully automated. The original observer's loading/display pass is separate.

This page is authoritative for shared architecture, generic combat and B2.1 installation/rollback. For the implemented but uncommitted, undeployed and not game-verified Rocky ★15 candidate, use [R15](../rocky/ROCKY_PLATEAU_15.md). Do not mix entry points or apply R15 equipment rules to the live baseline.

Current travel/slot rules are maintained in [Triskelion travel](../TRISKELION_TRAVEL.md) and [passive collection](../PASSIVE_STAR_STONE.md). Older B2/NR/PS introductions and the reserved-name correction remain in [revision history](../archive/BASELINE_REVISION_NOTES.md) and the archive. See [baseline tests](BASIC_TEST_PLAN.md), [results](BASIC_TEST_RESULTS.md) and [coverage](LOCATION_COVERAGE.md).

## Architecture

The original `scripts/main.txt` and `scripts/metrics/RunMetrics.txt` remain unchanged. The alternative entry is `scripts/basic/main.txt`, installed as `SpeedRunBasic/main.txt`. It reuses the original `SpeedRun/metrics/RunMetrics` object and reproduces the same entry/loop/attachment ordering around it. Original observer loading is user-verified; the new composition and all observer correctness cases still need tests.

- `config/Settings.txt`: flags, HP/distance thresholds, explicit inventory search criteria.
- `equipment/Catalog.txt`: initialization-time availability searches and bounded elemental arrays; optional cached stones. `ApplyPair` is the shared one-handed executor; combat `Apply` supplies the normal shield, travel supplies its selected R item. No shovel lookup. Restart manually after inventory/config changes.
- `locations/Dispatcher.txt`: caches classification by `loc.id` and quest status; eight main location aliases share the generic handler. Quest and unknown locations perform no automation.
- `combat/Generic.txt`: selects one ordinary loadout per frame, with no cancellation swaps or resource abilities. Native game AI performs attacks/movement.

These are project helpers, not new native APIs. Per-frame work is bounded: location/quest checks, necessary foe/HP queries, one policy pass, equipment application, measurement latch, and optional prints. No inventory loop runs per combat frame. Current-frame requests are cleared before policy evaluation. Missing core sword/wand/shield families suppress automation and show a warning, while native game AI remains active. Existing equip requests are reapplied to let native selection resolve them; this is not an exact-item handle cache. No CPU/performance gain has been measured.

## Policy and equipment rationale

Inventory CSVs were reviewed but not changed. Their DPS, effect probabilities, and units are not used to predict wins. Each configured selector is checked with `item.GetCount` before use. Broad selectors let the game choose a match; they do not guarantee the intended enchantment/duplicate. Refine criteria after observing actual equipment.

| Decision | Implemented policy / reason |
|---|---|
| Defense | Compound shield preferred (inventory lists strong armor); vigor shield fallback. Shield remains paired with one-handed offensive gear |
| Melee | Elemental one-handed sword, stone/general sword fallback; enter at 5 units and leave above 7 to reduce threshold oscillation |
| Ranged | Elemental ordinary wand with shield; selected beyond melee range and by default for bosses |
| Armor | One-handed elemental hammer when otherwise choosing melee; sword fallback if no hammer |
| Crowds | Wands at three foes within 20 units, based on community AoE usage; actual reach/benefit unverified |
| Physical/ranged immunity | Physical immunity forces wand; ranged immunity forces melee. Conflicting flags report manual intervention rather than claiming a solution |
| Low HP | At less than 40% HP, choose a cached vigor `dL` sword only in melee. Healing is not guaranteed to outpace damage |
| Potion | Disabled by default. If explicitly enabled, consume the current nonempty potion below 25% HP when activations are allowed. No automatic identification of potion effect, brewing or refill |
| Travel / passive pickups | Clear walking/full HP/no boss seen: Triskelion L + shield R when enabled/available. A bounded nearby pickup opportunity changes only R to Star Stone. Without Triskelion, retain the previous Star L + shield R fallback. Any targeted enemy uses combat gear; reported non-targeted threats request wand/shield. No shovel, collection detours or stone activation |
| Suspended AI | Skip equipment and potion decisions while disabled/paused |

The elemental weakness cycle is a community-derived policy, not a new native API. Current setup has five-element candidates and no special air matchup. An undamageable target reports a wait strategy; it does not dodge or force a phase transition. Missing item families produce diagnostics and may leave previous equipment in a slot. **Do not continue unattended with missing gear or a manual-intervention strategy.**

Crossbows in the inventory are promising ranged candidates but remove the shield and have ambiguous duplicate labels; the reliability-first default uses ordinary wands instead. Big swords, special staves and ability weapons are deliberately not needed for the initial policy. This avoids inventing precise enchantment mappings or ability holds.

## Install and rollback

The candidate is installed side-by-side under `SpeedRunBasic` in both existing script roots. Existing `SpeedRun` files and Mind Stone text are not overwritten. A timestamped backup of each known-working `SpeedRun` directory is created before candidate deployment. The deployment report records exact backup paths. If a candidate destination already exists with different contents, deployment stops rather than overwriting it.

See [DEPLOYMENT_BASIC_20261029.md](../archive/DEPLOYMENT_BASIC_20261029.md) for the initial installation; [DEPLOYMENT_BASIC_B2_20261029.md](../archive/DEPLOYMENT_BASIC_B2_20261029.md) records the diagnostic update and its separate candidate backups. Historical reports are retained.

For manual installation: back up the current `SpeedRun` directory, copy the contents of `scripts/basic/` into `Stonescript/SpeedRunBasic/`, and keep `SpeedRun/metrics/RunMetrics.txt` in place. Do not copy the `basic` folder as an extra path level.

To opt into testing, back up the current Mind Stone text, then **replace** the old observer import with:

```stonescript
import SpeedRunBasic/main
```

Do not leave both entry-point imports enabled. Remove/disable other equipment/ability automation for an isolated test, preserving its text for rollback. Native item inputs can still interfere; record any manual intervention. Start a fresh manual run so settings and inventory caches initialize. Diagnostics default on in this candidate; `config/Settings.txt` controls them independently of the original observer.

To return to the known-working observer, restore `import SpeedRun/main` and start manually. Because original files are retained, rollback normally needs no file restoration. Do not restore whole save folders or delete unrelated scripts. No game save data is modified by deployment.

## First tests

1. Begin on Rocky Plateau at a comfortable low difficulty. Verify B2 import loading and no new Stonescript errors. Check location/handler and requested versus actual equipment; `Missing core` should read `none`. Preferred-selector misses are shown separately by family and may be covered by fallbacks.
2. Verify sword + shield nearby, wand + shield at range/crowds, hammer against armor, and no repeated distance-boundary toggling. Stop and report incorrect selection before a boss attempt.
3. Observe low-HP behavior with potion use still disabled. Only enable potion consumption after choosing an appropriate potion and accepting its resource policy.
4. Finish only if ordinary combat is safe. Record the first boss mechanic requiring manual help; no boss completion claim exists yet.
5. Repeat the observer acceptance tests, including completion/loop resets. Two loops plus three successful attempts are a smoke test, not proof across difficulties.

Failure report: exact import error, game version, map/difficulty, handler/strategy, foe state and distance, requested/actual equipment, HP/armor, config, other scripts/manual input, and a screenshot/video if available. Mark partial or manual-assisted completions explicitly. Difficulty-specific completion tests are all NOT RUN.

## Research and validation limits

[Official manual](https://stonestoryrpg.com/stonescript/manual.html): item counts, search criteria, equipment commands, location/quest state, foe filters/counts, HP, AI state, potion activation and script objects were checked. Source/API review is not parser execution.

[Cobblestone by alexbarker234](https://github.com/alexbarker234/stonescript/blob/main/Cobblestone.txt) informed the location list and elemental/crowd policy. [Scribble by livercat](https://github.com/livercat/scribble) informed shielded approach and boss limitations. This implementation is original; no upstream timings, cancellation code, or boss strategies were copied. Upstream links are moving branches.

Static checks cover import resolution, project helper signatures, indentation, balanced delimiters, isolated inventory scans, guarded potion use, dispatcher routes, and preserved observer/inventory hashes. Full parser acceptance, item choice semantics, policy effectiveness, completion reliability, and timing remain unverified.

Run the reusable subset with `powershell -File tools/Test-BasicStatic.ps1` from the repository. This checks main's direct helper references (not every possible runtime signature or control-flow path). Manual source review covers the remaining helper calls and policy ordering. No Stonescript interpreter is included in that check.
