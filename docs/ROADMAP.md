# Current development roadmap

**`1c696fe` is the first owner-confirmed successful Rocky Plateau ★15 dual-wield + AAC baseline on `main`.** The owner confirms completion and resolution of the prior runtime error. The [results ledger](rocky/ROCKY_PLATEAU_TEST_RESULTS.md#successful-baseline-1c696fe) owns the approximate clear-time comparison and its measurement limits. B2.1-TS remains preserved; the [R15 guide](rocky/ROCKY_PLATEAU_15.md) owns current implementation and activation details.

| Priority | Gate | Evidence/status |
|---|---|---|
| Completed filesystem gate | Authorized R15 installation and runtime fix | Source/deployment hashes verified in both maintained roots; B2.1/observer preserved |
| Completed gameplay gate | First successful ★15 dual-wield + AAC run | Owner confirms `1c696fe` stage completion and runtime-error resolution; no statistical reliability claim |
| Now | Establish repeatability and comparable timing | A few matched ★15 runs with consistent timing boundaries, loadout/flags, completions, deaths/interventions and errors |
| Next controlled comparison | Isolate AAC-specific benefit | Compare AAC on/off under matched conditions; aggregate clear time does not prove per-hand throughput or damage preservation |
| If a new failure appears | Fix the observed bottleneck | Reproduce the failure; use targeted selector/mechanic checks, not a broad validation campaign |
| Later | Compare loadouts, defense and travel | Preserve `1c696fe` as the successful comparison baseline; optimize measured completion time/reliability, never farming |
| After repeatability | Expand difficulty and loop coverage | Separate recorded outcomes; one ★15 completion does not validate other difficulties, locations or loop boundaries |

The approximate owner timing improvement is an informal whole-strategy observation, not a formal multi-run benchmark or an AAC-specific speed claim. Individual recovery thresholds, selector variants, duplicate Vigor allocation, armor cases and observer lifecycle/timing/loop acceptance keep their existing verification limits. Actual game build, exact baseline conditions and active import root still need recorded evidence where missing.

R16 advanced-combat research and R17 recording remain independent experimental branches; this milestone does not merge or deploy them. Heavy Hammer sequences, new active abilities and additional boss timing remain deferred. Short-sword AAC remains part of the successful Rocky baseline, with its detailed throughput unverified.

The [earlier working plan](archive/ROCKY_PLATEAU_WORKING_PLAN.md) and [foundation roadmap](archive/FOUNDATION_ROADMAP.md) preserve historical design and milestone evidence. See [architecture](ARCHITECTURE.md) for implemented ownership. Preserve working scripts and rollback files; documentation work alone authorizes no gameplay deployment.

## R16 opt-in gate (independent branch)

[R16](rocky/ROCKY_R16.md) adds disabled Scout-only Mask/dash trials with exclusive ownership. Next gates are all-off equivalence, exact scoped selectors, one dash approach and one Mask activation tested separately; only then combine and compare measured runs. Debuff IDs, boss susceptibility, additional status rotations and potion availability remain unresolved. No R16 deployment or merge into the successful R15 baseline is implied.
