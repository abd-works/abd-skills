---
description: >-
  Get or set the engagement workspace root (skill-config.json active_skill_workspace).
  Use when deploy root, tracking paths, or engagement artifacts need the correct folder.
mode: agent
---

## Workspace root

The canonical engagement folder is **`workspace.active_skill_workspace`** in **`skill-config.json`** at the **agilebydesign-skills repository root** (not inside a packaged skill).

### Read current value

From **agilebydesign-skills repo root**:

```powershell
python skill-helpers/scripts/get_workspace.py
```

### Set workspace

```powershell
python skill-helpers/scripts/set_workspace.py "C:\absolute\path\to\project"
```

If **`skill-config.json`** is missing, **`set_workspace.py`** creates it when the repo root can be detected (**`scripts/deploy_family_package.py`**).

### After changing workspace

Run **`scripts/deploy-skills.ps1`** if Cursor rules/commands/skills should redeploy into the new **`DeployRoot`** (or rely on auto-resolution from **`skill-config.json`**).

### Reference

- Rule: **`skill-helpers/instructions/workspace.mdc`**
- Details: **`skill-helpers/content/workspace.md`**
