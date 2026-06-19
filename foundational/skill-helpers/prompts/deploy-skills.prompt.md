---
description: >-
  Interactively deploy agilebydesign-skills family packages to a project.
  Asks which IDE, which deploy target, and whether to use workspace root.
  Then runs deploy-skills.ps1 with the right flags.
agent: agent
---

You are running an interactive deploy. Follow every step in order.

## Mandatory interaction contract

- You **MUST** use `AskQuestion` for:
  1) IDE selection  
  2) Deploy target selection  
  3) Package selection
- If custom path or custom package is selected, ask one follow-up (plain chat) to capture the exact value, then continue.

## Step 1 — Ask which IDE

Use the `AskQuestion` tool to ask:

```
Which IDE are you deploying into?
- Cursor  (deploys to .cursor/)
- VS Code  (deploys to .github/ instructions + .vscode/)
```

## Step 2 — Ask where to deploy

**Before asking**, discover every candidate target so the question is pre-populated with real choices.

Run both commands to build the option list:

```powershell
# 1. All repos currently open in this Cursor/VS Code window.
#    Use the currently open workspace roots from session context.
#    Each open repo MUST be included as a selectable option.

# 2. Any .code-workspace files inside those open folders (depth 2)
Get-ChildItem -Path C:\dev -Filter *.code-workspace -Recurse -Depth 2 |
  Select-Object -ExpandProperty FullName
```

Build the `AskQuestion` options dynamically from what you find, using this pattern:

```
Where should skills be deployed? (pick one)

--- Open repos ---
[repo name]   →  <absolute path to repo root>     (one option per open folder)

--- Workspace files found ---
[filename]   →  <absolute path>                   (one option per .code-workspace)

--- Other ---
skill-config.json auto-resolve  →  currently: <value of active_skill_workspace>
Enter a custom path              →  I will type it next
```

Only include sections that have items. If no `.code-workspace` files are found, skip that section.

If the user picks **Enter a custom path**, ask them to type the absolute path in their next message before continuing.

## Step 3 — Ask which package

Use the `AskQuestion` tool to ask:

```
Which family package do you want to deploy?
- all  (everything — recommended)
- story-driven-delivery
- domain-driven-design
- architecture-centric-engineering
- user-experience-design
- kanban (delivery)
- skill-helpers  (infra rules + prompts)
- other  (I will type the name)
```

## Step 4 — Confirm and run

Echo back the resolved parameters:

| Setting | Value |
|---|---|
| IDE | `cursor` or `vscode` |
| Deploy root | resolved path |
| Package | chosen package |

Then run the script.

Run from the **agilebydesign-skills repo root**:

```powershell
# cursor (default)
& "C:\dev\agilebydesign-skills\scripts\deploy-skills.ps1" -ide cursor -Package <package> -DeployRoot "<deploy-root>"

# vscode
& "C:\dev\agilebydesign-skills\scripts\deploy-skills.ps1" -ide vscode -Package <package> -DeployRoot "<deploy-root>"
```

Omit `-DeployRoot` entirely when the user chose auto-resolve.

## Step 5 — After deploy

- Report script result.
- If the user chose a new deploy root and auto-resolve was not used, offer to update `skill-config.json` so future deploys resolve automatically:

```powershell
python scripts/set_workspace.py "<deploy-root>"
```
