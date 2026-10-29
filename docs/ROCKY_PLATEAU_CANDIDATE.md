# Rocky R1 candidate: not installed / not game verified

2026-10-29. Objective: reliable Rocky Plateau completion before tuning speed or other locations. This milestone prepares a separate `SpeedRunRocky/main` entry point. **No candidate has been installed into the game.** Preparation originally remained unstaged/uncommitted; the owner subsequently authorized local commits for review. Deployment still requires separate explicit authorization; nothing is pushed. The existing B2.1-TS and original observer remain unchanged. The pre-existing uncommitted research report is retained and extended.

## Files and architecture

| New file | Responsibility |
|---|---|
| `scripts/rocky/main.txt` | Same observer ordering, lifecycle preparation, exclusive Rocky/shared dispatch and optional diagnostics |
| `scripts/rocky/config/RockySettings.txt` | Enable switch, melee preference, basic healing preference, initial Scout/Bearer element and strict physical fallback selector |
| `scripts/rocky/equipment/RockyGear.txt` | Init-only strict elemental availability, allowed-element selection and honest missing-family fallback |
| `scripts/rocky/locations/RockyPlateau.txt` | Encounter/phase identification, boss-gap ownership, adaptive exclusion and phase policy |
| `tools/prepare_rocky_candidate.py` | Read-only checks and ignored immutable offline bundle; never installs or touches the Git index |
| `tests/stonescript_policy_harness.py`, `tests/test_rocky_candidate.py` | Limited test-only source evaluator and synthetic policy/ownership/packaging regression tests |

Shared `SpeedRunBasic/config/Settings`, `equipment/Catalog`, `combat/Generic`, `locations/Dispatcher` and original `SpeedRun/metrics/RunMetrics` are reused by reference, not edited or copied into gameplay forks. Ordinary encounters return unhandled before any gear request; shared combat runs once. Handled Scout/boss frames clear requests, apply existing missing-core/AI/potion safety, then use the shared one-handed executor once. Shared combat is skipped afterward. No extra observer import or duplicate per-frame observer call is added.

The candidate only calls Rocky specialization when the unchanged dispatcher allows the route and reports `rocky`. Other routes use shared automation unchanged; quests/unknown routes remain observer-only. Using this candidate on other locations is unnecessary for initial validation.

## Encounter and phase policy

| Observed case | Recognition / equipment |
|---|---|
| Ordinary foe / clear travel before boss | No Scout/Dysangelos match: return to unchanged shared combat/travel, including Triskelion and bounded Star behavior |
| Acronian Scout (user spelling Arconian) | Public `acronian_scout` criterion. Shielded melee by default; observed weakness when present, otherwise configurable fire preference; armor selects an allowed hammer first |
| Dysangelos Bearer | Documented `phase1`, otherwise community `dysangelos_bearer` identity. Prefer fire sword + shield by default; equipment availability and immunity take priority |
| Dysangelos Elementalist | `phase2`, otherwise `dysangelos_elementalist`. Five-element weakness mapping from research; warn on an unrecognized element rather than claiming a correct matchup |
| Dysangelos Perfected | `phase3`, otherwise `dysangelos_perfected`. Keep an allowed elemental choice stable while damage family stays unchanged; exclude recognized adaptive elements; hammer has priority over healing while armored |
| Missing target after Dysangelos | Retain boss ownership and last requested weapon + shield. Do not infer completion, a new phase number or clear travel from `!foe` |
| Undamageable or dead special target | Retain weapon/shield with a transition label. Numeric transformation states are shown diagnostically, not interpreted using community constants |
| Dysangelos with unknown phase | Handled physical fallback + visible warning; no guessed phase or travel fallback |
| Missing eligible selector / conflicting immunities | Explicit STOP/manual warning and shielded generic-wand fallback where necessary; this is a limitation requiring inspection, not successful support |

The encounter latch survives missing targets and does not reset just because a second `loc.begin` arrives while the candidate is already initialized. Fresh native script initialization, Ouroboros reset and attachment prepare/reset the candidate as documented in source. The observer's existing boundary ordering is preserved, including its still-unverified sub-location/timing behavior. Test these boundaries explicitly; a preserved observer does not establish correct timing.

All special handling sets the shared boss-seen flag and cancels its pickup budget, preserving B2.1-TS's conservative rule against travel stones after a boss/miniboss observation. A transformation gap cannot trigger Triskelion/Star requests. No mandatory progression interaction is removed and no native movement/pickup/utility system is globally disabled. There is still no specialized tool/progression handler to claim tested support for every obstacle.

## Equipment details and uncertainty

No personal selector candidates, raw upgrade values or inferred stars are integrated. Strict elemental candidates reuse the shared five-element sword/wand/hammer criteria, but cache each preferred selector separately **without** assigning a generic fallback to a supposedly known element. This avoids silently labelling a resisted fallback as safe. These remain broad selectors, not exact-instance confirmation or strongest-gear ranking. The right hand remains the existing shield throughout specialization.

Default elemental fallback order is fire, ice, vigor, aether, poison: a deterministic policy, **not a measured DPS ordering**. Fire for Scout/Bearer is community-informed and configurable. Melee is the default; `preferMelee = false` is an optional future range comparison. Physical immunity forces wand; ranged immunity forces melee; conflicting flags warn/manual. Armor chooses a one-handed hammer when using melee, otherwise the selected ranged family remains. Missing hammers fall back to an allowed sword with a visible fallback strategy. If no elemental choice is allowed, a cached `stone sword -big -socket` is the physical fallback where appropriate.

At low HP, a cached vigor `dL` sword may replace a non-armored melee choice, using the existing shared HP ratio, only when vigor is not excluded and adaptive parsing is understood. No active healing ability, brewing or potion persistence is added. The existing `usePotion` setting stays false unless independently opted in; handled frames honor its original simple guard once.

Adaptive handling uses the documented composite `foe.buffs.string` plus documented string APIs. It splits at colon/comma and matches complete community UID tokens `adaptive_defense_{poison,vigor,aether,fire,ice}`, without assuming an icon/field offset or converting duration text. Multiple recognized exclusions are supported. A changed string refreshes the bounded five-element mask; identical text reuses it. Duration updates can still invalidate this cache each frame: no measured CPU benefit is claimed.

An adaptive-looking token with unknown representation triggers physical fallback and a warning. If that cannot satisfy immunity/availability, the candidate reports a manual limitation instead of pretending an allowed item exists. Friendly labels, renamed/new effect UIDs, unreported resistances and native search behavior remain uncertainties. Supply the actual public foe-buff diagnostic when reporting a mismatch; never paste private save records.

## Intentionally not implemented

No hardcoded numeric boss-state schedule, timed dodge, AAC, Moondial cycling, quarterstaff/dash trick, summons, Mask/Bardiche/hammer activation or complex potion strategy. These require separate calibration. In particular, **reliable phase-3 survival is not established**; this shielded equipment candidate may still die or be stunned by attacks requiring avoidance. It is not an all-difficulty completion claim. A failure there should drive a narrowly tested defensive follow-up, not guessed source timers.

Community sources are the pinned original research references: [Rocky research](ROCKY_PLATEAU_RESEARCH.md), [asHOH Rocky](https://github.com/asHOH/Stonescript-for-Stone-Story-RPG/blob/856875b08c7e27247efe4aeb2bbc697d1595091a/00_rocky_plateau.txt), [Scribble phase/effect logic](https://github.com/livercat/scribble/blob/53ad8f0712d8373f999f97a22fcde0ff2f6b049f/scribble.dev.txt). This is a separately written implementation, not copied source; no upstream code or numeric timing constants are vendored. Native APIs were checked against the [official manual](https://stonestoryrpg.com/stonescript/manual.html). Community element preferences, UID spellings and exact current phase identities still require game observation.

## Checks and offline bundle

From the repository root, Python 3.10+ (substitute your Python executable if not on PATH):

```powershell
python -B tools/prepare_rocky_candidate.py
python -B -m unittest discover -s tests -p 'test_*.py' -v
python -B tools/prepare_rocky_candidate.py --prepare
```

The packager creates `artifacts/rocky-r1/<manifest-digest>/SpeedRunRocky/` plus `manifest.json`. Artifacts are Git-ignored. The digest derives from all four candidate files and six shared/baseline files. Only the four candidate modules are packaged for future copying; shared files must already match the manifest. Identical builds are no-op; differing/incomplete existing bundles are rejected, never overwritten. The tool never discovers game roots, reads saves, deploys files or runs staging/commit commands.

The test-only evaluator runs actual candidate function source against synthetic state. It models only the syntax subset used here; it cannot prove game parsing, real native searches, physical effects, frame scheduling, true variable lifetime or location reset behavior. These are **source-policy/static tests**, not in-game execution. Main dispatch, imports, reset guards and forbidden timer/equipment operations also have source checks. Use [ROCKY_PLATEAU_TEST_RESULTS.md](ROCKY_PLATEAU_TEST_RESULTS.md) for real results.

Final checks: **46 tests passed** (30 existing regressions and 16 candidate policy/source/bundle tests); the shared basic static checker and new source/import checks pass. No native interpreter or in-game execution was performed. Final prepared bundle: `artifacts/rocky-r1/34a7246830dcccb753b6972db488ec800d2b48a1f0ce125242aaa34dbdf53758/`. Its four candidate files match source; dependency hashes identify the unchanged B2.1-TS/observer baseline. Earlier immutable preparation output is retained but is not the finalized candidate. All game cases remain NOT RUN.

## Installation instructions — only after explicit deployment authorization

**Do not run these installation steps yet.** The current authorization is preparation only. Keep the existing live `SpeedRunBasic`/`SpeedRun` files intact. Verified backups of both B2.1-TS deployments were made before edits under `backups/pre-rocky-r1-20261029-8c0d59e2/{steam-SpeedRunBasic,save-SpeedRunBasic}`. Earlier backups are preserved.

After authorization, use the exact finalized bundle path recorded below. For **each** existing Stonescript root (the supplied Steam path and your existing save-folder Stonescript root), verify the shared/baseline hashes before copying anything. Do not update shared modules to force a mismatch to pass.

```powershell
$repo = 'E:\Projects\StoneStory-SpeedRun'
$bundle = Join-Path $repo 'artifacts\rocky-r1\34a7246830dcccb753b6972db488ec800d2b48a1f0ce125242aaa34dbdf53758'
$root = 'E:\Steam\steamapps\common\Stone Story RPG\Stone Story_Data\StreamingAssets\Stonescript'
# Repeat later for your existing save-folder Stonescript root; never use an active save file.
$manifest = Get-Content -LiteralPath (Join-Path $bundle 'manifest.json') -Raw | ConvertFrom-Json
foreach ($entry in $manifest.files.PSObject.Properties) {
  if (!$entry.Name.StartsWith('SpeedRunRocky/')) {
    $existing = Join-Path $root $entry.Name
    if (!(Test-Path -LiteralPath $existing) -or
        (Get-FileHash -LiteralPath $existing -Algorithm SHA256).Hash.ToLower() -ne $entry.Value) {
      throw 'Shared dependency differs. Stop; do not overwrite the working deployment.'
    }
  }
}
$destination = Join-Path $root 'SpeedRunRocky'
if (Test-Path -LiteralPath $destination) {
  $backup = Join-Path $repo ('backups/pre-rocky-install-' + [guid]::NewGuid().ToString('N'))
  New-Item -ItemType Directory -Path $backup | Out-Null
  Copy-Item -LiteralPath $destination -Destination (Join-Path $backup 'SpeedRunRocky') -Recurse
  foreach ($file in Get-ChildItem -LiteralPath $destination -File -Recurse) {
    $relative = $file.FullName.Substring($destination.Length + 1)
    if ((Get-FileHash -LiteralPath $file.FullName).Hash -ne
        (Get-FileHash -LiteralPath (Join-Path (Join-Path $backup 'SpeedRunRocky') $relative)).Hash) {
      throw 'Backup mismatch; stop before replacing files.'
    }
  }
}
$source = Join-Path $bundle 'SpeedRunRocky'
foreach ($file in Get-ChildItem -LiteralPath $source -File -Recurse) {
  $relative = $file.FullName.Substring($source.Length + 1)
  $target = Join-Path $destination $relative
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
  Copy-Item -LiteralPath $file.FullName -Destination $target
}
foreach ($entry in $manifest.files.PSObject.Properties) {
  if ((Get-FileHash -LiteralPath (Join-Path $root $entry.Name) -Algorithm SHA256).Hash.ToLower() -ne $entry.Value) {
    throw 'Installed/dependency hash mismatch; do not activate candidate.'
  }
}
```

Use the same bundle in both roots; do not nest it under an extra `rocky`/`SpeedRunRocky` directory. Preserve any existing namespace and unrelated files. After verifying both roots, back up your full current Mind Stone text yourself, then replace the active entry with only `import SpeedRunRocky/main`. Do not leave `SpeedRunBasic/main` or selector-validator imports active alongside it. Start a fresh manual run to initialize caches.

Rollback: turn Mind Stone off if unsafe, restore the original Mind Stone text (normally only `import SpeedRunBasic/main`) and start fresh. Existing B2.1-TS files are not replaced by this installation, so no shared file restoration is needed. Leave the candidate directory dormant; do not delete saves or restore entire save folders. If an older SpeedRunRocky namespace was replaced, its own verified backup can be restored independently.

## First supervised game test — after authorization/installation

1. Choose a comfortable low Rocky difficulty. Record actual build, difficulty and whether Scout/all phases are present. Expect header `Rocky R1 UNTESTED`, route rocky, Missing core none and no Tab errors. Stop on wrong gear or native errors.
2. During ordinary travel, expect Owner Rocky false and the unchanged shared Triskelion/Star policy. When Scout or Dysangelos appears expect Owner Rocky true, the encounter/phase label, a matching strategy and sword/hammer/wand L + shield R. Inspect Have L/R; selectors do not prove exact variants.
3. Observe phase changes and target gaps. Expect held weapon/shield and `transition-shield`, never travel stones during a latched boss gap. Check phase tags/aliases and raw buff text. Unknowns should warn, not silently label a tested phase/element.
4. Observe armor, adaptive resistance and naturally occurring low HP. Hammer takes priority over healing in melee; blocked elements must not be requested by specialization. An unknown adaptive format chooses physical fallback/warning. Stop on manual-limit messages; assisted outcomes are not automation passes.
5. Attempt completion only if safe. Report death/stun/armor stall/boss mechanic rather than improvising timers. If it completes, report the exact difficulty and whether any manual equipment, potion, movement or rescue input was used. Repeat safe loop/fresh-entry checks separately. No location status is marked successful until your explicit unassisted-completion confirmation.

Baseline and candidate timing/encounter fields are in the result template. Use an independent recorded timer/video until observer lifecycle/completion accuracy is accepted; no speed improvement is required for this reliability milestone.
