# StoneStory-SpeedRun development instructions

## Objective

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
