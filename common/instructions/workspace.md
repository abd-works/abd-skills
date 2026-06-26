# Workspace (skill-helpers)

## Purpose

Set and read the **agent engagement root**: artifacts (plans, outputs, corpus paths, deploy targets for skills) should live under **`workspace.active_skill_workspace`**, not inside the abd-skills skill packages.

## Commands

From **agilebydesign-skills repo root**:

```bash
python skill-helpers/scripts/get_workspace.py
python skill-helpers/scripts/set_workspace.py "C:\path\to\engagement\root"
```

- **`get_workspace.py`** walks upward from the script until it finds **`skill-config.json`**, then prints **`workspace.active_skill_workspace`**.
- **`set_workspace.py`** uses that walk if the file exists; otherwise detects the repo root via **`practices/`** + **`foundational/`**, and **creates `skill-config.json`** there on first run.

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
