param(
  [Parameter(Mandatory=$true)][string]$CandidatesDirectory,
  [Parameter(Mandatory=$true)][string]$StonescriptRoot
)
$ErrorActionPreference = 'Stop'
function Get-SelectorFileDigest([string]$Path) {
  $stream = [IO.File]::OpenRead($Path)
  $algorithm = [Security.Cryptography.SHA256]::Create()
  try { return [BitConverter]::ToString($algorithm.ComputeHash($stream)) }
  finally { $stream.Dispose(); $algorithm.Dispose() }
}
$repo = Split-Path -Parent $PSScriptRoot
$privateRoot = [IO.Path]::GetFullPath((Join-Path $repo 'data/raw/player_save/selector_validation/v1'))
$candidateFile = (Resolve-Path -LiteralPath (Join-Path $CandidatesDirectory 'Candidates.txt')).Path
if (!$candidateFile.StartsWith($privateRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
  throw 'Use a generated private candidate directory.'
}
git -C $repo check-ignore -q -- $candidateFile
if ($LASTEXITCODE -ne 0) { throw 'Private candidates must be Git-ignored.' }
$candidateLines = @(Get-Content -LiteralPath $candidateFile)
if ($candidateLines.Count -ne 3 -or !$candidateLines[0].StartsWith('// PRIVATE') -or
    !$candidateLines[1].StartsWith('var selectors = ') -or !$candidateLines[2].StartsWith('var hands = ')) {
  throw 'Unexpected generated candidate structure.'
}
$selectors = @($candidateLines[1].Substring(16) | ConvertFrom-Json)
$hands = @($candidateLines[2].Substring(12) | ConvertFrom-Json)
if ($selectors.Count -eq 0 -or $selectors.Count -ne $hands.Count) { throw 'Candidate arrays inconsistent.' }
foreach ($selector in $selectors) {
  if ($selector -cnotmatch '^[A-Za-z0-9 *+\-]+$' -or ($selector.Split(' ').Count -gt 7)) {
    throw 'Unsafe selector text.'
  }
}
foreach ($hand in $hands) { if ($hand -notin @('L','R','auto')) { throw 'Unknown hand mode.' } }
$root = (Resolve-Path -LiteralPath $StonescriptRoot).Path
if (!(Test-Path -LiteralPath $root -PathType Container)) { throw 'Stonescript root must exist.' }
$target = Join-Path $root 'EquipmentSelectorTest'
$main = Join-Path $repo 'scripts/selector_validation/main.txt'
if (!(Select-String -LiteralPath $main -SimpleMatch 'var allowEquip = false' -Quiet)) {
  throw 'Installer requires count-only source. Arm tests manually after installation.'
}
if (Test-Path -LiteralPath $target) {
  if ((Get-Item -LiteralPath $target).Attributes -band [IO.FileAttributes]::ReparsePoint) {
    throw 'Refusing a redirected diagnostic namespace.'
  }
  foreach ($entry in Get-ChildItem -LiteralPath $target -Recurse -Force) {
    if ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) {
      throw 'Refusing redirected files inside the diagnostic namespace.'
    }
  }
  $backup = Join-Path $repo ('backups/selector-validation-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N'))
  New-Item -ItemType Directory -Path $backup | Out-Null
  Copy-Item -LiteralPath $target -Destination (Join-Path $backup 'EquipmentSelectorTest') -Recurse
  foreach ($file in Get-ChildItem -LiteralPath $target -File -Recurse) {
    $relative = $file.FullName.Substring($target.Length + 1)
    $copied = Join-Path (Join-Path $backup 'EquipmentSelectorTest') $relative
    if ((Get-SelectorFileDigest $file.FullName) -ne (Get-SelectorFileDigest $copied)) {
      throw 'Backup verification failed; deployment stopped.'
    }
  }
}
New-Item -ItemType Directory -Force -Path $target | Out-Null
foreach ($pair in @(@($main,'main.txt'), @($candidateFile,'Candidates.txt'))) {
  $destination = Join-Path $target $pair[1]
  Copy-Item -LiteralPath $pair[0] -Destination $destination
  if ((Get-SelectorFileDigest $pair[0]) -ne (Get-SelectorFileDigest $destination)) {
    throw 'Deployment hash mismatch.'
  }
}
Write-Output 'Installed count-only EquipmentSelectorTest; hashes match. Mind Stone and combat scripts unchanged.'
