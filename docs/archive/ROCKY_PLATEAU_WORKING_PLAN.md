# Rocky Plateau working plan

> Historical record. Preserved behavior, timings, test counts and commands describe that development stage. This is not a current deployment or implementation guide. Start at the [documentation index](../README.md) and [current R15 guide](../rocky/ROCKY_PLATEAU_15.md).

**Owner correction (2026-10-29): FastGenShl is a Towering Shield nickname, not Compound Shield.** The owner also reports it can be used as an in-game name reference. Earlier Compound-to-0010 identity/probe suggestions in this historical review are superseded; do not use Compound queries to identify FastGenShl. Keep screenshot 0010 and 0065 stat/effect profiles separate. Existing private crosswalk files are preserved historical hypotheses and must not be treated as corrected exact-instance joins. See [current R15 selector policy](../rocky/ROCKY_PLATEAU_15.md).

Prepared 2026-10-29. **Planning only.** This document proposes later work; it authorizes no implementation, deployment, selector changes or Git operations. Existing scripts, equipment CSVs, private inputs, validator and deployments remain unchanged.

## 1. Executive summary

Build on the existing **Rocky R1** candidate rather than creating another combat system. Establish one reliable, equipment-aware Rocky difficulty first, then optimize that exact configuration and expand difficulty/loop coverage separately.

The smallest useful implementation is a **personalized shielded Bearer baseline** within R1: keep the current encounter/transition ownership, confirm only the weapon and shield needed for that decision, and use their explicit Rocky-only equipment requests. Fire Sword plus the upgraded shield corresponding to FastGenShl is a starting hypothesis, not a predetermined winner. Stone Sword is the first physical comparison. Retain the current other-phase behavior initially, clearly marked unverified; passing Bearer does not establish full-stage automation.

Next stabilize Elementalist matching, Perfected adaptive defenses and one-handed armor handling. If a dangerous attack prevents completion, calibrate one defensive response before pursuing burst damage or travel improvements. Heavy Hammer is a later challenger because its equipment/activation sequence is absent from the current executor. Do not delay a needed survival fix to finish an optimization checklist.

Use actual runs to choose the next change. No broad selector campaign, runtime CSV parser, universal gear scoring engine, harvesting, AAC or large collection of copied boss timers is proposed.

## 2. Current automation assessment

### What is present and reusable

| Component inspected | Current behavior | Use in the plan |
|---|---|---|
| `scripts/basic/main.txt` | Entry/loop/attachment initialization, dispatch, one combat tick and one observer tick; optional diagnostics | Preserve live B2.1-TS as baseline and rollback |
| `scripts/basic/locations/Dispatcher.txt` | Recognizes eight main routes, rejects quest/unknown routes; Rocky is a label | Reuse route gate; a route label is not successful support |
| `scripts/basic/combat/Generic.txt` | Range hysteresis at 5/7, wand crowd/boss policy, elemental choice, optional low-HP lifesteal; Triskelion/Star clear-travel gates | Retain fallback for ordinary/unknown encounters; do not tune other stages for Rocky |
| `scripts/basic/equipment/Catalog.txt` | Init-time availability cache and immediate one-handed `Apply`/`ApplyPair` commands; broad defaults/fallbacks | Reuse one-handed execution, but recognize that availability is not exact-item identity |
| `scripts/rocky/main.txt` | Separate `SpeedRunRocky` entry; calls Rocky first only on Rocky; calls Generic only when unhandled | Keep this integration seam and single observer call |
| `scripts/rocky/locations/RockyPlateau.txt` | Scout/three-phase recognition, boss-gap latch, adaptive exclusions, armor priority, stable Perfected preference and warnings | Extend incrementally; do not rewrite the state machine |
| `scripts/rocky/equipment/RockyGear.txt` | Strict init-only elemental availability and deterministic fallback order | Add a small reviewed role-to-selector configuration when required, not dynamic stat parsing |
| `scripts/metrics/RunMetrics.txt` | Existing completion observer using native time/completion values | Preserve; verify resets/capture against one independent timed run before trusting it for speed claims |
| Isolated selector diagnostic | Installed count-only in both known roots, unchanged 94 cases | Use one relevant case when a real loadout decision requires it; loading is not yet owner-confirmed |

R1 is prepared and documented but **not deployed or game-verified**. There is no owner-confirmed unassisted Rocky completion, B2.1 switching pass, exact-item selector pass, or observer timing/loop pass in the reviewed records. Original observer loading/display is confirmed; validator file installation/hash verification is confirmed. These are different evidence scopes.

### Missing capabilities and constraints

- **No strongest-owned-item selection.** Shared selectors can match duplicates. Missing elemental preferences can fall back to broad items; R1 is stricter, but its ordering is not a measured ranking.
- **No two-handed executor or protected ability sequence.** `ApplyPair` requests L then R. Adding Heavy Hammer through that path would risk incompatible or overwritten equipment. R1 currently uses only one-handed hammers.
- **No calibrated attack avoidance.** R1 does not time a Mind Stone response or distinguish all repeated attacks. Its shield baseline may fail a major phase-3 attack even with good DPS.
- **Diagnostics do not stop native combat.** A strategy label containing `manual`/`STOP` does not pause the game or guarantee harmless equipment. Some fallback branches still request a generic wand. Unknown mechanics must remain explicit blocked/untested outcomes, not claimed safe completion.
- **Shared low-HP policy can override a hammer decision.** R1 guards healing behind a sword decision, so its armored boss policy avoids this particular override. Do not import Generic's low-HP behavior into that policy. Any shared correction later needs a separate regression review for other stages.
- **State/reset and fallback metadata need runtime checks.** R1's encounter latch deliberately survives some boundaries; the observer still starts on `loc.begin`. Validate actual sub-location behavior. When a requested hammer falls back to another family, record the actual selected family/element rather than assuming the requested family describes it.
- **Travel is deliberately conservative.** Any targeted enemy wins over travel equipment; nearby counts cover 46 units. Special handling sets the boss-seen travel flag even for Scout, which can suppress later Triskelion travel. This is a possible later timing opportunity, not a reason to weaken threat handling now.
- Scripts execute each frame. Native API reads can be current each frame, while inventory searches and role configuration stay at initialization. No native pickup-event, saved-instance enumeration or runtime CSV API is assumed.

## 3. Evidence and encounter analysis

Labels used throughout:

- **Official:** documented syntax/API, not proof of a current enemy mechanic.
- **Display-confirmed:** a specific field visually checked against a local screenshot by the model; not owner verification or runtime testing.
- **Transcription:** screenshot-derived CSV text not individually rechecked.
- **Community:** implementation or observation from a cited public source; build/gear dependent.
- **Proposal/unresolved:** an intended local policy or question requiring actual gameplay.

### Stage sequence and decisions

| Segment | Supported understanding | Proposed behavior | Gameplay observation needed |
|---|---|---|---|
| Entry and open travel | Shared travel exists. Community annotated Rocky says the normal combat types are Scout and Dysangelos, not a long trash-wave roster | Existing clear-travel Triskelion; preserve mandatory interactions; no shovel farming or detours | Actual route, obstacles/dialog, first target distance, and whether the chosen difficulty has any unexpected foes |
| Scout, when encountered | Community identity `acronian_scout`; source comments place it at 11+ stars. Threshold and current mechanics are not locally verified | Stable weapon + shield baseline. Armor response only if native armor is observed. Compare physical/Fire damage, then a single control/sustain alternative if needed | Whether present, actual ID/filters, attack style, armor, stun/Chill susceptibility, damage and time. Absence is NOT ENCOUNTERED, not a pass |
| Dysangelos Bearer / phase 1 | Community sources prefer Fire or other elemental melee and defensive handling; numeric schedules disagree | Confirm phase, use one stable shielded damage choice, keep defense available; benchmark Fire against physical Stone Sword | Current phase labels/ID, whether Fire has an actual advantage, major hit/stun pattern, whether passive shield effects apply |
| Transformation gaps | Existing R1 explicitly handles missing/dead/undamageable targets while boss-latched | Retain encounter ownership and defensive loadout; no travel/Star override; change phase only from observed state | Missing-target duration, sub-location boundaries, actual completion versus transformation; no guessed timer-based phase advance |
| Elementalist / phase 2 | Community code matches changing elements; sources describe temporary debuff protection, especially around Vigor behavior | Select one suitable owned element, switch on a real element/protection change; immunity/availability override damage preference | Target filters versus visible eye/element, protection representation, whether selected counter improves damage. Do not assume every eye icon is already a native weakness label |
| Perfected / phase 3: ordinary attacks | Community records include repeating attacks, a stun/shield event, armor gain and adaptive elemental defenses | Keep an allowed element stable, react to actual armor, exclude observed adaptive elements; avoid unnecessary refresh swaps | Actual adaptive UID format, whether exclusions accumulate, armor timing/amount, attack-cycle distinction, dangerous stuns |
| Perfected: major energy/ray attack | Several implementations use Mind avoidance but disagree on timing origin/window. The community state table labels 115 post-damage | If this is a failure bottleneck, add one separately calibrated defensive sequence with protected restoration/reapproach | Actual impact at current distance/build, cooldown and equip behavior; repeat with Chill only after a no-new-debuff baseline |
| Completion and optional Ouroboros | Native completion metrics and loop state exist; observer correctness is pending | Capture completion once, reset attempt-specific state correctly, keep first-entry/loop results separate | Final-phase completion, no false intermediate completion, loop reset and changed encounter behavior |

Do not invent ordinary enemy species or swarm mechanics to fill coverage. Unknown foes keep the shared fallback and a diagnostic label until a real encounter warrants a narrow handler. Difficulty/quests can change the sequence; do not force all three phases or Scout into every run.

### Elements, armor and survival

The screenshot descriptions support these **conditional bonus targets**: Poison weapon → Vigor foe; Vigor → Æther; Æther → Fire; Fire → Ice; Ice → Poison. This is evidence for the listed item effects. It is not proof that every boss phase has an additional universal weakness multiplier. Current phase-2 filters and the effect of the counter-element on secondary boss effects require observation.

Treat armor as a separate decision from elemental matching. Use actual `foe.armor` rather than assuming an attack animation means armor is present. A Hammer's `x armored damage` differs from a flat elemental bonus. Heavy Hammer's Armor Fatigue reduces **armor gain**, not necessarily existing armor; it may be valuable only if applied before a relevant gain event and allowed on that target.

Survival wins when an attack can kill/stun-lock the player before the extra damage pays off, when a two-handed weapon removes necessary protection, when debuff protection invalidates an intended control effect, or when a dodge prevents more lost attack time than a DPS increase gains. A higher survival rate can reduce total time per successful completion even if successful-run median is slightly slower.

Do not assume every boss is susceptible to Compound stun, Hammer stun, unmake, Chill, percentage HP effects or cleanse. Observed immunity/protection takes priority. A shield may be useful for armor even if its attacker-status effect is ineffective.

## 4. Owned-equipment comparison and candidate loadouts

The new data has 65 descriptions/258 fragments. The offline inventory has 130 records, including 11 sword, 15 wand, 16 crossbow, 6 hammer, 17 shield and 8 staff records; these counts are not distinct verified equipped instances. Relevant tools/stones and special weapons also exist as structural candidates. All exact ownership-to-screenshot joins remain provisional until the selected item is inspected.

In the table, damage/DPS/range are the displayed/transcribed values, **not recomputed total effective DPS**. Do not add crit/elemental multipliers onto displayed DPS until inclusion rules are known.

| Candidate | Evidence and role | Alternatives / reason not to assume optimal |
|---|---|---|
| Fire Sword 0055 | Display-confirmed 18 / 108 / 5, 13% crit x4, flat +85 vs Ice. One corresponding Fire short-sword saved profile | Good first elemental case; bonus depends on target. Physical Stone Sword or a different counter-element may win |
| Stone Sword 0064 | Transcription 70 / 150 / 5, 25% crit x12. Two basic-sword saved profiles make broad selection ambiguous | Strong physical benchmark and potential adaptive-unknown fallback. Confirm the high-grade variant only when used, not merely any `stone sword` |
| Other elemental Swords 0052–0054/0056 | Base 18 / 108 / 5. Poison/Fire/Ice transcribe +85 against their target; Vigor/Æther +9 plus 109% Lifesteal/65% unmake descriptions | Matchups/sustain differ substantially despite equal base DPS. Retain >100% display values without inventing a healing formula; unmake may not affect bosses |
| Elemental Wands 0066–0070 | Transcription 20 / 100 / 20, 100% splash, flat +100 against target element; Poison values visually checked | Range/readiness and physical-immunity fallback while retaining shield. Single-boss splash may offer no extra benefit; opening attack and projectile behavior need measurement |
| Elemental Hammers 0024–0028 | Fire visually 28 / 84 / 5, 6.6x armored damage, +24 vs Ice, .4s stun. Poison/Æther/Ice transcribe 28 / 38.18 / 5, 6.6x and +105 vs target. Vigor transcribes 100 / 136.36 / 5, 2.4x, +24 and 1.03s stun | First armor experiment should keep a shield. Fire is not automatically best: compare an allowed element and actual armor-removal time. Stun may be ineffective on the target |
| Heavy Hammer 0061 | Display-confirmed 69 / 69 / 7, 2.8x armored damage, splash/stun; active -75% armor gain for 25s, 22s cooldown. One saved profile | Requires separate hand/restore ownership. First compare basic attacks against one-handed Hammer+shield; test active only if regeneration is a measured bottleneck |
| FastGenShl 0010 | Display-confirmed 1.75 armor/s, 35 armor, attacker stun 1.4s. Tentative Compound alias; two saved Compound profiles, only one enchanted | Strong unconditional defensive baseline. Exact custom-name/base identity remains unconfirmed; do not choose the basic duplicate |
| Vigor Shields 0038/0039 | Display-confirmed .7 armor/s, 7 armor, 30% evade. Healing variant: +1.8 engaging Æther armor and 70% heal-2 on attack; other: +7.2 engaging Æther armor | Both saved profiles have level-21 enchantment structures. +21 does not distinguish them. Choose neither by name alone; healing/conditional armor may beat raw armor only in the right encounter |
| Ice Shields 0044/0045 | Display-confirmed .7 armor/s, 7 armor; 15% evade/+1.8 engaging Poison armor/31.8s Chill versus 30% evade/+7.2 conditional armor | Control may improve survival but can invalidate previously calibrated timing. Shiny is only a refinement hypothesis, not proof of selecting the Chill variant |
| Other elemental shields | Distinct elemental-armor and attacker effects in the CSV; retain all variants | Consider only after observing a matching threat. No global best-shield score from evade or conditional armor alone |
| Towering 0065 | Display-confirmed 1.75 armor/s, 14 armor, -8 damage to armor, -2 movement speed | Situational mitigation challenger, poor default travel choice. Do not interpret -8 as unconditional HP damage reduction |
| DashStaff 0011 / Dashing / Bashing | DashStaff displayed 16 / 34.29 / 5, armor and 4.4s mini-dash cooldown; two saved Quarterstaff candidates. Shield descriptions show approach/dash effects | Movement sequence/hand loss can delay first attack or undo a dodge. Defer until ordinary travel and boss safety are measured |
| Triskelion / Star / Mind | One saved candidate each; existing travel uses equipped Triskelion and bounded Star. These stones are absent from the 65 detailed screenshots | Preserve conservative clear travel, opportunistic collection only. Mind is a later defense candidate with separate behavior verification, not an assumed activate-like-Quarterstaff action |
| Crossbows / big swords / named staves | Crossbow range 22, Repeating 20/200 with guaranteed crit described; big swords 28/120 with splash/status; several staves 78/167.14 with range 20/abilities | Two-handed roles and shield loss must be confirmed. Missing Fire/Ice crossbow fields and variant mismatches preclude automatic ranking. A range/crit/stat advantage is an experiment, not a deployment priority |
| Bardiche, Blade, Skeleton Arm, named Wands/talismans | Potential burst, protection, sustain or debuff roles; Blade visually 550/275 rather than legacy 500; Skeleton transcribes 80/300 and evade stacks | High sheet DPS does not prove boss value. Costs, active target restrictions, immunity and restoration can dominate. Skeleton theft/resource gain is not a goal. Berserker Staff increases incoming as well as outgoing damage; Reset cleanse may erase helpful debuffs. Defer until a bottleneck justifies one item |

### Proposed loadout roles, in order

1. **Stable shielded baseline:** a confirmed damage weapon plus confirmed upgraded FastGenShl/Compound candidate. Fire for the first Bearer hypothesis; physical Stone Sword is the first damage comparison. Keep one weapon stable through ordinary attacks.
2. **Matched-element shielded loadout:** only change weapon when the observed Elementalist counter, adaptive exclusion or immunity requires it. Confirm each additional selector when that branch is first needed.
3. **One-handed armor loadout:** an allowed elemental Hammer plus the already confirmed shield. Restore the unarmored role when native armor clears, without adding arbitrary waiting frames.
4. **Sustain/control alternatives:** one independently tested Vigor sword/shield or Ice shield. A low-HP branch must not discard the only effective armor counter, use an excluded element or interrupt a necessary defense. Add an observed exit threshold only if boundary oscillation occurs; do not copy arbitrary healing delays.
5. **Heavy/active and movement challengers:** separate, opt-in experiments after the relevant owner/restore contract exists. Never put Heavy into the one-handed ApplyPair path.

Legacy `armor_mul` misclassifies flat elemental bonuses on 19 weapon rows, and Heavy's multiplier is under `ele_dmg`; preserve those catalogs as conflicting references, not ranking input. The new CSVs are primary displayed-stat evidence with individual verification limits. `+21/21` does not identify stars. No private pointers, item signatures or raw save codes become native selectors.

## 5. Proposed decision architecture

### One frame, one owner

Use the existing Rocky-first `handled` contract. Keep the policy ordered:

1. Run/reset bookkeeping and current AI/target state.
2. Resolve a previously validated emergency response or protected sequence. A sequence may be interrupted only by an explicit higher-priority emergency/invalid-target rule.
3. Mandatory progression interaction if actually observed and supported.
4. Boss transformation ownership and phase/Scout policy.
5. Armor/immunity/adaptive-compatible offense, with eligible sustain subordinate to those constraints.
6. Verified approach movement, then clear-travel Triskelion.
7. Opportunistic Star collection, only if it cannot disrupt any higher owner or Triskelion benefit.
8. One selected equipment action, optional eligible activation, and one observer update.

This is conceptual ordering, not a new native event API. Poll essential changing state each frame. Cache inventory availability at initialization; refresh on a deliberate new run/configuration change, not through repeated per-frame searches. Five-element masks and a few scalar fields are enough.

### Detection and selection

- Start with native location, target identity/filter, phase tags, distance, HP/armor and immunity information. Use community names only as fallbacks with a visible unknown state. Do not equate arbitrary numeric state ranges with phases.
- For phase 2, map an actually observed target element to its relevant owned role. For phase 3, exclude confirmed adaptive elements; parse only when needed and preserve an honest unknown-format path. Prefer documented effect queries once the actual UID is observed, not guessed save ability codes.
- Select by **eligibility first** (hand mode, target immunity, armor, element exclusion, sequence ownership), then the current measured role preference. Do not multiply raw CSV columns into a universal score.
- Keep the last allowed choice while the relevant state remains unchanged. Switch for a real role change, not because five equivalent preferences are reevaluated in different order. A boss gap preserves defensive ownership rather than entering travel.
- Existing range hysteresis is a starting policy, not every weapon's range. A confirmed range-6/7 weapon or ranged enemy may warrant a Rocky-only approach threshold later. No fixed pre-attack delay is proposed.
- Unexpected multi-enemy counts use the existing shared wand/crowd fallback unless the boss owns the frame. Add a true group rule only after a group is observed; never let AoE override a necessary boss defense.

### Integration without other-stage changes

Add reviewed role overrides to `RockySettings`/`RockyGear`, used only by Rocky specialization. For a specialized one-handed action, call existing `gear.ApplyPair(chosenWeapon, rockyShield)` once. Do not mutate shared `settings.swords`, `gear.shield` or global defaults to personalize a single stage.

The main entry skips Generic after any handled Rocky action. For unhandled frames, no Rocky equipment/ability command has been issued; Generic executes once. Existing ordinary travel initially remains shared and unchanged. If personalized travel shield or post-Scout Triskelion later needs a Rocky override, give that route an explicit owner rather than appending a second equipment command after Generic.

When justified, put a small two-handed/ability helper under `scripts/rocky/` first. Its request explicitly has pair or two-handed mode, item, activation intent, owning phase and bounded stage/deadline. A two-handed frame suppresses both one-handed writes. Equip, check documented eligibility, activate once when allowed, preserve the tested action window and restore the correct current role. Do not assume cooldown zero or same-frame equip means activation succeeded.

Keep current repeated equipment-command semantics initially. Avoiding repeated commands may be useful, but skipping solely because the last requested string is unchanged can fail after manual/native changes. Measure actual changes, canceled attacks and first-hit time before optimizing that executor. Do not claim every repeated same-item command causes a physical switch.

## 6. Phased implementation roadmap

Each phase below requires later authorization. Deployment always needs verified backups of the current namespaces, matching shared dependencies and a single active Mind Stone entry. Keep original B2.1/observer available throughout.

### Phase 0 — establish a small baseline (no combat development)

- **Goal/dependency:** choose one currently accessible manual-completable difficulty, confirm running build and capture current behavior; no prerequisite broad selector results.
- **Files:** later record results in existing `ROCKY_PLATEAU_TEST_RESULTS.md` or an ignored local run note. No script change required.
- **Expected:** one supervised B2.1 attempt identifies the first actual failure/encounters. Two more baseline attempts only if needed for a timing comparison.
- **Risks:** B2.1 switching still unconfirmed, manual rescues, missing Scout, misleading observer boundaries.
- **Test:** watch one full attempt; note completion/failure phase, last selected gear and total time. Cross-check one completion with an independent timer/video if possible. If the isolated validator must be used, first confirm its already installed overlay loads; do not expand it.
- **Acceptance:** build/difficulty/config and baseline outcome recorded; unobserved phases/Scout and assisted runs remain separate. No requirement to finish all 94 queries.

### Phase 1 — personalized shielded Bearer baseline (recommended first code milestone)

- **Goal:** make one real boss decision use confirmed owned equipment with accurate requested/actual diagnostics.
- **Proposed files:** `scripts/rocky/config/RockySettings.txt`, `equipment/RockyGear.txt`, `locations/RockyPlateau.txt`; relevant cases in `tests/test_rocky_candidate.py`. Touch `scripts/rocky/main.txt` only for a genuinely needed compact status field.
- **Dependencies:** Phase 0 target/build; one-shot checks only for the chosen Fire/physical weapon and upgraded shield. Reuse an existing validator case; confirm details once and keep results privately. Do not require unrelated element/ability checks.
- **Expected:** correct Bearer identity, stable chosen weapon + shield, explicit fallback on unavailable role; phase-gap ownership preserved. Other phase rules remain existing R1 candidates, not newly certified behavior.
- **Risks:** Compound alias/duplicate, Fire preference wrong, passive stun immunity, role selector matching unintended gear.
- **Test:** static role/owner/fallback tests, then one supervised R1 import and Bearer encounter after separate deployment approval. Observe requested/actual equipment at the meaningful transition, not every frame.
- **Acceptance:** no parser/import errors; intended two items visibly equipped; no Generic overwrite or repeated alternating roles; Bearer handled without manual gear changes on three observed attempts, or exact failure documented for Phase 2/3. Full-run outcome remains independent. Unverified fallback roles are not silently promoted.

### Phase 2 — coherent full-fight elemental and armor policy

- **Goal:** make all encountered phases use appropriate allowed damage and retain control through transformations.
- **Files:** existing Rocky handler/catalog/settings and candidate tests; result document.
- **Dependencies:** Phase 1 load/ownership; observe actual phase/element/adaptive representation. Verify an additional owned selector only when that phase/armor branch actually needs it.
- **Expected:** Elementalist changes element only from real state changes; Perfected avoids confirmed resisted elements; actual armor selects one-handed Hammer+shield; healing cannot defeat armor/immunity rules. Unknowns stay visible, with a known compatible fallback only when established.
- **Risks:** stale adaptive parsing, false phase tags, broad fallback mislabeled safe, weapon oscillation at armor boundaries, low-HP override.
- **Test:** synthetic missing-gear/unknown-format/armor/healing/transition cases; observe one representative element change and armor cycle on real runs. No five-element screenshot checklist unless failures specifically require it.
- **Acceptance:** each phase actually encountered is labeled correctly; selected damage remains eligible; required armor response occurs and restores correctly; three supervised full attempts have no selection/ownership defect. If survival fails, move directly to Phase 3; do not declare completion coverage.

### Phase 3 — resolve the actual survival bottleneck

- **Goal:** achieve repeatable unassisted completion; add only the defensive response the failed runs demonstrate is needed.
- **Files:** Rocky handler/settings; a small `scripts/rocky/combat/Defense.txt` only if a bounded sequence warrants its own file; candidate tests/acceptance notes.
- **Dependencies:** observed failing attack/phase/distance; confirm the chosen shield/sustain/Mind candidate immediately before using it. This phase can take priority over Phase 2 tuning if a lethal event already blocks progress.
- **Expected:** first compare a stable shield/sustain alternative when appropriate. If timing is necessary, implement one observed attack response, protect it from travel/attack overrides and restore without dashing back into danger. Distinguish repeated attacks sharing a state before counting/timing them.
- **Risks:** copied timings, Chill-altered schedules, no eligible Mind action, equipment removal during a hit, endless healing/defense loops. Shielding alone may not solve the attack.
- **Test:** calibrate one event without new Chill, then repeated occurrences at the same build/difficulty. Capture one short clip of the failure/response if needed; do not require clips for every run. Test interruption, cooldown unavailable, transformation and loop reset paths.
- **Acceptance:** intended damage/stun avoided or survivably reduced, offense restored, no new stalls/approach hazards; five consecutive owner-confirmed unassisted completions at the chosen difficulty is an initial smoke gate. It is not proof of an arbitrary reliability percentage or other difficulty support.

### Phase 4 — compare loadouts and one justified ability

- **Goal:** lower total completion time without giving back established reliability.
- **Files:** Rocky role preferences and tests; introduce a minimal `scripts/rocky/combat/AbilitySequence.txt` only when a chosen two-handed/active experiment requires it. Do not edit shared executor preemptively.
- **Dependencies:** stable Phase 3 baseline and a measured phase bottleneck.
- **Expected:** compare Stone/Fire/matched Sword or Wand where appropriate; compare one-handed Hammers; then Heavy basic attacks if still justified. Test Heavy Armor Fatigue separately only if armor gain makes it useful. A named wand/burst/defense item gets its own experiment later, not all at once.
- **Risks:** sheet DPS misinterpretation, shield loss, proc immunity, activation timing, recovery interruption, killing a useful debuff with cleanse.
- **Test:** one feature/loadout difference per comparison; equip and actual hand mode first, basic attacks next, active next. Include restoration and whole-phase/run time, not only a large hit.
- **Acceptance:** lower measured time per successful completion, no selection errors and no unexplained survival regression. Discard a phase-speed gain if its full-run cost/failures erase it. Broader shared reuse is a separate decision after a second real consumer exists.

### Phase 5 — travel and switching efficiency

- **Goal:** reduce noncombat time once fights are reliable.
- **Files:** Rocky settings/handler; optional `scripts/rocky/movement/Travel.txt` only for a real protected movement sequence. Shared Generic changes require separate cross-stage regression review.
- **Dependencies:** actual travel splits and first-hit behavior; existing Triskelion/Star baseline.
- **Expected:** preserve stable equipped Triskelion on clear travel. Investigate post-Scout travel only if the remaining approach is demonstrably safe. Compare Star off/on independently. Quarterstaff and Dashing are separate later trials, with threat/phase cancellation and no arbitrary waiting.
- **Risks:** wrong near-enemy threshold, lost shield, delayed first attack, jump/dash into a hazard or past an interaction, Star slot conflict. Do not assume Triskelion bonus persists after removal.
- **Test/acceptance:** actual movement metric plus whole-run time, no missed first attacks/mandatory interactions, no oscillation, no new deaths. Collection must yield if it slows completion; resource yield is never a metric.

### Phase 6 — expand the acceptance envelope

- **Goal:** extend reliable behavior to the next relevant difficulty and then repeated loops.
- **Files:** existing Rocky config/test/result docs; handler changes only for newly observed mechanics.
- **Dependencies:** one explicit difficulty passed; known first-entry behavior.
- **Expected:** reuse roles and architecture, introduce difficulty-specific rules only from evidence. Maintain a per-difficulty result matrix; a no-Scout test does not certify Scout.
- **Risks:** scaling, different attack cycles/protection, new elites/modifiers, changed loop timing or stale latches.
- **Test/acceptance:** low-overhead consecutive runs; distinguish fresh versus loop and every encountered phase/Scout. No unattended difficult test before its failure mode has been observed. Unsupported/unobserved cases remain explicit rather than extrapolated from a handler's existence.

## 7. Lightweight evaluation and acceptance

### Minimal run record

Keep one line per attempt, with a fixed configuration header:

```text
build; difficulty; script/config revision; first-entry/loop; trial;
completed/failed/assisted; total time + units; failure phase;
deaths; manual interventions; lowest/end HP if available;
gear/phase/ability warning; unexpected movement/switching; short note
```

Use current overlay at the failure or end; no continuous screenshots, arrow browsing or large inventory form. A single cropped evidence image is useful when an exact item is first confirmed. One short video/diagnostic trace is justified for a timing-dependent failure, not required for ordinary passes. Chat reports can be transcribed later without making the user edit JSON.

Retain optional diagnostics; a later compact final summary can hold completion, phase durations, minimum HP and **requested-role transition count** in bounded scalar state. That is a proposal, not implemented logging. Native item descriptions cannot prove every exact physical swap; requested changes and observed actual switches must be labeled separately. No per-frame disk logging or invented file-write API is needed.

HP loss is not automatically total damage taken: healing and armor absorption confound it. Start with minimum/end HP and deaths/large-hit observations. Add damage instrumentation only if it would change a decision; never sum negative HP deltas and call that complete incoming damage without stating the limitation.

### Baseline versus improvement

1. Fix build, difficulty, potion policy (currently off), gear identities, travel/Star flags, diagnostics, fresh/loop mode and timing definition. Avoid upgrades or inventory changes mid-comparison.
2. Record up to three baseline attempts and three candidate attempts as a first screen. If baseline cannot complete, compare failure phase/time/HP and prioritize reliable completion; do not claim a full-clear speed gain.
3. Once successful, compare median full-run time and spread, completion rate and failures. Use five interleaved pairs only when noise or a claimed small gain warrants stronger evidence. Short A/B blocks reduce repeated configuration edits; reverse order if fatigue/session drift is plausible.
4. Include deaths/retries and intervention count. Where sessions continue through failures, also compare total measured attempt/restart time per completed run. Never exclude deaths to make successful-run medians look faster; incomplete sessions remain incomplete rather than assigned a fabricated completion cost.
5. Verify one observer result independently before using its frame counts as primary speed evidence. Frames are game-time evidence, not automatically wall-clock seconds; compare each metric consistently. If observer boundaries disagree, use an independent timer/video until fixed.

### Acceptance gates

- **Correctness:** no native errors, actual requested roles agree with intended items, missing/unknown conditions visible, one equipment owner, correct transition/reset behavior, no optional harvesting or collection detours.
- **Functionality:** an explicit owner-confirmed unassisted completion establishes that trial only. Five consecutive passes at the same difficulty/config are a provisional reliability gate; keep all earlier failures. Extend to ten routine passes before describing it as stable locally; this still does not prove 99% reliability.
- **Speed:** no absolute percentage target before a baseline exists. Prefer a time improvement larger than observed noise with no new failures in the small comparison. A survival tradeoff requires explicit review; a faster death is not an optimization.
- **Compatibility:** shared-source regression checks before any shared edit; other stages continue through unchanged Generic; original B2.1 remains an independent rollback entry point.
- **Coverage:** record Scout/phases actually seen, build, difficulty and first-entry/loop separately. Never infer support for every difficulty from a successful low-difficulty run.

## 8. Risks, unresolved questions and required observations

| Question | Why it matters / smallest useful observation |
|---|---|
| Which difficulty/build is the first target? | Choose one the owner can already complete manually. No invented default star level; Scout/high-difficulty coverage is separate |
| Does current B2.1 actually switch and finish? | One supervised baseline distinguishes unresolved deployment/selector problems from boss-strategy problems |
| Does the installed isolated validator load? | Installation/hash checks passed; loading still needs owner confirmation if used. Test only a required item, not the whole catalog |
| Which shield/physical duplicate is actually selected? | One details inspection per role; raw saved level or +21 alone is insufficient for some pairs |
| Are phase filters and adaptive UIDs correct on this build? | One observed transition/adaptive event with its public diagnostic text; no save upload |
| Which boss event causes deaths/stalls? | Failure phase plus a short observation/clip; choose armor/sustain/avoidance work from this, not from a public timer |
| How do debuffs alter behavior? | Establish no-new-Chill baseline; apply a single effect only if useful. No assumed stun/unmake/HP-percentage effect against bosses |
| Does listed DPS include crit/element/attack-speed effects? | Compare actual phase time for finalists; no guessed effective-DPS equation |
| Are first-entry and loop boundaries correct? | One manual reset and one loop observation after stable completion; no bulk lifecycle campaign first |
| Is mandatory traversal blocked without a tool? | Report the specific obstacle/phase. Preserve a narrow progression action; do not restore generic shovel harvesting |

Additional data concerns remain: 0021/0023 lack visible damage/range/critical-chance fields despite CSV entries; Infernal's splash claim is not visible in the reviewed crop; several descriptions are clipped. Keep those candidates deferred unless an actual decision needs them. Never silently repair legacy columns, promote model visual review to human verification, or map saved IDs/effect codes directly into selectors.

## 9. Recommended first implementation milestone and review boundary

**Authorize Phase 1 only after the small Phase 0 baseline: personalized shielded Bearer behavior in the existing R1 candidate.** Scope: two needed gear identities, Rocky-only role overrides, one-handed request ownership and a compact strategy diagnostic. Confirm a physical or armor fallback only if the actual run invokes it. Keep current shared automation untouched, abilities/potions off, and do not add a new selector-validation subsystem.

Success is correct equipped gear and reliable Bearer behavior in a real run, with the full-run result honestly recorded. The next milestone is chosen from the first observed limitation: phase matching/armor, a lethal attack, or—only after completion is stable—time optimization. Heavy Hammer and Fire Sword remain candidates to compare, not requirements to force into every phase.

This plan does not authorize deploying R1, editing Stonescript, changing CSVs or starting a test run. Implementation and deployment await owner review.

## Sources and provenance

- Local source files and documents inspected: shared/R1 modules, original observer; `STONESCRIPT_KNOWLEDGE.md`, `ROADMAP.md`, `ROCKY_PLATEAU_RESEARCH.md`, candidate/test-result docs, `GEAR_REFERENCE_REVIEW.md`, `ROCKY_EQUIPMENT_CROSSWALK.md`, selector deployment guide; both new CSVs and all three legacy gear catalogs. Private normalized inventory/crosswalk were read locally; no raw save or active save was needed.
- [Official Stonescript manual](https://stonestoryrpg.com/stonescript/manual.html): native execution, state, filters, equipment, ability and timing APIs. It does not specify a complete current Rocky attack schedule.
- [Eunomiac annotated Rocky, pinned source](https://github.com/Eunomiac/stone-story/blob/e9921f9b141d45ab650797e03915e737a6ba3fc0/Scripts-Annotated/SimpleRockyPlateau-Annotated.txt): encounter roster/Scout threshold comments, phase/counter equipment and two-hand ownership ideas. Historical community code, not a tested local strategy.
- [asHOH Rocky, pinned source](https://github.com/asHOH/Stonescript-for-Stone-Story-RPG/blob/856875b08c7e27247efe4aeb2bbc697d1595091a/00_rocky_plateau.txt): distinct phase/Scout behavior, protection/adaptive/armor observations and defense scheduling. Its numerical schedules are deliberately not adopted.
- [Hukutus state reference, pinned source](https://github.com/Hukutus/stone-script-reference/blob/b905f5721ea635d493fbb21ae21a4dbeafe483fe/README.md): attack/transform labels and explicit caveats about distance/debuff timing. Supplemental observation, not authoritative timing.
- Additional inspected public techniques and licenses remain indexed in `ROCKY_PLATEAU_RESEARCH.md`; no upstream code is copied by this planning document.
