# Normalize two missing fragment targets in Doxygen 1.18 HTML indexes.
# Only generated HTML is changed; source snapshots and API text are untouched.
$ErrorActionPreference = 'Stop'
$utf8 = [System.Text.UTF8Encoding]::new($false)
foreach ($branch in @('master', 'prod')) {
    $htmlRoot = Join-Path $PSScriptRoot ($branch + '/html')
    $changedFiles = 0
    foreach ($page in Get-ChildItem -LiteralPath $htmlRoot -Filter '*.html' -File) {
        $original = [System.IO.File]::ReadAllText($page.FullName)
        $updated = $original.Replace('#index_~', '#index__7E')
        $letters = [regex]::Matches($updated, 'href="#index_([a-z])"') |
            ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
        foreach ($letter in $letters) {
            $anchor = 'index_' + $letter
            if ($updated -notmatch ('id="' + $anchor + '"')) {
                $pattern = [regex]::new('<li>(?=' + $letter + ')', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
                $updated = $pattern.Replace($updated, '<li id="' + $anchor + '">', 1)
            }
        }
        if ($updated -ne $original) {
            [System.IO.File]::WriteAllText($page.FullName, $updated, $utf8)
            $changedFiles++
        }
    }
    Write-Output ('Normalized HTML indexes for ' + $branch + ': ' + $changedFiles + ' files')
}
