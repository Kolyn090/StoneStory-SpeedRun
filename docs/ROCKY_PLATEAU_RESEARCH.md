# Rocky Plateau source research and integration plan

Implementation follow-up (2026-10-29): a separate, uninstalled **Rocky R1** candidate now exists under `scripts/rocky/`. It implements encounter/phase ownership, transition-gap holding, strict cached elemental selection, armor/adaptive handling and diagnostics. Shared B2.1-TS is unchanged. No community numeric timings, timed dodges, AAC or movement abilities are integrated. See [candidate/installation limits](ROCKY_PLATEAU_CANDIDATE.md) and [pending game-test records](ROCKY_PLATEAU_TEST_RESULTS.md). Preparation left all work, including this previously untracked report, unstaged and uncommitted. The owner subsequently authorized local commits for review; deployment remains unauthorized. The original research-only scope below is historical.

Reviewed 2026-10-29. Target: game/manual **4.35.2**. Scope: research and design only; no gameplay, deployment, importer, selector-validator or private-inventory changes. Current baseline is B2.1-TS, repository revision `19332d7`; its installed copies are preserved. Loading of the original observer is user-confirmed, but recent automation, selectors, movement, phase handling and timing correctness do not inherit that confirmation.

Recommendation: first validate exact gear and observe Rocky phase transitions, then add a small phase-aware equipment policy, one independently calibrated defensive response, and a separate quarterstaff experiment. Keep AAC, Moondial cycling, potion persistence and transition exploits out of the first integration. No repository's popularity, complexity or author demonstration establishes that it is faster with this inventory/build.

## Evidence and reproducible source index

- **Official:** documented syntax/API or explicit release-note behavior; not execution of our scripts.
- **Community source:** inspected implementation/comment at the pinned commit; numeric timing and item effects remain hypotheses for this installation.
- **Local inventory:** observed offline records, not confirmed runtime selectors or displayed stars.
- **Proposal:** our design/acceptance gate. No recommendation below is a successful game test.

Default branches were resolved through GitHub to immutable commits before file review. Sources were read through the GitHub connector; no upstream executable/compiler was run or imported. Both readable and distributed variants were inspected where available.

| Key | Repository / pinned revision | Actual source inspected |
|---|---|---|
| A | alexbarker234/stonescript, `bd9ed98f5331e72bd2fbeb0b80546615316e4825` (2024-11-06) | [Readable Main](https://github.com/alexbarker234/stonescript/blob/bd9ed98f5331e72bd2fbeb0b80546615316e4825/stonescript/Main.txt), [distributed Cobblestone](https://github.com/alexbarker234/stonescript/blob/bd9ed98f5331e72bd2fbeb0b80546615316e4825/Cobblestone.txt) |
| E | Eunomiac/stone-story, `e9921f9b141d45ab650797e03915e737a6ba3fc0` (2024-04-22) | [Annotated Rocky](https://github.com/Eunomiac/stone-story/blob/e9921f9b141d45ab650797e03915e737a6ba3fc0/Scripts-Annotated/SimpleRockyPlateau-Annotated.txt), [PC Main](https://github.com/Eunomiac/stone-story/blob/e9921f9b141d45ab650797e03915e737a6ba3fc0/Scripts-PC/Main.txt), [Utilities](https://github.com/Eunomiac/stone-story/blob/e9921f9b141d45ab650797e03915e737a6ba3fc0/Scripts-PC/Utilities.txt), [annotated AAC](https://github.com/Eunomiac/stone-story/blob/e9921f9b141d45ab650797e03915e737a6ba3fc0/Scripts-Annotated/AttackAnimationCancelling-Annotated.txt) |
| M | TheMatjaz/StoneScript, `d880a8b26aafdb5ecbef722100231dc67ae4cad0` (2023-10-17) | [Rocky](https://github.com/TheMatjaz/StoneScript/blob/d880a8b26aafdb5ecbef722100231dc67ae4cad0/00_rocky_plateau.txt), [loadout helpers](https://github.com/TheMatjaz/StoneScript/blob/d880a8b26aafdb5ecbef722100231dc67ae4cad0/loadouts.txt) |
| S | livercat/scribble, `53ad8f0712d8373f999f97a22fcde0ff2f6b049f` (2023-11-19) | [Readable development source](https://github.com/livercat/scribble/blob/53ad8f0712d8373f999f97a22fcde0ff2f6b049f/scribble.dev.txt), [distributed source](https://github.com/livercat/scribble/blob/53ad8f0712d8373f999f97a22fcde0ff2f6b049f/scribble.txt) |
| H | asHOH/Stonescript-for-Stone-Story-RPG, `856875b08c7e27247efe4aeb2bbc697d1595091a` (2025-01-17) | [Rocky](https://github.com/asHOH/Stonescript-for-Stone-Story-RPG/blob/856875b08c7e27247efe4aeb2bbc697d1595091a/00_rocky_plateau.txt), [equipment](https://github.com/asHOH/Stonescript-for-Stone-Story-RPG/blob/856875b08c7e27247efe4aeb2bbc697d1595091a/eq.txt), [utilities](https://github.com/asHOH/Stonescript-for-Stone-Story-RPG/blob/856875b08c7e27247efe4aeb2bbc697d1595091a/util.txt), [state helpers](https://github.com/asHOH/Stonescript-for-Stone-Story-RPG/blob/856875b08c7e27247efe4aeb2bbc697d1595091a/s.txt), [frame driver](https://github.com/asHOH/Stonescript-for-Stone-Story-RPG/blob/856875b08c7e27247efe4aeb2bbc697d1595091a/all.txt) |
| R | Hukutus/stone-script-reference, `b905f5721ea635d493fbb21ae21a4dbeafe483fe` | [Community state tables](https://github.com/Hukutus/stone-script-reference/blob/b905f5721ea635d493fbb21ae21a4dbeafe483fe/README.md#rocky-plateau); supplemental observations, not another combat implementation or a current game specification |

Primary language references: [manual 4.35.2](https://stonestoryrpg.com/stonescript/manual.html), [official tutorial](https://stonestoryrpg.com/stonescript/), [official release notes](https://stonestoryrpg.com/releasenotes/). Phase tags and state/time reads are supported; the manual does not specify a complete current Rocky state-duration chart. R explicitly warns that distance and debuffs can affect its measurements.

## What each implementation actually does

| Implementation | Useful techniques | Advantages | Dependencies / limits / project fit |
|---|---|---|---|
| A: Cobblestone | Triskelion + compound shield travel; nearby Star; quarterstaff multi-frame hold; Scout chill/healing; all three Dysangelos identities; adaptive-element avoidance; armor hammers; Mind Stone avoidance; deferred equipment and ability execution | Readable Rocky functions and explicit transitions; boss encounter latch survives temporary target loss | Lucky-potion setup/loop policy, paired elemental swords, Moondial and ability-specific timings. Star can replace Triskelion on the setup run. Reuse ownership/phase concepts, not the whole policy or unconditional potion use |
| E: annotated Rocky / PC framework | First-accepted or priority equipment requests; explicit elemental match and adaptive exclusion; debuff selection, armor weapon, dash approach, Mind Stone dodge; optional quarterstaff in PC framework; AAC | Best explanation of request ownership and meaningful hand/two-hand distinctions | Annotated version harvests and scans inventory in frame logic; exact dodge constants, configured gear and potion assumptions. Some annotated behavior differs from PC utilities. No complete bespoke Scout state machine; no proof of universal timings |
| M: compact per-location scripts | Named loadout abstraction, full-HP Triskelion travel, Star attraction, simple phase identity/armor handling | Small, easy-to-inspect baseline and separation of location from loadout helpers | Rocky defaults to shovel; phase-2 element logic is explicitly TODO. Phase-3 potion threshold is tied to a stated 5-star attack. An invoked `star_ouroboros` helper is absent from the inspected loadouts file. Not a ready-to-run complete strategy |
| S: Scribble | Dual-stone pickup loadout; quarterstaff/dash approach; state/attack-cycle logic, Chill-adjusted schedules, adaptive-defense exclusion, boss/action locks; weapon-aware AAC exclusions | Strong model for protected actions and preventing immediate dash-back after a dodge; includes interruption-sensitive ability logic | Large configuration/item classification/effect parser. Pickup branch returns before boss handling. Has optional harvesting and quest-specific retreat behavior. Old ability aliases and empirical Chill timing require revalidation. Reuse bounded ownership and exclusion concepts only |
| H: asHOH | Dedicated Rocky module; phase/Scout defense times; dynamic elemental policy, armor/debuff maintenance; dual stones; quarterstaff/dash utilities; attack counter and post-dodge timer; explicit no-harvest Rocky setting | Clearest modular Rocky specialization; diagnostics expose stun failures; separate generic helpers | Author states tested v4.8.1, not 4.35.2. Defaults enable Lucky-potion persistence/mask setup; most combat uses two weapons, not our shield baseline. Hard-coded high-grade selector tables, immediate equip helpers and end-frame Moondial can override earlier choices |

This is source-completeness evidence, not an empirical ranking. No comparable run dataset with our gear, 4.35.2, difficulty, potion permissions and failure accounting was established. An author video link in E is a demonstration claim; it was not treated as our acceptance test.

### Concrete source pitfalls to avoid inheriting

- **A:** [Main 451-605](https://github.com/alexbarker234/stonescript/blob/bd9ed98f5331e72bd2fbeb0b80546615316e4825/stonescript/Main.txt#L451) itself labels the late-loop potion threshold arbitrary and expresses uncertainty about one transition state. Its item cooldown wrapper passes strings directly; `hammer` differs from the manual's `heavy_hammer`. Its dash helper can return success for being in a distance window even when no dash item was requested. Treat success as an observed/accepted action, not just a distance condition.
- **E:** [annotated Rocky 22-33](https://github.com/Eunomiac/stone-story/blob/e9921f9b141d45ab650797e03915e737a6ba3fc0/Scripts-Annotated/SimpleRockyPlateau-Annotated.txt#L22) assigns `dashFreeze = false` unconditionally before frame decisions. Under documented per-frame execution, this prevents the later intended 60-frame freeze from persisting as written. Its configuration also calls a `big ... sword` a default one-handed weapon; validate actual hand compatibility instead of trusting the variable label. The PC framework has different lock handling; do not conflate the examples.
- **M:** [Rocky 14-15](https://github.com/TheMatjaz/StoneScript/blob/d880a8b26aafdb5ecbef722100231dc67ae4cad0/00_rocky_plateau.txt#L14) calls `loadouts.star_ouroboros()`, but the pinned `loadouts.txt` inspected contains only `healwalk`. Keep this unresolved helper dependency visible rather than silently supplying invented behavior.
- **S:** [development progress 256-291](https://github.com/livercat/scribble/blob/53ad8f0712d8373f999f97a22fcde0ff2f6b049f/scribble.dev.txt#L256) prioritizes nearby pickups before boss decisions. That ordering violates our combat-first rule. The Scout quest branch may leave the location deliberately; it is not a completion strategy. Its Chill-delay multiplier and adaptive-buff string parser are project assumptions, not native contracts.
- **H:** [state helper 110-124](https://github.com/asHOH/Stonescript-for-Stone-Story-RPG/blob/856875b08c7e27247efe4aeb2bbc697d1595091a/s.txt#L110) identifies a boundary using total time 1, whereas the official `loc.begin`/brewing examples use time 0. Its dash check passes `dashing` to a direct cooldown alias, while the current manual lists `dash`; equipment selectors and cooldown IDs are separate namespaces. Its late `end_frame`/Moondial writes must not overwrite a protected dodge or ability.

## Technique comparison and selective recommendations

### Gaps relative to the current project

- `Dispatcher.txt` labels Rocky, but `main.txt` still always calls the shared Generic handler. A named route is not a Rocky strategy or a passed completion test.
- Generic forces ordinary wands for bosses; its hammer-for-armor branch is limited to a sword decision, so it does not supply a deliberate phase-3 armor counter. Existing element matching does not decode Perfected adaptive defense or distinguish three phases.
- B2.1-TS already has Triskelion/Star ownership and broad threat readiness. Preserve and measure these rather than reimplementing them from another script. Its boss-seen flag blocks travel stones after a boss is observed but does not implement phase-transition defense or a complete encounter state machine.
- The catalog executes one-handed pairs immediately. It has no two-handed ability owner, activation/hold/restoration sequence or confirmed intended-instance mapping. Basic cooldown gates alone cannot fill that gap.
- Existing observer timing/capture/loop correctness is still unaccepted. Phase traces and independent recorded timings are prerequisites for claiming a Rocky speed improvement.

### Travel, pickups and approach

The official tutorial demonstrates equipped `triskelion` movement and equip-only Star attraction; it does not establish a universal attraction radius or bonus carryover after removal. A uses pickup `<10`, E `<13`, M `<6` in Rocky / `<10` in its helper, and S `<9`. These are script thresholds, not interchangeable measurements of maximum range. H's state helper uses `<10` and can also request Star after enemies disappear based on position.

Keep our stable Triskelion-L / optional-Star-R arrangement. Do not copy S's pickup-first return or A's setup-run replacement of Triskelion. Compare Star off/on at fixed movement policy; native pickup pathing and slot-change costs need observation. Keep mandatory progression interactions outside optional collection logic and leave shovel farming disabled.

A [quarterstaff helper](https://github.com/alexbarker234/stonescript/blob/bd9ed98f5331e72bd2fbeb0b80546615316e4825/stonescript/Main.txt#L343) avoids use at distance <=16 and holds equipment across several frames. E's PC Main schedules a quarterstaff activation with priority and AI/activation guards. S uses action locks and an approach policy. H equips the two-handed quarterstaff and activates R through a separate helper. Their hold lengths, movement distances and target cutoffs are empirical, not proof of an optimal universal hop.

**Proposal:** quarterstaff is the first active travel ability worth an isolated experiment after exact-item validation. It needs one owner, equip/eligible-activation/confirmed-effect/restoration stages, a bounded timeout and immediate threat/progression cancellation. It temporarily replaces both hand items; a speed gain must include lost Triskelion time and first-attack readiness. Test Dashing Shield separately: source windows near 11-16 are approach policies, not automatic safety against ranged enemies. Do not dash straight back into an avoided attack. No fixed waiting period is justified unless a measured hazard/sequence demands it.

Our B2.1-TS already prepares combat for any targeted enemy; this is deliberately conservative. A Rocky profile may eventually permit travel during a verified safe far approach, but only with measured ranged/boss threat margins and spatial hysteresis. Do not weaken the shared guard for every location just because a public Rocky script uses a smaller distance.

### Scout (community source ID `acronian_scout`)

A uses dash approach, Chill swords while applicable, healing swords when injured, then fire swords/Moondial. E recognizes the Scout in its shared Rocky combat path; S normally delegates to generic melee-miniboss logic, while its special quest branch is not reusable for completion. H has a separate Scout routine: best physical sword, optional debuff weapon, and a defense check at state 32/time 54.

The claim that the Scout appears at 11+ stars is recorded in E's comments; verify the actual chosen difficulty/encounter rather than claiming universal coverage. The current inventory does not prove availability of A's two distinct identical-purpose ice/fire swords.

**Proposal:** identify and measure Scout separately, use a confirmed single weapon + shield baseline, then test one Chill or armor/debuff change at a time. Any timing check such as H's 54 belongs in a build/difficulty/modifier-specific calibration record. If the chosen test difficulty has no Scout, mark its case NOT APPLICABLE/NOT RUN, not passed.

### All three Dysangelos phases

| Phase | Source behavior | First integration candidate | Unverified dependencies |
|---|---|---|---|
| 1: Bearer | A favors Chill, situational lifesteal, then fire damage; E uses elemental matching/debuffs and a Mind dodge at state 33; M sword/shield; S timed blocking with Chill delay; H fire weapon/debuffs and defense at state 32/time 64 | Identify phase and transition explicitly; retain shield, test confirmed fire/elemental single weapon against current generic wand baseline | Fire effectiveness is community guidance to confirm with current target properties; 28/22/64/33 schedules are not universal |
| 2: Elementalist | A/E/H choose weapons from the current element; S mixes vulnerability matching, debuffs and timed defense; M leaves matching TODO | Supported elemental candidates + current immunity/protection checks; make one stable choice and change on actual element/protection transition | Element/buff representation, effect eligibility, per-element weapon quality; do not assume debuffs work during protection/vigor behavior |
| 3: Perfected | A/S/E/H account for adaptive elemental defense; A/H add armor hammers and healing/debuff decisions; Mind avoidance for the major ray/stun sequence; S/H count attack cycles | Exclude a confirmed resisted element, use confirmed armor counter while armor exists, and retain defensive fallback; calibrate one major avoidance response independently | Adaptive-buff decoding, repeated attack variants, Chill/stun timing, distance, actual shield/HP effects, Mind readiness and safe reapproach |

Phase-specific identity should use tested `phase1`/`phase2`/`phase3` filters and observed public foe types, not numeric-state ranges alone. During transformations there may temporarily be no target. A explicitly latches the boss encounter across this gap; our future handler should do so too, suppressing ordinary travel and pickup logic until phase resolution or an actual run boundary/completion. Generic `!foe` is not proof that a boss encounter ended.

Do not force each difficulty to have all three phases. Record which phases actually occur. No specialized counter for an unobserved variant should be enabled automatically.

### Avoidance, stuns and debuffs: why calibration comes before timers

The same major phase-3 event is treated differently: A uses state 115 after time 60; E's PC utility checks at/after 60; S uses a 70-oriented evasion window with a post-dodge lock; H starts a timer at entry to state 115 and sets it to 79. These numbers use different timing origins and modifiers. R labels state 115 as a post-damage energy-ball state, emphasizing the need to correlate visible projectile arrival with the state trace rather than trusting a comment that calls it pre-hit.

State 32 also covers multiple attacks. S tracks transitions through 32/33/2 to distinguish a cyclic stun/shield sequence and adjusts a timing model for Chill. H counts attacks and distinguishes defense from a Mind dodge. E's simple two-second no-dash intention is useful design guidance but its annotated reset issue must be corrected in an original implementation. Never combine all these timers into a single guessed threshold.

First observe without new debuffs, then repeat with one controlled Chill/stun effect. Record state/time, distance, HP/armor, debuff count/duration, actual impact, dodge effect and reapproach. Count a successful dodge only if the intended damage/stun is avoided and the next attack is not delayed enough to erase the benefit. A general `immune_to_stun` filter is documented; every additional effect UID/immunity token from a repository needs a separate check.

Prefer documented buff/debuff count/time functions for verified UIDs over repeatedly splitting display strings. Where adaptive-defense parsing is necessary, capture its current representation and fail safely to a known weapon/defense choice when decoding is unknown. No private save ability code is automatically a runtime modifier or effect UID.

### AAC and Moondial: separate, late experiments

A, E and H use equipped-item state 3 with a temporary weak-item swap; S has weapon-specific AAC logic and preserves hammer/Bardiche locks. E's annotated AAC explicitly assumes a one-handed setup always fills both slots when using empty-L to detect two-handed gear. Our optional travel/ability states make that assumption unsafe; use explicit validated hand metadata instead.

The manual documents numeric item state/time reads, not a guarantee that a state-3 swap preserves every projectile/hit or improves speed. S's `ai.idle` check likewise is not proof a hit landed. Test cancellation on one exact weapon/hand first, then projectiles and two-handed abilities separately. Confirm damage and completion, not just faster animation. Dummy selectors must resolve known owned items; no auto-forging or generic low-quality fallback is assumed.

Moondial cycling is a different multi-frame equipment technique. A/H rotate swords/slots and Moondial on periodic frames; this deliberately introduces repeated switching and generally needs two validated appropriate weapons. Keep both AAC and Moondial off during phase/defense/movement validation. Do not treat their source-level existence as a reason to abandon our stable-slot default.

## 4.35.2 compatibility audit

| Evidence | Consequence |
|---|---|
| Manual Appendix A lists `heavy_hammer`, `dash`, `talisman_fire`, `talisman_aether` | Audit old `hammer`, `heavy hammer`, `dashing`, `fire_talisman` aliases passed directly to native functions; project aliases may be retained only with an explicit correct translation |
| `GetCooldown` can return -1 for invalid or unused abilities | `<=0` alone is not eligibility. After a validated owned item is equipped, check the documented ability-specific `CanActivate` where applicable |
| Release notes add ranged classification to Dysangelos in v4.17.1 | Older range/type policies need retesting, including first-attack preparation |
| v4.33.0 changes dash/bash cooldown-bonus behavior; v4.21.1 and v4.23.1 include relevant enchantment/quarterstaff fixes | Read current cooldown/state data; do not port old fixed cooldowns or animation budgets |
| Triskelion fixes/non-stacking and quarterstaff/stat changes appear in official history | No duplicate-stone stacking, old timing arithmetic or assumed displayed-star conversion |

References: [manual](https://stonestoryrpg.com/stonescript/manual.html), [release notes](https://stonestoryrpg.com/releasenotes/). H's [README](https://github.com/asHOH/Stonescript-for-Stone-Story-RPG/blob/856875b08c7e27247efe4aeb2bbc697d1595091a/README.md) claims v4.8.1 operation. That is author-reported historical testing, not a 4.35.2 guarantee. Capture the actual running build as test metadata; the offline save/manual version alone does not establish the running executable's behavior.

Mind Stone/backflip, shield approach and quarterstaff jump are not interchangeable activation models. Sources often use equip-only Mind/dash behavior but equip-plus-activate for quarterstaff. Record the actual effect/cooldown transition in the game before generalizing an ability executor. Unknown eligibility must not cause endless equip/retry loops.

## Personal equipment feasibility, without promoting selectors

The private normalized snapshot was read locally, without modifying it or uploading contents. All statements below are sanitized record-family observations; source pointers, signatures, custom names and account data remain private. See [selector validation status](EQUIPMENT_SELECTOR_VALIDATION.md) and [inventory import semantics](PRIVATE_INVENTORY_IMPORT.md).

| Relevant family observed | Local records | What this enables investigating / what is not established |
|---|---|---|
| Quarterstaff | 2; only one has primary/secondary enchantment structures | Strong candidate for a controlled movement experiment; duplicate selection and actual cooldown/displayed level unresolved |
| Dashing shield | 1 | Approach experiment possible after selector/effect check; does not prove readiness/range or immunity to interruption |
| Triskelion / Star / Mind Stone | 1 each | Travel, attraction, dodge candidates; runtime selector success and exact current effects still need owner tests |
| Elemental socketed short-sword family | One record per each of five explicit elements, plus one with no saved element | Single elemental-weapon comparison is plausible; this is not evidence of two distinct matching chill/DPS swords per element |
| Elemental socketed hammer family | One per each of five elements | Armor-counter candidates; saved abilities/enchantments do not establish which native modifier/selector to use |
| Heavy hammer, Bardiche, Cultist Mask, Skeleton Arm, special blade family | 1 each | Later burst/debuff candidates; exact display aliases, hand mode, activation and intended variant must be confirmed |
| Compound shield | 2, with different raw upgrade values; only one has the enchantment structures | Broad `compound shield` may not identify the desired defensive variant; prioritize exact confirmation |

Do not map raw upgrade values to stars or assume raw `ra`/`sra` fields prove displayed +21/+21 or a particular cooldown/chance. Raw ability structures are preserved, not decoded into verified effect tokens. The existing 94 private selector hypotheses include ambiguity and unvalidated aliases; do not integrate them here. A zero count may mean alias mismatch, and a count of one is not exact-item confirmation.

Gear CSVs describe useful quarterstaff, shield and effect candidates, but `data/gears/note.md` assumes +21/21; cooldown/duration units, sentinel values and variant names remain unresolved. Treat CSV DPS as a hypothesis for testing, not a ranking of owned instances. No additional resources or crafting are needed or proposed.

## Proposed minimal Rocky specialization

This is a plan, not implemented files or native APIs:

```text
locations/RockyPlateau.txt  observe/dispatch Scout, phases, transformations
combat/Generic.txt         unchanged fallback for unhandled ordinary cases
equipment/Catalog.txt     confirmed cached selectors + one-/two-hand execution
combat/AbilitySequence.txt only when the first multi-frame ability needs ownership
metrics/RunMetrics.txt     retained; phase splits added separately after validation
```

1. **Start observation-only.** The current dispatcher recognizes `rocky` but main always calls Generic.Tick. A proposed Rocky handler initially reads phase/state transitions, reports a label, and returns unhandled without issuing equipment. Generic continues exactly once; observer metrics stay outside dispatch.
2. **Explicit handled contract.** When a validated Rocky action later owns a frame, it clears current requests, uses the shared safety/AI/core-gear gate and calls the catalog executor once, then returns handled. Do not issue Rocky commands and then call Generic.Tick: Generic clears requests and equips immediately, overwriting them. Unhandled means no commands were issued.
3. **Small persistent context.** Track encounter/phase, previous state, observed attack-cycle index only if required, action owner/deadline and post-dodge suppression. Latch boss transitions across missing-foe frames. Reset on fresh entry/loop/attachment; cancel experimental sequences on unsupported phase/target change. While an encounter remains latched, an unknown/missing phase must retain handled defensive/manual ownership rather than fall through to Generic's clear-travel branch. Do not infer a stable foe instance from a type ID alone.
4. **Shared execution, not a framework.** Reuse current one-handed Apply/ApplyPair. A later two-handed/ability executor must mark hand mode, clear incompatible offhand requests, equip the validated item, gate activation, and retain only the tested sequence ownership. First versus loop policy must be explicit; keep potion use opt-in.
5. **Priority.** Required safety/avoidance and protected ability work, mandatory progression, phase combat, verified approach movement, clear Triskelion travel, optional bounded Star collection. One owner per frame. Movement/pickup cannot cancel a defense or turn a transformation gap into travel.
6. **Native checks only.** Use documented state, HP/armor, count/time, item availability and activation APIs. Request handles, `handled`, phase labels and sequence fields above are proposed project helpers/fields, not new native features. Cache static inventory checks; parse only relevant changing effects. No runtime CSV importer, general event bus or unbounded damage history.

## Priorities, independent tests and measurable gates

All gates below are proposals requiring actual game results. They do not authorize implementation in this documentation-only pass.

| Order | Small feature / reason | Test individually before combination | Initial acceptance criterion |
|---|---|---|---|
| P0 | Exact gear validation plus observation-only Rocky phase/transition labels | Confirm intended sword/shield/quarterstaff/Mind candidates; capture unmodified baseline and no-debuff boss state/distance trace | No gameplay change, no new errors, correct observed Scout/phase labels across fresh entry and loops; unknown cases explicitly flagged; exact-item evidence private |
| P1 | Phase-aware single-weapon + shield, including adaptive-defense exclusion and an armor counter | One element/armor rule at a time, AAC/dash/quarterstaff/new debuffs off | Requested/actual item agrees; resistance/armor rule responds only to observed changes; no fallthrough override; repeated unassisted completion at chosen difficulty; lower phase time without worse full-run reliability |
| P2 | One major phase-3 avoidance/protected reapproach response, if it is a current failure/time bottleneck | Calibrate without Chill, then with one controlled modifier; separately test Mind equip behavior and cooldown | Observed damage/stun avoided over multiple occurrences; no immediate dash-back into hazard; combat restored; unknown state/cooldown has bounded safe fallback |
| P3 | Quarterstaff clear-travel jump | Exact duplicate selector, activation, minimal useful hold, interruption and restoration; Star/AAC off | Actual movement effect observed; no repeated activation per cooldown; no first-attack delay or progression overshoot; lower travel split and lower complete-run time including equipment costs |
| P4 | Scout-specific Chill/defense and carefully timed debuff refresh | Only at a difficulty where Scout occurs; one effect at a time; then phase-specific tests | Distinct Scout completion evidence; debuffs demonstrably apply; no unnecessary refresh/switch loop; measured encounter/run improvement |
| Later | Dash shield, burst weapons, AAC, Moondial | Each separately before combining with movement/avoidance | Damage preserved, bounded ownership, no interrupted ability; paired total-time gain with acceptable failures; exact weapon-specific evidence |

If a boss currently prevents completion, P2 safety precedes pure P3 movement work. If baseline completes reliably and travel dominates, quarterstaff can move ahead of optional debuff tuning after P0/P1 contracts are stable. No predicted percentage gain is asserted.

**Measurement proposal:** record build/platform, difficulty, revision, exact equipped instances, feature flags, potion policy and manual/loop boundary. Start with ten interleaved baseline/candidate pairs per feature where feasible; keep every death, retry and assisted outcome. Compare median full-run frames plus spread/tail, travel/Scout/phase splits, first-attack delay and intervention count. Ten successes are a smoke gate, not statistical proof of a long-run reliability target. Do not accept a faster phase if total completion time or failures worsen without an explicit owner-approved tradeoff. Observer reset/completion/loop correctness must be checked before using its metrics as acceptance evidence; use an independent recorded timer/video meanwhile. Resource yield is never a success metric.

Combine in order only after individual passes: phase detection + confirmed equipment; calibrated defense; then quarterstaff; then Star with Triskelion; finally optional offensive sequences. Recheck all transition/abort paths after each combination. Keep current B2.1-TS and all deployment backups available for rollback.

## Licensing and attribution before code reuse

| Repository | Inspected license / action |
|---|---|
| A | No root LICENSE file found; [README](https://github.com/alexbarker234/stonescript/blob/bd9ed98f5331e72bd2fbeb0b80546615316e4825/README.md) grants informal use/modification permission. Do not invent an MIT/BSD grant or assume redistribution terms. Prefer independently written ideas with attribution; clarify terms before substantial verbatim reuse |
| E | [Unlicense](https://github.com/Eunomiac/stone-story/blob/e9921f9b141d45ab650797e03915e737a6ba3fc0/LICENSE). Attribute the source/commit for traceability even when implementing the idea independently |
| M | [BSD 3-Clause](https://github.com/TheMatjaz/StoneScript/blob/d880a8b26aafdb5ecbef722100231dc67ae4cad0/LICENSE.md), also stated in script headers. Retain applicable copyright, conditions/disclaimer and non-endorsement requirement when reusing code |
| S | [MIT](https://github.com/livercat/scribble/blob/53ad8f0712d8373f999f97a22fcde0ff2f6b049f/LICENSE), Dmitriy Safonov. Retain copyright and permission notice for copied/substantial portions |
| H | [LICENSE.md](https://github.com/asHOH/Stonescript-for-Stone-Story-RPG/blob/856875b08c7e27247efe4aeb2bbc697d1595091a/LICENSE.md) has an inconsistent BSD heading but MIT body, copyright asHOH 2024. README also acknowledges third-party code permissions. Preserve relevant notices and clarify file provenance/heading conflict before substantial reuse; do not label everything unconditionally BSD or MIT based only on GitHub metadata |
| R | No license file found in the inspected root. Cite measurements as community reference, not permission to republish its complete tables |

This report paraphrases techniques and links sources; it does not vendor code or copy an implementation into automation. Future adaptations should record source path/commit, exact adapted behavior, applicable notices, deliberate departures and local test evidence. Do not copy upstream license files into our project merely to imply permission for unrelated code.

## Current outcome and next decision

Research completed for all five requested repositories plus the supplemental state reference. The report was preserved through R1 preparation; subsequent owner authorization covers focused local commits of the candidate, tests and supporting documentation. No external script, game deployment, save, inventory output, selector-validator or importer was modified. No in-game test or Rocky completion is claimed.

Documentation validation: 28 pinned GitHub file/line references were checked against the fetched source revisions; local documentation links and Markdown fences resolve. The existing basic static checker passes. All 107 protected original file hashes (scripts, tooling/tests, gear/private data, prior backups and both observer/basic deployments) remain unchanged. These checks validate preservation and research references, not native parser execution or gameplay techniques.

Next recommended implementation milestone is **P0 observation-only Rocky dispatch plus validation of the exact sword/shield/quarterstaff/Mind candidates**, followed by P1 phase-aware equipment. Owner inputs before gameplay implementation: initial Rocky difficulty/observed phase coverage and Scout availability; actual running build; acceptable completion reliability; permission for potion consumption (unchanged/off unless explicitly enabled); and willingness to test one supervised defensive dodge. AAC and Moondial remain research-only/deferred.
