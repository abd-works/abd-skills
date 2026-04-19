<#
.SYNOPSIS
  Run abd-answers memory pipeline stages one at a time (convert → chunk → Pinecone sync via HTTP).

.DESCRIPTION
  Stages match PIPELINE_CONTRACT.md: markdown/ then chunked/ then POST build-rag (vectors).
  Runs scripts from the local skill tree (agilebydesign-skills canonical source).

.PARAMETER SourcePath
  Folder or file to convert (passed to convert_to_markdown.py --memory).

.PARAMETER SkipConvert
.PARAMETER SkipChunk
.PARAMETER SkipBuildRag
  Skip individual stages after prior stages have been run.

.PARAMETER AnswersBaseUrl
  Default http://127.0.0.1:3001 — app-server must be running for build-rag unless -SkipBuildRag.

.EXAMPLE
  .\scripts\run-pipeline-stages.ps1 -SourcePath "C:\data\my-docs"

.EXAMPLE
  .\scripts\run-pipeline-stages.ps1 -SourcePath "C:\data\my-docs" -SkipConvert
#>
param(
  [Parameter(Mandatory = $true)]
  [string] $SourcePath,
  [switch] $SkipConvert,
  [switch] $SkipChunk,
  [switch] $SkipBuildRag,
  [string] $AnswersBaseUrl = "http://127.0.0.1:3001"
)

$ErrorActionPreference = "Stop"
$agentRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $agentRoot

$py = "python"
$convert = Join-Path $agentRoot "skills\convert-content\scripts\convert_to_markdown.py"
$chunk   = Join-Path $agentRoot "skills\chunk-content\scripts\chunk_markdown.py"

if (-not $SkipConvert) {
  Write-Host "=== Stage 1: convert_to_markdown (--memory) ===" -ForegroundColor Cyan
  & $py $convert --memory $SourcePath
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

if (-not $SkipChunk) {
  Write-Host "=== Stage 2: chunk_markdown ===" -ForegroundColor Cyan
  & $py $chunk --path $SourcePath
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

if (-not $SkipBuildRag) {
  Write-Host "=== Stage 3: POST /api/answers/files/build-rag (Pinecone delta) ===" -ForegroundColor Cyan
  $uri = "$AnswersBaseUrl/api/answers/files/build-rag"
  $body = '{"scope":"memory"}'
  try {
    $r = Invoke-RestMethod -Uri $uri -Method Post -ContentType "application/json" -Body $body
    $r | ConvertTo-Json -Depth 8
  } catch {
    Write-Warning "build-rag failed (is app-server running and auth off for local dev?): $_"
    throw
  }
}

Write-Host "Done." -ForegroundColor Green
