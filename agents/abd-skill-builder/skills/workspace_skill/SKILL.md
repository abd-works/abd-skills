---
name: workspace
description: Set and read the agent engagement root (skill-config.json → workspace.active_skill_workspace). Run scripts from this folder; they resolve the agent root automatically.
---

# Workspace (agent)

## What this is

This leaf skill holds **set/get workspace** helpers for the **parent agent** repo. Engagement artifacts (plans, outputs, corpus paths) should live under **`active_skill_workspace`**, not inside the agent package.

## Commands

From **agent root** (parent of `skills/`):

```bash
python skills/workspace/scripts/get_workspace.py
python skills/workspace/scripts/set_workspace.py "C:\path\to\engagement\root"
```

Empty or `.` means “current agent directory” until you set a real project path.

## Config

Values are stored in the agent’s **`skill-config.json`** → **`workspace`** (same shape as skill packages).
