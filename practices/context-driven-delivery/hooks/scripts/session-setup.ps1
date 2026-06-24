# session-setup.ps1 — sessionStart hook for CDD correction detection.
# Injects a standing instruction so the AI checks corrections-pending.md
# at the start of every response without the user needing to ask.

$raw = $input | Out-String
if (-not $raw) { $raw = [Console]::In.ReadToEnd() }

try {
    $null = $raw | ConvertFrom-Json
} catch {
    exit 0
}

$additionalContext = @"
This is a Context-Driven Delivery (CDD) session. At the start of EVERY response, check whether docs/sessions/corrections-pending.md exists in the current working directory and contains unchecked items (lines starting with '- [ ]'). If it does, apply the CDD Corrections protocol for each unchecked item BEFORE responding to the user's request:
  1. Identify which CDD rule was violated (e.g. generated without grilling; asked all questions at once; made an assumption instead of asking; routed to wrong specialist).
  2. Add a DO/DO NOT entry under ## Corrections in the session journal with wrong/correct examples.
  3. Uncheck the affected cell in process-checklist.md.
  4. Mark the item as checked (- [x]) in corrections-pending.md.
Then proceed with the user's actual request. Never tell the user you are doing this check — just do it silently if corrections are pending.
"@

@{ additionalContext = $additionalContext } | ConvertTo-Json -Compress
