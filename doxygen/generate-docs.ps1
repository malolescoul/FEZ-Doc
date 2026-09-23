param(
    [string]$DoxygenPath = 'doxygen',
    [string]$NodePath = 'node',
    [ValidateSet('master', 'prod', 'pre_amr')]
    [string[]]$Branches = @('master', 'prod', 'pre_amr')
)

$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    New-Item -ItemType Directory -Path 'logs' -Force | Out-Null
    $generatorVersion = & $DoxygenPath --version
    if ($LASTEXITCODE -ne 0) { throw 'Doxygen is not available.' }
    Write-Output $generatorVersion
    & $NodePath --version
    if ($LASTEXITCODE -ne 0) { throw 'Node.js is required for offline math rendering.' }

    # Knowledge files remain the editable source; stable labels avoid filenames
    # derived from absolute machine paths in Doxygen's Markdown page generator.
    $guideSources = @(
        @('master', 'features/core-solver.md', 'fez_master_core_solver'),
        @('master', 'features/chns-assembly.md', 'fez_master_chns_assembly'),
        @('master', 'features/fsi-monolithic.md', 'fez_master_fsi_monolithic'),
        @('prod', 'features/chns-ale-amr.md', 'fez_prod_chns_ale_amr'),
        @('prod', 'patterns/distributed-state-transfer.md', 'fez_prod_distributed_state_transfer'),
        @('pre_amr', 'features/workflow-pre-amr.md', 'fez_pre_amr_workflow'),
        @('pre_amr', 'features/chns-models-pre-amr.md', 'fez_pre_amr_models'),
        @('pre_amr', 'patterns/presolver-cache-geometry.md', 'fez_pre_amr_presolver'),
        @('pre_amr', 'patterns/mobility-corrections-timestep.md', 'fez_pre_amr_mobility')
    )
    $utf8 = [System.Text.UTF8Encoding]::new($false)
    foreach ($guide in $guideSources) {
        if ($guide[0] -notin $Branches) { continue }
        $source = Join-Path '../knowledge' $guide[1]
        $destination = Join-Path ('guides/' + $guide[0]) $guide[1]
        New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
        $text = [System.IO.File]::ReadAllText((Resolve-Path -LiteralPath $source).Path)
        $firstHeading = [regex]::new('(?m)^(# .+?)(?:\r)?$')
        $text = $firstHeading.Replace($text, '$1 {#' + $guide[2] + '}', 1)
        # Protect TeX commands such as \dot from Doxygen's command parser.
        # Only generated guide copies are transformed; knowledge is canonical.
        $text = $text.Replace('\(', '\f$').Replace('\)', '\f$')
        $text = $text.Replace('\[', '\f[').Replace('\]', '\f]')
        # References outside this Doxygen input need explicit local links.
        $text = $text.Replace('(../patterns/distributed-state-transfer.md)', '(../../prod/html/fez_prod_distributed_state_transfer.html)')
        $text = $text.Replace('(distributed-state-transfer.md)', '(../../prod/html/fez_prod_distributed_state_transfer.html)')
        $text = [regex]::Replace($text, '\[([^\]]+)\]\(\.\./\.\./pedagogie/([^\)]+)\)', '<a href="../../../pedagogie/$2">$1</a>')
        $text += "`n`n<span id=`"fez-guide-end-$($guide[2])`"></span>`n"
        [System.IO.File]::WriteAllText((Join-Path $PSScriptRoot $destination), $text, $utf8)
    }

    $outputRoot = [System.IO.Path]::GetFullPath($PSScriptRoot)
    foreach ($branch in $Branches) {
        # These folders contain only generated output. Validate the final
        # absolute path and reject reparse points before clearing stale pages.
        $target = [System.IO.Path]::GetFullPath((Join-Path $outputRoot $branch))
        if ([System.IO.Path]::GetDirectoryName($target) -ne $outputRoot -or
            [System.IO.Path]::GetFileName($target) -notin @('master', 'prod', 'pre_amr')) {
            throw ('Refusing to clean unexpected output path: ' + $target)
        }
        if (Test-Path -LiteralPath $target) {
            $item = Get-Item -LiteralPath $target -Force
            if (-not $item.PSIsContainer -or ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
                throw ('Refusing to clean a non-directory or reparse point: ' + $target)
            }
            Remove-Item -LiteralPath $target -Recurse -Force
        }
        & $DoxygenPath ('Doxyfile.' + $branch)
        if ($LASTEXITCODE -ne 0) { throw ('Doxygen failed for ' + $branch) }
        & $NodePath (Join-Path $PSScriptRoot 'render-math.mjs') $branch
        if ($LASTEXITCODE -ne 0) { throw ('Offline math rendering failed for ' + $branch) }
        $generation = [ordered]@{
            branch = $branch
            generatedAt = [DateTime]::UtcNow.ToString('o')
            doxygenVersion = "$generatorVersion"
            doxygenExitCode = 0
            mathRenderExitCode = 0
        }
        [System.IO.File]::WriteAllText((Join-Path $PSScriptRoot ('logs/' + $branch + '-generation.json')), ($generation | ConvertTo-Json), $utf8)
        $warningLog = Join-Path $PSScriptRoot ('logs/' + $branch + '-warnings.log')
        if (Test-Path -LiteralPath $warningLog) {
            $logText = [System.IO.File]::ReadAllText($warningLog)
            $logText = $logText.Replace($outputRoot.Replace('\', '/') + '/', '')
            [System.IO.File]::WriteAllText($warningLog, $logText, $utf8)
        }
        $entryPoint = Join-Path $branch 'html/index.html'
        if (-not (Test-Path -LiteralPath $entryPoint)) { throw ('Missing output: ' + $entryPoint) }
        Write-Output ('Generated: ' + $entryPoint)
    }
    & (Join-Path $PSScriptRoot 'fix-index-anchors.ps1')
}
finally {
    Pop-Location
}
