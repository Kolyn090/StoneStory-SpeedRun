# Rocky Plateau ★15: first playable R15 candidate

Status: **implemented and committed locally, undeployed, and not yet verified in-game**. Static/source checks have passed. Built on the existing R1 modules. No ★15 completion or exact native selector match is claimed. Review this candidate before authorizing installation.

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

Other difficulties and routes retain the shared fallback; quests/unknown locations remain subject to the existing dispatcher. A manual warning does **not** pause native AI or make a dangerous encounter safe. Leave/disable the test manually if required. No healing-weapon swaps are enabled by default; potion policy remains the shared default off. There is no new defense timing, active sequence, dash, AAC or two-handed handling.

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

Finalized checks: 65 automated synthetic/static tests PASS, including 23 Rocky cases; Rocky source/import contracts and the unchanged shared B2 static checker PASS. The prepared bundle matches current sources. Preservation was audited separately against the pre-implementation file hashes; only the intended Rocky/tool/test/documentation files may differ. No native interpreter or in-game testing has occurred.

## Review bundle and future activation — do not install yet

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

After separate explicit installation authorization:

1. Verify the manifest's existing `SpeedRunBasic/*` and `SpeedRun/metrics/RunMetrics.txt` dependencies against each current Stonescript root. Stop on mismatches; do not replace the working dependencies.
2. Back up/hash-check any existing `SpeedRunRocky` namespace. Copy only this bundle's four `SpeedRunRocky` files beside the working `SpeedRunBasic` folder in both maintained roots. Preserve unrelated files. Confirm source/deployed hashes against this manifest.
3. Save current Mind Stone text. Activate **only** `import SpeedRunRocky/main`; never combine it with B2.1 or the isolated selector validator.
4. Start a fresh normal Rocky Plateau **★15** run, supervised. Shared Triskelion behavior applies on eligible clear travel; the Rocky overlay identifies R15.

No step above was executed. Existing B2.1, observer and installed selector diagnostic remain untouched. Rollback after a future installation: disable the candidate if needed, restore the saved Mind Stone text (normally only `import SpeedRunBasic/main`) and loadout, then start fresh. The existing B2.1 files remain available without restoration.

## Short in-game checklist — after authorized installation

1. **Load:** R15 header, normal Rocky ★15, readable diagnostics, no Tab errors. A different difficulty should show shared behavior, not a claimed R15 test.
2. **Travel and Scout:** eligible clear travel retains Triskelion. At Scout, request `fire sword -big +21` + `FastGenShl`. Inspect those displayed items once; report zero/multiple-match or incorrect details rather than accepting a generic similar name.
3. **Phases:** Bearer uses Fire; Elementalist switches when an observed element changes; Perfected avoids recognized adaptive elements. Record one wrong phase/selection with current foe/buff text if it occurs, rather than taking screenshots each frame.
4. **Armor and transformations:** an allowed one-handed Hammer replaces Sword when armor is present and restores after armor clears. Shield stays. Missing/dead/undamageable boss gaps must not request travel stones or let Generic override combat.
5. **Survival/completion:** report completed/failed/assisted, death or stall phase, minimum/end HP if visible, actual gear at failure, time metric and manual interventions. There is no calibrated major-attack avoidance; a ★15 death can identify the next required defense.

Record build/platform, exact ★15, fresh/loop, R15 bundle digest, nickname/fallback shield and native errors. Do not call a run fully automated if equipment/potion/rescue inputs were needed. One owner-confirmed completion establishes that trial only. No completion is currently recorded.
