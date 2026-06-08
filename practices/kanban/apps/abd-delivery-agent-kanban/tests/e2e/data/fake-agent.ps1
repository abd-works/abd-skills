param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$Args
)

$prompt = if ($Args.Length -gt 0) { $Args[$Args.Length - 1] } else { '' }

if ($prompt -match 'role:\s*(?<role>[a-z\-]+)') {
  $role = $Matches['role']
} else {
  $role = 'engineer'
}

if ($role -eq 'ux-designer') {
  Write-Error 'simulated failure for ux-designer'
  exit 1
}

$roleText = $role
$textEvent = '{"type":"assistant","message":{"content":[{"type":"text","text":"booting ' + $roleText + '"}]}}'
$toolEvent = '{"type":"tool_call","subtype":"started","name":"shell"}'
$doneEvent = '{"type":"result"}'

Write-Output $textEvent
Start-Sleep -Milliseconds 120
Write-Output $toolEvent
Start-Sleep -Milliseconds 120
Write-Output $doneEvent
exit 0
