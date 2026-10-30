# B2.1-TS baseline testing

This procedure tests the installed generic `SpeedRunBasic/main` baseline, not R15. All eight location-completion results remain NOT RUN. Use [R15's short checklist](../rocky/ROCKY_PLATEAU_15.md#short-in-game-checklist--after-authorized-installation) for the separate candidate after deployment authorization. Old B2/NR/PS introductions are preserved in [revision history](../archive/BASELINE_REVISION_NOTES.md).

## Deployment and minimal settings

Both live `SpeedRunBasic` roots must contain identical copies of `main.txt`, `config/Settings.txt`, `equipment/Catalog.txt`, `locations/Dispatcher.txt`, and `combat/Generic.txt`. Each root must also contain the existing `SpeedRun/metrics/RunMetrics.txt` dependency. The deployment verification record is [DEPLOYMENT_BASIC_B2_20261029.md](../archive/DEPLOYMENT_BASIC_B2_20261029.md).

Settings: `enabled = true`, `showDiagnostics = true`, `usePotion = false`; other combat thresholds are unchanged. No harvesting setting, automated brewing, resource refill, file logging, exception interception, or permanent storage is introduced. The `B2.1-TS` overlay header identifies the installed baseline.

Inventory audits run on initialization/fresh manual entry only. Their cached results are not refreshed after inventory changes until the next manual restart. Each visible frame prints a fixed twelve lines; with diagnostics off no diagnostic strings are built or rendered. No added per-frame inventory search or history array exists. Actual processing overhead is unmeasured.

## Read the display

| Display | Meaning / action |
|---|---|
| `B2.1-TS location *difficulty -> handler` | Actual `loc.id`, numeric difficulty, selected named route; report mismatches |
| Strategy / request mode | Decision currently taken; `none` means no equipment commands this frame. Current generic policy uses one-handed combat/travel requests; no harvest strategy |
| Want L/2H and Want R | Current-frame selectors, not guaranteed exact inventory items. No optional shovel request should appear |
| Have L / Have R | Native equipped-item descriptions. A blank left hand can be normal for two-handed gear |
| Missing core | Unavailable sword/wand/shield families after fallbacks. Any missing core item stops equipment/potion automation; native game AI still runs |
| Unavailable S/W/H | Preferred elemental selectors that found zero items, before fallbacks. Codes P=poison, V=vigor, A=aether, F=fire, I=ice; `-` means no preferred-selector misses in that family |
| Unavailable base | Missing configured default sword/wand/hammer/shield or optional heal selector. Shovel is no longer queried or reported. A base miss may have a fallback, so this alone is not a fatal error |
| Condition | Missing gear, conflicting immunities, unsupported location, disabled automation, or other project warning. `UNTESTED; Tab shows native errors` does not mean no native errors exist |
| Metrics | Existing entry/loop/attached tag, accumulated frames, captured completion, loops, last completion and count; their correctness remains unverified |

For example `S:PI` means the configured poison and ice sword selectors were unavailable; the policy will use available default swords for them. Read the actual selector strings in `config/Settings.txt`. Missing core is distinct from missing a preferred elemental option or an optional utility.

The script cannot catch or enumerate the game's parser/runtime errors through a documented error-query API. A parser/import error may prevent B2 from drawing at all. Use **Tab** on PC for recent Stonescript errors and copy the exact message; never interpret an absent overlay as successful execution.

## What to do in-game

1. Back up your current Mind Stone text. Replace the old entry import with exactly `import SpeedRunBasic/main`; do not run both entry points. Temporarily remove other equipment/potion scripts from the active text while preserving them in your backup.
2. Start **Rocky Plateau** manually at the lowest available difficulty you can comfortably survive. Do not change the deployment/settings while collecting a trial.
3. Confirm the header starts `B2`, handler is `rocky`, and Missing core is `none`. If not, pause/leave manually and report the display and any Tab error. Missing optional selectors alone need not block a supervised trial.
4. Pass the first optional boulder/tree: expect travel sword + shield, no shovel or harvest strategy. Then watch approach, ordinary combat, armor/crowds and boss transition. Record any stalled movement or object that actually requires a tool, including exact location, difficulty and rescue needed. Requested/actual gear should agree. Do not intentionally risk death to manufacture a low-HP test.
5. If safe, let the script finish without equipment/potion inputs. If you assist, record it as assisted even if the game awards completion. Report a death, stall, or manual rescue honestly; no boss workaround is required for this milestone.
6. Only if the first attempt is safe, allow two Ouroboros boundaries and observe three attempts total as an initial repeatability check. Capture completion/count before and after each boundary. Manually leave/re-enter once and check entry reset separately. A smoke test is not an all-difficulty reliability claim.
7. Report Rocky Plateau first. Shared selector/import/stale-request defects take priority; repeat Rocky after fixes before expanding. If Rocky fails only at a boss mechanic, record the limitation and proceed with supervised ordinary-combat testing on other maps if safe; do not falsely mark Rocky complete.

Use `import SpeedRun/main` and start manually to return to the unchanged observer. No restoration of full saves is needed. Native attacks/movement are not disabled by a project warning; use the game's pause/leave controls when needed.

## Eight-location sequence

Choose a comfortable low difficulty per map, record the exact value, and repeat the same observation sequence. The order is a practical test order, not an asserted unlock order. Mark locked/unavailable maps BLOCKED and continue accessible ones. Do not increase difficulty until basic behavior is understood.

| Order | Location / expected handler | Focus after import/gear checks | Status |
|---|---|---|---|
| 1 | Rocky Plateau / rocky | No optional shovel swap; passage past boulders; travel/combat transition; boss entry | NOT RUN |
| 2 | Deadwood Canyon / deadwood | Ranged/crowd choices; record reflection or root failures | NOT RUN |
| 3 | Caves of Fear / caves | Shielded approach, ordinary melee/ranged and boss positioning failures | NOT RUN |
| 4 | Mushroom Forest / mushroom | Crowd selection and armor; record explosion/phase failures | NOT RUN |
| 5 | Haunted Halls / halls | Physical-immunity magic choice and summoned crowds | NOT RUN |
| 6 | Boiling Mine / mine | Armored melee hammer choice; record explosion/Guardian failures | NOT RUN |
| 7 | Icy Ridge / icy | Elemental choices, wall/stall or snowball failures | NOT RUN |
| 8 | Temple / temple | Ordinary combat transitions, projectile/positioning failures | NOT RUN |

Use [BASIC_TEST_RESULTS.md](BASIC_TEST_RESULTS.md) for results. Only an explicit owner confirmation of actual completion can change a location/difficulty to completion-confirmed. An assisted completion, implementation, successful import, or positive observer score alone is insufficient to claim successful automation.

## Report back

For the first Rocky trial, send this short report (a screenshot at a problem point is useful):

```text
B2 / game version:
Rocky Plateau difficulty:
Handler / strategy:
Missing core / unavailable S,W,H / unavailable base:
Requested L/2H + R / actual L + R:
Outcome: completed unassisted / assisted / died / stalled / blocked
Where it failed or behaved unexpectedly (foe and phase if known):
Tab error text, or 'none observed':
Completion / last / count / loops before -> after, if tested:
Any manual equipment, potion, pause, or other script interference:
```

Do not report “works” as evidence for all locations/difficulties. The separate observer acceptance cases remain pending unless you explicitly test and report them.
