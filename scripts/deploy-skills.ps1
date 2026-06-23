<#
.SYNOPSIS
  Deploy capability family packages to Cursor or VS Code.

.DESCRIPTION
  Self-contained deploy script (no Python dependency).
  Deploy root resolves from: explicit -DeployRoot → *.code-workspace walk → repo root.
  Instructions are sourced from *.instructions.md and can be deployed to either IDE:
    - vscode: copied to .github/*.instructions.md
    - cursor: copied to .cursor/rules/*.mdc (extension renamed)

.PARAMETER ide
  Target IDE: cursor or vscode. Default: cursor.

.PARAMETER DeployRoot
  Explicit workspace root. When omitted: *.code-workspace file walk → repo root fallback.

.PARAMETER Force
  Accepted for backward compatibility (deploy always replaces).

.PARAMETER Package
  Qualified package name or "all" (default: all).
  Format: "<top>/<name>" for family packages (e.g. "practices/story-driven-delivery",
  "stages/discovery") or bare name for flat collections ("utilities", "others").

.PARAMETER SkipChecks
  Skip pre-deploy encoding and structure validation.
#>
param(
    [ValidateSet("cursor", "vscode")]
    [string] $ide = "cursor",

    [string] $DeployRoot = "",

    [string] $Package = "all",

    [switch] $Force,

    [switch] $SkipChecks,

    [switch] $Status
)

$ErrorActionPreference = 'Stop'

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot '..') | Select-Object -ExpandProperty Path

function New-Directory {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Remove-AndCopyDirectory {
    param(
        [string]$Source,
        [string]$Destination
    )
    if (Test-Path -LiteralPath $Destination) {
        try {
            Remove-Item -LiteralPath $Destination -Recurse -Force -ErrorAction Stop
        } catch {
            # Folder is locked (e.g. open in IDE) — fall back to file-by-file overwrite
            Write-Host "  ⚠️  Cannot remove '$Destination' (in use) — merging files instead."
            New-Directory -Path $Destination
            Copy-Item -Path (Join-Path $Source '*') -Destination $Destination -Recurse -Force -ErrorAction SilentlyContinue
            return
        }
    }
    New-Directory -Path (Split-Path -Parent $Destination)
    Copy-Item -LiteralPath $Source -Destination $Destination -Recurse -Force
}

function Merge-DirectoryContents {
    param(
        [string]$SourceDir,
        [string]$DestinationDir
    )
    if (-not (Test-Path -LiteralPath $SourceDir)) { return }
    New-Directory -Path $DestinationDir
    Copy-Item -Path (Join-Path $SourceDir '*') -Destination $DestinationDir -Recurse -Force -ErrorAction SilentlyContinue
}

function Get-WorkspaceDeployRootFromPwd {
    param([string]$StartPath)
    $current = Resolve-Path -LiteralPath $StartPath | Select-Object -ExpandProperty Path
    while ($true) {
        $ws = Get-ChildItem -LiteralPath $current -Filter '*.code-workspace' -File -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($ws) { return $current }
        $parent = Split-Path -Parent $current
        if (-not $parent -or $parent -eq $current) { break }
        $current = $parent
    }
    return $null
}

function Resolve-DeployRoot {
    param(
        [string]$ExplicitRoot,
        [string]$RepoRoot
    )
    if ($ExplicitRoot) {
        return (Resolve-Path -LiteralPath $ExplicitRoot | Select-Object -ExpandProperty Path)
    }
    $fromWorkspace = Get-WorkspaceDeployRootFromPwd -StartPath (Get-Location).Path
    if ($fromWorkspace) { return $fromWorkspace }
    return $RepoRoot
}

$script:KnownPackageFolders = [System.Collections.Generic.HashSet[string]]@(
    'skills','agents','content','reference','lib','instructions','prompts',
    'vscode','rules','scanners','templates','scripts','ide-files','inputs',
    'tests','test','catalog','retired'
)

function Get-PackageRoots {
    param([string]$RepoRoot)
    $roots = [System.Collections.Generic.List[pscustomobject]]::new()

    # Family packages: each subdir of these tops is a package root
    foreach ($top in @('practices', 'foundational', 'stages')) {
        $topPath = Join-Path $RepoRoot $top
        if (-not (Test-Path -LiteralPath $topPath)) { continue }
        Get-ChildItem -LiteralPath $topPath -Directory | ForEach-Object {
            $roots.Add([pscustomobject]@{ Name = "$top/$($_.Name)"; Value = $_.FullName })
        }
    }

    # Flat collections: the top-level dir itself is the package root;
    # each direct subdir with SKILL.md is deployed as an individual skill
    foreach ($flat in @('utilities', 'others')) {
        $p = Join-Path $RepoRoot $flat
        if (Test-Path -LiteralPath $p) {
            $roots.Add([pscustomobject]@{ Name = $flat; Value = $p })
        }
    }

    # common/ — shared reference folder; deploys whole directory to .cursor/skills/common/
    $commonPath = Join-Path $RepoRoot 'common'
    if (Test-Path -LiteralPath $commonPath) {
        $roots.Add([pscustomobject]@{ Name = 'common'; Value = $commonPath })
    }

    return ,$roots
}

function Merge-VscodeFiles {
    param(
        [string]$SourceDir,
        [string]$DeployRoot
    )
    $vscodeDst = Join-Path $DeployRoot '.vscode'
    New-Directory -Path $vscodeDst

    # Merge tasks.json — combine tasks[] and inputs[] arrays
    $srcTasks = Join-Path $SourceDir 'tasks.json'
    if (Test-Path -LiteralPath $srcTasks) {
        $dstTasks = Join-Path $vscodeDst 'tasks.json'
        $incoming = Get-Content -LiteralPath $srcTasks -Raw | ConvertFrom-Json
        if (Test-Path -LiteralPath $dstTasks) {
            $existing = Get-Content -LiteralPath $dstTasks -Raw | ConvertFrom-Json
            $merged = [pscustomobject]@{ version = "2.0.0" }
            $allTasks  = @($existing.tasks)  + @($incoming.tasks)  | Where-Object { $_ -ne $null }
            $allInputs = @($existing.inputs) + @($incoming.inputs) | Where-Object { $_ -ne $null }
            # dedupe by label / id
            $seenLabels = @{}; $allTasks  = $allTasks  | Where-Object { $l = $_.label;  if ($seenLabels[$l])  { $false } else { $seenLabels[$l]  = $true; $true } }
            $seenIds    = @{}; $allInputs = $allInputs | Where-Object { $i = $_.id;     if ($seenIds[$i])     { $false } else { $seenIds[$i]     = $true; $true } }
            Add-Member -InputObject $merged -NotePropertyName 'tasks'  -NotePropertyValue $allTasks
            if ($allInputs.Count -gt 0) {
                Add-Member -InputObject $merged -NotePropertyName 'inputs' -NotePropertyValue $allInputs
            }
            $merged | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $dstTasks -Encoding UTF8
        } else {
            Copy-Item -LiteralPath $srcTasks -Destination $dstTasks -Force
        }
    }

    # Merge settings.json — shallow key merge (incoming wins on conflict)
    $srcSettings = Join-Path $SourceDir 'settings.json'
    if (Test-Path -LiteralPath $srcSettings) {
        $dstSettings = Join-Path $vscodeDst 'settings.json'
        $incoming = Get-Content -LiteralPath $srcSettings -Raw | ConvertFrom-Json
        if (Test-Path -LiteralPath $dstSettings) {
            $existing = Get-Content -LiteralPath $dstSettings -Raw | ConvertFrom-Json
            $incoming.PSObject.Properties | ForEach-Object {
                if ($existing.PSObject.Properties[$_.Name]) {
                    $existing.PSObject.Properties[$_.Name].Value = $_.Value
                } else {
                    Add-Member -InputObject $existing -NotePropertyName $_.Name -NotePropertyValue $_.Value
                }
            }
            $existing | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $dstSettings -Encoding UTF8
        } else {
            Copy-Item -LiteralPath $srcSettings -Destination $dstSettings -Force
        }
    }
}

function Deploy-Package {
    param(
        [string]$PackageRoot,
        [string]$DeployRoot,
        [ValidateSet("cursor", "vscode")]
        [string]$Ide
    )
    $githubDst            = Join-Path $DeployRoot '.github'
    $githubInstructionsDst = Join-Path $githubDst 'instructions'
    $githubPromptsDst     = Join-Path $githubDst 'prompts'
    $githubSkillsDst      = Join-Path $githubDst 'skills'
    $githubAgentsDst      = Join-Path $githubDst 'agents'

    $cursorRoot   = Join-Path $DeployRoot '.cursor'
    $skillsDst    = Join-Path $cursorRoot 'skills'
    $agentsDst    = Join-Path $cursorRoot 'agents'
    $contentDst   = Join-Path $cursorRoot 'content'
    $referenceDst = Join-Path $cursorRoot 'reference'
    $libDst       = Join-Path $cursorRoot 'lib'
    $rulesDst     = Join-Path $cursorRoot 'rules'
    $commandsDst  = Join-Path $cursorRoot 'commands'

    # common/ — copy whole directory to .cursor/skills/common/
    # prompt/*.prompt.md also deploy to .cursor/commands/
    if ((Split-Path -Leaf $PackageRoot) -eq 'common') {
        if ($Ide -eq 'vscode') {
            Remove-AndCopyDirectory -Source $PackageRoot -Destination (Join-Path $githubSkillsDst 'common')
        } else {
            Remove-AndCopyDirectory -Source $PackageRoot -Destination (Join-Path $skillsDst 'common')
            $promptsSrc = Join-Path $PackageRoot 'prompt'
            if (Test-Path -LiteralPath $promptsSrc) {
                Get-ChildItem -LiteralPath $promptsSrc -Filter '*.prompt.md' -File | ForEach-Object {
                    New-Directory -Path $commandsDst
                    Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $commandsDst $_.Name) -Force
                }
            }
        }
        return
    }

    # Standard layout: skills/ subdirectory; supports one level of grouping (e.g. skills/supporting/)
    $skillsSrc = Join-Path $PackageRoot 'skills'
    if (Test-Path -LiteralPath $skillsSrc) {
        Get-ChildItem -LiteralPath $skillsSrc -Directory | ForEach-Object {
            $candidateDir = $_
            if (Test-Path -LiteralPath (Join-Path $candidateDir.FullName 'SKILL.md')) {
                if ($Ide -eq 'vscode') {
                    Remove-AndCopyDirectory -Source $candidateDir.FullName -Destination (Join-Path $githubSkillsDst $candidateDir.Name)
                } else {
                    Remove-AndCopyDirectory -Source $candidateDir.FullName -Destination (Join-Path $skillsDst $candidateDir.Name)
                }
            } else {
                # Grouping folder (e.g. supporting/) — recurse one level
                Get-ChildItem -LiteralPath $candidateDir.FullName -Directory | ForEach-Object {
                    $skillDir = $_
                    if (Test-Path -LiteralPath (Join-Path $skillDir.FullName 'SKILL.md')) {
                        if ($Ide -eq 'vscode') {
                            Remove-AndCopyDirectory -Source $skillDir.FullName -Destination (Join-Path $githubSkillsDst $skillDir.Name)
                        } else {
                            Remove-AndCopyDirectory -Source $skillDir.FullName -Destination (Join-Path $skillsDst $skillDir.Name)
                        }
                    }
                }
            }
        }
    }

    # Flat layout: skills live directly as subdirs of the package root (no skills/ wrapper).
    # Skip known infrastructure folder names.
    Get-ChildItem -LiteralPath $PackageRoot -Directory | ForEach-Object {
        $flatSkillDir = $_
        if ($flatSkillDir.Name -notin $script:KnownPackageFolders -and
            (Test-Path -LiteralPath (Join-Path $flatSkillDir.FullName 'SKILL.md'))) {
            if ($Ide -eq 'vscode') {
                Remove-AndCopyDirectory -Source $flatSkillDir.FullName -Destination (Join-Path $githubSkillsDst $flatSkillDir.Name)
            } else {
                Remove-AndCopyDirectory -Source $flatSkillDir.FullName -Destination (Join-Path $skillsDst $flatSkillDir.Name)
            }
        }
    }

    $agentsSrc = Join-Path $PackageRoot 'agents'
    if (Test-Path -LiteralPath $agentsSrc) {
        Get-ChildItem -LiteralPath $agentsSrc -Directory | ForEach-Object {
            $hasAgentDoc = (Test-Path -LiteralPath (Join-Path $_.FullName 'AGENT.md')) -or (Test-Path -LiteralPath (Join-Path $_.FullName 'AGENTS.md'))
            if ($hasAgentDoc) {
                if ($Ide -eq 'vscode') {
                    Remove-AndCopyDirectory -Source $_.FullName -Destination (Join-Path $githubAgentsDst $_.Name)
                } else {
                    Remove-AndCopyDirectory -Source $_.FullName -Destination (Join-Path $agentsDst $_.Name)
                }
            }
        }
    }

    if ($Ide -ne 'vscode') {
        Merge-DirectoryContents -SourceDir (Join-Path $PackageRoot 'content') -DestinationDir $contentDst
        Merge-DirectoryContents -SourceDir (Join-Path $PackageRoot 'reference') -DestinationDir $referenceDst

        $libSrc = Join-Path $PackageRoot 'lib'
        if (Test-Path -LiteralPath $libSrc) {
            Merge-DirectoryContents -SourceDir $libSrc -DestinationDir $libDst
        }
    }

    $instructionsSrc = Join-Path $PackageRoot 'instructions'
    if (Test-Path -LiteralPath $instructionsSrc) {
        Get-ChildItem -LiteralPath $instructionsSrc -Filter '*.instructions.md' -File | ForEach-Object {
            if ($Ide -eq 'vscode') {
                New-Directory -Path $githubInstructionsDst
                Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $githubInstructionsDst $_.Name) -Force
            } else {
                New-Directory -Path $rulesDst
                $base = $_.Name -replace '\.instructions\.md$', ''
                $destName = "$base.mdc"
                Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $rulesDst $destName) -Force
            }
        }
    }

    $promptsSrc = Join-Path $PackageRoot 'prompts'
    if (Test-Path -LiteralPath $promptsSrc) {
        Get-ChildItem -LiteralPath $promptsSrc -Filter '*.prompt.md' -File | ForEach-Object {
            if ($Ide -eq 'vscode') {
                New-Directory -Path $githubPromptsDst
                Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $githubPromptsDst $_.Name) -Force
            } else {
                New-Directory -Path $commandsDst
                Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $commandsDst $_.Name) -Force
            }
        }
    }

    $vscodeSrc = Join-Path $PackageRoot 'vscode'
    if (Test-Path -LiteralPath $vscodeSrc) {
        Merge-VscodeFiles -SourceDir $vscodeSrc -DeployRoot $DeployRoot
    }
}

# ── Pre-deploy validation ──────────────────────────────────────────────────

if (-not $SkipChecks) {
    Write-Host "Running pre-deploy checks..."
    $validationFailed = $false

    # Encoding scan
    try {
        & python3 "$RepoRoot/scripts/scan_encoding.py" --check 2>&1 | ForEach-Object { Write-Host $_ }
        if ($LASTEXITCODE -ne 0) { $validationFailed = $true }
    } catch {
        Write-Host "  ⚠️  Could not run encoding scan: $_"
    }

    # Deploy-path + structure test
    try {
        & python3 "$RepoRoot/tests/test_deploy_paths.py" 2>&1 | ForEach-Object { Write-Host $_ }
        if ($LASTEXITCODE -ne 0) { $validationFailed = $true }
    } catch {
        Write-Host "  ⚠️  Could not run deploy-path test: $_"
    }

    if ($validationFailed) {
        Write-Host ""
        throw "Pre-deploy checks failed. Fix issues above or pass -SkipChecks to deploy anyway."
    }
    Write-Host "✅ Pre-deploy checks passed."
    Write-Host ""
}

# ── Deploy ─────────────────────────────────────────────────────────────────

$resolvedDeployRoot = Resolve-DeployRoot -ExplicitRoot $DeployRoot -RepoRoot $RepoRoot

# Status check — compare source manifest with deployed receipt
Write-Host "Checking deploy status..."
try {
    $deltaJson = & python3 "$RepoRoot/scripts/generate_manifest.py" --deployed "$resolvedDeployRoot" 2>$null
    if ($deltaJson) {
        $delta = $deltaJson | ConvertFrom-Json
        switch ($delta.status) {
            "current" {
                Write-Host "✅ $($delta.message)"
                if ($Status) { exit 0 }
            }
            "outdated" {
                Write-Host "⚠️  $($delta.message)"
                if ($Status) { exit 0 }
            }
            "fresh" {
                Write-Host "🆕 $($delta.message)"
                if ($Status) { exit 0 }
            }
        }
    } else {
        Write-Host "🆕 No previous deploy found — full deploy."
        if ($Status) { exit 0 }
    }
} catch {
    Write-Host "  (no previous deploy info)"
    if ($Status) { exit 0 }
}
Write-Host ""

New-Directory -Path $resolvedDeployRoot

$packageRoots = Get-PackageRoots -RepoRoot $RepoRoot
if ($packageRoots.Count -eq 0) {
    throw "No package roots found under practices/, foundational/, stages/, utilities/, others/, or common/."
}

$selected = @()
if ($Package -eq 'all') {
    $selected = $packageRoots | Sort-Object Name
} else {
    $match = $packageRoots | Where-Object { $_.Name -eq $Package } | Select-Object -First 1
    if (-not $match) {
        $available = ($packageRoots | Sort-Object Name | ForEach-Object { $_.Name }) -join ', '
        throw "Unknown package '$Package'. Available: $available"
    }
    $selected = @($match)
}

foreach ($pkg in $selected) {
    Write-Host ("  Deploying package: {0}" -f $pkg.Name)
    Deploy-Package -PackageRoot $pkg.Value -DeployRoot $resolvedDeployRoot -Ide $ide
}

Write-Host ("Deploy complete. ide={0} package={1} root={2}" -f $ide, $Package, $resolvedDeployRoot)

# Write deploy receipt
try {
    & python3 "$RepoRoot/scripts/generate_manifest.py" --write-receipt "$resolvedDeployRoot" --ide $ide 2>$null
} catch {
    # Receipt writing is best-effort
}

# Build skill index
$skillIndexScript = Join-Path $resolvedDeployRoot ".cursor/skills/common/scripts/build_skill_index.py"
if (Test-Path -LiteralPath $skillIndexScript) {
    Write-Host "Building skill index..."
    try {
        & python $skillIndexScript 2>&1 | ForEach-Object { Write-Host "  $_" }
    } catch {
        Write-Host "  WARNING: Could not build skill index: $_"
    }
}
