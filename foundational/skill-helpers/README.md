# Skill helpers package

Infrastructure skills and cross-cutting helpers used across practice families.

## Skills

- `execute-skill-using-skills-rules` — rules + scanner pass before declaring skill output done
- `track_task` — checkbox progress files under the engagement workspace
- `commit-msg` — meaningful commit messages from scope and changed files

## Package helpers (not packaged skills)

| Slot | Purpose |
| --- | --- |
| `instructions/` | Always-on rules: workspace, deploy-skills, log-and-fix-skill-errors, execute-skill-using-skills-rules |
| `prompts/` | Slash commands: `/workspace`, fix-skill, refresh-all-instructions |
| `scripts/` | `get_workspace.py`, `set_workspace.py` — read/write `skill-config.json` |
| `reference/` | Workspace docs, correction log template |

## Workspace CLI

From **agilebydesign-skills repo root**:

```powershell
python skill-helpers/scripts/get_workspace.py
python skill-helpers/scripts/set_workspace.py "C:\path\to\engagement\root"
```

Details: `reference/workspace.md`

## Deploy

```powershell
& scripts/deploy-skills.ps1 -Force
```
