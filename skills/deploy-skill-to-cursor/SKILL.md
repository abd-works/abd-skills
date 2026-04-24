---
name: deploy-skill-to-cursor
catalog_garden_tier: foundational
catalogue_one_liner: >-
  Junction-link a repo skill into Cursor user skills on Windows (no file copy).
description: >-
  Deploy a skill from agilebydesign-skills into Cursor's user skills folder using a Windows
  directory junction (no duplicate copy). Run scripts/Deploy-SkillToCursor.ps1 with the
  skill folder name. Use when you want the global Cursor skills path to point at the repo
  canonical skill.
---

# deploy-skill-to-cursor

## When to use this skill

- You added or changed a skill under **`agilebydesign-skills/skills/<name>/`** and want **Cursor** to load it from **`%USERPROFILE%\.cursor\skills`** without maintaining a second copy.
- You previously copied a skill into `.cursor\skills` and want to **replace** that tree with a **junction** to the repo.

## What it does

Creates a **directory junction**:

- **Link:** `%USERPROFILE%\.cursor\skills\<SkillName>`
- **Target:** `<repo>\skills\<SkillName>`

Edits in the repo are visible immediately through the junction path.

## Script

**`scripts/Deploy-SkillToCursor.ps1`**

```powershell
# From repo: default infers skills/ from script location
.\skills\deploy-skill-to-cursor\scripts\Deploy-SkillToCursor.ps1 -SkillName story-graph-ops

# Replace an existing folder or junction at the Cursor path
.\skills\deploy-skill-to-cursor\scripts\Deploy-SkillToCursor.ps1 -SkillName story-graph-ops -Force

# Custom repo root (folder that contains skills/)
.\skills\deploy-skill-to-cursor\scripts\Deploy-SkillToCursor.ps1 -SkillName execute_using_rules -SkillsRepoRoot C:\dev\agilebydesign-skills

# Skill lives under agents/.../skills/ (junction name is still SkillName)
.\skills\deploy-skill-to-cursor\scripts\Deploy-SkillToCursor.ps1 -SkillName domain-scan -SkillSourcePath C:\dev\agilebydesign-skills\agents\abd-ooad\skills\domain-scan -Force
```

**Parameters**

| Parameter | Default | Meaning |
| --- | --- | --- |
| `SkillName` | (required) | Folder name under `skills/`. |
| `SkillsRepoRoot` | inferred | Path to **agilebydesign-skills** repo root (contains `skills/`). Omit when you run the script from this repo layout. |
| `CursorSkillsRoot` | `%USERPROFILE%\.cursor\skills` | Cursor global skills directory. |
| `SkillSourcePath` | (empty) | Full path to the skill folder when it is **not** under `skills/<SkillName>` (e.g. `agents/<agent>/skills/<name>`). |
| `Force` | off | Remove existing destination path, then create the junction. |

## Notes

- **Junctions** are Windows directory links; if you move or delete the repo folder, the link breaks until you recreate it or fix the target.
- Do **not** commit anything under `%USERPROFILE%\.cursor\skills`; the canonical skill lives in **agilebydesign-skills**.
