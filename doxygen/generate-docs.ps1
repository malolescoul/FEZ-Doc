param(
    [string]$DoxygenPath = 'doxygen'
)

$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    New-Item -ItemType Directory -Path 'logs' -Force | Out-Null
    & $DoxygenPath --version
    if ($LASTEXITCODE -ne 0) { throw 'Doxygen is not available.' }

    # Knowledge files remain the editable source; stable labels avoid filenames
    # derived from absolute machine paths in Doxygen's Markdown page generator.
    $guideSources = @(
        @('master', 'features/core-solver.md', 'fez_master_core_solver'),
        @('master', 'features/chns-assembly.md', 'fez_master_chns_assembly'),
        @('master', 'features/fsi-monolithic.md', 'fez_master_fsi_monolithic'),
        @('prod', 'features/chns-ale-amr.md', 'fez_prod_chns_ale_amr'),
        @('prod', 'patterns/distributed-state-transfer.md', 'fez_prod_distributed_state_transfer')
    )
    $utf8 = [System.Text.UTF8Encoding]::new($false)
    foreach ($guide in $guideSources) {
        $source = Join-Path '../knowledge' $guide[1]
        $destination = Join-Path ('guides/' + $guide[0]) $guide[1]
        $text = [System.IO.File]::ReadAllText((Resolve-Path -LiteralPath $source).Path)
        $firstHeading = [regex]::new('(?m)^(# .+?)(?:\r)?$')
        $text = $firstHeading.Replace($text, '$1 {#' + $guide[2] + '}', 1)
        [System.IO.File]::WriteAllText((Join-Path $PSScriptRoot $destination), $text, $utf8)
    }

    $outputRoot = [System.IO.Path]::GetFullPath($PSScriptRoot)
    foreach ($branch in @('master', 'prod')) {
        # These two folders contain only generated output. Validate the final
        # absolute path and reject reparse points before clearing stale pages.
        $target = [System.IO.Path]::GetFullPath((Join-Path $outputRoot $branch))
        if ([System.IO.Path]::GetDirectoryName($target) -ne $outputRoot -or
            [System.IO.Path]::GetFileName($target) -notin @('master', 'prod')) {
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
