# Documentation index

This index owns project status/navigation. Each topic below has one authoritative page; archive records preserve evidence but do not override current instructions.

## Current project status

| Component | Status | Authoritative guide |
|---|---|---|
| B2.1-TS / `SpeedRunBasic` | Existing live baseline; deployments preserved. No recorded automated completion | [Baseline behavior/install](guides/BASIC_AUTOMATION.md) |
| Rocky ★15 R15 / `SpeedRunRocky` | `1c696fe`: first owner-confirmed successful ★15 dual-wield + AAC baseline; runtime error resolved. Approximate timing is informal; AAC-specific throughput/repeatability remain unverified | [R15 decisions/bundle/activation/checklist](rocky/ROCKY_PLATEAU_15.md) |
| Original observer / `SpeedRun` | Loading/display owner-verified; lifecycle/timing/capture/loops unverified | [Observer installation](guides/INSTALLATION.md), [acceptance](guides/OBSERVER_ACCEPTANCE.md) |
| Isolated selector diagnostic | Installed count-only in both known roots; native execution/matches unconfirmed | [Selector guide](gear/EQUIPMENT_SELECTOR_VALIDATION.md) |
| R1 | Historical predecessor; no inherited R15 gameplay passes | [R1 record](archive/ROCKY_PLATEAU_CANDIDATE.md) |

The active game script root remains unisolated. A native count, exact selected variant, completion, repeatability and measured speed are separate evidence gates. The [R15 results ledger](rocky/ROCKY_PLATEAU_TEST_RESULTS.md#successful-baseline-1c696fe) owns the confirmed completion and approximate timing; this documentation update makes no deployment.

## Current user guides — `guides/`

- [B2.1-TS behavior, architecture and install/rollback](guides/BASIC_AUTOMATION.md).
- [Baseline test procedure](guides/BASIC_TEST_PLAN.md), [baseline results](guides/BASIC_TEST_RESULTS.md), [generic location coverage](guides/LOCATION_COVERAGE.md).
- [Observer installation](guides/INSTALLATION.md) and [observer acceptance](guides/OBSERVER_ACCEPTANCE.md).

## Architecture, language and project policy

- [AGENTS instructions](../AGENTS.md) — future-session development rules and authorization boundaries.
- [Implemented architecture](ARCHITECTURE.md) — modules, imports and equipment ownership.
- [Stonescript knowledge](STONESCRIPT_KNOWLEDGE.md) — syntax/API evidence and uncertainty rules.
- [Current roadmap](ROADMAP.md) — immediate gates and deferred work.
- [Triskelion travel](TRISKELION_TRAVEL.md) — current movement/slot policy and evidence.
- [Passive Star collection](PASSIVE_STAR_STONE.md) — current collection bounds/priority; no farming or detours.

## Gear references and offline tooling — `gear/`

- [Gear reference review](gear/GEAR_REFERENCE_REVIEW.md) — primary displayed-stat provenance, units, conflicts and verification limits. Source CSVs remain under `data/gears/`; [the original note](../data/gears/note.md) records a legacy assumption, not fresh verification.
- [Private save verification](gear/PLAYER_SAVE_VERIFICATION.md) — dated sanitized structural evidence.
- [Private importer workflow](gear/PRIVATE_INVENTORY_IMPORT.md) — safe local regeneration and schema limits.
- [Isolated selector diagnostic](gear/EQUIPMENT_SELECTOR_VALIDATION.md) — current diagnostic install/use, not combat integration.
- [B2 selector/API audit](gear/SELECTOR_API_AUDIT.md) — historical technical review, not R15 native validation.

## Rocky strategy/development — `rocky/`

- [R15 current candidate](rocky/ROCKY_PLATEAU_15.md) — source behavior, equipment, current manifest and future activation.
- [Current identity crosswalk](rocky/ROCKY_EQUIPMENT_CROSSWALK.md) — FastGenShl is an owner-confirmed Towering nickname; distinct screenshot stats and saved-record joins remain separate.
- [R15 acceptance/results](rocky/ROCKY_PLATEAU_TEST_RESULTS.md) — authoritative owner-confirmed baseline, approximate timing limits and historical attempts; individual component checks remain separate.
- [Public source research](rocky/ROCKY_PLATEAU_RESEARCH.md) — pinned sources, attribution/licenses and hypotheses; not current implementation instructions.

## History — `archive/`

The [archive index](archive/README.md) covers R1, earlier plans/crosswalk/tests, B2/NR/PS revisions, deployment records, reserved-name failure, knowledge milestones and the foundation roadmap. Preserve historical test counts and failed attempts with their original scope. Do not execute archived deployment commands for the current candidate.

## Maintenance

Run commands from the repository root unless a page explicitly says otherwise. Update current guides first; link instead of copying equipment rules, status narratives or install procedures. Keep imported private notes and backup snapshots immutable. The two old-path redirects exist only for those preserved references.

Validate local Markdown links, anchors and explicit documentation path references with `python -B tools/check_documentation_links.py`. This check does not fetch external sites or validate in-game behavior. See [the organization audit](DOCUMENTATION_AUDIT.md) for moves, retained evidence and remaining uncertainties.

## R16 independent experiment

[Scout Mask/dash experiment](rocky/ROCKY_R16.md) is local, disabled by default and undeployed on its own branch, based on successful R15 `1c696fe` plus documentation `5d57ccf`. It does not replace the deployed baseline; other effect rotations and Berserk remain deferred.
