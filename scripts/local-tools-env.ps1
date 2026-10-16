# Dot-source in the same PowerShell process before invoking project tools.
$projectToolsRoot = Split-Path $PSScriptRoot -Parent
$projectGitRoot = Split-Path (Split-Path (Get-Command git -CommandType Application).Source -Parent) -Parent
$env:PATH = (Join-Path $projectToolsRoot '.tools/bun/node_modules/bun/bin') + ';' + (Join-Path $projectGitRoot 'bin') + ';' + (Join-Path $projectGitRoot 'usr/bin') + ';' + $env:PATH
$env:GSTACK_STATE_ROOT = (Join-Path $projectToolsRoot '.tools/gstack-state').Replace('\', '/')
$env:BUN_INSTALL_CACHE_DIR = (Join-Path $projectToolsRoot '.tools/bun-cache').Replace('\', '/')
$env:npm_config_cache = (Join-Path $projectToolsRoot '.tools/npm-cache').Replace('\', '/')
$env:PLAYWRIGHT_BROWSERS_PATH = (Join-Path $projectToolsRoot '.tools/playwright').Replace('\', '/')
