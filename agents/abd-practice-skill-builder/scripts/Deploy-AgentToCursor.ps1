<#
.SYNOPSIS
  Junction-links an agent package folder into Cursor's user agents directory (~/.cursor/agents).

.DESCRIPTION
  Creates a Windows directory junction (not a symlink) so AGENTS.md, skill-config.json,
  scripts/, and nested skills/ appear under %USERPROFILE%\.cursor\agents\<AgentFolderName>\
  without copying the tree.

.PARAMETER AgentSourcePath
  Full path to the agent root (folder containing AGENTS.md). Default: parent of this script.

.PARAMETER CursorAgentsRoot
  Cursor user agents directory. Default: $env:USERPROFILE\.cursor\agents

.PARAMETER AgentFolderName
  Name of the folder under CursorAgentsRoot. Default: leaf name of AgentSourcePath.

.PARAMETER Force
  Remove an existing destination path before creating the junction.
#>
param(
    [string] $AgentSourcePath = "",

    [string] $CursorAgentsRoot = $(Join-Path $env:USERPROFILE '.cursor\agents'),

    [string] $AgentFolderName = "",

    [switch] $Force
)

$ErrorActionPreference = 'Stop'

if (-not $AgentSourcePath) {
    $AgentSourcePath = Join-Path $PSScriptRoot '..'
}

$source = (Resolve-Path -LiteralPath $AgentSourcePath).Path
$agentsMd = Join-Path $source 'AGENTS.md'
if (-not (Test-Path -LiteralPath $agentsMd -PathType Leaf)) {
    throw "Not an agent root (missing AGENTS.md): $source"
}

if (-not $AgentFolderName) {
    $AgentFolderName = Split-Path $source -Leaf
}

$dest = Join-Path $CursorAgentsRoot $AgentFolderName
if (Test-Path -LiteralPath $dest) {
    if (-not $Force) {
        throw "Already exists: $dest (use -Force to replace)"
    }
    Remove-Item -LiteralPath $dest -Recurse -Force
}

if (-not (Test-Path -LiteralPath $CursorAgentsRoot -PathType Container)) {
    New-Item -ItemType Directory -Path $CursorAgentsRoot -Force | Out-Null
}

New-Item -ItemType Junction -Path $dest -Target $source | Out-Null
Write-Host "Junction: $dest -> $source"
Write-Host "Open: $(Join-Path $dest 'AGENTS.md')"
