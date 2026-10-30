# Current development roadmap

R15 is **implemented but uncommitted, undeployed, and not yet verified in-game**. B2.1-TS remains the existing live baseline. [The documentation index](README.md) owns the project-status table; [the R15 guide](rocky/ROCKY_PLATEAU_15.md) owns current equipment, fallback, bundle and activation details.

| Priority | Next gate | Required evidence |
|---|---|---|
| Now | Review the small Rocky ★15 R15 implementation | Source/test review; no automatic staging, commit or deployment |
| After explicit authorization | Back up and install R15 separately | Dependency/bundle hashes; preserve live B2.1/observer and all backups |
| First game attempt | Load, actual equipped roles, phases, armor and transformations | Short [R15 checklist](rocky/ROCKY_PLATEAU_15.md); report one concrete failure or actual completion |
| Stabilization | Fix the observed ★15 bottleneck | Reproduce the selection/survival failure; targeted selector checks only when a real decision needs them |
| Later | Compare loadouts, defense and travel | Matched build/difficulty/flags; full-run time plus deaths/interventions, no farming objective |
| After a stable target | Expand difficulty and loop coverage | Separate recorded outcomes; do not infer Scout/phase support from unencountered cases |

Heavy Hammer sequences, new active abilities, advanced attack timing and AAC are outside the current first-playable scope. Observer lifecycle/timing/completion/loop acceptance remains pending. Actual game build, baseline completion and the active script root still need gameplay evidence where not already recorded.

The detailed [earlier working plan](archive/ROCKY_PLATEAU_WORKING_PLAN.md) remains design background, not current implementation or deployment authorization. The [foundation roadmap](archive/FOUNDATION_ROADMAP.md) preserves earlier M0–M8 decisions, architecture proposals, test counts and milestone history. See [architecture](ARCHITECTURE.md) for the structure that actually exists.
