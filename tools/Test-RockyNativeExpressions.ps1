param([Parameter(Mandatory=$true)][string]$ManagedDirectory, [switch]$R16)
# Offline native LANGUAGE regression only. No Unity component, imports, storage,
# combat commands, primary save or live-process access. Never distribute game DLLs.
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$managed=(Resolve-Path -LiteralPath $ManagedDirectory).Path
[void][Reflection.Assembly]::LoadFrom((Join-Path $managed 'Antlr4.Runtime.Standard.dll'))
$assembly=[Reflection.Assembly]::LoadFrom((Join-Path $managed 'Assembly-CSharp.dll'))
$machineType=$assembly.GetType('Stonescript.Machine',$true)
$objectType=$assembly.GetType('StonescriptObject',$true)
$scriptRoot=Split-Path -Parent $PSScriptRoot
$lines=@(Get-Content -LiteralPath (Join-Path $scriptRoot 'scripts/rocky/locations/RockyPlateau.txt') |
    Where-Object {$_ -match '^  allowAAC = '})
if($lines.Count -ne 1){throw 'Expected exactly one current AAC gate'}
$gate=$lines[0].Trim()
$broken='allowAAC = rockyConfig.aacEnabled & equipment.pickedKind = "sword" & equipment.offhandKind = "sword" & !physicalOnly'

function Get-GateTree([string]$line){
    $inputText=[Antlr4.Runtime.AntlrInputStream]::new($line)
    $lexer=[Activator]::CreateInstance($assembly.GetType('Stonescript.Compiler.StonescriptLexer'),@($inputText))
    $tokens=[Antlr4.Runtime.CommonTokenStream]::new($lexer)
    $parser=[Activator]::CreateInstance($assembly.GetType('Stonescript.Compiler.StonescriptParser'),@($tokens))
    return $parser.program().ToStringTree($parser)
}

function Invoke-GateProbe([string]$line, [string]$configMode='valid',
    [string]$leftKind='sword', [string]$rightKind='sword',
    [bool]$physicalOnly=$false, [bool]$enabled=$true, [bool]$missingEquipment=$false){
    $config=[Activator]::CreateInstance($objectType)
    if($configMode -eq 'valid'){$config.Declare('aacEnabled',$enabled)}
    elseif($configMode -eq 'null'){$config=$null}
    elseif($configMode -eq 'scalar'){$config=$false}
    elseif($configMode -ne 'missing-aac'){throw 'Unknown fixture configuration'}
    $equipment=[Activator]::CreateInstance($objectType)
    $equipment.Declare('pickedKind',$leftKind)
    $equipment.Declare('offhandKind',$rightKind)
    if($missingEquipment){$equipment=$null}
    $source="func Probe(rockyConfig, equipment, physicalOnly)`n  var allowAAC`n  $line`n  return allowAAC"
    $machine=[Activator]::CreateInstance($machineType)
    $exe=$machine.Compile($source,'OfflineAACGateRegression',$true)
    if(!$exe){throw 'Synthetic native probe failed to compile'}
    $ctx=$machine.CreateExecutionContext()
    [void]$machine.Execute($exe,$ctx)
    $function=$exe.Target.GetFunction('Probe',$true)
    $arguments=[System.Collections.Generic.List[object]]::new()
    $arguments.Add($config);$arguments.Add($equipment);$arguments.Add($physicalOnly)
    $value=$machine.Execute($exe,$function,$arguments,$ctx)
    $errors=@($machine.Results | Where-Object {$_.type.ToString() -eq 'Error'} |
        ForEach-Object {$_.param})
    return [pscustomobject]@{Value=$value; Errors=$errors}
}

$checks=0
# The whole STATEMENT grammar, not expression() in isolation, exposes the bug.
$badTree=Get-GateTree $broken
if($badTree.StartsWith('(program (stmt (assignment (lvalue allowAAC) =')){
    throw 'Historical trap no longer reproduces in this engine; review fixture'
}
if(!$badTree.Contains('. offhandKind) =')){throw 'Historical member-assignment target changed'}
$checks++
$goodTree=Get-GateTree $gate
if(!$goodTree.StartsWith('(program (stmt (assignment (lvalue allowAAC) =')){
    throw 'AAC must assign a simple variable, not a member on an expression'
}
$checks++
foreach($enabled in @($true,$false)){
    $old=Invoke-GateProbe -line $broken -enabled $enabled
    if($old.Errors.Count -ne 1 -or $old.Errors[0] -notmatch 'Attempting to access member on a non-object'){
        throw 'Historical native runtime error did not reproduce with initialized objects'
    }
    $checks++
}
foreach($probe in @(
    @('sword','sword',$false,$true,$true),
    @('sword','sword',$false,$false,$false),
    @('sword','sword',$true,$true,$false),
    @('sword','shield',$false,$true,$false),
    @('hammer','hammer',$false,$true,$false),
    @('wand','wand',$false,$true,$false),
    @('physical-sword','shield',$true,$true,$false),
    @('sword','',$false,$true,$false),
    @('','sword',$false,$true,$false)
)){
    $result=Invoke-GateProbe -line $gate -leftKind $probe[0] -rightKind $probe[1] -physicalOnly $probe[2] -enabled $probe[3]
    if($result.Errors.Count -ne 0 -or $result.Value -isnot [bool] -or $result.Value -ne $probe[4]){
        throw "Native gate truth-table failure: $($probe -join ','); errors=$($result.Errors -join ';')"
    }
    $checks++
}
foreach($mode in @('null','scalar','missing-aac')){
    $result=Invoke-GateProbe -line $gate -configMode $mode
    if($result.Errors.Count -ne 1){throw "Invalid $mode config must fail explicitly, not silently disable AAC"}
    $checks++
}
$result=Invoke-GateProbe -line $gate -missingEquipment $true
if($result.Errors.Count -ne 1){throw 'Missing equipment object must fail explicitly'}
$checks++
Write-Output "PASS: $checks offline native parser/runtime checks; original bug reproduced, current source gate verified."
Write-Output 'LIMIT: synthetic language-only execution; no live combat, gear timing or completion test.'

if($R16){
    $syntaxChecks=0
    foreach($relative in @('scripts/rocky_r16/main.txt','scripts/rocky_r16/config/Experiments.txt',
                           'scripts/rocky_r16/combat/Experiments.txt','scripts/rocky/locations/RockyPlateau.txt')){
        $source=Get-Content -LiteralPath (Join-Path $scriptRoot $relative) -Raw
        # The standalone grammar has no game's native command registration step.
        # Check only these documented commands separately in source/policy tests;
        # substitute a simple assignment for grammar checking of the surrounding flow.
        $source=[regex]::Replace($source,'(?m)^(\s*)(equip @selector@|activate R|activate potion)\s*$', '$1r16CommandProbe = 0')
        $inputText=[Antlr4.Runtime.AntlrInputStream]::new($source)
        $lexer=[Activator]::CreateInstance($assembly.GetType('Stonescript.Compiler.StonescriptLexer'),@($inputText))
        $tokens=[Antlr4.Runtime.CommonTokenStream]::new($lexer)
        $parser=[Activator]::CreateInstance($assembly.GetType('Stonescript.Compiler.StonescriptParser'),@($tokens))
        [void]$parser.program()
        if($parser.NumberOfSyntaxErrors -ne 0){throw "Native R16 syntax errors in $relative"}
        $syntaxChecks++
    }
    # Execute only flag declarations; no action body, command, import or game state.
    $machine=[Activator]::CreateInstance($machineType)
    $source=Get-Content -LiteralPath (Join-Path $scriptRoot 'scripts/rocky_r16/config/Experiments.txt') -Raw
    $exe=$machine.Compile($source,'OfflineR16Defaults',$true)
    if(!$exe){throw 'Native R16 configuration compile failed'}
    [void]$machine.Execute($exe,$machine.CreateExecutionContext())
    if($machine.Results.Count -ne 0 -or $exe.Target.GetVariable('maskEnabled') -ne $false -or $exe.Target.GetVariable('dashEnabled') -ne $false){
        throw 'R16 native defaults must disable experiments'
    }
    Write-Output "PASS: $syntaxChecks R16 control-flow sources parsed (equip/activate excluded); disabled config executed offline. No gameplay actions executed."
}
