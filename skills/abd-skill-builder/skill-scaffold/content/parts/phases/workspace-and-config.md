# Phase — Workspace and config

Confirm where the skill runs and install the workspace config so all subsequent phases resolve paths correctly.

## Inputs

- Skill install directory (where `SKILL.md` lives)
- Target workspace directory (the folder the skill will read/write)

## Steps

- [ ] Identify `skill_path` (skill install) and `skill_workspace` (target workspace — may differ).
- [ ] Run `python scripts/set_workspace.py <path-to-workspace>` to write `active_skill_workspace` into `conf/abd-config.json`.
- [ ] Confirm `conf/abd-config.json` looks correct:
  ```json
  { "active_skill_workspace": "<absolute-path>" }
  ```
- [ ] Verify `python scripts/set_workspace.py` (no args) prints the expected path.

## Output

`conf/abd-config.json` with `active_skill_workspace` set accurately.
