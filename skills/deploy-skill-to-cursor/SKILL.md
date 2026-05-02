---
name: deploy-skill-to-cursor
catalog_garden_tier: foundational
catalogue_one_liner: >-
  Junction-link a repo skill into Cursor/VS Code — skill folder, rules, instructions, and commands.
description: >-
  Deploy a skill from agilebydesign-skills into Cursor and/or VS Code using Windows directory
  junctions and hard links. Deploys the skill folder plus any `.mdc`, `.instructions.md`, and
  `.prompt.md` files under **`ide-files/`** (or the skill root for legacy packages).
---

# deploy-skill-to-cursor

## When to use this skill

- You added or changed a skill under **`agilebydesign-skills/skills/<name>/`** and want **Cursor** and/or **VS Code** to load it without maintaining a second copy.
- You want the skill's rule (`.mdc`), instruction (`.instructions.md`), and command (`.prompt.md`) files deployed to the correct IDE locations automatically.

## What it does

Creates links from the skill's canonical location to where each IDE expects them:

| What | Cursor target | VS Code target |
| --- | --- | --- |
| Skill folder | `~/.cursor/skills/<name>/` (junction) | — |
| Rule (`.mdc`) | `<project>/.cursor/rules/<name>.mdc` (hard link) | — |
| Instruction (`.instructions.md`) | — | `<project>/.vscode/<name>.instructions.md` (hard link) |
| Command (`.prompt.md`) | `<project>/.cursor/commands/<name>.prompt.md` (hard link) | `<project>/.github/prompts/<name>.prompt.md` (hard link) |

The script reads **`ide-files/`** first; if that folder is missing, it uses the skill root. If there are no matching files, those steps are skipped.

## Script

**`scripts/Deploy-SkillToCursor.ps1`**

```powershell
# Cursor only (default) — skill junction + .mdc rule + .prompt.md command
.\skills\deploy-skill-to-cursor\scripts\Deploy-SkillToCursor.ps1 -SkillName story-graph-ops

# Both IDEs — also deploys .instructions.md and .prompt.md to VS Code locations
.\skills\deploy-skill-to-cursor\scripts\Deploy-SkillToCursor.ps1 -SkillName abd-story-mapping -IDE Both -Force

# VS Code only
.\skills\deploy-skill-to-cursor\scripts\Deploy-SkillToCursor.ps1 -SkillName abd-story-mapping -IDE VSCode -Force

# Skill lives under agents/ (junction name is still SkillName)
.\skills\deploy-skill-to-cursor\scripts\Deploy-SkillToCursor.ps1 -SkillName domain-scan -SkillSourcePath C:\dev\agilebydesign-skills\agents\abd-domain-driven-design\skills\domain-scan -Force

# Deploy into a different project (Cursor by default; use -IDE Both only if that project uses VS Code / Copilot prompts)
.\skills\deploy-skill-to-cursor\scripts\Deploy-SkillToCursor.ps1 -SkillName correct-output -SkillSourcePath C:\dev\agilebydesign-skills\skills\correct_output -ProjectRoot C:\dev\other-project -Force
```

**Parameters**

| Parameter | Default | Meaning |
| --- | --- | --- |
| `SkillName` | (required) | Folder name under `skills/`. |
| `SkillsRepoRoot` | inferred | Path to **agilebydesign-skills** repo root. |
| `CursorSkillsRoot` | `%USERPROFILE%\.cursor\skills` | Cursor global skills directory. |
| `SkillSourcePath` | (empty) | Full path when skill is not under `skills/<SkillName>`. |
| `ProjectRoot` | repo root | Target project for rule/instruction/command deployment. |
| `IDE` | `Cursor` | `Cursor`, `VSCode`, or `Both`. |
| `Force` | off | Remove existing entries before linking. |

## Skill file conventions

For the deploy script to pick up a skill's IDE files, place them in the skill root with these extensions:

| Location | Purpose | Deployed to |
| --- | --- | --- |
| `ide-files/*.mdc` | Cursor always-on rule | `.cursor/rules/` |
| `ide-files/*.instructions.md` | VS Code always-on instruction | `.vscode/` (**`-IDE VSCode`** or **`Both`**) |
| `ide-files/*.prompt.md` | Slash command | `.cursor/commands/` (always with **`Cursor`** or **`Both`**); `.github/prompts/` (**`VSCode`** or **`Both`** only) |

Legacy skills may keep the same filenames in the skill root instead of **`ide-files/`**; the script falls back to the root when **`ide-files/`** is absent.

## Notes

- **Junctions** are Windows directory links; if you move or delete the repo folder, the link breaks.
- **Hard links** are used for individual files (rules, instructions, commands) since junctions only work on directories.
- Do **not** commit anything under `%USERPROFILE%\.cursor\skills`; the canonical skill lives in **agilebydesign-skills**.
- The **agilebydesign-skills** **`.gitignore`** ignores **`.cursor/`**, **`.github/`**, and **`.vscode/`** at **any path** so IDE deploy outputs are never committed; canonical rule text remains under each skill’s **`ide-files/`**. Use **`-IDE Both`** when you need those paths in **another** project whose `.gitignore` allows them. To ship **GitHub Actions** from this repo, use **`git add -f`** on workflow files (or add a negated pattern like `!.github/workflows/` after `.github/` — see Git docs).
