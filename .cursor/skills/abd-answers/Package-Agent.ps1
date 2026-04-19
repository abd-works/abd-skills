<#
.SYNOPSIS
  Verify the abd-answers agent skill tree is complete.

.DESCRIPTION
  This skill tree is the canonical source for the abd-answers agent.
  All TS and Python scripts live here — there is no longer a copy step
  from the abd-answers application repo.

  This script checks that expected files exist and reports any missing ones.
  To deploy junctions into Cursor or the abd-answers project, use
  Deploy-ToCursor.ps1 instead.

.NOTES
  Previously this script copied files FROM the abd-answers repo INTO this tree.
  That workflow is retired: edit files here and commit to agilebydesign-skills.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$agentDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

$expected = @(
    "AGENTS.md"
    "README.md"
    "Install-Agent.ps1"
    "Deploy-ToCursor.ps1"
    "package.json"
    "tsconfig.json"
    "conf\.secrets.example"
    "conf\answers-memory.env.example"
    "scripts\run-pipeline-stages.ps1"
    "scripts\shared\types.ts"
    "scripts\shared\abd-answers-paths.ts"
    "scripts\shared\load-conf-openai-key.ts"
    "scripts\shared\rag\pinecone-rag.ts"
    "scripts\shared\rag\pinecone-deployment-rag.ts"
    "scripts\shared\rag\pinecone-namespace.ts"
    "scripts\shared\rag\rag-path-semantic-search.ts"
    "scripts\shared\rag\openai-keys.ts"
    "scripts\shared\rag\chunk-keyword-rank.ts"
    "skills\convert-content\SKILL.md"
    "skills\convert-content\scripts\convert_to_markdown.py"
    "skills\convert-content\scripts\_config.py"
    "skills\chunk-content\SKILL.md"
    "skills\chunk-content\scripts\chunk_markdown.py"
    "skills\chunk-content\scripts\_config.py"
    "skills\embed-pinecone\SKILL.md"
    "skills\embed-pinecone\scripts\migrate-memory-to-pinecone.ts"
    "skills\query-pinecone\SKILL.md"
    "skills\query-pinecone\scripts\agent-pinecone-query.ts"
)

Write-Host "=== abd-answers agent: verify skill tree ===" -ForegroundColor Cyan
Write-Host "  Agent root: $agentDir"
Write-Host ""

$missing = @()
foreach ($rel in $expected) {
    $full = Join-Path $agentDir $rel
    if (-not (Test-Path $full)) {
        $missing += $rel
        Write-Host "  MISSING: $rel" -ForegroundColor Red
    }
}

if ($missing.Count -eq 0) {
    Write-Host "  All $($expected.Count) expected files present." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "  $($missing.Count) file(s) missing." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "This skill tree is the canonical source (agilebydesign-skills)."
Write-Host "To deploy junctions: .\Deploy-ToCursor.ps1"
Write-Host "To install deps:     .\Install-Agent.ps1"
