# Passive Star Stone collection: current B2.1-TS policy

This is the current collection-policy reference; [Triskelion travel](TRISKELION_TRAVEL.md) owns movement and slot arbitration. The full earlier PS research/deployment record is [archived](archive/PASSIVE_STAR_STONE_PS.md), including original source links and historical slot descriptions.

Never farm, wait or detour for optional resources. Collection is subordinate to combat, boss/protected actions, mandatory progression and movement. No optional shovel harvesting is present. Preserve any tool interaction actually shown necessary to progress.

The existing shared `TryPassiveStar` path requires enabled configuration, cached Star availability, enabled/unpaused AI, clear ordinary walking, full HP, no targeted/reported nearby foe and no boss observed in the attempt. It observes the current `pickup` and exclusive distance threshold, not a pickup-instance list or event.

| Setting | Existing default / meaning |
|---|---|
| `passiveStarEnabled` | true; false disables this collection branch for comparison |
| `passiveStarDistance` | 10; exclusive trigger threshold, not a verified maximum attraction radius |
| `passiveStarHoldFrames` | 15; maximum opportunity budget, not a native attraction-duration requirement |
| `passiveStarCooldownFrames` | 90; project spacing between starts, not a native ability cooldown |

With eligible Triskelion travel, L stays Triskelion and R briefly becomes Star. Without eligible/available Triskelion, the existing fallback uses Star L + shield R. The pulse ends early on an unsafe condition or lost/out-of-range pickup; no waiting for drops. Only one bounded attempt occurs per observed presence window; a no-pickup frame reopens that window. Combat takes priority immediately; AI suspension issues no equipment command until resumed.

Official examples show equipped Star attraction without activation. They do not establish a universal range, carryover or enough hold time on this build. Existing queries and the empirical gates are documented in the [PS evidence record](archive/PASSIVE_STAR_STONE_PS.md) and [knowledge base](STONESCRIPT_KNOWLEDGE.md). Actual collection/movement benefit and completion effect remain unverified.

For game evaluation, compare collection off/on at the same build/difficulty/gear and Triskelion setting. Observe attraction, no combat interruption/oscillation and full-run time. Disable if it worsens reliability or time. Resource yield is never an acceptance metric. Current Rocky behavior remains scoped by [R15](rocky/ROCKY_PLATEAU_15.md), not by historical pickup-first community code.
