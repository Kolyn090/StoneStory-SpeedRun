# Rocky Plateau ★15: first playable R15 candidate

Status: **experimental Perfected Mind Stone release authorized for local commit and supervised deployment; timing and native dodge behavior remain unverified**. Existing travel, Bearer recovery, elemental and armor rules are retained. The owner reached Perfected but has not completed ★15.

## Decisions

| Situation on normal Rocky ★15 | R15 request |
|---|---|
| Safe travel / unknown enemies | Existing shared Generic fallback, unchanged Triskelion/Star safety gates and no harvesting |
| Acronian Scout, no armor | Fire Sword + Rocky shield; Fire preference is explicit even if another elemental tag appears |
| Dysangelos Bearer, no armor | Fire Sword + Rocky shield |
| Elementalist, no armor | Counter Sword: Vigor foe → Poison; Æther → Vigor; Fire → Æther; Ice → Fire; Poison → Ice |
| Perfected, no armor | Keep last available, non-excluded elemental Sword; choose another allowed element when resistance changes |
| Recognized encounter with armor | Compatible allowed one-handed elemental Hammer + same shield. No Heavy Hammer or activation |
| Missing/dead/undamageable Dysangelos during transformation | Preserve the last combat weapon and Rocky shield; retain boss ownership, no travel fallthrough |
| Unknown phase/adaptive format or all elements excluded | Strict physical Sword fallback, if one native match; otherwise manual warning and shield-only request |
| Physical immunity | Existing compatible ranged exception, using cached elemental Wand + Rocky shield |
| No compatible weapon / conflicting immunities | Explicit manual warning; request shield only, leave L unchanged rather than invent a generic safe attack |
| Missing/ambiguous Rocky shield | Handled manual warning; no new equipment request. Generic cannot override it |

Other difficulties and routes retain the shared fallback; quests/unknown locations remain subject to the existing dispatcher. A manual warning does **not** pause native AI or make a dangerous encounter safe. Leave/disable the test manually if required. The new working-tree revision adds only Bearer recovery as described below; historical general healing remains off and potion policy remains off. There is no new defense timing, active sequence, dash, AAC or two-handed handling.

## Shield decision: owner-confirmed Towering nickname

The owner confirms **FastGenShl is their nickname for a Towering Shield** and can be used as an in-game name reference. The earlier Compound Shield inference was incorrect and is superseded. The preferred selector is now `FastGenShl`, with `fastGenShieldConfirmed = true`. This is owner-reported identity/name-reference evidence; this candidate's native count/equip execution is still untested.

The init-only inventory check accepts the nickname only when it matches exactly one native copy. If it matches zero or multiple copies, the documented fallback remains `towering shield +21`, also requiring exactly one copy. This is a **base-family fallback**, potentially matching the same renamed item; it does not prove a separate shield or identical stats. If both checks fail/are ambiguous, the existing handled warning sends no new equipment request.

Screenshot 0010's 35 armor, 1.75 armor/s and attacker Stun 1.4s stay associated with that displayed profile. Screenshot 0065's 14 armor, mitigation and movement penalty stay associated with its own profile. Do not merge or transfer those effects because the base family is shared. The exact normalized-save record linking the nickname and the reason for differing descriptions remain unresolved; private snapshots/crosswalk outputs and CSVs are preserved.

## Exact selector configuration and evidence limits

`scripts/rocky/config/RockySettings.txt` contains:

- Five elemental Swords: element + `sword -big +21`.
- Five one-handed elemental Hammers: element + `hammer -heavy +21`.
- Five elemental Wands for immunity exceptions: element + `wand +21`.
- Physical fallback: `stone sword -big +21`.
- Preferred shield (owner-confirmed nickname): `FastGenShl`.
- Base-family fallback: `towering shield +21`, if the nickname is missing/ambiguous.

The [official manual](https://stonestoryrpg.com/stonescript/manual.html) documents inventory-copy counts, `+N` enchantment criteria, exclusions, hand commands and native difficulty. These forms were reviewed against the current manual; no stars are inferred from raw saved upgrades.

The normalized snapshot contains one elemental short-sword/one-handed-hammer type profile per explicit element; the crosswalk supports the named shield candidates. Screenshot 0064 supports an enchanted displayed Stone Sword; the physical selector intentionally does not add `-socket`, since internal socketed/base-type naming does not establish the native exclusion behavior. Its native match remains a hypothesis. Wand family overlap likewise remains possible.

R15 queries these roles once at preparation and accepts **exactly one** native matching copy. Zero and multiple copies are both shown as missing/ambiguous; a count of one still does not prove the intended displayed item. That final identity must be inspected in the actual first run. No save IDs, signatures, raw enchantment codes or runtime CSV parsing are introduced. There is no new manual selector campaign: use the requested/actual overlay and inspect only a role that is actually selected; use an existing isolated probe only to diagnose a specific mismatch.

Selection retains R1's deterministic allowed-element order Fire, Ice, Vigor, Æther, Poison. This is fallback order, not a DPS ranking. If the requested Sword is unavailable/ambiguous, another allowed Sword is used. If an allowed Hammer is unavailable, it falls back to an allowed Sword with a visible warning, then the strict physical role where compatible. No missing family is silently relabeled as the intended element. Armor/damage-compatibility rules outrank the disabled-by-default healing swap.

## Architecture and checks

Only the four Rocky scripts change gameplay. The main route delegates once; `handled = true` prevents Generic from running afterward. Every specialized equipment path uses the existing `ApplyPair` executor with the cached Rocky shield. Missing-target/dead/undamageable transitions retain that pair; a transition before the first weapon request chooses a cached allowed Sword or physical fallback. State/phase logic and existing reset guards remain in place.

`RockyGear.Available` caches one-copy checks; no inventory scan is added to the frame loop. Diagnostics show R15, owner/encounter/phase/strategy, requested/live hands, strict missing/ambiguous families and shield fallback status. The limited Python source-policy evaluator is not the native Stonescript interpreter. Its targeted cases cover all five elemental counters, Scout/Bearer low-HP stability, armor priority, personalized shield preservation, ambiguous selectors, missing shield, target difficulty, no per-frame queries and exclusive ownership. The packager's import check now matches actual import/new statements, avoiding false dependencies from diagnostic text.

Historical first-playable checks: 65 automated synthetic/static tests PASS, including 23 Rocky cases; Rocky source/import contracts and the unchanged shared B2 static checker PASS. The prepared bundle matches current sources. Preservation was audited separately against the pre-implementation file hashes; only the intended Rocky/tool/test/documentation files may differ. No native interpreter or in-game testing has occurred.

## Installed bundle and supervised activation

Prepared offline bundle:

```text
artifacts/rocky-r1/e49bf6838459b6b1075a16341289ce36379351509c3a4262049519b6faecc60c/
  manifest.json
  SpeedRunRocky/
    main.txt
    config/RockySettings.txt
    equipment/RockyGear.txt
    locations/RockyPlateau.txt
```

The historical `rocky-r1` artifact parent is retained for packager compatibility; this manifest identifies R15. Earlier bundles/backups are preserved. Use this manifest for this candidate, not the older R1 digest in historical instructions.

Installation was explicitly authorized. The procedure is retained for reproducibility; file installation in steps 1–2 is complete, while the owner must perform steps 3–4 in-game:

1. Verify the manifest's existing `SpeedRunBasic/*` and `SpeedRun/metrics/RunMetrics.txt` dependencies against each current Stonescript root. Stop on mismatches; do not replace the working dependencies.
2. Back up/hash-check any existing `SpeedRunRocky` namespace. Copy only this bundle's four `SpeedRunRocky` files beside the working `SpeedRunBasic` folder in both maintained roots. Preserve unrelated files. Confirm source/deployed hashes against this manifest.
3. Save current Mind Stone text. Activate **only** `import SpeedRunRocky/main`; never combine it with B2.1 or the isolated selector validator.
4. Start a fresh normal Rocky Plateau **★15** run, supervised. Shared Triskelion behavior applies on eligible clear travel; the Rocky overlay identifies R15.

Deployment completed from committed source `afdbb34` using the manifest above. Four Rocky modules were installed into each maintained Steam/player-data Stonescript root (eight files total); all deployed SHA-256 hashes match source/bundle. All six shared/observer dependencies per root already matched and were not overwritten. All 607 pre-existing Stonescript files remain unchanged. No Mind Stone text or active save was read or edited. Loading, exact native equipment matches, ★15 survival/completion and timing remain NOT RUN.

Verified pre-install observer/basic backups, absent-candidate markers, before-file hashes and the deployment receipt are retained under `backups/r15-first-supervised-20261029-c031be557c0749cf852f1054dc2594d0/`. Prior backups are untouched.

Existing B2.1, observer and installed selector diagnostic remain untouched. Rollback: disable the candidate if needed, restore the saved Mind Stone text (normally only `import SpeedRunBasic/main`) and loadout, then start fresh. The existing B2.1 files remain available without restoration.

## Short in-game checklist — after authorized installation

1. **Load:** R15 header, normal Rocky ★15, readable diagnostics, no Tab errors. A different difficulty should show shared behavior, not a claimed R15 test.
2. **Travel and Scout:** eligible clear travel retains Triskelion. At Scout, request `fire sword -big +21` + `FastGenShl`. Inspect those displayed items once; report zero/multiple-match or incorrect details rather than accepting a generic similar name.
3. **Phases:** Bearer uses Fire; Elementalist switches when an observed element changes; Perfected avoids recognized adaptive elements. Record one wrong phase/selection with current foe/buff text if it occurs, rather than taking screenshots each frame.
4. **Armor and transformations:** an allowed one-handed Hammer replaces Sword when armor is present and restores after armor clears. Shield stays. Missing/dead/undamageable boss gaps must not request travel stones or let Generic override combat.
5. **Survival/completion:** report completed/failed/assisted, death or stall phase, minimum/end HP if visible, actual gear at failure, time metric and manual interventions. There is no calibrated major-attack avoidance; a ★15 death can identify the next required defense.

Record build/platform, exact ★15, fresh/loop, R15 bundle digest, nickname/fallback shield and native errors. Do not call a run fully automated if equipment/potion/rescue inputs were needed. One owner-confirmed completion establishes that trial only. No completion is currently recorded.

## First native load failure and minimal parser correction

The owner reported `Mindstone.main line 1: Incomplete parsing` with the correct Mind Stone text `import SpeedRunRocky/main`. The local game log identifies the underlying error: `SpeedRunRocky/main line 8: Variable "profile" is reserved`. Source/manifest hashes and every dependency resolved in both roots; the deployment copy/path was correct.

The uncommitted parser correction renames only that script variable and corresponding function parameters/references to `rockyConfig`. No equipment selectors or combat decisions change. The three changed Rocky modules are installed in both roots and match the corrected repository source; they therefore supersede the original committed bundle for this test. The original bundle remains historical and must not be reinstalled without the correction. Backups and before/after hashes: `backups/r15-reserved-profile-20261029-212432/`. B2.1 and the observer are unchanged.

The packager now rejects the known reserved identifier in candidate code, with a synthetic regression case. All 24 targeted tests pass; this is not a full native parser check or proof that other native errors cannot follow. Retry only `import SpeedRunRocky/main`, then report the first underlying module error if loading still fails. Post-fix native loading, equipment execution and completion remain unverified.

## Next candidate: post-Scout travel and Bearer recovery

**Installed for the second supervised test; uncommitted and not yet game-tested.** B2.1/observer remain unchanged. Use the new second-test bundle below; the original first-test manifest does not describe this revision.

- Scout no longer sets `combat.travelBossSeen`. Dysangelos still sets it, and missing/dead/undamageable boss transformation handling retains combat ownership. Generic is unchanged: Triskelion still requires no target, zero nearby enemies, walking, full HP, configured/enumerable Triskelion, enabled/unpaused AI and no latched boss. Injured post-Scout travel will still retain ordinary equipment; no healing, waiting or detour is added there.
- Normal Bearer remains Fire Sword + FastGenShl (or the existing guarded shield fallback). `bearerRecoveryEnabled = true` adds recovery at **HP <= 60%**, holds it between thresholds, and restores the normal decision at **HP >= 85%**. The configurable ratios must satisfy `0 < enter < exit <= 1`; invalid values disable this recovery decision with a diagnostic. These are project test thresholds, not established game mechanics or survival guarantees.
- The one-handed recovery selector is `vigor sword dL -big +21`, accepted only with one cached native match. The [manual](https://stonestoryrpg.com/stonescript/manual.html) demonstrates `vigor sword dL`; exclusion and enchantment criteria are documented. The owned Vigor Sword screenshot 0053 displays 18 damage / 108 DPS / range 5 and **109% chance to Lifesteal**. This is not a healing fraction. The new exact selector's native match and effective healing still require observation.
- Missing/ambiguous recovery gear leaves normal combat unchanged. Armor (including missing-hammer fallback), physical immunity/ranged exceptions, blocked Vigor, unknown-adaptive physical fallback, missing shield/core equipment, suspended AI and boss transitions outrank recovery. No inventory queries occur in the frame policy. Recovery state clears when interrupted/outside Bearer and on reset; after interruption, HP must meet the entry threshold again.
- Transformations retain the last combat pair, which may include the Vigor Sword. `Recovery:false` there means no new recovery decision is active, not that the held sword must instantly become Fire. No travel request is allowed during the latched boss gap.
- Optional overlay row 15 shows `Recovery:true/false`, reason and HP; strategy becomes `bearer-recovery-sword-shield` only when recovery is selected. Normal fallback, invalid thresholds and missing/ambiguous Vigor have explicit statuses. No new abilities, dodge timing or other-stage changes are introduced.

For the authorized second supervised test, test: (1) Scout defeated, no travel stone while threats remain or HP is below full; at full-HP clear walking, Triskelion returns; (2) Bearer starts with Fire + FastGenShl, switches only the sword at entry HP, remains in recovery through the middle band, returns to normal at exit HP; (3) armor/immunity overrides recovery and transformations keep combat ownership; (4) report actual Vigor identity, healing observed, sharp versus gradual HP loss, survival and reached phase. A lethal hit may still require a separate calibrated defense.

Validation for this working-tree revision: full automated suite **83 PASS**, including **33 Rocky tests**; Rocky source/import checks, unchanged B2 shared static checks, documentation link validation and `git diff --check` PASS. SHA-256 preservation audit: **638 protected files unchanged**, including both deployed Stonescript roots, shared scripts and gear/private data. These are synthetic/static and filesystem checks; the revised recovery/travel behavior has not run in-game.

## Second supervised test deployment

Authorized and installed on 2026-10-29 from the latest tested **uncommitted working-tree source**, retaining the reserved-name parser correction. Bundle: `artifacts/rocky-r1/ba5ee839d06738f95ed852bb1a01477bd7820e20133af1f7cb0c685d15cebf76/`. All 83 automated tests passed before preparation. Four Rocky files were backed up and replaced in each maintained Stonescript root; eight deployed SHA-256 hashes match the new manifest and repository source. Shared dependencies already matched and were not replaced. All 607 other existing root files are unchanged. No Mind Stone text, active save or combat logic was edited during installation.

Backup and receipt: `backups/r15-second-supervised-20261029-39c438ecbbc1/` (`before.json`, `receipt.json`, and previous four files per root). Older backups are preserved. An initial backup-check path-separator error stopped the first installation attempt before any target replacement; the check was corrected and the completed attempt passed verification.

Mind Stone: use only `import SpeedRunRocky/main`, then begin a fresh normal Rocky Plateau ★15 run. Confirm `Recovery` diagnostics appear. Test full-HP safe post-Scout Triskelion restoration and Bearer Vigor recovery at <=60% HP, holding until >=85%, while keeping the shield. Recovery missing/ambiguous status means normal combat fallback. Report actual gear, healing, death/completion and reached phase. Second-test gameplay results remain **NOT RUN**.

Rollback to B2.1: restore the saved Mind Stone text, normally only `import SpeedRunBasic/main`. To restore the prior R15 revision, copy the backup's four Rocky files from each root label back to its corresponding Stonescript root. Do not mix candidate revisions.

## Perfected ray timing diagnostic — not deployed

Only `scripts/rocky/main.txt` changes script behavior for this revision, adding observation and drawing only. All combat handlers, selectors, travel, Bearer recovery and equipment execution stay unchanged. No Mind Stone equip/activation, dodge, attack timer or defensive response is implemented.

With the existing `SpeedRunBasic` setting `showDiagnostics = true`, the top two overlay rows are replaced **only on Rocky at the configured ★15 difficulty with the Rocky profile enabled and a targeted Dysangelos phase3/Perfected**. Other overlay rows remain available. Turning diagnostics off stops trace observation/drawing; leaving Perfected discards the active trace and re-entry starts a new observation. No new imports, inventory checks, disk logging or growing history are introduced.

```text
R15 P3 *115* s:115 f:61 HP:100/100
Last:prev 32:89 -> 115:0 @2400 d:5
```

This is an illustrative display, not observed timing. `s` is `foe.state`; `f` is `foe.time`, native frames in that state. Normal Perfected is cyan, state 115 is red, and the immediately following observed state is yellow (`AFTER 115`). The last transition stays readable until another transition. It records the last sampled previous-state frame, the first sampled new-state frame and `totaltime` at that observation; it does not prove exact state duration, attack start or impact time. A decreasing timer in the same state is also shown as an observation boundary, not automatically a new attack. Color 115 never implies a confirmed safe dodge window. If the target disappears or ceases to be Perfected, the specialized banner stops.

Official support: the [manual](https://stonestoryrpg.com/stonescript/manual.html) documents `foe.state`, `foe.time`, `foe.distance`, HP, `totaltime`, variable persistence, advanced top-left printing and named colors. It does not map state 115 to a guaranteed pre-impact ray event. The diagnostic has not been parsed/rendered in-game yet; UI legibility and simulation/display sampling require testing.

### Future diagnostic deployment procedure

No installation is authorized by these instructions alone. After authorization:

1. Run `python -B -m unittest discover -s tests`, then `python -B tools/prepare_rocky_candidate.py --prepare` from the repository. Use the newly reported artifact/manifest, not either historical bundle above.
2. Verify the manifest's shared dependencies match both maintained Stonescript roots; stop on mismatches instead of replacing B2.1. Back up all four installed `SpeedRunRocky` files in each root and record hashes, preserving older backups.
3. Copy the new bundle's four Rocky files to the matching `SpeedRunRocky` namespace in each root. Verify SHA-256 against the manifest and latest source; verify unrelated files unchanged. No new dependency is required by the trace.
4. Keep Mind Stone as the single line `import SpeedRunRocky/main`; start a fresh normal ★15 run. Existing diagnostics default on. Roll back to the previous R15 using those four backed-up files, or use the preserved `import SpeedRunBasic/main` baseline.

### Recording procedure

- Record the actual running game build/platform and fresh-versus-loop. Keep the existing loadout/config and current travel/recovery behavior; do not add Chill, manual gear changes or a defensive action for this observation.
- Begin video before Perfected's ray windup (recording from entry into Perfected is easiest), with the upper-left overlay and boss animation visible. Capture continuously through the ray/HP loss and death screen. A 30 fps or higher recording is useful; video frames are not assumed to equal simulation frames.
- Report or share one short clip covering the windup and impact. We need the last readable `s/f` before HP loss, whether/when 115 begins relative to the visible windup, the transition out of 115 if reached, HP/distance, any stun/Chill or other modifiers, and manual interventions. The last readable overlay sample is not automatically the damage frame. Capture any native errors if the banner fails to appear.
- The ray may still kill the character: this version only observes. One clip can establish a candidate signal; reliable dodge calibration will need its own controlled test. No dodge implementation is authorized until the ★15 timing is reviewed.

Diagnostic revision checks: **88 automated tests PASS**, including five new trace tests; Rocky import/source checks, B2 static checks, documentation links and diff checks PASS. Preservation audit confirms all existing combat/config/equipment/tool/test files and both deployments unchanged; removing only trace additions reproduces the deployed main. Native parsing, colors/legibility and captured timing remain unverified.

## Perfected diagnostic deployment receipt

The diagnostic described in the earlier implementation section is now **installed for supervised testing**, not yet game-verified. Authorized deployment completed on 2026-10-29 from the uncommitted tested source. New bundle: `artifacts/rocky-r1/fd83389c293c664363cbe844c61fb02217be78ad782b0505cb6b6a7725dbe931/`. All 88 automated tests passed before installation.

All four R15 files were backed up in both roots and copied from the new bundle; eight deployed hashes match current source/manifest. Only main content differs from the previous deployment. Combat/config/equipment modules and all 607 unrelated root files remain unchanged; no shared dependency was replaced. Backup/receipt: `backups/r15-ray-diagnostic-20261029-d508b61d041e/`. All earlier backups are preserved. No deployment errors occurred.

Use only `import SpeedRunRocky/main` for a fresh normal ★15 run. Record Perfected entry through ray impact/death with the top-left trace and boss animation visible, plus running game version and modifiers. Display legibility, state-115 relationship to impact and all dodge timing remain unverified. No dodge is implemented. Rollback: restore the four backed-up Rocky files to each corresponding root, or use the preserved `import SpeedRunBasic/main` baseline.

## Experimental Perfected Mind Stone sequence — local only

**Not deployed. No backflip or ray avoidance has been verified.** The preceding diagnostic-only bundle remains installed. This revision adds one configurable, protected equip-only experiment for live Perfected in normal Rocky ★15; no other boss attack or stage gains a defensive response.

### Evidence and trial configuration

Owner-reported diagnostic capture: `foe.state = 115`, `foe.time = 23`, player HP **80/80**, distance **5**, Poison Sword + FastGenShl, boss HP **12,964/30,000**. Previous state 114 was reported as lasting 14 frames. If that value came from the trace's previous-state field, it is the last sampled frame rather than an independently measured complete duration. This establishes **alive at 115:23**, not the actual impact time, windup length, safe trigger or dodge duration.

`RockySettings.txt` adds:

| Setting | Initial value | Meaning |
|---|---:|---|
| `rayDodgeEnabled` | true | Enable only this experimental sequence; false retains ordinary combat |
| `rayDodgeTriggerFrame` | 23 | First observed state-115 frame at or above this threshold requests Mind Stone |
| `rayDodgeHoldFrames` | 30 | Frames from request until normal combat is recomputed |
| `rayDodgeTimeoutFrames` | 90 | Maximum armed wait; also a hard hold timeout |
| `mindStone` | `mind stone` | Native candidate accepted only with exactly one preparation-time match |

**23/30/90 are experimental project settings**, not a confirmed attack schedule. Frame 23 was selected as an observed alive sample, not copied from historical 60/79-frame leads. The 30-frame hold could end too early or cost unnecessary attack time. On a late first observation, the request occurs immediately if the threshold has passed. Invalid negative trigger, non-positive hold or timeout below hold disables that event with an unavailable diagnostic.

### Equipment ownership and restoration

The Rocky handler calls `TryPerfectedRay` after its existing core/AI/shield guards and before transition/ordinary weapon selection. An armed event continues normal combat until its trigger. Trigger/hold frames request **Mind Stone L + the cached Rocky shield R** (normally FastGenShl) through the existing `ApplyPair` executor and return handled immediately. Generic, recovery, armor and ordinary weapon requests cannot overwrite this pair in that frame. Holding maintains the same pair; it does not alternate gear or issue an `activate` command. `lastWeapon` and its element/kind remain the previous combat choice, never Mind Stone.

One request attempt is counted per observed state-115 event. Repeated frames, including the same timer value or a timer rollback while continuously in 115, do not rearm it. An observed departure from 115 permits a later event. Events are inferred from samples, not native unique attack IDs; an unobserved departure cannot be distinguished. A new event during an existing protected hold is not queued to interrupt that hold.

At the configured hold deadline or hard timeout, the helper releases ownership in that frame; ordinary Rocky selection then **recomputes** the current allowed element and armor/immunity choice. A target-free boss gap retains the protected pair only until the bounded deadline, then uses the existing last-combat transition hold. A confirmed phase change/dead target cancels the sequence; ordinary phase/transition handling resumes. AI suspension, missing core gear or missing shield cancels the protected hold with an unavailable reason. Reset/loop clears state. No automatic reapproach, dash, potion or timed second action is added.

### Availability, APIs and evidence limits

Mind Stone availability is cached once with existing one-copy criteria. Missing/ambiguous Mind Stone, positive cooldown or global ability prohibition consumes the event attempt opportunity and retains normal behavior; there is no repeated retry when cooldown later clears within the same event. There is no unvalidated shield substitution. The [official manual](https://stonestoryrpg.com/stonescript/manual.html) documents equipment requests, state/time, global `item.CanActivate()` and cooldown ID `mind`. It warns that cooldown **-1** can indicate invalid or unused abilities. With a uniquely matched candidate and the documented ID, this experiment allows one equip request at -1 but explicitly labels the cooldown **unused/unknown**, not proven ready.

Equip-only Mind avoidance is a community technique, inspected in [Cobblestone](https://github.com/alexbarker234/stonescript/blob/bd9ed98f5331e72bd2fbeb0b80546615316e4825/stonescript/Main.txt#L554) and [asHOH's dodge helper](https://github.com/asHOH/Stonescript-for-Stone-Story-RPG/blob/856875b08c7e27247efe4aeb2bbc697d1595091a/eq.txt). This is an original bounded integration, not a copied whole strategy. The current game must establish whether equipping this selector with FastGenShl retained causes a backflip, when the cooldown starts, whether repeated same-pair maintenance is harmless, whether the ray is avoided and when combat can safely resume. Global `CanActivate()` is only a conservative eligibility gate; it does not prove passive dodge success.

### Diagnostics and first future gameplay experiment

The existing recording trace is preserved. A compact top-row `Ray EXP` status and the detailed lower rows show **armed**, **triggered**, **holding**, **restored** or **unavailable**, attempt count, sampled cooldown, reason, request total-frame and hold deadline. `triggered` means **equip requested**, not confirmed backflip. It may last a single frame; a run first observing 115 at/above threshold may go directly to triggered without an armed display frame. `restored` means sequence ownership was released, not that a safe hit or correct exact gear instance was independently verified.

Do not deploy until separately authorized. For a future test, prepare a fresh bundle and follow the existing backup/dependency/hash procedure; preserve the currently working diagnostic bundle and both roots' prior files. Use only `import SpeedRunRocky/main` on a fresh ★15 run. Record from Perfected entry through ray and restoration with the state/frame trace, Ray EXP status, character and equipped hands visible.

The first trial must answer separately: (1) did exactly one attempt/backflip occur, at what state/frame; (2) did FastGenShl stay in R; (3) did the ray cause damage/death; (4) did ordinary equipment return after the hold with correct current element/armor handling; (5) any unavailable reason, repeated attempt or native error? Include build, effects/modifiers, distance, HP before/after and any intervention. Do not label a backflip alone as ray avoidance or one avoided ray as full-stage reliability.

Local experimental revision checks: **100 automated tests PASS**, including **45 Rocky policy/package cases and five trace cases**. Targeted cases cover entry/repeated115frames, once-per-observed-event, configurable timing, unavailable gear/cooldown, arm timeout and hold release, target gap/defeat, phase changes, shield/AI cancellation and recomputed element/armor restoration. Source/import checks, unchanged shared B2 static checks, documentation links and diff checks PASS. Preservation audit confirms both deployments and all shared/private/inventory tools and data unchanged; no staging/commit/push. Native parsing, actual backflip and avoided ray remain unverified.

## Authorized experimental release checkpoint

The owner explicitly authorized finalizing, locally committing and deploying the completed experimental sequence. No combat redesign or timing changes accompany this release. Earlier local-only/undeployed statements above describe implementation checkpoints; this section supersedes their authorization status. Deployment succeeds only after source/deployed hashes pass; its commit, bundle, backup and outcome are recorded in the ignored deployment receipt and reported to the owner. A verification failure requires restoring and verifying the backup.

The release includes the R15 parser correction, post-Scout travel fix, Bearer recovery and recording trace as necessary previously uncommitted prerequisites. The unrelated workflow-policy/general status edits are excluded. Private inputs, generated bundles and deployment backups are never committed. The first supervised dodge run must establish actual backflip, FastGenShl retention, ray avoidance and recomputed combat restoration separately; **23/30/90 timing remains experimental**. No in-game success is implied by committing/deploying this checkpoint.
