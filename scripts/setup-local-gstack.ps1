$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $projectRoot
$env:PATH = (Join-Path $projectRoot '.tools/bun/node_modules/bun/bin') + ';' + $env:PATH
$env:GSTACK_STATE_ROOT = (Join-Path $projectRoot '.tools/gstack-state').Replace('\', '/')
$env:BUN_INSTALL_CACHE_DIR = (Join-Path $projectRoot '.tools/bun-cache').Replace('\', '/')
$env:npm_config_cache = (Join-Path $projectRoot '.tools/npm-cache').Replace('\', '/')
$env:PLAYWRIGHT_BROWSERS_PATH = (Join-Path $projectRoot '.tools/playwright').Replace('\', '/')
$setupPath = Join-Path $projectRoot '.agents/skills/gstack/setup'
# Upstream still uses the home state path for welcome markers and projects.
# Keep the upstream file intact; generate a separate project-only entrypoint.
$setupText = [System.IO.File]::ReadAllText($setupPath).Replace('$HOME/.gstack', '$GSTACK_STATE_ROOT')
[System.IO.File]::WriteAllText("$setupPath.project", $setupText, [System.Text.UTF8Encoding]::new($false))
$gitExe = (Get-Command git -CommandType Application).Source
$gitRoot = Split-Path (Split-Path $gitExe -Parent) -Parent
$gitBash = Join-Path $gitRoot 'bin/bash.exe'
$env:PATH = (Join-Path $gitRoot 'usr/bin') + ';' + $env:PATH
& $gitBash -l .agents/skills/gstack/setup.project --host codex --no-team --no-browser
$gstackSetupExit = $LASTEXITCODE
& (Join-Path $PSScriptRoot 'namespace-gstack-skills.ps1')
exit $gstackSetupExit
