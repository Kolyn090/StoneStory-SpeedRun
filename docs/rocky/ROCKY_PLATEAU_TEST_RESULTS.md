# Rocky R15 acceptance and results

**`1c696fe` is the first owner-confirmed successful Rocky Plateau ★15 dual-wield + AAC baseline.** The owner confirms stage completion and resolution of the previous line-290 runtime error. See [the successful-run record](#successful-baseline-1c696fe) for approximate timing and evidence limits. [Current implementation/checklist](ROCKY_PLATEAU_15.md) remains authoritative for behavior; the [R1 ledger](../archive/ROCKY_R1_TEST_RESULTS.md) supplies no R15 passes.

Current evidence summary: completion is confirmed for the reported run, not a measured success rate or independent validation of every component. Earlier deployment notes and failed/NOT RUN entries below are historical checkpoints; they are preserved rather than retroactively marked successful.

| R15 case | Acceptance observation | Current result |
|---|---|---|
| LOAD | Current R15 executes without the previously reported native error | PASS, owner confirms `1c696fe` completion and runtime-error resolution |
| GEAR | Actual equipment and fallback match intended roles | Earlier Fire Sword + FastGenShl observed; completion does not independently verify every selector or variant |
| PHASES | Scout and boss phases handled through completion | Full stage completed; diagnostic recognition of each phase not separately verified |
| ARMOR | Compatible armor counter and restoration | Targeted armor-case validation remains NOT RUN |
| GAPS | Combat equipment retained through transformations | Completion confirmed; detailed ownership/transition trace not independently verified |
| SURVIVAL | Completion, deaths and interventions reported | Reported run completed; total attempts, death count and intervention details not supplied |
| COMPLETION | Owner confirms an actual ★15 completion; assistance details recorded separately | PASS: first owner-confirmed dual-wield + AAC baseline `1c696fe`; assistance details not supplied |
| LOOPS/TIMING | Boundary and timer accuracy checked independently | Informal timing comparison recorded below; loops, timer accuracy and multi-run reliability remain unverified |

One short record per attempt is enough:

```text
Build/platform; ★15; fresh/loop; bundle/config; requested/actual gear;
completed/failed/assisted; failure phase; deaths/interventions;
time + metric; shield/fallback status; native error or short note.
```

Keep failed attempts and unencountered cases explicit. Screenshot only a meaningful mismatch or failure; no per-frame campaign. Owner confirmation of the nickname is not confirmation that R15 loaded or completed. Store private inventory references in ignored local results, not this ledger.

## Historical deployment checkpoint

Filesystem deployment on 2026-10-29: committed source `afdbb34`, eight Rocky files verified in both maintained roots, dependencies preserved. This was filesystem evidence only; no native LOAD pass or in-game cases were confirmed at that checkpoint. The later owner-confirmed outcome is recorded separately above and in the successful-baseline entry.

## First supervised load attempt — FAIL

Owner reported Mind Stone line 1 `Incomplete parsing` while using `import SpeedRunRocky/main`. Game log identifies reserved variable `profile` in Rocky main line 8. Import failed before combat; no survival/completion result follows from this attempt. Minimal identifier-only correction is deployed with backup; corrected loading and all gameplay acceptance cases remain pending. See [parser correction](ROCKY_PLATEAU_15.md#first-native-load-failure-and-minimal-parser-correction).

## Owner-reported first gameplay trial — partial progress, failed run

Rocky Plateau ★15, after the parser correction: script ran, Scout was defeated, Triskelion was not restored afterward, and the character died against Dysangelos Bearer. The owner confirms Fire Sword + FastGenShl at death. Elementalist/Perfected were not reached. This verifies loading and the observed equipped pair for that trial; it does not establish all selector variants, HP thresholds, phase detection, timing accuracy or completion. Build, entry HP, damage/attack trace, time and intervention count were not supplied.

The repository-only follow-up fixes the Scout travel latch and adds Bearer recovery; **both retests are NOT RUN and the follow-up is not deployed**. Record post-Scout HP/threat/Triskelion behavior, recovery entry/hold/exit, actual Vigor Sword and shield, healing observed, armor/transition priority, and whether death is a sharp hit or gradual attrition. No successful ★15 completion is recorded.

## Second supervised candidate — installed, gameplay NOT RUN

Travel/recovery bundle `ba5ee839d06738f95ed852bb1a01477bd7820e20133af1f7cb0c685d15cebf76` installed with eight matching source/deployment hashes; 607 other game-script files unchanged. Prior R15 copies and receipt retained at `backups/r15-second-supervised-20261029-39c438ecbbc1/`. This is filesystem deployment evidence only. Post-Scout Triskelion, Vigor recovery/healing, Bearer survival and further phases remain pending owner testing.

## Second gameplay trial — reached Perfected, failed to ray

Owner-reported Rocky Plateau ★15: Scout, Bearer and Elementalist defeated; Perfected reached; its ray killed the character in one hit. Travel/Vigor changes appeared beneficial to the owner, but individual travel gates, healing amounts and thresholds were not separately measured. No full completion or reliable repeatability is established. Actual executable build, timing trace, modifiers and exact ray impact frame remain missing.

The new repository-only Perfected overlay is **NOT DEPLOYED / NOT RUN**. Its capture procedure is in [the R15 guide](ROCKY_PLATEAU_15.md#recording-procedure). Record build/platform, fresh/loop, clip with windup/impact and readable state/frame/transition rows, HP/distance, modifiers, interventions and native errors. State 115 remains a historical lead pending observation. No Mind Stone dodge has been implemented.

## Perfected diagnostic — installed, gameplay NOT RUN

Diagnostic bundle `fd83389c293c664363cbe844c61fb02217be78ad782b0505cb6b6a7725dbe931` installed in both roots after 88 tests passed. Eight deployed hashes match source; 607 unrelated files unchanged. Backup/receipt: `backups/r15-ray-diagnostic-20261029-d508b61d041e/`. No combat changes or dodge were deployed. Native banner display and state/time-to-ray correlation await the owner recording. Earlier undeployed labels describe the implementation checkpoint before this authorization.

## Owner diagnostic capture — alive at 115:23

At ★15: Perfected state115/time23, player HP80/80, distance5, Poison Sword + FastGenShl, boss12,964/30,000. Previous state114 reported14frames; distinguish last sampled frame from full duration if derived from overlay. This verifies a live observation in115; impact, safe trigger and dodge duration are unknown. The local experimental sequence is NOT DEPLOYED / NOT RUN. Future results must separately record equip request, actual backflip, shield retention, damage avoided, equipment restoration, repeated attempts/errors and full-run outcome.

## Owner report: one successful ray avoidance

The owner now confirms the shielded R15 experimental Mind Stone backflip avoided the lethal Perfected ray on one ★15 attempt. Full completion, repeatability and exact impact timing remain unconfirmed. The dual-wield/AAC candidate is authorized for a supervised release; native tests are NOT RUN. Record pair availability, recovery, per-hand AAC progress versus target loss, phase/armor choices, resource pauses, ray outcome, full-run completion/deaths and comparable timing before claiming an improvement.

## Dual-Vigor configuration gate

A second Vigor Sword may be crafted; none is assumed owned or independently equippable. Native two-copy allocation is NOT VERIFIED. The current candidate defaults to one Vigor + offense at recovery thresholds. A future confirmed two-copy configuration may opt into dual Vigor, including identical names, guarded by refreshed native counts and selector-overlap rules. Existing ray timing/body remain unchanged. At that checkpoint, no dual-wield/AAC clear-time improvement had been reported. The later approximate whole-strategy timing is recorded in [the successful baseline](#successful-baseline-1c696fe).

## Successful baseline: 1c696fe

**Owner report recorded 2026-10-30.** Implementation `1c696fe` on `main` successfully completed Rocky Plateau ★15. The previous `RockyPlateau` line-290 member-on-non-object runtime error is resolved in this gameplay report. The dual-wield + AAC implementation works well enough, as part of the complete R15 strategy, to finish the stage. This is the **first owner-confirmed successful ★15 dual-wield + AAC baseline**.

| Informal comparison | Owner-observed approximate value |
|---|---|
| Previous clear time | About 3 minutes; reference revision and matched conditions not supplied |
| `1c696fe` clear time | About 2 minutes |
| Approximate time saved | About 1 minute |
| Estimated reduction in clear time | About 33%, calculated as `(3 - 2) / 3` |

**Measurement limits:** these are owner-observed approximate timings, not formal multi-run benchmarks, exact frame measurements or an agent-run game test. One successful completion is explicitly confirmed; total attempt count, timing method/start-stop boundaries, exact earlier revision, build/platform, modifiers, loadout/flags, first-entry versus loop, deaths and manual interventions were not provided. Do not infer a completion percentage, precise mean/variance, repeatability, all-difficulty support or a guaranteed 33% improvement.

**AAC evidence boundary:** the complete dual-wield + AAC strategy finished this run and the owner observed a shorter overall clear time. This does not isolate AAC's contribution, establish per-hand attack throughput, prove every cancel preserved damage, or separate weapon/loadout, recovery, travel, defense and diagnostics effects. AAC-specific throughput and causal speed claims still require matched comparisons with AAC enabled/disabled. Duplicate Vigor allocation and detailed selector/timing checks retain their existing individual verification status.

Use `1c696fe` as the gameplay baseline for future comparisons. A lightweight next measurement should record a few repeat runs with the same difficulty, build, loadout and flags, consistent timing boundaries, completion/deaths/interventions and any errors. Keep R16/R17 experiments separate; this documentation milestone changes no scripts or deployments.
