# Resource policy and B2.1-NR acceptance

Owner requirement, 2026-10-29: resources are effectively unlimited. Optimize reliable progression, movement, combat, bosses and total completion time. Resource accumulation/farming/optional harvesting is never a goal. Resources obtained during required actions are incidental. Potion activation permissions remain unchanged; this policy does not silently enable consumption.

## Architecture and source audit

Previously `Generic.Tick` entered travel mode when no foe was present or its distance exceeded 22, then switched to a cached shovel whenever any harvest target was within 7. It did not identify a mandatory obstacle, quest state, location-specific requirement or traversal phase. It therefore prioritized optional collection over the travel loadout. `Catalog.Prepare` also queried shovel availability and could report it missing despite no progression dependency.

B2.1-NR removes that branch, `harvestEnabled`/shovel settings, shovel availability search/field and the unused `EquipHarvestTool` helper. Travel continues directly to the existing default sword/shield application. Header is B2.1-NR so the owner can identify the policy. All offensive/defensive selectors, ranges, immunity decisions, HP thresholds, potion guard, dispatcher and observer remain unchanged. No per-frame replacement logic or new API is added.

Required progression is an explicit architectural exception, not optional collection. Future location handlers must identify the mandatory object/phase with evidence, request the minimum needed tool/action, stop once passage is possible and restore combat gear. Do not use a generic harvest-distance fallback, globally disable pickup/AI, discard utility equipment or claim all tools are unnecessary. No separate mandatory-tool handler exists in the current source; none was removed. Native utility-belt interactions are not changed, but their successful operation under combat equipment is not established by this audit.

The [official manual](https://stonestoryrpg.com/stonescript/manual.html) documents `harvest` as a harvestable target and `harvest.distance` as its distance. These do not establish that an object blocks passage. The change uses only existing language forms and removes behavior. No undocumented `disable harvesting` or `disable pickup` command is assumed. Public [Cobblestone](https://github.com/alexbarker234/stonescript/blob/main/Cobblestone.txt) is reference material, not proof that a tool branch is mandatory or optimal for this inventory/build.

## Static checks and deployment gate

Run `powershell -File tools/Test-BasicStatic.ps1` and `python -B -m unittest discover -s tests -p 'test_*.py'`. The static checker now rejects reintroducing harvesting queries/old shovel helper/configuration in the generic framework while retaining the reserved-name regression. The new `tests/test_no_resource_policy.py` executes the checker on temporary copies, verifies the current source passes, and confirms that injected harvest queries, collection settings, shovel fields and the reserved helper fail. This guard is scoped to current generic files; future verified progression mechanics should live in a location-specific path with an intentionally updated test contract.

Before replacing anything, back up both current `SpeedRunBasic` trees, verify every copied file against its live original, and preserve all old backups. Stop on unexpected source/live divergence. Verify every deployed module against repository source after copying. Preserve the observer, inventory data, selector diagnostic, Mind Stone text, saves and unrelated files. Deployment evidence is recorded below after execution.

Static dependency verification can establish that no implemented mandatory progression handler changed. It cannot establish every map's actual passage/completion behavior. All in-game tests below remain **NOT RUN**. No speed improvement or successful location automation is claimed.

## In-game acceptance

1. Start a fresh safe Rocky Plateau run with only `import SpeedRunBasic/main`, preserving any prior Mind Stone text before changing imports. Expect header B2.1-NR. Confirm no Tab errors and no missing core gear.
2. With no nearby enemy, approach optional boulders. Expect `travel-shield`, sword in L and shield in R; no `harvest`, two-hand shovel request or missing-shovel warning. Check that walking continues toward combat/boss progression rather than stopping to mine. Native incidental drops/pickups may still occur.
3. Verify normal ranged/melee, armor, crowd and boss transitions remain as before. Do not infer this change fixes broad selector ambiguity or boss mechanics.
4. At any actually mandatory interaction, observe whether the character progresses. Record map/difficulty, object/phase, strategy, actual/requested gear, position/time stalled and whether a tool/manual input resolves it. Stop or rescue manually if blocked; classify the result as assisted. Do not re-enable blanket harvesting. A narrow progression exception requires separate evidence and implementation.
5. On other accessible maps, specifically watch river/waterfall/door/wall/traversal transitions **where encountered**; these examples are test prompts, not claims that B2.1 implements each mechanic. Quest/unknown routes remain observer-only. Repeat safe loop and fresh-entry checks. Report time/completion/failures; never judge success by resource yield.

Report: `build; revision; map/difficulty; object/phase; strategy; requested/actual hands; movement continued?; combat/completion outcome; intervention; Tab errors; elapsed metric`. Completion and progression safety stay unverified until owner confirmation. For rollback, restore the five SpeedRunBasic files from the corresponding new backup and start a fresh manual run; do not restore whole save folders or delete historical backups.

## Deployment evidence

Completed 2026-10-29:

- Static checker passed before deployment and again afterward. All **25 Python tests passed**, including the four negative mutation cases in the new policy test.
- Both live roots matched the original repository B2.1 files before replacement. Backup: `backups/pre-no-resource-20261029-5d016ed4/steam-SpeedRunBasic` and sibling `save-SpeedRunBasic`. Every backup file was hash-verified before any overwrite; older backups remain unchanged.
- Installed all five B2.1-NR modules under the existing SpeedRunBasic namespace in both Steam and save-folder Stonescript roots. All **10 installed file hashes match source**. The dispatcher remains byte-identical.
- Verified **56 protected original files** unchanged, covering the observer, dispatcher, selector diagnostic, gear data, private exports/normalized/probe output and pre-existing backups. Only four intended basic source files and their live equivalents changed. Mind Stone text was not accessed or overwritten; no active game save was read or edited.
- In-game parsing, passage past objects, mandatory tool interactions, completion reliability and timing are **NOT RUN**. The static audit established absence of removed mandatory-tool handlers, not all-location progression safety. Start a fresh manual run for settings/imports to reload and report results before treating this revision as accepted.
