# Keep gstack names distinct from Matt Pocock skills such as retro.
$namespaceProjectRoot = Split-Path $PSScriptRoot -Parent
$namespaceSkillsRoot = Join-Path $namespaceProjectRoot '.agents/skills'
foreach ($skillDirectory in (Get-ChildItem -LiteralPath $namespaceSkillsRoot -Directory -Filter 'gstack-*')) {
    $manifestPath = Join-Path $skillDirectory.FullName 'SKILL.md'
    if (Test-Path -LiteralPath $manifestPath) {
        $manifestText = [System.IO.File]::ReadAllText($manifestPath)
        $namePattern = [regex]::new('(?m)^name:[^\r\n]+')
        $manifestText = $namePattern.Replace($manifestText, ('name: ' + $skillDirectory.Name), 1)
        [System.IO.File]::WriteAllText($manifestPath, $manifestText, [System.Text.UTF8Encoding]::new($false))
    }
}
