# Owner-reported basic automation results

> Scope: preserved B2/B2.1 baseline evidence. B2.1-TS is the live baseline; old trial rows remain unchanged. R15 results belong to the [separate ledger](../rocky/ROCKY_PLATEAU_TEST_RESULTS.md). No completion is promoted by documentation work.

Diagnostic revision: B2. Created 2026-10-29. **No basic-automation in-game completion has been reported.** Original observer loading/display verification remains separate (DEP-01 in OBSERVER_ACCEPTANCE.md).

Current correction candidate: B2.1. B2's equipment-module load failure is recorded below; no corrected-version completion or switching pass has been reported.

Keep one record per location/difficulty/config/trial; add rows rather than replacing failures. Use NOT RUN, BLOCKED, FAILED, ASSISTED COMPLETION, or OWNER-CONFIRMED UNASSISTED COMPLETION. A completion confirms that trial only; repeatability and higher difficulty remain unverified. Only update completion status after explicit owner confirmation.

| Location | Difficulty | Trial/build | Completion/outcome | Equipment issue | Failure/unexpected behavior | Owner confirmation/evidence |
|---|---|---|---|---|---|---|
| Rocky Plateau | Not supplied | B2 / game unknown | NOT RUN | Not tested | Not tested | None |
| Deadwood Canyon | Not supplied | B2 / game unknown | NOT RUN | Not tested | Not tested | None |
| Caves of Fear | Not supplied | B2 / game unknown | NOT RUN | Not tested | Not tested | None |
| Mushroom Forest | Not supplied | B2 / game unknown | NOT RUN | Not tested | Not tested | None |
| Haunted Halls | Not supplied | B2 / game unknown | NOT RUN | Not tested | Not tested | None |
| Boiling Mine | Not supplied | B2 / game unknown | NOT RUN | Not tested | Not tested | None |
| Icy Ridge | Not supplied | B2 / game unknown | NOT RUN | Not tested | Not tested | None |
| Temple | Not supplied | B2 / game unknown | NOT RUN | Not tested | Not tested | None |

## Trial record template

### B2 load failure / B2.1 retest pending

- Evidence: game log rejects `Catalog` line 125 with `Variable "Harvest" is reserved`; subsequent `gear` resolution/object errors follow. Earlier agent inspection also found the observer-only import initially active, then activated `SpeedRunBasic/main` and reproduced the module load error during a Rocky Plateau diagnostic run. No location completion was established.
- Functional outcome: B2 equipment automation blocked by module initialization failure, not a successful automated run. Exact owner trial difficulty/build was not supplied.
- Source correction: `EquipHarvestTool()` replaces the conflicting helper and call; no combat-policy changes.
- B2.1 status: static/deployment verification only; owner must retest catalog loading and actual equipment switching. Do not count this as a completion or silently replace the failed B2 evidence.

## Detailed trial template

Copy under a new dated trial heading or send in chat for recording:

```text
Date / trial ID / tester:
Location and difficulty / game build and platform:
B2 file hashes or deployment record / any config changes:
Mind Stone import and other active scripts:
Handler / strategy / request mode:
Missing core / unavailable elemental codes / unavailable base:
Requested and actual equipment (include enchantments if relevant):
Outcome / number of attempts / explicit owner completion confirmation:
Assistance: equipment, potion, pause, rescue, or none:
Failed encounter/phase / HP, armor, foe state/distance if available:
Exact Tab error / screenshot or video reference:
Unexpected behavior and reproduction steps:
Observed completion, last, count, loops before -> after:
Observer cases independently tested / pending:
```

Report the first shared defect before adjusting multiple settings. Preserve failed attempts in the record and cite the later fix/retest separately. For no overlay: verify B2 import, Mind Stone power, and exact native error before concluding the combat code is at fault.
