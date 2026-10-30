# Stonescript knowledge and evidence rules

This is the authoritative language/evidence reference. It does not certify a build's gameplay behavior. Current deployment/source status belongs to the [index](README.md); implemented ownership belongs to [architecture](ARCHITECTURE.md); current Rocky decisions belong to [R15](rocky/ROCKY_PLATEAU_15.md). Historical milestone notes are [archived](archive/KNOWLEDGE_MILESTONES.md).

## Project policies and data sources

Resources are incidental. Never farm, detour or equip a shovel for optional collection; preserve proven mandatory progression. [Triskelion travel](TRISKELION_TRAVEL.md) owns movement/slot rules and [passive Star collection](PASSIVE_STAR_STONE.md) owns collection bounds and priority. Do not replace those current policies with archived NR/PS behavior.

Use the [gear evidence review](gear/GEAR_REFERENCE_REVIEW.md) for displayed fields/units/conflicts, [current crosswalk](rocky/ROCKY_EQUIPMENT_CROSSWALK.md) for identity evidence (including owner-confirmed FastGenShl), and [selector guide](gear/EQUIPMENT_SELECTOR_VALIDATION.md) for isolated diagnostic behavior. Raw upgrades do not become stars or native selectors. Model visual review, owner confirmation and native execution are separate evidence classes.

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

## Native parser finding: reserved profile identifier

Owner-reported R15 import failure was traced in the local game log to `Variable "profile" is reserved` at `SpeedRunRocky/main` line 8. Avoid `profile` for project variables and parameters; the candidate uses `rockyConfig`. This is native error evidence, not an exhaustive documented reserved-word list. An outer Mind Stone `Incomplete parsing` error can accompany this underlying imported-module failure. See [the R15 correction](rocky/ROCKY_PLATEAU_15.md#first-native-load-failure-and-minimal-parser-correction). Post-fix native execution remains pending.

## R15 first gameplay evidence and recovery proposal

Owner-reported: parser-corrected R15 ran, defeated Scout, then died against Bearer holding Fire Sword + FastGenShl; later phases were not reached. Post-Scout Triskelion failed to return. Source review found Scout incorrectly setting the shared boss-travel latch. Its Rocky-only correction and Bearer-only 60%/85% HP recovery hysteresis are implemented in the working tree but undeployed/unverified. See [current revision rules](rocky/ROCKY_PLATEAU_15.md#next-candidate-post-scout-travel-and-bearer-recovery). Existing no-target/nearby-enemy/walking/full-HP travel guards stay intact.

Official syntax: `hp`, `maxhp`, arithmetic/comparisons, persistent variables and `vigor sword dL` are documented in the [manual](https://stonestoryrpg.com/stonescript/manual.html). Screenshot 0053 visibly says **109% chance to Lifesteal**, not a 109% damage-to-healing ratio. Exact recovery selector, healing amount, switch costs and ★15 survival remain in-game questions. No timed Bearer defense is added.

## Perfected ray observation gate

Owner reports the second ★15 trial defeated Scout/Bearer/Elementalist and reached Perfected, whose ray killed in one hit. This is a burst-survival failure; it does not validate historical state-115 timings. A working-tree diagnostic-only top-row trace uses documented state/time, distance, HP, total frames and named-color printing; it is undeployed/unverified. See [capture and evidence limits](rocky/ROCKY_PLATEAU_15.md#perfected-ray-timing-diagnostic--not-deployed). Last sampled state frames are not guaranteed exact impact frames. No new attack response or Mind Stone action is implemented.

## State-115 alive sample and experimental dodge boundary

Owner capture at Rocky ★15: Perfected 115:23, player 80/80 HP, distance 5, Poison Sword + FastGenShl, boss 12,964/30,000 HP; previous 114 reported 14 frames (a trace last-sample value is not necessarily complete duration). State 115 occurs while alive; actual impact frame remains unknown. A local, undeployed protected Mind Stone experiment uses configurable 23-frame trigger / 30-frame hold / 90-frame timeout; none is a verified avoidance window. Equip-only behavior is community evidence; unique selector match, actual backflip/cooldown, shield compatibility and ray avoidance still need native testing. See [the authoritative sequence and acceptance procedure](rocky/ROCKY_PLATEAU_15.md#experimental-perfected-mind-stone-sequence--local-only).
