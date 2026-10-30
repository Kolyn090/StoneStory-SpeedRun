# Observer in-game acceptance

Updated: 2026-10-29. Scope: deployment, lifecycle, timing, completion observation, and diagnostic display only. No combat automation is requested or required.

## Recorded deployment result

| ID | Status | Evidence | Limits |
|---|---|---|---|
| DEP-01 | PASS (user-reported) | Owner saw the observer display and explicitly confirmed that the script loads and runs in Stone Story RPG with `import SpeedRun/main` | Loading/import execution and diagnostics rendering only; no timing/lifecycle inference |

Test environment: local Windows/Steam installation. Exact game build, tested map/difficulty, deployed revision/hash at the time of the successful run, and sample size were not recorded. Diagnostics had been enabled. Two deployment roots contain the files; which copy is resolved has not been isolated. These missing details do not invalidate the narrow user observation, but limit reproducibility. No agent-run game test is claimed.

## Preparation

1. Keep the working deployment and Mind Stone text unchanged for the normal tests. Diagnostics are already enabled. Do not redeploy just to run this checklist.
2. Record game build, location/difficulty, equipment, potion/resource settings, other Mind Stone logic, and the start method. Use a comfortably completable location with a boss completion score and Ouroboros access for the full sequence.
3. Record the repository revision and deployed file hashes if available; note local differences rather than assuming repository and deployment are identical.
4. Capture the overlay at relevant boundaries, ideally with video. Check Tab's recent Stonescript errors on PC. Do not use wall-clock seconds as an exact reference for simulation frames.

Use PASS, FAIL, BLOCKED (missing access/evidence), or NOT RUN. Every case below is currently **NOT RUN**. Record actual results before changing status. A blank or missing score is not a zero-frame completion.

## Core acceptance sequence

| ID | Steps | Expected result | Evidence / failure signal | Status |
|---|---|---|---|---|
| LIFE-01 | Leave to location selection and start manually; observe the first playable frames | `entry`; loops 0; current/last completion -1; completion count 0 | Capture early overlay. A later screenshot may show a positive elapsed interval; that alone is not a failed reset | NOT RUN |
| TIME-01 | Observe ordinary progression; compare overlay samples with an independent game-frame reference if available | Observed interval follows accumulated frames minus its boundary value, without unexpected regression | Record paired frame values. Increasing text alone verifies activity, not accuracy; mark accuracy BLOCKED if no independent frame reference is available | NOT RUN |
| TIME-02 | Cross into the boss sub-location without leaving | Accumulated interval remains continuous; local `time` may reset; no new entry/loop initialization | Before/after values and video; unexpected session clearing or accumulated-time regression is a failure | NOT RUN |
| CAP-01 | Defeat the boss; remain on the result long enough to observe several updates | Current completion becomes positive; last equals current; count increases once; score stays fixed afterward | Capture before/after and compare with the game's leaderboard score. Rounded seconds cannot establish exact frame equality; mark exact accuracy BLOCKED if only rounded output is available | NOT RUN |
| LOOP-01 | Allow one Ouroboros loop after CAP-01 | `loop`; loops seen increases by 1; interval restarts; current becomes -1; last/count retain previous captured result until next completion | Capture immediately around boundary; stale score must not be recounted | NOT RUN |
| LOOP-02 | Finish and loop a second time | One additional completion count for the new result; one additional loop count; correct clearing/retention repeats | Record each boundary and count; duplicates, missing captures, or premature clears fail the corresponding behavior | NOT RUN |
| LIFE-02 | After a captured completion, leave and manually start again | `entry`; loops 0; count 0; current/last -1 | Demonstrates session reset rather than merely a fresh display | NOT RUN |
| LIFE-03 | Open and close Mind Stone without edits during a run | No unintended reset or duplicated completion | Record values before/after; elapsed frames may advance according to actual game behavior | NOT RUN |

## Separate edge cases and optional checks

These may interrupt a run or require a temporary configuration change. Do not modify the current working deployment as part of this documentation task. Perform only when ready, preserve backups for any later changes, and restore the known working configuration afterward.

| ID | Steps | Expected result / limit | Status |
|---|---|---|---|
| EDGE-01 | In a separate trial, first enable/load the observer after a run has started | `attached`; interval starts at attachment; no full completion credited until a subsequently observed loop. Requires a genuinely new observer instance; merely reopening Mind Stone does not establish this precondition | NOT RUN |
| EDGE-02 | Fail or abandon before completion | No synthetic successful result; count is not an attempts/deaths metric. A previously retained last result is not evidence that this attempt succeeded | NOT RUN |
| EDGE-03 | Disable/re-enable Mind Stone around a boundary | Record actual behavior; a missed boundary invalidates that trial for timing/loop acceptance. Manual restart should restore the LIFE-01 baseline | NOT RUN |
| DIAG-01 | Later, with a backed-up, identified resolved file, disable diagnostics and restart manually | Overlay absent; no newly introduced gameplay control. This does not prove the observer stopped or that timing overhead is zero | NOT RUN |
| PERF-01 | Later, compare repeated equivalent runs with diagnostics on/off and observer absent | Record timing distributions and failures; no speed/overhead threshold is established yet | NOT RUN |

## Report a result or failure

Copy this template into a message or a new test record. Preserve expected values separately from observations. If a failure appears, save evidence before restarting; do not alter the script to make the case pass. One failure need not block unrelated safe observations.

```text
Case ID and status: e.g. LOOP-01 / FAIL
Date / tester:
Game build / platform:
Repository revision / deployed hashes (or unknown):
Known script root / import line / diagnostics setting:
Location / difficulty / first entry or loop:
Equipment / potion / other Mind Stone scripts:
Exact steps, including pause, edits, restart, or missed frames:
Expected result:
Actual result:
Before -> after:
  startKind:
  loops seen:
  observed interval:
  location time / accumulated time:
  current completion / last completion / count:
Game completion score and displayed precision:
Stonescript error text, exact if present:
Screenshot/video or log reference (optional but useful):
Reproduction attempts / failures:
Unknown or missing evidence:
```

Do not publish full save files or unrelated account data to report an error. For an invisible overlay, report whether the Mind Stone is enabled, whether its power/import text changed, and any error; distinguish display/import failure from a measurement failure.

## Acceptance decision

DEP-01 is the only passed case. Lifecycle resets, timing accuracy, completion capture, and Ouroboros loop handling remain unverified until their cases have separate evidence. BLOCKED is not PASS. Record a failed case and retest after any later authorized fix; retain the earlier result. Verify at least two consecutive loops as specified, and do not generalize one tested location/build to all difficulties or versions.

Only after the core cases pass should the observer support controlled speedrun benchmarks. Combat remains outside this milestone.
