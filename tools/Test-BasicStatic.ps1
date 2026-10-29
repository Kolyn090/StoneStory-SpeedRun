param([string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot))
$ErrorActionPreference = 'Stop'
$basicRoot = Join-Path $ProjectRoot 'scripts\basic'
$scriptFiles = @(Get-ChildItem -LiteralPath $basicRoot -Recurse -File -Filter '*.txt')
if ($scriptFiles.Count -ne 5) { throw 'Expected five basic automation modules' }
$objects = @{}
foreach ($file in $scriptFiles) {
    $source = Get-Content -Raw -LiteralPath $file.FullName
    foreach ($line in ($source -split '\r?\n')) {
        if ($line -match "`t" -or ([regex]::Match($line, '^ *').Length % 2 -ne 0)) {
            throw "Indentation: $($file.Name): $line"
        }
    }
    # Delimiter lint only, not a Stonescript parser.
    $withoutComments = ($source -split '\r?\n' | Where-Object { $_ -notmatch '^\s*//' }) -join "`n"
    $withoutStrings = [regex]::Replace($withoutComments, '"[^"\r\n]*"', '""')
    foreach ($pair in @(@('(', ')'), @('[', ']'))) {
        $opening = ([regex]::Matches($withoutStrings, [regex]::Escape($pair[0]))).Count
        $closing = ([regex]::Matches($withoutStrings, [regex]::Escape($pair[1]))).Count
        if ($opening -ne $closing) { throw "Unbalanced delimiters: $($file.Name)" }
    }
    foreach ($reference in [regex]::Matches($source, 'var (\w+) = new ([\w/]+)')) {
        $module = $reference.Groups[2].Value
        if ($module.StartsWith('SpeedRunBasic/')) {
            $target = Join-Path $basicRoot ($module.Substring(14) + '.txt')
        } elseif ($module -eq 'SpeedRun/metrics/RunMetrics') {
            $target = Join-Path $ProjectRoot 'scripts\metrics\RunMetrics.txt'
        } else { throw "Unexpected module: $module" }
        if (-not (Test-Path -LiteralPath $target)) { throw "Unresolved module: $module" }
        $objects[$reference.Groups[1].Value] = Get-Content -Raw -LiteralPath $target
    }
}
# Check main's directly referenced project methods exist; native APIs excluded.
$main = Get-Content -Raw -LiteralPath (Join-Path $basicRoot 'main.txt')
foreach ($call in [regex]::Matches($main, '\b(\w+)\.(\w+)\(')) {
    $owner = $call.Groups[1].Value
    $method = $call.Groups[2].Value
    if ($objects.ContainsKey($owner) -and $objects[$owner] -notmatch ('func ' + $method + '\(')) {
        throw "Unresolved helper: $owner.$method"
    }
}
$combat = Get-Content -Raw -LiteralPath (Join-Path $basicRoot 'combat\Generic.txt')
$combat = ($combat -split '\r?\n' | Where-Object { $_ -notmatch '^\s*//' }) -join "`n"
$dispatcher = Get-Content -Raw -LiteralPath (Join-Path $basicRoot 'locations\Dispatcher.txt')
if ($combat -match 'item.GetCount|\bnew\b|\bbrew\b|activate (R|L)|storage\.') {
    throw 'Unexpected per-frame search/allocation/resource operation'
}
foreach ($route in @('rocky','deadwood','caves','mushroom','halls','mine','icy','temple')) {
    if ($dispatcher -notmatch ('loc = ' + $route + '\b')) { throw "Missing route: $route" }
}
$settings = Get-Content -Raw -LiteralPath (Join-Path $basicRoot 'config\Settings.txt')
if ($settings -notmatch 'var usePotion = false') { throw 'Potion must default off' }
if ($main -notmatch 'metrics.Observe\(\)' -or $main -notmatch 'func DrawTest\(\)' -or $main -notmatch 'gear.selectedShield') {
    throw 'B2 measurement/diagnostic contract missing'
}
if ($combat.IndexOf('gear.ClearRequest()') -lt 0 -or $combat.IndexOf('?gear.missing > 0') -lt 0 -or
    $combat.IndexOf('?settings.usePotion') -lt 0 -or
    $combat.IndexOf('gear.ClearRequest()') -gt $combat.IndexOf('?gear.missing > 0') -or
    $combat.IndexOf('?gear.missing > 0') -gt $combat.IndexOf('?settings.usePotion')) {
    throw 'B2 missing-gear guard ordering changed'
}
$catalog = Get-Content -Raw -LiteralPath (Join-Path $basicRoot 'equipment\Catalog.txt')
if ($catalog -match '(?im)^\s*func\s+Harvest\s*\(') { throw 'Harvest is a native reserved name; do not use as helper' }
if ($combat -match '\bharvest\b|\bshovel\b|EquipHarvestTool' -or
    $settings -match 'var (harvestEnabled|shovel)\b' -or
    $catalog -match '\bshovel\b|EquipHarvestTool') {
    throw 'Optional resource harvesting must not return to generic automation'
}
foreach ($field in @('missingCore','unavailableSwords','unavailableWands','unavailableHammers','unavailableBase','selectedShield','requestMode')) {
    if ($catalog -notmatch ('var ' + $field + '\b')) { throw "B2 audit field missing: $field" }
}
# Source contracts only: these do not simulate native pickup/equipment timing.
foreach ($contract in @(
    'func TryPassiveStar\(gear, settings\)',
    '\?!settings.passiveStarEnabled\s+starUntil = 0\s+return false',
    '\?travelBossSeen \| foe \| foe.count > 0 \| !ai.walking \| hp < maxhp',
    '\?settings.passiveStarDistance <= 0 \| settings.passiveStarDistance > 10',
    '\?settings.passiveStarHoldFrames <= 0',
    '\?settings.passiveStarCooldownFrames < settings.passiveStarHoldFrames',
    '\?pickup.distance >= settings.passiveStarDistance',
    '\?starWindowUsed \| totaltime < starNextFrame',
    'starWindowUsed = true',
    'starUntil = totaltime \+ settings.passiveStarHoldFrames',
    'starNextFrame = totaltime \+ settings.passiveStarCooldownFrames',
    '\?foe = boss\s+travelBossSeen = true',
    '\?!pickup\s+starWindowUsed = false\s+starUntil = 0',
    '\?TryPassiveStar\(gear, settings\)\s+\?useTriskelion\s+strategy = "travel-triskelion-star"\s+travelOffhand = gear.starStone\s+:\s+strategy = "travel-star-passive"\s+travelWeapon = gear.starStone\s+gear.ApplyPair\(travelWeapon, travelOffhand\)\s+return'
)) {
    if ($combat -notmatch $contract) { throw 'Passive Star safety/timeout/ownership contract missing' }
}
$travelHelper = [regex]::Match($combat, '(?s)func CanTravelWithTriskelion.*?(?=func TryPassiveStar)').Value
if ($travelHelper -notmatch '\?!settings.triskelionTravelEnabled \| string.Equals\(gear.triskelion, ""\)' -or
    $travelHelper -notmatch '\?travelBossSeen \| foe \| foe.count > 0 \| !ai.walking \| hp < maxhp\s+return false' -or
    $travelHelper -match 'totaltime|time\b|activate') {
    throw 'Travel safety/configuration contract missing or timed delay added'
}
foreach ($contract in @(
    '\?!foe\s+melee = false\s+strategy = "travel-shield"\s+\?foe.count > 0\s+starUntil = 0\s+strategy = "threat-ready-shield"\s+gear.Apply\(gear.defaultWand\)\s+return',
    'useTriskelion = CanTravelWithTriskelion\(gear, settings\)\s+\?useTriskelion\s+strategy = "travel-triskelion"\s+travelWeapon = gear.triskelion',
    '\?settings.passiveStarEnabled \| settings.triskelionTravelEnabled\s+\?foe = boss',
    '\?foe = immune_to_physical & foe = immune_to_ranged\s+strategy = "immunity-conflict-manual"\s+gear.Apply\(gear.defaultWand\)\s+return'
)) {
    if ($combat -notmatch $contract) { throw 'Travel threat/slot ownership contract missing' }
}
if ($catalog -notmatch '\?settings.triskelionTravelEnabled\s+triskelion = Find\("triskelion", "triskelion"\)' -or
    $catalog -notmatch 'func Apply\(weapon\)\s+ApplyPair\(weapon, shield\)' -or
    $catalog -notmatch 'func ApplyPair\(weapon, offhand\)' -or
    $catalog -notmatch 'selectedShield = offhand' -or $catalog -notmatch 'equipR @offhand@' -or
    $settings -notmatch 'var triskelionTravelEnabled = (true|false)' -or
    $combat -match 'foe.distance > 22|activate trisk|GetCooldown\("trisk' -or
    $main -notmatch 'player.framesPerMove') {
    throw 'Travel selector/executor/API/diagnostic contract invalid'
}
if ($catalog -notmatch '\?settings.passiveStarEnabled\s+starStone = Find\("star stone", "star stone"\)' -or
    $settings -notmatch 'var passiveStarEnabled = (true|false)' -or
    $combat -match 'activate star|GetCooldown\("star|pickup\.(id|count|GetCount)|loc\.Pause|loc\.Leave') {
    throw 'Passive Star API/configuration contract invalid'
}
'PASS: five modules; import/helper references; indentation/delimiters; eight routes; no per-frame inventory searches; potion defaults off.'
'PASS: B2 request/audit fields, measurement call, and missing-gear guard ordering.'
'PASS: no generic harvesting branch, shovel lookup/equip helper or collection setting; reserved Harvest guard retained.'
'PASS: passive Star guards, bounded window, cooldown, early return and optional cached lookup; no invented pickup API or Star activation.'
'PASS: optional Triskelion, no travel timer, early threat response, persistent L slot, single pair executor and movement diagnostic.'
'LIMIT: static lint only, not Stonescript parser execution or in-game testing.'
