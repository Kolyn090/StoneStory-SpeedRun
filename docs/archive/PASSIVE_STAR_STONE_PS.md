# Passive Star Stone: B2.1-PS

> Historical record. Preserved behavior, timings, test counts and commands describe that development stage. This is not a current deployment or implementation guide. Start at the [documentation index](../README.md) and [current R15 guide](../rocky/ROCKY_PLATEAU_15.md).

Current B2.1-TS refinement: [TRISKELION_TRAVEL.md](../TRISKELION_TRAVEL.md) supersedes the slot and threat descriptions below. When Triskelion travel is active it stays in L and Star Stone temporarily uses R, replacing the shield rather than the movement stone. If Triskelion is disabled/unavailable, the old Star L + shield R fallback remains. The existing 15-frame/90-frame collection bounds and off switch remain; no timer delays Triskelion travel. Historical PS installation/rollback evidence below is preserved.

Owner policy (2026-10-29): no resource farming, optional shovel harvesting, collection detours or waiting. Resources remain incidental. Star Stone may attract already-nearby pickups as background ordinary travel, subordinate to survival, progression, combat, bosses, movement optimizations and protected equipment sequences. The importer, private inventories and isolated selector validator are unchanged.

## Verified sources versus unresolved mechanics

| Question | Evidence and boundary |
|---|---|
| Is equipping required? | [Official tutorial, section 7](https://stonestoryrpg.com/stonescript/) describes attraction while equipped and demonstrates left-hand equipment. Merely possessing it is not documented as sufficient for this effect. This does not describe its separate menu/unlock functions. |
| Is activation required? | Official examples use equip only. No `activate` is needed/issued for attraction; no Star Stone cooldown identifier is invented. Current potion opt-in remains unchanged. |
| Can the script detect resources? | [Manual, Game State](https://stonestoryrpg.com/stonescript/manual.html) documents `pickup`, `pickup.distance` and `pickup.z` for the currently targeted pickup. This is not an all-resources scan or a stable per-item ID. No assumed event API. |
| What is the effective range? | Official tutorial uses `<10`; manual example uses `<5`. These are trigger examples, **not a stated maximum radius**. Reviewed official material does not establish an exact maximum or item-level formula. Current candidate caps its trigger at 10; installed effective attraction distance still requires observation. |
| What do public scripts do? | [Cobblestone, PickupWhenClose](https://github.com/alexbarker234/stonescript/blob/main/Cobblestone.txt) uses `<10`, with different hand choices; [Scribble, progress](https://github.com/livercat/scribble/blob/master/scribble.txt) uses `<9`. Their constants are observations of implementations, not proof of range. No code or combat-overriding policy copied. |
| Does this conflict with equipment? | Yes: Star Stone occupies L instead of the travel sword. Shield remains R. It is an equipment change, not a free inventory passive. Same-frame command order matters: [manual Tips](https://stonestoryrpg.com/stonescript/manual.html) says later equip commands win. Whether swapping affects outstanding projectiles, armor/HP, attacks or movement needs game testing. |

No exact maximum is claimed. The implemented API forms are documented; selection/hold/retry policy is a project proposal, not in-game verified mechanics. If the observed pickup is not attracting at the configured distance, disable collection and report it rather than broadening the radius or waiting. The safe fallback is ordinary travel sword + shield. Native AI still owns movement; the script adds no detour/pause/leave command and cannot prove from source that native pickup targeting never changes its path.

## Exact decision and equipment flow

`Catalog.Prepare` checks `star stone` only at initialization/fresh entry and only if enabled. A miss adds optional `star` to Unavailable base, never Missing core. It does not read the private save or infer ownership from internal IDs. Restart manually after changing settings/inventory.

`Generic.Tick` retains all existing missing-gear, AI suspension and combat policies. Only its ordinary travel branch calls `TryPassiveStar`, before issuing either travel loadout. There is no later pickup override after combat commands. Quest/unknown routes remain observer-only. Future higher-priority handlers must bypass this ordinary-travel branch; no general sequence engine is introduced.

Collection requires all of:

- Feature enabled; selector available; positive distance/hold bounds and retry interval at least hold duration.
- No targeted foe and `foe.count = 0` (documented 46-unit scan), native AI enabled/unpaused, `ai.walking`, full HP, and no boss observed during this attempt.
- A targeted pickup with distance strictly below the configured threshold, which may not exceed 10.
- A fresh observed pickup-presence window and elapsed retry spacing, or the same still-eligible bounded pulse.

At pulse start, the policy requests **Star Stone L + existing shield R**, using the same single `gear.Apply` executor as normal travel. It returns before the travel sword request, so there is no sword/star alternation in the same frame. The executor continues issuing the same requested loadout during the pulse, as it already does for ordinary gear; this is not attack cancellation or intermediate swapping.

At default settings, the pulse lasts at most **15 simulation frames** (nominally 0.5 seconds). It ends earlier if movement stops, HP drops, an enemy is detected, pickup disappears/leaves the threshold, or the AI suspends. Ordinary travel restores sword/shield on the next permitted policy frame; combat selects its usual combat gear immediately when eligible. Suspended AI deliberately issues no equipment commands until resumed. After seeing a boss, collection remains blocked until the next fresh-entry/Ouroboros reset.

Only one pulse is attempted per observed presence window, with at least **90 simulation frames** (nominally 3 seconds) between starts. A new window requires a frame observing no targeted pickup; target changes without absence do not imply a new item/window. A timeout or unsafe interruption cannot retry the same presence window. Skipping some drops is intentional when safety/anti-thrashing guards apply. No loops enumerate drops or wait for collection to finish. Bounds use `totaltime`; Reset clears state on entry, loop and attachment using the existing lifecycle.

| Setting | Default | Meaning |
|---|---|---|
| `passiveStarEnabled` | `true` | Set `false` for the B2.1-NR-style benchmark baseline; no Star lookup/pickup polling from collection logic when off |
| `passiveStarDistance` | `10` | Exclusive trigger threshold; 0/negative or above 10 disables attempts, not a guessed attraction-radius formula |
| `passiveStarHoldFrames` | `15` | Maximum opportunity budget, not a verified time needed for attraction |
| `passiveStarCooldownFrames` | `90` | Minimum spacing between starts, not a native ability cooldown; must be at least hold duration |

Missing equipment, invalid bounds, a blocked condition or collection disabled falls back to ordinary travel. No optional shovel logic remains. No mandatory progression handler or native utility item is removed. The current code has no specialized mandatory-tool handler, so location-specific passage is still a test gate, not a blanket support claim.

## In-game test sequence and failure report

1. Start a fresh safe Rocky Plateau run with only `import SpeedRunBasic/main`. Expect **B2.1-PS**, no native errors (Tab), Missing core `none`. Do not manufacture pickups by enabling harvesting. If no loose pickups occur, use a comfortable Deadwood Canyon run or another naturally dropping encounter; report SKIPPED rather than claiming a pass.
2. With enabled settings, full HP, no enemies detected, no boss previously seen and walking, watch a natural pickup as its diagnostic distance crosses below 10. Expect `travel-star-passive`, Want L `star stone`, Want R your usual shield; compare Have L/R. Pickups should move toward the character without a manual activation. Record the observed distance and displayed Star Stone level, not raw upgrade values. The general Tab diagnostics can show pickup state/distance; no separate per-frame logging is added.
3. Confirm the same drop/window does not cause repeated sword/star oscillation after the maximum budget. A pulse may abort immediately if native AI stops walking. Note whether this prevents useful attraction. Leave unresolved resources behind as far as native AI permits; the script must not wait, mine or issue collection detours. Report any native path divergence.
4. Observe enemy appearance during collection: expect the regular combat loadout on the next eligible frame, never a collection override. Confirm low HP, AI suspension/stopped movement, boss encounter/post-boss period, unknown/quest routes and an unavailable Star selector do not trigger collection. Do not risk death to force a test. Missing Star can be checked with a temporary nonmatching selector only in a separate backed-up test copy; do not alter personal gear data.
5. Check fresh-entry, Ouroboros and boss sub-location transitions. A boss-seen latch intentionally suppresses post-boss chest attraction for this conservative version. Future protected sequences/movement handlers must explicitly exclude this policy; none currently exists to claim tested protection for.
6. Set `passiveStarEnabled = false` in both script-root Settings copies for paired baseline runs, then fresh-entry. Confirm no Star requests; compare completion time/failures against enabled runs with fixed build, difficulty, gear, potion policy and first-entry/loop conditions. Record several paired attempts and unresolved observer timing limits. If slower or less reliable, keep disabled. Resource yield is not the success metric.

Report `build; script revision; map/difficulty; Star Stone displayed level; enabled/distance/hold/retry settings; pickup distance; strategy; requested/actual hands; movement/HP/enemy state; pulse duration; attraction observed?; repeated swaps?; completion time/failure; Tab errors; manual interventions`. No save dumps or private identifiers. Do not call attraction radius, timing, completion safety or a speed gain verified until the owner supplies those results.

## Static validation and deployment

Completed 2026-10-29: backups of both B2.1-NR deployments were created and hash-verified **before gameplay edits** under `backups/pre-passive-star-20261029-5f1546e0/{steam-SpeedRunBasic,save-SpeedRunBasic}`. Existing live files were rechecked against those backups before replacement. All previous backups remain preserved. The existing namespace/import and observer dependency remain unchanged. No Mind Stone text, active save, private importer, selector validator or private inventory is modified.

All **28 Python tests passed**, including the off-switch configuration, rejected farming mutations, six broken safety/timeout/ownership mutations, unconditional Star lookup and invented pickup-ID/activation mutations. The existing checker passed before and after deployment. These are source contracts, not a Stonescript interpreter or actual attraction simulation; they cannot establish frame-level behavior.

Installed five modules in each existing Steam/save-folder SpeedRunBasic namespace; all **10 installed hashes match source**. **69 protected original files** remain byte-identical, including the dispatcher, observer, selector validator/importer, private files and old backups. Only the four intended basic gameplay files and their live copies changed, plus policy documentation and tests. No push or Mind Stone edit is part of installation.

All attraction, effective-range, pulse timing, restoration, movement, completion and benchmark cases remain **NOT RUN in-game**. To roll back, restore the five SpeedRunBasic modules from the corresponding pre-passive-star backup and start a fresh run; do not restore whole save folders. For a quick supervised benchmark baseline, set `passiveStarEnabled = false` consistently in both live Settings copies and start fresh; this does not alter inventory/importer/validator files.
