<#
.SYNOPSIS
  Deploy capability family packages to Cursor or VS Code.

.DESCRIPTION
  Thin wrapper around deploy_family_package.py.
  Deploy root auto-resolves from skill-config.json when -DeployRoot is omitted.

.PARAMETER ide
  Target IDE: cursor or vscode. Default: cursor.

.PARAMETER DeployRoot
  Explicit workspace root. When omitted: skill-config.json → *.code-workspace walk → repo root.

.PARAMETER Force
  Accepted for backward compatibility (deploy always replaces).

.PARAMETER Package
  Family package name or "all" (default: all).
#>
param(
    [ValidateSet("cursor", "vscode")]
    [string] $ide = "cursor",

    [string] $DeployRoot = "",

    [string] $Package = "all",

    [switch] $Force
)

$ErrorActionPreference = 'Stop'

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot '..') | Select-Object -ExpandProperty Path
$deployPy = Join-Path $RepoRoot 'scripts\deploy_family_package.py'
if (-not (Test-Path -LiteralPath $deployPy)) {
    throw "Missing $deployPy"
}

$args_ = @('--package', $Package, '--ide', $ide)
if ($DeployRoot) {
    $args_ += @('--to', $DeployRoot)
}

& python $deployPy @args_
if ($LASTEXITCODE -ne 0) {
    throw "deploy_family_package.py failed with exit code $LASTEXITCODE"
}
