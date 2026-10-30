# Documentation organization audit

2026-10-29. Documentation organization only: no gameplay/selector/CSV/private-save/deployment change, Git staging, commit, push or history rewrite.

## Inventory and authority

Initial scan read all 44 Markdown files outside `.git`: 28 project-owned pages (25 in docs, root README/AGENTS and the data-adjacent note), five backup copies, one private generated test note and ten third-party environment license pages. Backup/private/dependency pages are immutable reference material and were not reorganized. The original gear note remains byte-identical. The [index](README.md) identifies one current authority per topic.

R15 is implemented but uncommitted, undeployed, and not yet verified in-game. B2.1-TS is the existing live baseline. R1 is historical; its tests and bundle instructions cannot certify R15.

## Moved or archived original pages

| Original file (all directly under the old `docs/` root) | Destination | Treatment |
|---|---|---|
| `INSTALLATION.md` | [current location](guides/INSTALLATION.md) | Topic organization; links rebased |
| `BASIC_AUTOMATION.md` | [current location](guides/BASIC_AUTOMATION.md) | Topic organization; links rebased |
| `BASIC_TEST_PLAN.md` | [current location](guides/BASIC_TEST_PLAN.md) | Topic organization; links rebased |
| `BASIC_TEST_RESULTS.md` | [current location](guides/BASIC_TEST_RESULTS.md) | Topic organization; links rebased |
| `LOCATION_COVERAGE.md` | [current location](guides/LOCATION_COVERAGE.md) | Topic organization; links rebased |
| `OBSERVER_ACCEPTANCE.md` | [current location](guides/OBSERVER_ACCEPTANCE.md) | Topic organization; links rebased |
| `EQUIPMENT_SELECTOR_VALIDATION.md` | [current location](gear/EQUIPMENT_SELECTOR_VALIDATION.md) | Topic organization; links rebased |
| `GEAR_REFERENCE_REVIEW.md` | [current location](gear/GEAR_REFERENCE_REVIEW.md) | Topic organization; links rebased |
| `PLAYER_SAVE_VERIFICATION.md` | [current location](gear/PLAYER_SAVE_VERIFICATION.md) | Topic organization; links rebased |
| `PRIVATE_INVENTORY_IMPORT.md` | [current location](gear/PRIVATE_INVENTORY_IMPORT.md) | Topic organization; links rebased |
| `SELECTOR_API_AUDIT.md` | [current location](gear/SELECTOR_API_AUDIT.md) | Topic organization; links rebased |
| `ROCKY_PLATEAU_15.md` | [current location](rocky/ROCKY_PLATEAU_15.md) | Topic organization; links rebased |
| `ROCKY_PLATEAU_RESEARCH.md` | [current location](rocky/ROCKY_PLATEAU_RESEARCH.md) | Topic organization; links rebased |
| `ROCKY_PLATEAU_CANDIDATE.md` | [current location](archive/ROCKY_PLATEAU_CANDIDATE.md) | Historical evidence; superseded status labeled |
| `ROCKY_PLATEAU_WORKING_PLAN.md` | [current location](archive/ROCKY_PLATEAU_WORKING_PLAN.md) | Historical evidence; superseded status labeled |
| `RESOURCE_POLICY.md` | [current location](archive/RESOURCE_POLICY.md) | Historical evidence; superseded status labeled |
| `BUG_HARVEST_RESERVED.md` | [current location](archive/BUG_HARVEST_RESERVED.md) | Historical evidence; superseded status labeled |
| `DEPLOYMENT_BASIC_20261029.md` | [current location](archive/DEPLOYMENT_BASIC_20261029.md) | Historical evidence; superseded status labeled |
| `DEPLOYMENT_BASIC_B2_20261029.md` | [current location](archive/DEPLOYMENT_BASIC_B2_20261029.md) | Historical evidence; superseded status labeled |
| `ROCKY_EQUIPMENT_CROSSWALK.md` | [current location](archive/ROCKY_EQUIPMENT_CROSSWALK_INITIAL.md) | Historical evidence; superseded status labeled |
| `ROCKY_PLATEAU_TEST_RESULTS.md` | [current location](archive/ROCKY_R1_TEST_RESULTS.md) | Historical evidence; superseded status labeled |
| `PASSIVE_STAR_STONE.md` | [current location](archive/PASSIVE_STAR_STONE_PS.md) | Historical evidence; superseded status labeled |

## Consolidated/current pages

- Root README now points to the index, candidate and live baseline; AGENTS uses current paths/scope without losing permanent rules.
- The index is navigation/status authority; architecture describes actual modules; roadmap is current gates rather than the old M0–M8 chronology.
- Knowledge retains native/evidence/community guidance; extracted milestone/data/build chronology is preserved in KNOWLEDGE_MILESTONES.
- Current baseline/test introductions replace several competing “current” revisions; their original text is in BASELINE_REVISION_NOTES.
- Current Star rules replace obsolete slot instructions; the complete original PS evidence is archived. Triskelion remains the slot-policy authority.
- Current Rocky crosswalk owns identity status, linking to the gear review for stats and R15 for selection. The old detailed matrix/campaign is preserved separately.
- R15 outcome ledger is separate from the original R1 ledger; no result was promoted.
- Old R15 and crosswalk root paths are link-only redirects for preserved private notes and earlier links, not duplicate guides.

## Remaining evidence limitations

- Active game script root remains unisolated; both maintained deployments exist.
- R15 native selectors/execution, ★15 survival/completion and observer correctness remain unverified. FastGenShl identity is owner-confirmed, not a new runtime test.
- Distinct screenshot shield profiles and exact save-record joins remain unresolved; immutable private crosswalk output retains superseded Compound hypotheses. Current crosswalk explicitly warns against using them.
- Archived documents intentionally retain obsolete commands, historical test counts and assumptions, under historical banners. Proposed future module paths in plans are not claimed to exist.
- External web URLs are retained, but reachability/content is not network-validated by local link checks.

## Validation

Validation completed: all 73 tests PASS (65 pre-existing tests plus 8 documentation-checker cases); Rocky source/import contracts PASS. The offline documentation checker reports zero errors. Final offline validation: 40 owned Markdown pages, 223 local links/anchors and 17 explicit documentation references checked, zero errors. All 99 external-link occurrences were retained without network fetching. All pre-existing non-Markdown project/tool/test/data/backup/deployment files match their pre-cleanup hashes, preserving the exact uncommitted R15 implementation. No script/test/tool path references needed updating because existing gameplay/tooling contains no literal Markdown paths.

All original fenced Markdown code blocks are checked for retention in the reorganized/current/archive corpus, allowing documentation-path rebasing. This preserves historical commands and examples without treating them as current authorization. External links are syntax-preserved only, not fetched. The Git index remains empty and HEAD/history unchanged. No in-game test follows from documentation validation.
