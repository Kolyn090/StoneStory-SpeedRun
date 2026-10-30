# Basic automation coverage

> This matrix describes the generic B2.1 baseline. The separate [Rocky R15 candidate](../rocky/ROCKY_PLATEAU_15.md) exists but is uncommitted, undeployed and not game-verified; it does not change any completion cell below.

2026-10-29: implementation candidate only. **No location or difficulty has a verified automated completion.** A named dispatch route is not a support claim. The original observer's loading test does not validate this new entry point.

## Scope and sources

The initial scope is the eight main locations named in the official manual's location/music examples and dispatched by [alexbarker234's public implementation](https://github.com/alexbarker234/stonescript/blob/main/Cobblestone.txt). The [official manual](https://stonestoryrpg.com/stonescript/manual.html) defines `loc`, `loc.id`, `loc.stars`, `loc.isQuest`, foe state/filter queries and equipment APIs; it is not a guarantee that generic tactics can beat every encounter. This is not an exhaustive enumeration of special events, Legends, or future content.

## Matrix

Each named route is implemented in `scripts/basic/locations/Dispatcher.txt` and invokes the same `combat/Generic.txt` policy through the entry point. This baseline matrix excludes the separate R15 boss specialization. All difficulties use the same candidate logic, with no tested difficulty range.

| Location / route | Implementation | Automated completion tests | Difficulties verified | Specialized logic to investigate if generic fails |
|---|---|---|---|---|
| Rocky Plateau / rocky | Generic combat/travel; no optional shovel harvesting | NOT RUN | None | Verify passage past objects without collection; Dysangelos phases, changing resistances, blocks/dodges |
| Deadwood Canyon / deadwood | Generic | NOT RUN | None | Wasp nest, Xylo root, Poena reflection/protection |
| Caves of Fear / caves | Generic | NOT RUN | None | Ceiling decorator and Bolesh damage/positioning windows |
| Mushroom Forest / mushroom | Generic | NOT RUN | None | Explosive enemies, Mushroom phase attacks |
| Haunted Halls / halls | Generic magic branch for physical immunity | NOT RUN | None | Pallas phases, summoned enemies and defensive windows |
| Boiling Mine / mine | Generic armor branch | NOT RUN | None | Explosions and Bronze Guardian hammer windows |
| Icy Ridge / icy | Generic | NOT RUN | None | Hrimnir wall, snowballs, chill effects |
| Temple / temple | Generic | NOT RUN | None | Nagaraja poison projectiles, boulder and positioning |
| Quest/Legend locations | Explicit observer-only guard | NOT RUN; automation excluded | None | Quest mechanics and permitted equipment require separate profiles |
| Unknown/event/other locations | Observer-only fallback | NOT RUN; automation excluded | None | Add explicit route after identifying location and requirements |

Boss concerns are community-informed investigation targets, not measured failures of this implementation. See [Scribble's boss notes](https://github.com/livercat/scribble) for attribution. No attack windows or thresholds were copied. Generic automation is not claimed adequate for bosses, elites, yellow tiers, or any other difficulty. There is no automatic map selection, difficulty selection, unlocking, or death/retry management.

## Acceptance progression

Current test order and expected observations: [BASIC_TEST_PLAN.md](BASIC_TEST_PLAN.md). Report actual trials in [BASIC_TEST_RESULTS.md](BASIC_TEST_RESULTS.md), beginning with Rocky Plateau. Completion status changes require explicit owner confirmation of an actual unassisted completion on the recorded difficulty/configuration. B2 deployment and static review do not change any NOT RUN entry.

1. Verify the new import and diagnostics with no conflicting equipment scripts.
2. On a familiar safe difficulty, verify actual item selection before attempting harder encounters. Do not assume a cached selector identifies the intended enchantment.
3. For each row, record build/platform, difficulty, deployed hashes/config, exact gear, potion policy, number of runs, successful completions, failures/manual intervention, and error text. Test at least three consecutive attempts including two observed loop boundaries as an initial smoke gate; this does not establish a statistical reliability target.
4. Exercise single-target melee/ranged, crowds, armor, immunity, low HP, target loss, and boss transitions where present. Retest observer lifecycle/measurement cases independently.
5. Promote only the specifically tested location/difficulty/config to tested status. Keep harder tiers and changed builds unverified. Investigate the first reproducible failure before adding specialized boss behavior.

Use the failure template in [OBSERVER_ACCEPTANCE.md](OBSERVER_ACCEPTANCE.md), adding handler, strategy, requested and actual equipment, missing-gear count, enemy ID/state/time/distance/armor, and whether the potion setting was enabled. Record game failure separately from a script error or incorrect selector. The current candidate has no automated failure detector.
