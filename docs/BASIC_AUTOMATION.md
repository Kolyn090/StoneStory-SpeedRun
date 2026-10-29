# Basic automation candidate

Current revision: **B2.1-PS** adds configurable passive attraction with Star Stone L + shield R only in safe ordinary travel. It never adds optional shovel harvesting or collection detours. See [PASSIVE_STAR_STONE.md](PASSIVE_STAR_STONE.md); physical range, timings and completion benefit remain unverified. Earlier B2.1-NR policy below records the shovel-removal baseline; the current bounded Star Stone exception supersedes its general prohibition on collection-only swaps.

Current policy revision: **B2.1-NR** removes optional resource harvesting. Resources are incidental; movement, combat, boss completion and run time take priority. Earlier B2/B2.1 reports are historical. See [RESOURCE_POLICY.md](RESOURCE_POLICY.md) for the source audit, backup/deployment evidence and progression test gate. Mandatory interactions remain in scope; no blanket native-interaction suppression is applied.

Status: source-reviewed, not parsed or executed in-game. Priority is broad basic coverage and reliability; speed optimizations, AAC, dash sequences and boss timing are deferred. See [coverage matrix](LOCATION_COVERAGE.md).

Current stabilization build: **B2**. Follow [BASIC_TEST_PLAN.md](BASIC_TEST_PLAN.md), starting with Rocky Plateau; record results in [BASIC_TEST_RESULTS.md](BASIC_TEST_RESULTS.md). No completion status changes without explicit owner confirmation. See [SELECTOR_API_AUDIT.md](SELECTOR_API_AUDIT.md) for API and selector review.

Correction **B2.1** supersedes the B2 diagnostic header: `Harvest()` was rejected as reserved by the game, preventing the catalog object from loading. It is now `EquipHarvestTool()`; its call site and diagnostic revision are the only runtime changes. See [BUG_HARVEST_RESERVED.md](BUG_HARVEST_RESERVED.md). The B2 test sequence still applies, with B2.1 expected in the header; corrected import/execution remains pending owner retest.

## Architecture

The original `scripts/main.txt` and `scripts/metrics/RunMetrics.txt` remain unchanged. The alternative entry is `scripts/basic/main.txt`, installed as `SpeedRunBasic/main.txt`. It reuses the original `SpeedRun/metrics/RunMetrics` object and reproduces the same entry/loop/attachment ordering around it. Original observer loading is user-verified; the new composition and all observer correctness cases still need tests.

- `config/Settings.txt`: flags, HP/distance thresholds, explicit inventory search criteria.
- `equipment/Catalog.txt`: initialization-time availability searches and bounded elemental arrays; one-handed equipment application and optional cached Star Stone. No shovel lookup. Refreshes on fresh manual entry, not loops. Restart manually after inventory/config changes.
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
| Travel / passive pickups | Sword + shield by default when no target is within 22 units. A bounded Star Stone L + shield R opportunity is permitted only with no targeted foe/no foes within 46, full HP, walking, no boss seen and a nearby targeted pickup; see PASSIVE_STAR_STONE.md. No shovel, collection detours or resource abilities |
| Suspended AI | Skip equipment and potion decisions while disabled/paused |

The elemental weakness cycle is a community-derived policy, not a new native API. Current setup has five-element candidates and no special air matchup. An undamageable target reports a wait strategy; it does not dodge or force a phase transition. Missing item families produce diagnostics and may leave previous equipment in a slot. **Do not continue unattended with missing gear or a manual-intervention strategy.**

Crossbows in the inventory are promising ranged candidates but remove the shield and have ambiguous duplicate labels; the reliability-first default uses ordinary wands instead. Big swords, special staves and ability weapons are deliberately not needed for the initial policy. This avoids inventing precise enchantment mappings or ability holds.

## Install and rollback

The candidate is installed side-by-side under `SpeedRunBasic` in both existing script roots. Existing `SpeedRun` files and Mind Stone text are not overwritten. A timestamped backup of each known-working `SpeedRun` directory is created before candidate deployment. The deployment report records exact backup paths. If a candidate destination already exists with different contents, deployment stops rather than overwriting it.

See [DEPLOYMENT_BASIC_20261029.md](DEPLOYMENT_BASIC_20261029.md) for the initial installation; [DEPLOYMENT_BASIC_B2_20261029.md](DEPLOYMENT_BASIC_B2_20261029.md) records the diagnostic update and its separate candidate backups. Historical reports are retained.

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
