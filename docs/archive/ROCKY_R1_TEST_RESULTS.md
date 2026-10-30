# Rocky R1 acceptance and results

> Historical record. Preserved behavior, timings, test counts and commands describe that development stage. This is not a current deployment or implementation guide. Start at the [documentation index](../README.md) and [current R15 guide](../rocky/ROCKY_PLATEAU_15.md).

Status 2026-10-29: candidate prepared only; **NOT INSTALLED / ALL GAME TESTS NOT RUN**. No Rocky difficulty is completion-confirmed. Static/model checks are not acceptance results. See [candidate instructions](ROCKY_PLATEAU_CANDIDATE.md).

| Case | Expected observation | Result |
|---|---|---|
| R1-LOAD | Candidate imports resolve; header/route/owner/current requested and actual gear readable; no native errors | NOT RUN |
| R1-SHARED | Ordinary/travel frames fall back once to existing shared automation; no optional shovel harvesting | NOT RUN |
| R1-SCOUT | Scout identified when present; default fire/observed element + shield; armor priority; mark not encountered if absent | NOT RUN |
| R1-PHASES | Bearer/Elementalist/Perfected identified only when observed; unrecognized form warns | NOT RUN |
| R1-GAPS | Boss latch persists through missing/dead/undamageable target and sub-location boundary; no travel override | NOT RUN |
| R1-ADAPTIVE | Exact observed adaptive UID excludes element; malformed/unrecognized family warns/falls back | NOT RUN |
| R1-ARMOR | Eligible hammer + shield while armored, allowed fallback visible; no healing overriding armor priority | NOT RUN |
| R1-PRIORITY | One owner; matching requests/actual hands; core/AI/immunity/manual-limit conditions visible | NOT RUN |
| R1-LIFECYCLE | Fresh entry, loop, attachment and boss sub-location behavior recorded; no false completion capture | NOT RUN |
| R1-COMPLETE | Exact location/difficulty completes without manual intervention; all failures/assists retained | NOT RUN |

Copy this record per baseline/candidate run. Keep exact private inventory provenance in ignored local notes, not in this public template. Do not paste a save, profile ID, authentication field, random seed or custom item tag.

```text
Run ID / date:
Actual game build / platform:
Baseline B2.1-TS or candidate Rocky R1 / bundle digest:
Map / loc.id / difficulty:
Entry / loop / attached:
Profile flags / shared travel and potion flags:
Displayed actual equipment / exact selector checks completed?:
Core/strict misses / native errors:
Scout encountered? / phase tags and identities observed:
Observed adaptive UID text / armor behavior / warnings:
Requests and actual L/R at failure or phase boundary:
Baseline total time (metric + units):
Candidate total time (metric + units):
Travel / Scout / phase-1 / phase-2 / phase-3 splits (metric + units, or not measured):
Observer startKind / currentCompletion / lastCompletion / count / loop changes:
Independent timing/video reference:
Completed? / unassisted? / manual inputs or rescue:
Deaths / stalls / retries / stun or unavoidable-attack observations:
Expected versus actual / next single issue to investigate:
Owner-confirmed result (leave pending until explicitly reported):
```

For first acceptance, prioritize import/gear correctness and an actual unassisted completion at one chosen difficulty. Missing Scout or a phase does not pass that unencountered case. A fast assisted result is not full automation. Record phase-3 survival failures candidly: R1 has no calibrated avoidance timing, and broader completion may need that follow-up. Repeatability/other difficulties remain separate gates.
