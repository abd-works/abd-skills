# detect-correction.ps1 — userPromptSubmitted hook for CDD correction detection.
# Parses the prompt for correction signals. If found, writes a pending entry to
# docs/sessions/corrections-pending.md so the sessionStart-primed AI processes it.

$raw = $input | Out-String
if (-not $raw) { $raw = [Console]::In.ReadToEnd() }

try {
    $data = $raw | ConvertFrom-Json
} catch {
    exit 0
}

$prompt = ($data.prompt ?? $data.Prompt ?? '').ToLower()

$patterns = @(
    "that'?s? (was )?wrong",
    "you'?re? wrong",
    "you (were|are) wrong",
    "you assumed",
    "made an assumption",
    "you'?re? assuming",
    "you generated (when|instead)",
    "should have grilled",
    "should have asked (first|me|one)",
    "you grilled all",
    "asked all (at once|questions)",
    "all questions at once",
    "(that'?s?|that was|not) (right|correct)",
    "\bincorrect\b",
    "correct that",
    "you made a mistake",
    "that was a mistake",
    "you skipped (the )?grill",
    "you didn'?t? grill",
    "you didn'?t? ask (first|me)",
    "you should have (grilled|asked)",
    "wrong approach",
    "wrong answer"
)

$matched = $false
foreach ($pattern in $patterns) {
    if ($prompt -match $pattern) {
        $matched = $true
        break
    }
}

if (-not $matched) { exit 0 }

$cwd = if ($data.cwd) { $data.cwd } else { Get-Location }
$correctionsDir = Join-Path $cwd 'docs' 'sessions'
if (-not (Test-Path $correctionsDir)) {
    New-Item -ItemType Directory -Path $correctionsDir -Force | Out-Null
}

$correctionsFile = Join-Path $correctionsDir 'corrections-pending.md'
$ts = Get-Date -Format 'yyyy-MM-dd HH:mm'
$excerpt = $prompt.Substring(0, [Math]::Min(200, $prompt.Length)).Replace("`n", ' ')

Add-Content -Path $correctionsFile -Value "- [ ] $ts — correction signal detected: `"$excerpt`""

exit 0
