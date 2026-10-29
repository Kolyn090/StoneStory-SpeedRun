# Development roadmap and architecture

Status (2026-10-29): original observer retained with user-verified loading/display; correctness tests still pending. Basic automation and eight-route dispatcher implemented as an untested side-by-side candidate. No automated completion or speed result is verified.

Current objective: broad completion coverage, functional correctness, and reliability before speed tuning. Long-term objective: minimize completion time subject to an agreed reliability target across relevant locations/difficulties. Resources are effectively unlimited: farming, optional shovel harvesting, collection detours and accumulation are never optimization goals. Collection is incidental; configurable Star Stone attraction is permitted only as safe background travel behavior with no waiting or higher-priority interruption. Preserve mandatory progression. Read [the knowledge base](STONESCRIPT_KNOWLEDGE.md), [resource policy](RESOURCE_POLICY.md) and [Star Stone validation](PASSIVE_STAR_STONE.md).

## Proposed structure

Paths describe responsibilities, not files to create immediately. Begin with a small entry script and add modules when a second consumer or substantial strategy justifies them.

```text
AGENTS.md
data/gears/                  existing inventory reference, preserved
docs/
  STONESCRIPT_KNOWLEDGE.md
  ROADMAP.md
  benchmarks/                future experiment records
scripts/
  main.txt                   entry point, lifecycle, location dispatch
  config/                    exact gear selectors and run profiles
  core/                      minimal state and action arbitration
  locations/                 location/difficulty policy and phase dispatch
  bosses/                    encounter-specific state machines
  equipment/                 availability, selectors, fallback loadouts
  combat/                    target policy, debuffs, later optional AAC
  movement/                  travel, approach, mandatory traversal interactions
  abilities/                 ability sequences and potion policy
  metrics/                   splits, counters, optional diagnostics
  shared/                    small genuinely reused helpers
```

Do not build a generic plugin framework, event bus, dynamic scoring engine, or runtime CSV parser at the outset. Inventory CSVs remain reference data; any future generated configuration needs an explicit build/deployment design and authorization for tooling.

## Frame workflow and ownership (proposal)

Current B2.1-TS travel refinement implements optional cached `triskelion`, a stable left-hand travel slot, and Star Stone in R only for bounded clear-area pickup opportunities. Ordinary travel and combat share one final pair executor; no post-combat collection override and no Triskelion activation/timer. Any targeted foe prepares existing combat gear immediately; non-targeted foes reported within 46 units request wand/shield readiness. Mandatory/protected handlers continue to outrank ordinary travel. See [TRISKELION_TRAVEL.md](TRISKELION_TRAVEL.md).

1. Handle fresh-entry/loop resets, clearing frame-local requests separately from persistent sequence state.
2. Read only the state needed by the active profile. Reuse values within that decision pass; refresh after mutations if subsequent logic needs updated equipment/activation state.
3. Dispatch the current location and difficulty only. Delegate to a boss handler when appropriate.
4. Resolve competing actions with a deterministic priority: required survival response, protected sequence, mandatory progression interaction, boss strategy, regular combat, movement optimization, ordinary travel. Only ordinary travel may offer its loadout to bounded passive Star Stone attraction. Never append pickup equipment commands after a higher-priority handler. Future progression tools require a narrow location/phase condition, evidence that passage needs them, and restoration of combat gear; optional farming is not an action owner.
5. Execute the selected ordinary equipment/ability action or the selected bounded sequence.
6. Record transitions/splits. Keep optional rendering and analysis off the critical decision path.

This workflow is not an API contract. Module initialization, per-frame execution, imported scope, and argument passing must follow the manual. Choose `import` versus `new` deliberately; avoid duplicate active script bodies or hidden dependence on shared globals.

Initially use scalar fields or a small fixed request representation. An action has an owner, intended equipment/hand, activation intent, and optional sequence phase/deadline. These are conceptual fields, not native Stonescript objects or APIs.

Only the executor and explicitly approved sequence routines issue equipment commands. Normal selection avoids accidental oscillation; an AAC experiment may intentionally issue intermediate swaps. Emergency interruption must release ownership and restore a valid loadout. Every sequence needs completion, timeout, target/phase-change cancellation, and reset behavior.

Cache static gear information at initialization. Keep volatile distance/state/eligibility checks current. Do not throttle defensive timing or cancellation checks. Add modules incrementally and measure overhead rather than assuming abstractions are free.

## Milestones and acceptance gates

Authorized next travel gate: test Triskelion equipped versus disabled under identical build/gear/difficulty, verify `player.framesPerMove` and timed travel splits, both-hand stone coexistence, threat/first-attack transitions (including ranged), no boundary oscillation and mandatory traversal. Keep Star separately configurable to isolate gains/losses. No bonus magnitude/carryover or all-location safety claim is accepted from source inspection; no arbitrary travel delay or duplicate-stone stacking optimization. All B2.1-TS game tests remain NOT RUN.

Current incremental gate: B2.1-PS adds bounded passive attraction to ordinary travel with an off switch. Verify targeted-pickup detection, installed effective range, actual attraction while moving, no combat/boss interruption, no repeated swaps and timeout restoration. Compare paired enabled/disabled completion timings at fixed gear/build/difficulty; disable if slower or less reliable. Raw material yield is not an acceptance metric. Do not expand the range beyond the documented tutorial threshold without separate evidence; exact maximum radius is unresolved. See PASSIVE_STAR_STONE.md; all in-game outcomes remain NOT RUN.

| Priority / milestone | Scope | Dependencies | Acceptance gate |
|---|---|---|---|
| P0 / M0: documentation foundation | Knowledge, instructions, architecture, evidence boundaries | None | Three documents reviewed; inventory/runtime untouched |
| P0 / M1: define reproducible baseline | Select target and timing rules; clarify units and exact gear identities; establish manual baseline | M0 and owner decisions below | Repeatable run configuration and baseline records; unresolved data explicitly excluded |
| P1 / M2: noncombat runtime foundation | Entry/loop lifecycle, optional diagnostics, reusable frame timing and completion observer | Authorized shared subset proceeds independently of target/gear decisions in M1 | Partial acceptance: loading/import execution and visible diagnostics passed by user report; lifecycle resets, timing, completion and loops pending per OBSERVER_ACCEPTANCE.md |
| P1 / M3: broad generic automation | Shared shielded combat, cached gear, named dispatch, basic survivability; required progression only | Authorized now; retain original observer; exact-gear and M2 tests still open | Candidate implemented; optional harvesting removed in B2.1-NR; all completion tests NOT RUN |
| P2 / M4: travel tuning | Direct approach, quarterstaff/shields where measured useful, mandatory traversal | Stable M3 | Lower net completion time without collection detours, unacceptable failures or delayed first hits |
| P2 / M5: combat and boss tuning | Armor/element/AoE policy, debuff payback, phase-aware bursts and potion timing | M3; measured bottlenecks | Repeated encounter/phase gains translate into net run improvement |
| P3 / M6: advanced cancellation | Per-weapon AAC/juggling experiments behind opt-in configuration | Stable baseline and frame traces from M5 | Damage preserved, repeatable time gain, safe interruption and fallback verified |
| P1 / M7: validate broad coverage | Test each main route, record difficulty limits, add necessary boss exceptions | M3 import/gear smoke tests; failures drive specialization | Per-location/difficulty recorded completions and manual-intervention rates; no inferred support from route existence |
| Ongoing / M8: efficiency audit | Optional diagnostics, bounded history, repeated searches, module cost | Measurable overhead | Reduced overhead without degraded timing decisions or completion reliability |

M7 now precedes advanced M4-M6 optimization: establish basic completion first, then add necessary specialized mechanics. M4-M6 remain deferred until reliability and coverage warrant tuning. M7 proceeds one measured profile at a time; there is no all-difficulty support claim.

## Benchmark protocol

- Fix game build, platform, gear, difficulty, potion/summon/resource policy, and first-entry/loop conditions.
- Define start/end boundaries for the chosen metric. Keep leaderboard frames, accumulated game frames, and real elapsed time distinct.
- Use repeated paired or interleaved baseline/candidate runs. Agree sample size before drawing conclusions; expand it when variation makes the result inconclusive.
- Capture median, best, spread, completion rate, failures and manual interventions. Include retry time in the chosen completion metric. Record potion/summon use for reproducibility, not resource conservation or accumulation.
- Preserve total and travel/boss splits so an apparent local improvement cannot hide a slower run.
- Exercise target disappearance, phase transitions, cooldown unavailability, interrupted sequences, and loop resets.
- Keep a known-good fallback. Record actual results in `docs/benchmarks/` once experiments exist and summarize discoveries in the knowledge base.

## Decisions requiring owner input

Before M1 closes:

1. First location and difficulty, installed game build/platform, and whether a current Mind Stone script exists outside this repository.
2. Primary timing metric: leaderboard frames or real elapsed completion time. Define whether retries count; resource farming is excluded.
3. Acceptable completion reliability, risk tolerance, and potion/summon activation permissions. Resource cost is not an optimization constraint; current opt-in settings remain unchanged.
4. Actual gear selectors and modifiers; meaning/units of ambiguous CSV fields; whether +21/21 is current inventory or a target assumption.

Deployment files exist in both the supplied Steam directory and the discovered save-folder directory. The working import has been confirmed by the owner; which copy the game resolves remains unisolated. Preserve both working copies during documentation work. A future deployment workflow should resolve that ambiguity before updates; no deployment automation is chosen yet.

Later: define the relevant location/difficulty coverage list and whether experimental AAC/juggling is allowed for the intended run category.

## Current validation

M0 documentation delivered. M1 baseline decisions remain open. The user authorized the location-independent M2 subset before those decisions; `scripts/main.txt` and `scripts/metrics/RunMetrics.txt` now implement it. Equipment validation is deferred until exact gear identities are supplied; manual phase splits and persistent results are deferred until needed.

Deployment gate passed by user report: script loading/import execution and visible diagnostics. No lifecycle reset, timing accuracy, completion capture, or Ouroboros result is marked passed. No inventory changes or speed improvements are claimed. See [INSTALLATION.md](INSTALLATION.md) and [OBSERVER_ACCEPTANCE.md](OBSERVER_ACCEPTANCE.md).

The owner subsequently authorized shared basic automation and broad location dispatch. The candidate lives under `scripts/basic/` and uses the original observer module unchanged. Read [BASIC_AUTOMATION.md](BASIC_AUTOMATION.md) for deployment, rollback, and smoke tests. Potion consumption is opt-in; no boss strategies or advanced cancellation are implemented. Inventory CSVs remain unchanged.

Next: verify new imports and actual gear selection on a safe run, then test each route/difficulty and repeat pending observer cases. Record all outcomes in [LOCATION_COVERAGE.md](LOCATION_COVERAGE.md). M2 remains partially accepted, M3 is source-implemented only, and M7 testing is NOT RUN. Close exact-gear/build/resource/reliability questions from M1 as test metadata rather than inventing them.

## Active phase: B2 testing and stabilization

### Prerequisite: exact equipment selector validation

The private importer is complete. An isolated diagnostic and reproducible private candidate builder now exist; see [EQUIPMENT_SELECTOR_VALIDATION.md](EQUIPMENT_SELECTOR_VALIDATION.md). Source, synthetic tests and a backup-first optional installer are ready; live installation and all in-game results remain pending. Neither B2.1 nor the observer was modified.

1. Owner verifies count-only import, browsing/recount, zero/multiple handling and no equipment changes with test mode disabled.
2. Owner explicitly enables supervised one-shot tests, beginning with B2.1 sword/wand/shield families, and compares exact inventory details.
3. Resolve displayed stars, primary/secondary enchantments, effect tokens, hand requirements and ambiguous variants. Keep unknown aliases deferred; do not infer stars from raw upgrade values.
4. Only after exact-item confirmation, authorize a separate B2.1 integration milestone using individually verified selectors and a fallback policy. Continue Rocky Plateau stabilization before broader coverage/optimization.

Current evidence: all 130 inventory records profiled privately, 94 candidate queries, 30 with multiple saved profiles, 21 equipment/tool records deferred; 23 automated tests pass. No selector exact-match or location-completion status is promoted to verified.

Freeze advanced features. The compact B2 configuration adds selector-availability and unsupported-condition diagnostics and fixes misleading/stale equipment requests. Missing core gear stops project equipment/potion automation. Source fixes do not constitute in-game acceptance.

Follow [BASIC_TEST_PLAN.md](BASIC_TEST_PLAN.md): Rocky Plateau, then the other seven recognized locations at recorded safe difficulties. Keep all location completion statuses NOT RUN until the owner confirms results; record failures/assisted completions separately in [BASIC_TEST_RESULTS.md](BASIC_TEST_RESULTS.md). Prioritize shared import, selector, switching and lifecycle defects before map-specific logic. Existing observer and all historical backups must remain unchanged. See [SELECTOR_API_AUDIT.md](SELECTOR_API_AUDIT.md) and the B2 deployment record for static evidence.
