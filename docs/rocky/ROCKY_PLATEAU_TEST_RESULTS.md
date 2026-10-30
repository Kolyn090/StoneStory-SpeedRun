# Rocky R15 acceptance and results

**R15 is committed locally and deployed for supervised testing; not yet verified in-game.** No ★15 automated completion is recorded. [Current checklist, selectors and bundle](ROCKY_PLATEAU_15.md) are authoritative; the [R1 test ledger](../archive/ROCKY_R1_TEST_RESULTS.md) is retained separately and supplies no R15 passes.

Filesystem deployment on 2026-10-29: committed source `afdbb34`, eight Rocky files verified in both maintained roots, dependencies preserved. This is not a native LOAD pass; all in-game cases below remain NOT RUN.

| R15 case | Acceptance observation | Result |
|---|---|---|
| LOAD | R15 overlay at normal Rocky ★15; no native import/parser errors | Owner confirms gameplay after parser correction; new revision NOT RUN |
| GEAR | Fire Sword and preferred FastGenShl nickname, or explicitly reported guarded fallback, match intended details | Fire Sword + FastGenShl confirmed at Bearer death; recovery NOT RUN |
| PHASES | Actual Scout/Bearer/Elementalist/Perfected cases correctly identified | NOT RUN |
| ARMOR | Compatible one-handed Hammer + shield; restoration when armor clears | NOT RUN |
| GAPS | Combat ownership/equipment preserved through transformation; no Generic/travel override | NOT RUN |
| SURVIVAL | Deaths, stalls, manual intervention and unsupported conditions recorded | FAIL: died against Bearer; later phases not reached |
| COMPLETION | Owner confirms an actual unassisted ★15 completion | NOT RUN |
| LOOPS/TIMING | Boundaries and timing independently checked before speed/reliability claims | NOT RUN |

One short record per attempt is enough:

```text
Build/platform; ★15; fresh/loop; bundle/config; requested/actual gear;
completed/failed/assisted; failure phase; deaths/interventions;
time + metric; shield/fallback status; native error or short note.
```

Keep failed attempts and unencountered cases explicit. Screenshot only a meaningful mismatch or failure; no per-frame campaign. Owner confirmation of the nickname is not confirmation that R15 loaded or completed. Store private inventory references in ignored local results, not this ledger.

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

A second Vigor Sword may be crafted; none is assumed owned or independently equippable. Native two-copy allocation is NOT VERIFIED. The current candidate defaults to one Vigor + offense at recovery thresholds. A future confirmed two-copy configuration may opt into dual Vigor, including identical names, guarded by refreshed native counts and selector-overlap rules. Existing ray timing/body remain unchanged. No dual-wield/AAC clear-time improvement is established.
