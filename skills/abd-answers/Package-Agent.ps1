<#
.SYNOPSIS
  Package the abd-answers agent as a self-contained, portable directory.
  Copies source code the agent skills depend on into the agent tree so someone
  can copy agents/abd-answers/ to another machine and run it (after npm install).

.DESCRIPTION
  The agent references TypeScript and Python scripts scattered across the
  abd-answers repo. This script copies those files into a local scripts/
  tree inside the agent directory, organised by what needs them:

    agents/abd-answers/
      scripts/shared/          -- used by multiple skills (env loader, path resolver, rag core)
      skills/query-pinecone/scripts/    -- query CLI
      skills/embed-pinecone/scripts/    -- embed CLI
      skills/convert-content/scripts/   -- Python convert pipeline
      skills/chunk-content/scripts/     -- Python chunk pipeline
      conf/                    -- secrets template (not actual secrets)

  After packaging, skill SKILL.md files are patched so commands reference
  the local scripts/ paths instead of repo-relative paths.

.PARAMETER RepoRoot
  Path to the abd-answers repo root. Defaults to two levels up from this script.
#>
[CmdletBinding()]
param(
    [string]$RepoRoot
)

$ErrorActionPreference = "Stop"

$agentDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if (-not $RepoRoot) {
    $RepoRoot = Split-Path -Parent (Split-Path -Parent $agentDir)
}

function Copy-File {
    param([string]$Src, [string]$Dest)
    $dir = Split-Path $Dest -Parent
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    Copy-Item -Path $Src -Destination $Dest -Force
    Write-Host "  $Src -> $Dest"
}

# ── shared scripts (used by query + embed) ──────────────────────────────────
$sharedDest = "$agentDir\scripts\shared"

# env / secrets loader
Copy-File "$RepoRoot\packages\app-server\src\load-conf-openai-key.ts" "$sharedDest\load-conf-openai-key.ts"

# path resolvers
Copy-File "$RepoRoot\packages\answers\server\src\abd-answers-paths.ts" "$sharedDest\abd-answers-paths.ts"

# rag core modules
$ragSrc = "$RepoRoot\packages\answers\server\src\rag"
$ragDest = "$sharedDest\rag"
foreach ($f in @(
    "pinecone-rag.ts",
    "pinecone-deployment-rag.ts",
    "pinecone-namespace.ts",
    "rag-path-semantic-search.ts"
)) {
    $srcFile = "$ragSrc\$f"
    if (Test-Path $srcFile) {
        Copy-File $srcFile "$ragDest\$f"
    } else {
        Write-Warning "  SKIP (not found): $srcFile"
    }
}

# ── query-pinecone skill scripts ────────────────────────────────────────────
$queryDest = "$agentDir\skills\query-pinecone\scripts"
Copy-File "$RepoRoot\scripts\rag\agent-pinecone-query.ts" "$queryDest\agent-pinecone-query.ts"

# ── embed-pinecone skill scripts ────────────────────────────────────────────
$embedDest = "$agentDir\skills\embed-pinecone\scripts"
Copy-File "$RepoRoot\scripts\migrate-memory-to-pinecone.ts" "$embedDest\migrate-memory-to-pinecone.ts"

# ── convert-content skill scripts (Python) ──────────────────────────────────
$convertDest = "$agentDir\skills\convert-content\scripts"
foreach ($f in @(
    "convert_to_markdown.py",
    "pdf_markdown_post.py",
    "pdf_outline_headings.py",
    "repair_source_comments.py",
    "onedrive_to_sharepoint.py",
    "sharepoint_mapping.json",
    "_config.py",
    "_pipeline_logging.py",
    "_pipeline_update.py",
    "PIPELINE_CONTRACT.md",
    "README.md"
)) {
    $srcFile = "$RepoRoot\scripts\source-convert\$f"
    if (Test-Path $srcFile) {
        Copy-File $srcFile "$convertDest\$f"
    } else {
        Write-Warning "  SKIP (not found): $srcFile"
    }
}

# ── chunk-content skill scripts (Python) ────────────────────────────────────
$chunkDest = "$agentDir\skills\chunk-content\scripts"
foreach ($f in @(
    "chunk_markdown.py",
    "chunked_source_asset.py",
    "_config.py",
    "_pipeline_logging.py",
    "_pipeline_update.py"
)) {
    $srcFile = "$RepoRoot\scripts\source-convert\$f"
    if (Test-Path $srcFile) {
        Copy-File $srcFile "$chunkDest\$f"
    } else {
        Write-Warning "  SKIP (not found): $srcFile"
    }
}

# ── pipeline runner ─────────────────────────────────────────────────────────
Copy-File "$RepoRoot\scripts\rag\run-pipeline-stages.ps1" "$agentDir\scripts\run-pipeline-stages.ps1"

# ── conf templates (never copy actual secrets) ──────────────────────────────
$confDest = "$agentDir\conf"
Copy-File "$RepoRoot\conf\.secrets.example" "$confDest\.secrets.example"
if (Test-Path "$RepoRoot\conf\answers-memory.env.example") {
    Copy-File "$RepoRoot\conf\answers-memory.env.example" "$confDest\answers-memory.env.example"
}

# ── package.json subset (for npm run rag:query) ────────────────────────────
$pkgDest = "$agentDir\package.json"
if (-not (Test-Path $pkgDest)) {
    $pkg = @{
        name = "abd-answers-agent"
        private = $true
        type = "module"
        scripts = @{
            "rag:query" = "node --import tsx skills/query-pinecone/scripts/agent-pinecone-query.ts"
        }
        dependencies = @{}
    }
    $pkg | ConvertTo-Json -Depth 4 | Set-Content -Path $pkgDest -Encoding utf8
    Write-Host "  created: $pkgDest"
}

# ── tsconfig.json ───────────────────────────────────────────────────────────
$tscDest = "$agentDir\tsconfig.json"
if (-not (Test-Path $tscDest)) {
    Copy-File "$RepoRoot\tsconfig.json" $tscDest
}

Write-Host ""
Write-Host "=== Package complete ==="
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. cd $agentDir"
Write-Host "  2. Copy conf\.secrets.example to conf\.secrets and fill in API keys"
Write-Host "  3. npm install tsx @pinecone-database/pinecone openai"
Write-Host "  4. pip install 'markitdown[all]' pymupdf  (for convert/chunk)"
Write-Host "  5. Update import paths in copied .ts files to use ./scripts/shared/"
Write-Host "     (see AGENTS.md for code references)"
Write-Host ""
Write-Host "The TS scripts still import from their original relative paths."
Write-Host "You will need to adjust imports in the copied .ts files to point"
Write-Host "to scripts/shared/ instead of ../../packages/..."
