---
description: >-
  Interactively deploy agilebydesign-skills family packages to a project.
  Reads last deploy parameters from state file. Offers "use last parameters"
  shortcut. Saves all choices after every deploy.
agent: agent
---

You are running an interactive deploy. Follow every step in order.

## Step 1 — Read state file

```powershell
$stateFile = "C:\dev\abd-skills\.abd-deploy-state.json"
if (Test-Path -LiteralPath $stateFile) {
  Get-Content -LiteralPath $stateFile -Raw | ConvertFrom-Json
} else {
  $null
}
```

Extract these fields (use `$null` / defaults when missing):

| Field | Default |
|---|---|
| `last_deploy_root` | *(ask user)* |
| `last_ide` | cursor |
| `last_package` | all |
| `last_deploy_mode` | delta |
| `last_encoding_guard` | false |

## Step 2 — Resolve deploy root

**If `last_deploy_root` is set:** Use it silently. Do **not** ask.

**If missing:** Ask the user in plain chat: "Where should I deploy? (paste the absolute path)" and wait for the answer.

## Step 3 — Ask questions (one AskQuestion call)

**If the state file has all five fields set**, make a single `AskQuestion` call with **one** question:

> **Use last parameters?**
> - Yes — deploy immediately with: `<ide>`, `<package>`, `<mode>`, encoding guard `<on|off>`, root `<root>` (Recommended)
> - No — let me choose new settings

If **Yes**, skip to Step 4 directly.

**If the state file is missing any field** (or the user picked No above), make a single `AskQuestion` call with these four questions:

1. **Which IDE** — Cursor (Recommended) / VS Code
2. **Which package** — all (Recommended) / story-driven-delivery / domain-driven-design / architecture-centric-engineering / user-experience-design / kanban / skill-helpers / other
3. **Deploy mode**:
   - **Delta** (Recommended) — copy only changed/new files
   - **Clean** — wipe all cursor-managed folders first, then deploy (removes stale files)
4. **Encoding guard** — after deploy, run `scan_encoding.py --fix` to scrub mojibake, Kanji, and surrogate-pair characters:
   - **No** (Recommended)
   - **Yes**

If the user picks **other** for package, ask for the name in a follow-up before continuing.

## Step 4 — Pre-deploy actions

**Delta** — nothing extra, proceed to Step 5.

**Clean** — wipe every folder the deploy script manages:
```powershell
$r = "<deploy-root>"
foreach ($sub in @('skills','commands','rules','agents','content','reference','lib','scripts')) {
  Remove-Item "$r\.cursor\$sub" -Recurse -Force -ErrorAction SilentlyContinue
}
Remove-Item "$r\.github\hooks" -Recurse -Force -ErrorAction SilentlyContinue
```

## Step 5 — Run deploy

```powershell
& "C:\dev\abd-skills\common\scripts\deploy-skills.ps1" -ide <ide> -Package <package> -DeployRoot "<deploy-root>" -SkipChecks
```

## Step 6 — Encoding guard (if Yes)

```powershell
cd "C:\dev\abd-skills"
python3 common/scripts/scan_encoding.py --fix
```

Report how many files were fixed and any remaining issues.

## Step 7 — Save all parameters to state file

```powershell
$stateFile = "C:\dev\abd-skills\.abd-deploy-state.json"
@{
  last_deploy_root     = "<deploy-root>"
  last_ide             = "<ide>"
  last_package         = "<package>"
  last_deploy_mode     = "<delta|clean>"
  last_encoding_guard  = $<true|false>
} | ConvertTo-Json | Set-Content -LiteralPath $stateFile -Encoding UTF8
```

Report script result and confirm parameters saved.
