<#
.SYNOPSIS
  Install dependencies for the abd-answers agent after copying it to a new location.
  Run this once from the agent root directory.

.DESCRIPTION
  Installs Node.js (npm) and Python (pip) packages the agent skills need.
  Does NOT install Node.js or Python themselves — those must already be on PATH.

  After install, copy conf\.secrets.example to conf\.secrets and fill in your
  OPENAI_API_KEY, PINECONE_API_KEY, and PINECONE_INDEX.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$agentDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Push-Location $agentDir
try {
    Write-Host "=== abd-answers agent install ===" -ForegroundColor Cyan
    Write-Host "  Agent root: $agentDir"
    Write-Host ""

    # ── npm packages (query + embed skills) ─────────────────────────────
    Write-Host "[1/3] Installing npm packages..." -ForegroundColor Yellow
    npm install tsx @pinecone-database/pinecone openai dotenv
    Write-Host ""

    # ── Python packages (convert + chunk skills) ────────────────────────
    Write-Host "[2/3] Installing Python packages..." -ForegroundColor Yellow
    pip install "markitdown[all]" pymupdf
    Write-Host ""

    # ── conf/.secrets setup ─────────────────────────────────────────────
    $secretsFile = "$agentDir\conf\.secrets"
    $secretsExample = "$agentDir\conf\.secrets.example"

    if (-not (Test-Path $secretsFile)) {
        if (Test-Path $secretsExample) {
            Copy-Item $secretsExample $secretsFile
            Write-Host "[3/3] Created conf\.secrets from template." -ForegroundColor Yellow
            Write-Host "       Edit conf\.secrets and fill in your API keys:" -ForegroundColor Red
            Write-Host "         OPENAI_API_KEY=sk-..."
            Write-Host "         PINECONE_API_KEY=pcsk_..."
            Write-Host "         PINECONE_INDEX=abd-answers-memory"
        } else {
            Write-Warning "  conf\.secrets.example not found — create conf\.secrets manually."
        }
    } else {
        Write-Host "[3/3] conf\.secrets already exists — skipping." -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "=== Install complete ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Quick test:"
    Write-Host "  npm run rag:query -- `"what is story mapping`" --k 3"
    Write-Host ""
} finally {
    Pop-Location
}
