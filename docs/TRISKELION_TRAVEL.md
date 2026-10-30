# Triskelion travel: B2.1-TS

Owner rule, 2026-10-29: reduce travel time without sacrificing combat, boss handling, mandatory progression or protected sequences. Resources remain incidental. No farming, optional shovel harvesting, waits or detours. Triskelion movement has priority over Star Stone when equipment competes. This candidate is source-checked, not game-accepted.

## Evidence and mechanics

| Question | Evidence / limit |
|---|---|
| Selector and slot | [Official tutorial, Mobility and logical branches](https://stonestoryrpg.com/stonescript/) demonstrates `equipL triskelion` with `equipR shield`. Use exactly `triskelion`, not the internal save ID. This occupies a hand. |
| Passive or activation? | Tutorial uses equipment only; [official release notes](https://stonestoryrpg.com/releasenotes/) document its movement bonus, fixes and non-stacking duplicates. No activation/cooldown API is used or invented. |
| Movement conditions / magnitude | Official examples establish equipped travel use; sources reviewed do not establish an exact level formula or every movement/terrain restriction. The project's clear/full-HP/walking gates are safety policy, not native prerequisites. Measure rather than assume a fixed reduction. |
| Bonus after removal? | No verified post-unequip duration established. Implementation assumes no usable carryover and keeps Triskelion equipped through travel/collection. Do not claim a snapshot exploit or persistence. |
| Star Stone interaction | [Official pickup tutorial](https://stonestoryrpg.com/stonescript/) uses equip-only attraction below 10 units, not a claimed maximum radius. [Scribble](https://github.com/livercat/scribble/blob/master/scribble.txt) combines Star/Triskelion in opposite hands; [Cobblestone](https://github.com/alexbarker234/stonescript/blob/main/Cobblestone.txt) demonstrates Star in R and Triskelion travel. Current exact pair/slot effectiveness still needs a game test. |
| Detection / measurement APIs | [Manual](https://stonestoryrpg.com/stonescript/manual.html): targeted `foe`, distance/type, `foe.count` within 46 units, radius count, targeted `pickup`/distance/z, AI state/walking, HP, `totaltime`, and `player.framesPerMove`. No all-pickup enumeration, projectile-danger oracle, range-query or movement-forcing API is assumed. |

These are documented API/selection forms and community observations. They do not prove a numeric bonus, universal threat coverage, instant hand switching or net completion gain. Ranged attacks/projectiles can matter outside detection; the 46-unit guard is conservative, not a proof of all threats absent. No general protected-sequence or mandatory-tool module currently exists; future handlers must bypass the ordinary-travel policy.

## Decisions and slot ownership

Equipment inventory checks happen at init/fresh entry, never during combat frames. Triskelion and Star are optional; unavailable selectors add `triskelion`/`star` to Unavailable base, not Missing core. No private inventory/selector-validator integration is introduced.

| State | L | R | Decision |
|---|---|---|---|
| Clear travel, Triskelion enabled/available | Triskelion | Normal shield | Walking, full HP, no target/no foes within 46, no boss seen this attempt |
| Same travel plus bounded eligible pickup | Triskelion | Star Stone | Triskelion stays in the same slot; only R changes, with the inherited collection budget/spacing |
| Triskelion disabled/unavailable | Default sword | Normal shield | Existing ordinary travel fallback |
| Eligible pickup in that fallback | Star Stone | Normal shield | Previous passive-collection behavior retained |
| Any targeted enemy, even beyond 22/46 | Existing sword/wand/hammer decision | Normal shield | Immediately take existing combat policy; distance/immunity/armor/crowd/HP still select combat gear |
| No target but nonzero foe.count | Default wand | Normal shield | Threat readiness; no movement/collection stone |
| Low HP, not walking or boss already seen, with no foe | Default sword | Normal shield | Conservative travel fallback; no optimized stone request |
| AI disabled/paused or core gear missing | No new commands | No new commands | Existing safety/manual behavior preserved; an old loadout can remain until native AI permits decisions |
| Unknown/quest route or automation disabled | Observer-only | Observer-only | Dispatcher still prevents generic automation |

`Catalog.ApplyPair` is the sole shared equipment executor; old combat `Apply(weapon)` delegates with the normal shield. The field `selectedShield` now means requested R selector and may show Star Stone. Diagnostics Want/Have L/R remain meaningful. Normal combat commands/order are preserved through that wrapper.

Intentional preparation fix: the old `!foe | foe.distance > 22` branch kept a sword until a target crossed 22, even for ranged threats. Now only `!foe` enters travel; any targeted enemy reaches the existing combat policy and can prepare ranged gear earlier. Immunity conflict remains manual, but explicitly equips default wand/shield so a travel-only pair is not left equipped. No damage/immunity solution, boss strategy or AAC is added.

Triskelion has **no hold/retry timer or fixed travel delay**. It stays in L while safe clear movement continues. State transitions follow actual detection, walking, HP and the existing boss-seen latch; no alternating frame pattern or stone hand migration. Star retains the 15-frame maximum / 90-frame minimum-start-spacing / presence-window latch. During combined collection only R changes to Star and back; Triskelion is never removed for collection. No resource disappearance is awaited. If dual equipment fails in-game, disable Star rather than cycling Triskelion to another slot.

Both slots change back to combat gear on the next eligible policy frame when an enemy is targeted/reported. First-hit delay, pending projectile effects, shield loss during clear-area collection, native AI walking feedback and detection jitter remain in-game tests. This does not claim zero boundary oscillation under noisy native input; report it rather than adding arbitrary wait frames. Native movement is not directly controlled.

## Configuration and diagnostics

`scripts/basic/config/Settings.txt`: `triskelionTravelEnabled = true` independently enables movement; `passiveStarEnabled = true` retains collection. Disable either for benchmarks, in both live copies, then start fresh so lookup caches refresh. Existing Star distance/hold/spacing bounds remain unchanged. No new timing constants or native abilities.

Header **B2.1-TS**; strategies `travel-triskelion`, `travel-triskelion-star`, `travel-star-passive`, `travel-shield`, `threat-ready-shield`, or existing combat labels. Optional diagnostics add `Move frames` from `player.framesPerMove`; lower values mean fewer simulation frames per position, not proof of a faster complete run. Disabled diagnostics perform no rendering/read for this additional value. Existing lifecycle/measurement correctness remains unverified.

## Owner acceptance and comparisons

1. Fresh safe Rocky Plateau run with only `import SpeedRunBasic/main`; expect B2.1-TS, Missing core none, no Tab errors. Do not generate resources by harvesting. Observe a clear walking segment: expect Triskelion L + shield R. Record build, difficulty, exact displayed gear and Move frames.
2. Repeat matched travel segments with Triskelion false/Star false, Triskelion true/Star false, and both true. Keep all other settings/build/difficulty/gear and entry-versus-loop conditions fixed. Record travel splits, first attack, full completion/failures and movement frames. Flags compare modes of this revision; they do not undo its early combat-preparation change. Full B2.1-PS rollback is separate.
3. With both enabled, approach a naturally existing nearby pickup under clear/full-HP/walking conditions. Expect `travel-triskelion-star`, Triskelion still L, Star R instead of shield. Observe attraction and Move frames without manual activation, waits or detours. After budget/eligibility ends expect shield R restored, Triskelion L unchanged. If no eligible pickup occurs, record SKIPPED.
4. Observe an approaching ranged enemy and a melee enemy separately. Record first detected foe/distance, strategy, requested/actual hands and first attack. Any target must choose combat, even beyond the old 22-unit cutoff; no-target reported enemies should request wand/shield. Stop if a travel pair persists into active combat or the first attack is delayed. Do not provoke unsafe mechanics just for a test.
5. Test stopped movement, low HP naturally encountered, boss entry/post-boss period, missing optional stone, fresh-entry/Ouroboros reset, and applicable native progression interactions. Do not infer a supported difficulty or completion from import/UI alone. Check for rapid mode flips at detection boundaries and whether native AI walking toggles cause gear feedback.
6. Compare movement frames with Triskelion equipped, then normally removed after combat transition, and in a separate safe controlled manual observation if needed. Record any observed carryover without assuming its cause/duration; no active-save modification is needed. Measure actual completion timings over several paired runs before choosing flags. Keep Star disabled if it worsens time/reliability even while Triskelion remains enabled.

Report: `build/revision; map/difficulty; flags; displayed stone levels; before/during/after Move frames; requested/actual L/R; enemy type/distance and first attack; pickup distance/attraction; mode flips; travel/completion timing; failures/interventions; Tab errors`. No private identifiers/save contents. No completion safety, exact movement formula, bonus persistence or speed gain is verified yet.

## Preservation, static checks and deployment

Both prior B2.1-PS trees were backed up and hash-verified before edits at `backups/pre-triskelion-20261029-fe9842b2/{steam-SpeedRunBasic,save-SpeedRunBasic}`. Keep every older backup. Importer, isolated selector validator, private data, observer, dispatcher and Mind Stone text must remain unchanged. Rollback restores only the corresponding five SpeedRunBasic modules and starts a fresh run; never restore whole save folders.

Validation/deployment completed 2026-10-29: static checker passed before and after installation; all **30 Python tests passed**. New source-contract mutations reject losing the Triskelion slot, restoring the 22-unit shortcut, adding a timed travel wait, unguarded equipment lookup, bypassing the requested offhand and invented Triskelion activation. Both benchmark flags are accepted independently. These are static regressions, not executed game physics/AI tests.

All five modules were installed into each existing Steam/save-folder SpeedRunBasic root, after rechecking live files against the verified backups; all **10 deployed hashes match source**. **79 protected original files** remain byte-identical, including the dispatcher, observer, selector validator/importer, private inventory and previous backups. Only four intended basic source files and their live copies changed, plus documentation/test infrastructure. Mind Stone text was not accessed, no active save was read/edited, and no private data was staged.

Reproduce with `powershell -File tools/Test-BasicStatic.ps1` and `python -B -m unittest discover -s tests -p 'test_*.py'`. Static contracts/mutations cannot execute Stonescript or simulate movement, native enemy detection, equipment effects or pickup physics. All game cases remain **NOT RUN**, including both-stone effectiveness, numeric speed bonus, carryover, ranged first-hit timing, boundary stability, mandatory progression and completion benchmarks.
