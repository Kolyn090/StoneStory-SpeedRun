# B2 equipment switching: reserved helper name

Historical correction: current B2.1-NR removes the optional harvesting path and its helper entirely. The trace and shovel test below describe the earlier B2.1 revision; use [RESOURCE_POLICY.md](RESOURCE_POLICY.md) and the current basic test plan for current expected behavior.

Status: confirmed B2 module-load defect; minimal B2.1 correction deployed for retesting. **Not fully resolved until the owner confirms in-game switching.**

## Evidence and root cause

The game log reported:

```text
SpeedRunBasic/main line 4: SpeedRunBasic/equipment/Catalog line 125: Variable "Harvest" is reserved
```

It then reported unresolved `gear`, non-object `gear` access, and invalid downstream comparisons. `main` cannot obtain a valid catalog object because the custom function name conflicts with native `harvest`. The native state name appears in the [official manual](https://stonestoryrpg.com/stonescript/manual.html); the game log supplies the direct reserved-name evidence. Do not infer that capitalization makes native names safe for helpers.

## Complete source trace

1. `main` loads Settings, Catalog, Dispatcher, Generic and the original metrics object. **The broken Catalog declaration fails here**, before availability checks or equip commands.
2. With successful loading, entry/first attachment calls `gear.Prepare(config)`: availability checks populate bounded family arrays and default selectors. Loops retain the cache. Missing core items suppress project automation.
3. `locations.Update()` classifies known main locations, excluding quest/unknown routes. If enabled/allowed, `combat.Tick(gear, config)` runs; otherwise requests clear and it observes only.
4. `Tick` clears requests and checks missing gear / AI state. It chooses travel/harvesting or a sword/wand/hammer strategy from foe distance, tags, armor, crowd count and HP.
5. `gear.Weapon()` returns an availability-checked selector. `gear.Apply()` records requests and issues `equipL @weapon@` plus `equipR @shield@`. Harvesting uses `gear.EquipHarvestTool()` and `equip @shovel@` instead, then returns.
6. Only metrics and diagnostic prints follow. Neither issues equipment commands. There is no current-equipment suitability shortcut or “already equipped” cache. Equipment application is requested each eligible frame.

Within the candidate there is no later same-frame equipment writer. The original observer also has none. Another Mind Stone import or command after this entry point could still override selection; the manual states later equipment commands win. Use a single entry-point import for the retest. See also the attributed public selector helpers in [Scribble](https://github.com/livercat/scribble/blob/master/scribble.txt), which use the same documented variable-selector equip form.

## Interrupted-session audit and correction

Repository source and both deployed candidates still matched B2; only local staging contained the interrupted rename. No partial live replacement or pre-fix backup directory existed.

Runtime changes:

- `scripts/basic/equipment/Catalog.txt`: `func Harvest()` -> `func EquipHarvestTool()`.
- `scripts/basic/combat/Generic.txt`: update the one corresponding call.
- `scripts/basic/main.txt`: diagnostic header B2 -> B2.1.

`tools/Test-BasicStatic.ps1` adds a regression check for the rejected name and renamed declaration/call. Existing staged/unstaged user changes are preserved; no commit, reset, or index update is performed.

The other catalog helpers (`Find`, `Prepare`, `ClearRequest`, `Weapon`, `Apply`) and fields were reviewed against used native state/namespaces; no additional documented collision was identified. Initialization order and the five-entry arrays were inspected. This is not an exhaustive reserved-word parser or proof against later runtime errors. Selectors, fallbacks, HP/distance thresholds, and observer logic remain unchanged.

## Backups and deployment

Before replacement, both complete live B2 folders are copied to these new destinations and each copied file's hash is verified:

```text
backups/pre-harvest-reserved-fix-20261029/steam-SpeedRunBasic
backups/pre-harvest-reserved-fix-20261029/save-SpeedRunBasic
```

All older backups, the observer, diagnostics and inventory data are preserved. Only the three changed runtime files are installed into both existing `SpeedRunBasic` roots. All five deployed module hashes and the sibling `SpeedRun/metrics/RunMetrics.txt` dependency are checked against repository sources. Historical deployment records remain intact.

## Verification boundaries

- Broken B2 source is rejected by the new regression check; corrected staging passes the static checker.
- Renamed helper has one declaration and one corresponding call; no remaining `Harvest()` helper/call in active source. Native `harvest` queries remain intentional.
- Imports, helper references, delimiter/indentation checks and source/deployment hashes are checked. Original observer, every prior backup and inventory hashes remain unchanged.
- **Not tested after correction:** native parser acceptance, successful catalog object creation, concrete selector matches, actual switching, lifecycle/measurement correctness, boss handling or map completion. Log entries from the failed B2 attempt remain historical; check for new errors on a new run.

## Rocky Plateau confirmation steps

1. Restart the game to avoid relying on external-file hot reload. Confirm Mind Stone power is on and its only automation entry is `import SpeedRunBasic/main` (not `SpeedRun/main`). Start a fresh manual Rocky run at a comfortable low difficulty.
2. Look for **B2.1**, handler `rocky`, and `Missing core: none`. If the display is absent or the catalog errors recur, capture exact new Tab errors and stop that trial.
3. Before combat expect `travel-shield`: configured stone/default sword in the left hand and compound/vigor fallback shield on the right. At a nearby harvest target, expect `harvest` and an available shovel as a two-handed request; blank left-hand display can be normal for two-handed gear.
4. When a target is beyond melee range but within 22 units, expect `ranged-shield`: the available matching/default wand plus shield. Against a nearby ordinary target, expect sword plus shield; armor can choose a hammer, crowds/bosses can retain a wand, and low HP can choose the available healing sword. These are policy expectations, not fixed encounter guarantees.
5. Compare Want versus Have over several frames. Report whether actual equipment changes when the strategy changes. If core gear is missing, report the named families rather than treating the deliberate stop as a switching fix failure.
6. Send header, difficulty, handler, strategy, Missing core, unavailable codes, Want/Have equipment, and exact new error text. A screenshot at a mismatch helps. Explicitly confirm whether switching now works; location completion remains a separate test.

Remaining possible blockers: missing or ambiguous selectors, suspended AI, quest/unknown guard, stale cache after inventory changes, or other active scripts overriding equipment. None is established as a second root cause without observations. Do not broaden the code change based only on these possibilities.
