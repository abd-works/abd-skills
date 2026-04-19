---
name: skill-garden-catalogue
description: >-
  Scan a folder of deployed skills and regenerate a one-pager Markdown
  inventory and an HTML catalogue. Each entry shows the challenge the skill
  addresses and the solution it provides, hyperlinked to the skill directory.
  Re-run on command to keep the catalogue current.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
---

# Skill Garden Catalogue

Generate a browsable inventory of every skill deployed in a folder.

## When to use this skill

- You want a single-page overview of all available skills.
- You need to share a skills catalogue with a team or stakeholder.
- Skills have been added, removed, or updated and the catalogue is stale.
- You want an HTML catalogue page to open in a browser.

## What it produces

| Artifact | Format | Location |
| --- | --- | --- |
| **Skill inventory** | Markdown table | `skill-inventory.md` in the output directory |
| **Skill catalogue** | HTML card grid | `catalog/index.html` in the output directory |

Both artifacts show every skill with:

- **Skill name** — hyperlinked to the skill directory.
- **Challenge** — the problem or situation the skill addresses.
- **Solution** — what the skill does about it.

## Agent instructions

1. **Regenerate on command.**
   Run `python scripts/generate_catalogue.py --skills-dir <path>` with the
   folder that contains the deployed skills (each subdirectory must have a
   `SKILL.md`). Default output lands next to the script; override with
   `--output-dir <path>`.

2. **Extraction rules.**
   The script reads each `SKILL.md`:
   - *Name* — YAML frontmatter `name`, falling back to the directory name.
   - *Challenge* — first sentence of the `## Purpose` section, or derived
     from the `## When to use this skill` section, or a generic fallback.
   - *Solution* — YAML frontmatter `description` (first ~200 chars).

3. **Templates.**
   Markdown and HTML templates live in `templates/`. The script uses them
   as the structural skeleton; skill entries are injected at generation time.

4. **Idempotent.** Running the script twice with the same input produces
   identical output. Safe to re-run whenever the skill set changes.
