# StoneStory-SpeedRun development instructions

## Permanent rule: Triskelion Stone for faster clear travel

Prioritize completion time with configurable equipped Triskelion movement during safe travel. Use verified `triskelion` equipment criteria; do not invent an activation/cooldown or assume a lingering bonus after removal. Reserve travel gear for clear ordinary movement: current conservative policy requires no targeted foe, no enemies reported within 46 units, full HP, walking, and no boss observed this attempt. Every targeted enemy takes priority regardless of melee distance, including ranged/imminent threats; keep combat gear ready before the first attack.

Keep Triskelion in a stable slot. Star Stone may briefly use the other slot without replacing it; collection must yield if slots conflict or measured completion time/reliability worsens. Never add repeated alternating swaps, fixed travel waits or collection detours. Protected combat, movement and mandatory progression sequences must bypass ordinary travel equipment decisions. Verify movement with documented `player.framesPerMove` and actual timed runs; magnitude, exact applicability, carryover and switching side effects require in-game evidence. See [TRISKELION_TRAVEL.md](docs/TRISKELION_TRAVEL.md).

## Permanent rule: passive resource collection using Star Stone

The owner has effectively unlimited resources. Optimize reliable location progression, movement, combat, boss completion and total run time. Never add farming, optional shovel harvesting, resource-accumulation targets or collection detours. Collection is incidental, never an optimization objective. Exception: opportunistically equip Star Stone to attract already-nearby pickups during safe ordinary travel, without activation, waiting or interrupting combat, boss mechanics, mandatory progression, movement optimizations or protected equipment sequences. Keep this behavior configurable for benchmarks and bound/latch requests to avoid equipment thrashing.

Consult [PASSIVE_STAR_STONE.md](docs/PASSIVE_STAR_STONE.md). Use documented `pickup`/`pickup.distance`; they describe the currently targeted pickup, not an enumerable list or stable instance ID. The official tutorial's `<10` trigger is not proof of a universal maximum attraction radius. Do not invent pickup events, IDs, range queries or Star Stone activation APIs. Confirm effective range, collection duration, native movement and any timing benefit in-game before making broader claims. Higher-priority handlers must bypass passive collection, not have their equipment overwritten afterward.

Preserve interactions and tool use genuinely required to progress (for example a confirmed blocking object or mandatory traversal interaction). Classify these by explicit location/phase evidence; the presence of a `harvest` target alone is not proof of a progression requirement. Do not globally disable native interactions or remove required utility items to suppress optional gathering. Any future progression-tool handler must be narrow, restore combat equipment, and be tested for passage/completion. Do not reintroduce generic harvesting as a fallback.

## Performance objective

Current priority: broad basic automation coverage, correctness, and reliability before advanced speed optimization. Long term, minimize Stone Story RPG completion time while maintaining an explicitly agreed reliability target. Optimize measured in-game results, with maintainable code that supports continued tuning.

## Required research

- Read `docs/STONESCRIPT_KNOWLEDGE.md` and `docs/ROADMAP.md` before development.
- Consult the current [official manual](https://stonestoryrpg.com/stonescript/manual.html) before implementing unfamiliar syntax, APIs, lifecycle behavior, or equipment interactions.
- Study relevant public Stonescript implementations linked in the knowledge base. Treat them as examples, not authoritative specifications; attribute adapted ideas and check licenses before reusing code.
- Never infer language support from Python, JavaScript, or another language. Clearly label proposed helpers as project functions rather than native APIs.

## Implementation principles

- Account for execution every frame: command order, attack windup, recovery, equipment transitions, activation eligibility, and state persistence matter.
- Prefer small location profiles and explicit bounded sequences. Avoid premature generic engines, repeated inventory searches, unbounded histories, or expensive debug work in the frame loop.
- Preserve existing functionality and unrelated user changes. Inspect the worktree before edits.
- Keep inventory CSVs unchanged unless the user authorizes changes. Resolve ambiguous data in a separate documented mapping first.
- Distinguish ordinary equipment selection from intentional intermediate swaps used by experimental cancellation techniques.
- Keep emergency actions, protected sequences, boss decisions, normal combat, and travel from accidentally overwriting one another.
- Measure actual completion times and reliability. Static DPS and cleaner code do not establish an improvement.

## Evidence and reporting

- Label findings as official documentation, community observation, project proposal, or in-game verified result.
- Record important findings in the knowledge base and milestone status in the roadmap.
- For game tests, record game build/platform, script revision, location/difficulty, exact gear, potion/resource policy, first-entry versus loop, timing metric, sample size, failures, and results.
- Never claim in-game testing from source review or static checks. Record untested behavior and known limitations explicitly.
- Change one optimization at a time; compare against a reproducible baseline and retain a fallback.
- Expand coverage only after the current profile passes its agreed timing and reliability gates.

## Current scope

The original observer is in `scripts/main.txt` and `scripts/metrics/RunMetrics.txt`; read `docs/INSTALLATION.md`. Its loading/import execution and visible diagnostics are user-verified (2026-10-29); lifecycle, timing, completion and loops remain unverified. Keep it available for rollback.

The authorized basic automation candidate is separate in `scripts/basic/`, deployed as `SpeedRunBasic`, reusing the original metrics module. Read `docs/BASIC_AUTOMATION.md` and `docs/LOCATION_COVERAGE.md`. Named routes do not prove completion support; all new combat and location/difficulty results remain untested. Use only one entry point in Mind Stone. Back up working files before deployment and preserve unrelated scripts and gear CSVs. Add boss specialization only in response to evidence that generic behavior is inadequate; advanced speed optimizations are deferred.

Active phase: B2 testing/stabilization. Read `docs/BASIC_TEST_PLAN.md` and record owner reports in `docs/BASIC_TEST_RESULTS.md`. Begin with Rocky Plateau and fix shared defects first. Do not mark a location/difficulty successfully automated without explicit owner confirmation of an actual unassisted completion; keep assisted outcomes separate. Preserve every historical backup and the original observer. No advanced boss strategies or AAC in this phase.
