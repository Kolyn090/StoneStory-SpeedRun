# Rocky R15 acceptance and results

**R15 is implemented and committed locally, undeployed, and not yet verified in-game.** No ★15 automated completion is recorded. [Current checklist, selectors and bundle](ROCKY_PLATEAU_15.md) are authoritative; the [R1 test ledger](../archive/ROCKY_R1_TEST_RESULTS.md) is retained separately and supplies no R15 passes.

| R15 case | Acceptance observation | Result |
|---|---|---|
| LOAD | R15 overlay at normal Rocky ★15; no native import/parser errors | NOT RUN |
| GEAR | Fire Sword and preferred FastGenShl nickname, or explicitly reported guarded fallback, match intended details | NOT RUN |
| PHASES | Actual Scout/Bearer/Elementalist/Perfected cases correctly identified | NOT RUN |
| ARMOR | Compatible one-handed Hammer + shield; restoration when armor clears | NOT RUN |
| GAPS | Combat ownership/equipment preserved through transformation; no Generic/travel override | NOT RUN |
| SURVIVAL | Deaths, stalls, manual intervention and unsupported conditions recorded | NOT RUN |
| COMPLETION | Owner confirms an actual unassisted ★15 completion | NOT RUN |
| LOOPS/TIMING | Boundaries and timing independently checked before speed/reliability claims | NOT RUN |

One short record per attempt is enough:

```text
Build/platform; ★15; fresh/loop; bundle/config; requested/actual gear;
completed/failed/assisted; failure phase; deaths/interventions;
time + metric; shield/fallback status; native error or short note.
```

Keep failed attempts and unencountered cases explicit. Screenshot only a meaningful mismatch or failure; no per-frame campaign. Owner confirmation of the nickname is not confirmation that R15 loaded or completed. Store private inventory references in ignored local results, not this ledger.
