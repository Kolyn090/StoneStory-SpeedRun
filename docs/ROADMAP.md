# Current development roadmap

R15 is **committed locally and deployed for supervised testing; not yet verified in-game**. B2.1-TS remains the existing live baseline. [The documentation index](README.md) owns the project-status table; [the R15 guide](rocky/ROCKY_PLATEAU_15.md) owns current equipment, fallback, bundle and activation details.

| Priority | Next gate | Required evidence |
|---|---|---|
| Completed filesystem gate | Authorized R15 installation | Committed-source/bundle hashes verified in both maintained roots; B2.1/observer preserved |
| Now | Authorized dual-wield + short-sword AAC release | Preserve the owner-reported one successful ray dodge; pass checks, commit/deploy, then measure damage preservation and survival |
| Next game attempt | Establish actual backflip, ray avoidance and correct restoration | Short [R15 checklist](rocky/ROCKY_PLATEAU_15.md); report one concrete failure or actual completion |
| Stabilization | Fix the observed ★15 bottleneck | Reproduce the selection/survival failure; targeted selector checks only when a real decision needs them |
| Later | Compare loadouts, defense and travel | Matched build/difficulty/flags; full-run time plus deaths/interventions, no farming objective |
| After a stable target | Expand difficulty and loop coverage | Separate recorded outcomes; do not infer Scout/phase support from unencountered cases |

Heavy Hammer sequences, new active abilities and additional boss timing remain deferred. Short-sword AAC is explicitly authorized in the current Rocky-only candidate. Observer lifecycle/timing/completion/loop acceptance remains pending. Actual game build, baseline completion and the active script root still need gameplay evidence where not already recorded.

The detailed [earlier working plan](archive/ROCKY_PLATEAU_WORKING_PLAN.md) remains design background, not current implementation or deployment authorization. The [foundation roadmap](archive/FOUNDATION_ROADMAP.md) preserves earlier M0–M8 decisions, architecture proposals, test counts and milestone history. See [architecture](ARCHITECTURE.md) for the structure that actually exists.
