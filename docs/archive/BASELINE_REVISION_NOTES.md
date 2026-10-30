# Baseline guide revision history

Historical introductions extracted from the live-baseline guides during organization. For current behavior use [B2.1-TS](../guides/BASIC_AUTOMATION.md).

## BASIC_AUTOMATION prior introduction

# Basic automation candidate

Current revision **B2.1-TS** adds configurable Triskelion travel: clear movement uses Triskelion L + shield R; bounded passive collection uses Triskelion L + Star Stone R. Every targeted foe enters existing combat selection without the old 22-unit travel shortcut. Immunity conflicts restore wand/shield for manual handling. Combat selection rules otherwise remain unchanged. See [TRISKELION_TRAVEL.md](../TRISKELION_TRAVEL.md); earlier PS/NR notes below describe historical behavior.

Current revision: **B2.1-PS** adds configurable passive attraction with Star Stone L + shield R only in safe ordinary travel. It never adds optional shovel harvesting or collection detours. See [PASSIVE_STAR_STONE.md](../PASSIVE_STAR_STONE.md); physical range, timings and completion benefit remain unverified. Earlier B2.1-NR policy below records the shovel-removal baseline; the current bounded Star Stone exception supersedes its general prohibition on collection-only swaps.

Current policy revision: **B2.1-NR** removes optional resource harvesting. Resources are incidental; movement, combat, boss completion and run time take priority. Earlier B2/B2.1 reports are historical. See [RESOURCE_POLICY.md](RESOURCE_POLICY.md) for the source audit, backup/deployment evidence and progression test gate. Mandatory interactions remain in scope; no blanket native-interaction suppression is applied.

Status: source-reviewed, not parsed or executed in-game. Priority is broad basic coverage and reliability; speed optimizations, AAC, dash sequences and boss timing are deferred. See [coverage matrix](../guides/LOCATION_COVERAGE.md).

Current stabilization build: **B2**. Follow [BASIC_TEST_PLAN.md](../guides/BASIC_TEST_PLAN.md), starting with Rocky Plateau; record results in [BASIC_TEST_RESULTS.md](../guides/BASIC_TEST_RESULTS.md). No completion status changes without explicit owner confirmation. See [SELECTOR_API_AUDIT.md](../gear/SELECTOR_API_AUDIT.md) for API and selector review.

Correction **B2.1** supersedes the B2 diagnostic header: `Harvest()` was rejected as reserved by the game, preventing the catalog object from loading. It is now `EquipHarvestTool()`; its call site and diagnostic revision are the only runtime changes. See [BUG_HARVEST_RESERVED.md](BUG_HARVEST_RESERVED.md). The B2 test sequence still applies, with B2.1 expected in the header; corrected import/execution remains pending owner retest.


## BASIC_TEST_PLAN prior introduction

# B2 testing and stabilization

Current revision: **B2.1-TS**. Follow [TRISKELION_TRAVEL.md](../TRISKELION_TRAVEL.md) for movement, stable slots, ranged threat/first-attack transitions, benchmark toggles and the movement-frame diagnostic. All older header/slot descriptions below are historical. No completion status changes from this source/deployment milestone.

Current revision: **B2.1-PS**. First follow [PASSIVE_STAR_STONE.md](../PASSIVE_STAR_STONE.md): Star Stone is allowed only in safe ordinary travel with nearby targeted pickups, with bounded duration and a benchmark off switch. Expect no shovel or harvest strategy. The B2.1-NR description below is historical; all existing completion statuses remain unchanged.

Current revision: **B2.1-NR**. Optional harvesting is removed; preserve mandatory passage/interactions. Follow [RESOURCE_POLICY.md](RESOURCE_POLICY.md) for this change's tests. Historical B2 expectations are superseded where noted below; no prior completion status changes.

Status: prepared for owner testing; **all eight location completion tests remain NOT RUN**. No advanced boss logic or AAC is introduced. The original observer and all prior backups are preserved. B2 uses the existing five modules and the unchanged original metrics dependency.
