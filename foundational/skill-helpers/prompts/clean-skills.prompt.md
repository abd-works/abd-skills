---
description: >-
  Interactively clean agilebydesign-skills deployments from a project.
  Asks which deploy target to clean, then runs clean-skills.ps1.
mode: agent
---

You are running an interactive clean. Follow every step in order.

## Step 1 — Ask where to clean

**Before asking**, discover every candidate target.

Run:

```powershell
Get-ChildItem -Path C:\dev -Filter *.code-workspace -Recurse -Depth 2 |
  Select-Object -ExpandProperty FullName
```

Build the `AskQuestion` options from currently open workspace folders, any `.code-workspace` files found, and the `skill-config.json` auto-resolve value. Do not include any other options.

## Step 2 — Run clean

Run from the **agilebydesign-skills repo root**:

```powershell
& "C:\dev\agilebydesign-skills\scripts\clean-skills.ps1" -DeployRoot "<deploy-root>"
```

Omit `-DeployRoot` only if the user explicitly chose auto-resolve.

## Step 3 — Report result

Report the script output.
