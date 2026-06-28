---
description: >-
  Re-deploy using the exact parameters from the last deploy. No questions asked.
  Reads .abd-deploy-state.json and executes immediately.
agent: agent
---

You are re-running the last deploy with no interaction. Follow every step in order.

## Step 1 — Read state file

```powershell
$stateFile = "C:\dev\abd-skills\.abd-deploy-state.json"
if (Test-Path -LiteralPath $stateFile) {
  Get-Content -LiteralPath $stateFile -Raw | ConvertFrom-Json
} else {
  $null
}
```

**If the state file is missing or incomplete**, stop and tell the user:
> "No saved deploy parameters found. Run `/deploy-skills` first."

Otherwise extract and confirm:

| Parameter | Value |
|---|---|
| Deploy root | `last_deploy_root` |
| IDE | `last_ide` (default: cursor) |
| Package | `last_package` (default: all) |
| Mode | `last_deploy_mode` (default: delta) |
| Encoding guard | `last_encoding_guard` (default: false) |

Tell the user in one line what you are about to do:
> "Re-deploying: `<package>` → `<deploy-root>` (mode: `<mode>`, ide: `<ide>`, encoding guard: `<on|off>`)"

## Step 2 — Pre-deploy actions

**delta** — nothing extra, proceed to Step 3.

**clean** — wipe every folder the deploy script manages:
```powershell
$r = "<deploy-root>"
foreach ($sub in @('skills','commands','rules','agents','content','reference','lib','scripts')) {
  Remove-Item "$r\.cursor\$sub" -Recurse -Force -ErrorAction SilentlyContinue
}
Remove-Item "$r\.github\hooks" -Recurse -Force -ErrorAction SilentlyContinue
```

## Step 3 — Run deploy

```powershell
& "C:\dev\abd-skills\common\scripts\deploy-skills.ps1" -ide <ide> -Package <package> -DeployRoot "<deploy-root>" -SkipChecks
```

## Step 4 — Encoding guard (if last_encoding_guard is true)

```powershell
cd "C:\dev\abd-skills"
python3 common/scripts/scan_encoding.py --fix
```

Report how many files were fixed and any remaining issues.

## Step 5 — Done

Report script result. No need to re-save state (parameters did not change).
