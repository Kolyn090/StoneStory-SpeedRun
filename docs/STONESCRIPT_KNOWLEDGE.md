# Stonescript knowledge base

Reviewed: 2026-10-29. Official manual displayed v4.35.2, dated 2026-09-25. The installed game version has not been established. Loading/import execution and visible diagnostics are user-verified in-game; observer correctness remains pending.

## Permanent project policy: resources are incidental

The owner reports effectively unlimited resources. Resource farming, optional shovel harvesting and accumulation are not goals. Prioritize reliable progression, movement, combat, bosses and total completion time; avoid collection-only detours. The authorized exception is configurable, bounded Star Stone attraction of already-nearby pickups in safe ordinary travel, subordinate to combat, boss mechanics, movement optimizations and protected sequences. Never wait for collection. Preserve required tools/interactions with location-specific evidence rather than a generic `harvest` trigger. This is an owner requirement, not a claim about native game mechanics.

**Official Star Stone evidence:** the [official tutorial, Pickups](https://stonestoryrpg.com/stonescript/) says attraction occurs while equipped and demonstrates `pickup.distance < 10` with `equipL star`; no activation is used. The [manual](https://stonestoryrpg.com/stonescript/manual.html) documents `pickup` as the player's current targeted pickup, its distance/z, and a `<5` Star Stone example. Possession alone is not the documented attraction method. No exact maximum attraction radius, pickup-instance enumeration/event, or Star Stone activation/range-query API was established. Ten is a tutorial trigger threshold, not an independently verified maximum or level formula.

**Community:** [Cobblestone](https://github.com/alexbarker234/stonescript/blob/main/Cobblestone.txt) uses `<10`; [Scribble](https://github.com/livercat/scribble/blob/master/scribble.txt) uses `<9`. Their switching policies are not copied. **Project B2.1-PS:** cached optional selector, no-foe/no-nearby-enemy walking/full-HP gate, boss-seen latch, one bounded pulse per observed pickup-presence window and retry spacing. Replaces only the ordinary-travel loadout with Star Stone L + normal shield R; no post-combat override. Physical maximum range, native movement path, sufficient hold time, equipment side effects and net completion-time effect remain in-game tests. See [PASSIVE_STAR_STONE.md](PASSIVE_STAR_STONE.md). B2.1-NR history below remains valid for the shovel removal.

**B2.1-NR change:** the generic nearby-harvest branch, cached shovel lookup, shovel configuration and unused helper are removed. Travel keeps sword + shield. No native AI, pickup, utility-belt, quest or interaction behavior is globally disabled. Existing source contains no separate mandatory-tool handler; none is removed. This is a static dependency audit, not proof that every location/difficulty passes without intervention. Test traversal and report blocking objects before claiming progression safety. See [policy/change acceptance](RESOURCE_POLICY.md).

## Evidence labels

- **Official:** documented language/API behavior; not a claim that this project was executed.
- **Community:** inspected implementation or author observation; may depend on version and gear.
- **Proposal:** project design or optimization hypothesis.
- **In-game verified (user-reported):** directly observed by the owner; record scope and missing test metadata. This is not an agent-run test or a broader acceptance claim.
- **In-game verified (recorded test):** a separately documented test with environment, steps, expected/actual results, and evidence. No detailed observer acceptance cases have been completed yet.

## Official reference: syntax and execution

Source: [official Stonescript manual](https://stonestoryrpg.com/stonescript/manual.html), sections Basics, Game State, Commands, Variables, Functions, Importing External Scripts, Tips, and Appendix A.

- Execution: once per frame, nominally 30/second; indentation defines scope.
- Syntax: `?` condition, `:` else, `//` comment, `var` declaration, `func` function; arrays and loops exist. `=` can mean equality or string containment; use `string.Equals` for exact strings.
- `var` initializes once. Variables persist across Ouroboros loops; `loc.begin` excludes loops, while `loc.loop` identifies their first frame.
- `time` is location frames; `totaltime` accumulates boss sub-locations; `lbtime` is leaderboard completion frames, zero before boss defeat.
- `foe.state` identifies state; `foe.time` counts its frames. `foe.count` covers 46 units; `foe.GetCount(distance)` narrows the radius. Buff/debuff count/time queries exist.
- `equip`, `equipL`, `equipR` select equipment; two-handed items require `equip`. Later equipment commands determine final equipment. Variable selectors use `@variable@`; subtractive criteria are supported.
- `activate` accepts hand/potion aliases and ability IDs. `item.GetCooldown(id)` returns frames; `-1` can mean invalid ID or unused ability. `item.CanActivate(id)` requires equipped, eligible equipment; zero cooldown alone is insufficient.
- `brew` operates only at time zero. Appendix A lists cooldown IDs, including `heavy_hammer`.
- `import` executes a shared script instance; `new` creates an independent instance whose body executes once. Imported variables are scoped to their script.

## Community techniques and attribution

These are source observations, not guarantees of speed or compatibility. Sources below follow moving branches; record the exact upstream revision when implementing a technique.

### livercat: Scribble

[Repository and author guidance](https://github.com/livercat/scribble) · [source](https://raw.githubusercontent.com/livercat/scribble/master/scribble.txt)

The source snapshots combat state, prepares configured equipment choices, protects selected ability sequences, and dispatches boss handling. Its AAC helper excludes some weapon types and protects hammer/Bardiche locks. Boss logic combines state, elapsed frames, and distance; some projectile decisions inspect screen symbols. The author describes gear-dependent limitations.

**Proposal:** adapt bounded sequence ownership and inventory-specific configuration. Recalibrate all frame thresholds; treat screen-symbol detection as fragile until tested under the actual display configuration.

### alexbarker234: Cobblestone

[Repository](https://github.com/alexbarker234/stonescript) · [source](https://raw.githubusercontent.com/alexbarker234/stonescript/main/Cobblestone.txt)

The implementation defers equipment requests, applies them centrally, then activates abilities. Location handlers, quarterstaff sequences, multi-frame Moondial patterns, and Dysangelos phase splits provide useful study examples. Its rolling DPS calculation scans stored history. Some ability checks use `hammer`, differing from the current manual's `heavy_hammer` identifier.

**Proposal:** adopt explicit arbitration and phase measurements, not copied thresholds. Prefer bounded counters over a large diagnostic history. Validate every native identifier individually.

### Eunomiac: annotated attack animation cancellation

[Repository](https://github.com/Eunomiac/stone-story) · [annotated source](https://raw.githubusercontent.com/Eunomiac/stone-story/master/Scripts-Annotated/AttackAnimationCancelling-Annotated.txt)

The example checks item state `3`, temporarily swaps equipment, then restores weapons. Its two-handed detection assumes that a one-handed loadout always has an occupied off-hand; the author explicitly documents that assumption.

**Proposal:** use explicit equipment metadata and test cancellation separately for each weapon. The presence of readable state APIs does not prove that a particular swap preserves damage or improves completion time.

## Project-specific data observations

Initial inspection: two commits through `1351869`; inventory only. A subsequent lifecycle/measurement observer now exists; see [installation and test plan](INSTALLATION.md). Inventory tables contain 46 offensive, 20 defensive, and 30 effect rows. `data/gears/note.md` says the data represents the owner's inventory and assumes +21/21.

Open questions; preserve original data until clarified:

- Row labels such as Crossbow 1/2 need exact in-game selectors, star levels, modifiers, and unique duplicate identification.
- Durations/cooldowns need declared units; `999` needs an explicit sentinel definition.
- Values above 1 in effect `chance` fields may describe amounts rather than probabilities.
- DPS inclusion of critical, elemental, and armor effects is unspecified.
- Cross-table names and spellings need a separate canonical mapping.
- Mobility, utility items, summons, potion access, and availability need confirmation; a table omission does not prove absence from inventory.

## Unverified behavior and experiments

| Question | Required evidence |
|---|---|
| Do intermediate swaps reset recovery while preserving a hit? | Weapon-specific frame trace and damage/completion comparison; test projectiles and both hands separately |
| How long must equipment remain equipped around activation? | Activation frame, effect appearance, animation completion, and safe release observation |
| Are boss thresholds valid under chill/stun and different difficulties? | Per-phase state traces with modifiers and distances recorded |
| Does travel gear save net time? | Travel split plus next first-hit delay; compare approach distance and overshoot |
| When does debuff setup pay back? | Setup frames versus total encounter time, including short-lived targets |
| Can an item selector choose the wrong duplicate? | Inventory selection checks with exact modifiers and identifiers |
| Does CPU/UI work affect elapsed time? | Paired debug-on/off comparisons; distinguish wall time from simulation frames |

Neither `ai.idle` nor target HP loss alone is proof that the player's attack completed: target changes, damage-over-time, and other damage sources can confound inference. Exact boss numeric states and attack windows require encounter-specific evidence.

## Measurement policy (proposal)

Record build/platform, revision, location/difficulty, exact loadout, resource policy, loop status, timing boundaries, sample size, failures, and median/best times. Preserve failed attempts rather than reporting only successful records. Measure travel, encounters, boss phases, and total completion separately. Do not compare the game's weighted location average as though it were an independent controlled trial mean.

Before adoption, change one variable, compare repeated baseline/candidate runs, and verify the selected reliability target. No expected percentage improvement is established yet.

## Findings log

| Date | Finding | Evidence/status |
|---|---|---|
| 2026-10-29 | Inventory foundation exists; runtime and benchmarks absent | Local source/Git inspection |
| 2026-10-29 | Lifecycle, timing, equipment, activation, and modularity reviewed | Official manual, version above |
| 2026-10-29 | AAC, juggling, boss thresholds, and travel gains remain unverified locally | Community source inspection only |
| 2026-10-29 | Script loads/runs, import executes, diagnostics overlay appears | User-reported in-game deployment test; see acceptance record DEP-01 |

For future entries include exact source revision or game test conditions. Update conclusions when contradictory evidence appears.

## Observer implementation review (2026-10-29)

**Official source review:** external-script examples demonstrate assigning a `new` object, calling its functions, and reading its fields. The observer uses that composition pattern and advanced prints. Reference: [manual, external scripts and functions](https://stonestoryrpg.com/stonescript/manual.html#import). No additional native APIs were assumed.

**Project design:** the entry point dispatches entry/loop before measurement. A first load without either flag becomes a partial observation. Completion captures require a full boundary and a zero-to-positive `lbtime` observation, with one result per attempt. This deliberately favors omitted results over stale results. Optional diagnostics render every enabled frame; disabled diagnostics do no rendering. Retained data is bounded and in-memory only.

**Static validation:** source structure, import paths, helper calls, scope restrictions, and unchanged gear data were checked. These source checks alone did not establish game execution or correctness.

**User-reported deployment verification (2026-10-29):** after adding `import SpeedRun/main` and enabling diagnostics, the owner saw the overlay and explicitly confirmed that the script loads and runs in Stone Story RPG. This verifies loading/import execution for the working deployment, including enough module execution to render diagnostics. It does not verify every code path. Both the Steam installation and save-folder copies exist; the exact copy resolved by the game was not isolated. Installed build, map/difficulty, exact deployed revision, and frame-level evidence were not supplied. See [DEP-01 and the acceptance checklist](OBSERVER_ACCEPTANCE.md).

**Still unverified:** lifecycle resets, timing accuracy, completion capture, Ouroboros loop handling, boss sub-location transitions, reload behavior, and performance overhead. No benchmark gain is claimed. Do not promote an expected result to verified merely because the overlay renders.

## Basic automation candidate (2026-10-29)

**Official API review:** `item.GetCount(criteria)` checks availability; `foe.GetCount(radius)` counts nearby targets. The manual lists physical/ranged immunity and undamageable filters, AI enabled/paused state, harvesting and potion availability. These provide inputs, not a proven combat policy. [Manual](https://stonestoryrpg.com/stonescript/manual.html).

**Community-informed choices:** the eight main-location aliases and weakness cycle were reviewed in [Cobblestone](https://github.com/alexbarker234/stonescript/blob/main/Cobblestone.txt). Shielded combat, wand crowd handling, and boss-specific limitations were cross-checked against [Scribble](https://github.com/livercat/scribble). No boss frame constants or cancellation routines were copied.

**Implemented project policy, unverified:** `scripts/basic/` caches available one-handed swords/wands/hammers and shields, dispatches eight locations, switches range with hysteresis, prefers wands for crowds/bosses, uses hammers against armor in melee, and permits low-HP lifesteal swords. Optional potion consumption defaults off. B2.1-NR removed optional shovel harvesting; current B2.1-PS adds only the bounded passive Star Stone travel exception. No dash ability or resource refill. Quest/unknown routes observe only. See [BASIC_AUTOMATION.md](BASIC_AUTOMATION.md). Historical B2/B2.1 harvesting descriptions below record earlier revisions and are superseded for current behavior by RESOURCE_POLICY.md and PASSIVE_STAR_STONE.md.

**Limits:** inventory row labels and enchantments are unresolved, so broad selector matching requires inspection of actual equipment. Cached existence is not proof of the intended item or adequate damage. Boss reflection, lethal telegraphs, resistance changes, walls, elite modifiers, missing gear and reload behavior remain risks. All new imports, combat decisions and difficulty completions are untested in-game. The original loading pass does not apply to the new entry point. See [LOCATION_COVERAGE.md](LOCATION_COVERAGE.md).

## B2 stabilization preparation (2026-10-29)

**Source-confirmed shared defects:** prior diagnostics retained stale requests during skipped frames and displayed a shield request during two-handed shovel use. B2 clears request fields before decisions and records the actual requested hand mode. Preferred-selector misses and fatal missing-core families are now distinct; missing core gear suppresses project automation. These are source-level fixes, not verified in-game outcomes.

**Official review:** all used native forms and selector families were audited in [SELECTOR_API_AUDIT.md](SELECTOR_API_AUDIT.md). `dL` appears in the manual's vigor-sword example. Valid string-query syntax does not guarantee a concrete name/modifier match; B2 records cached availability for owner inspection. No native error interception is assumed; Tab remains the route for game errors.

**Test status:** diagnostics/configuration and eight-location sequence prepared, Rocky Plateau first. All location completions, lifecycle resets, timing accuracy, captures and loops remain unverified. Original observer loading/display is the only prior user-confirmed pass. Use [BASIC_TEST_RESULTS.md](BASIC_TEST_RESULTS.md); only owner-confirmed actual completions can change location status. No advanced boss strategy or AAC was added.

## Equipment module load failure: B2.1 correction

The installed game's log confirmed `SpeedRunBasic/main line 4: SpeedRunBasic/equipment/Catalog line 125: Variable "Harvest" is reserved`, followed by unresolved/non-object `gear` errors. The module failed to load before its equipment commands could execute. The native `harvest` game-state name is documented in the [official manual](https://stonestoryrpg.com/stonescript/manual.html); the exact reserved-name rejection is runtime evidence from this build, not an invented exhaustive language rule.

Minimal correction: rename project helper `Harvest()` to `EquipHarvestTool()` and update its sole call in `combat/Generic.txt`. Entry diagnostics identify the corrected candidate as B2.1. No selection thresholds, gear criteria, lifecycle, or equipment commands change. A reserved-name regression check now rejects the broken declaration and checks the renamed call. Static success does not prove the corrected module loads in-game or that other errors will not appear.

## Isolated selector-validation milestone (2026-10-29)

**Official:** `item.GetCount(criteria)` returns inventory copies, not a matching-instance list. `*N` is displayed star-level filtering; `+N` is enchantment bonus filtering. The manual demonstrates `shiny`, `dL` and subtractive criteria, but provides no full save-code-to-selector dictionary. `item.left`/`item.right`, their IDs and gear power do not document unique saved-instance identity. See the [official manual](https://stonestoryrpg.com/stonescript/manual.html) and [validation matrix/procedure](EQUIPMENT_SELECTOR_VALIDATION.md).

**Community:** [Cobblestone](https://github.com/alexbarker234/stonescript/blob/main/Cobblestone.txt) narrows duplicates with bonus, effect and shiny criteria. No raw upgrade/star or raw ability/effect mapping is inferred from it.

**Implemented, not game-verified:** separate `EquipmentSelectorTest` diagnostic, default count-only; optional explicitly enabled Up-arm/Enter one-shot equip test. The private builder preserves provenance and raw variant profiles, emits fixed allowlisted selector hypotheses, never converts raw upgrades to stars, and defers unknown aliases. 130 records analyzed; 94 private queries; 30 queries span multiple saved profiles; 21 tentative equipment/tool records deferred. Native count one still requires inventory detail confirmation. All game match counts, exact variants, input gating and module loading remain untested. B2.1 is unchanged; no game-root deployment performed.

**Validation:** 23 Python tests pass, including synthetic installer backup/hash verification. Original save, normalized inventory, observer, B2.1, live deployment and pre-existing backup hashes are preserved. Static checks are not Stonescript interpreter tests. Future property mappings must cite owner-confirmed display/equipment evidence before automation integration.

Interrupted-session audit: the rejected installation had not executed; repository and both live roots remained B2, while the rename existed only in staging. A new verified backup precedes deployment of the correction. See [BUG_HARVEST_RESERVED.md](BUG_HARVEST_RESERVED.md) for the trace, remaining risks and Rocky retest. No location completion is promoted to verified.
