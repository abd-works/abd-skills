# Workspace (guidance + scripts)

This is **not** a Cursor skill package. It is **guidance** (rule + slash command) plus **Python helpers** under **`guidance/workspace/scripts/`**.

## Purpose

Set and read the **agent engagement root**: artifacts (plans, outputs, corpus paths, deploy targets for skills) should live under **`workspace.active_skill_workspace`**, not inside the agilebydesign-skills skill packages.

## Commands

From **agilebydesign-skills repo root**:

```bash
python guidance/workspace/scripts/get_workspace.py
python guidance/workspace/scripts/set_workspace.py "C:\path\to\engagement\root"
```

- **`get_workspace.py`** walks upward from the script until it finds **`skill-config.json`**, then prints **`workspace.active_skill_workspace`**.
- **`set_workspace.py`** uses that walk if the file exists; otherwise treats the repo root as the directory containing **`skills/`** and **`scripts/deploy-skills.ps1`**, and **creates `skill-config.json`** there on first run.

## Config shape

Values live in **`skill-config.json`** → **`workspace`**:

```json
{
  "workspace": {
    "active_skill_workspace": "C:\\path\\to\\engagement",
    "known_skill_workspaces": [],
    "context_paths": []
  }
}
```

## IDE integration

- **Rule:** `workspace.mdc` (deployed to `.cursor/rules/`).
- **Command:** `workspace.prompt.md` (deployed to `.cursor/commands/`, typically **`/workspace`**).
