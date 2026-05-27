---
name: skill-garden-catalogue
description: >-
  Scan a folder of deployed skills and regenerate a one-pager Markdown
  inventory and an HTML index page. Each entry shows the challenge the skill
  addresses and the solution it provides, hyperlinked to the skill directory.
  Re-run on command to keep the inventory current.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
---

# Skill Garden Inventory

Generate a browsable inventory of every skill deployed in a folder.

## When to use this skill

- You want a single-page overview of all available skills.
- You need to share a skills inventory with a team or stakeholder.
- Skills have been added, removed, or updated and the inventory is stale.
- You want an HTML index page to open in a browser.

## What it produces

| Artifact | Format | Location |
| --- | --- | --- |
| **Skill inventory** | Markdown, one section per category | `skill-inventory.md` in the output directory |
| **Skill index (HTML)** | HTML card grid, one section per category | `catalog/index.html` in the output directory |

Both artifacts organise skills into **categories** — one per top-level folder
directly under the skills root (e.g. `delivery/`, `engineering/`, `utilities/`).
Every skill with a `SKILL.md` anywhere beneath a category folder appears in that
category. Skills sitting at the root level land in **General**.

Each card / row shows:

- **Skill name** — hyperlinked to the skill directory.
- **Challenge** — the problem or situation the skill addresses.
- **Solution** — what the skill does about it.

## Agent instructions

1. **Regenerate on command.**
   Run `python scripts/generate_catalogue.py --skills-dir <path>` pointing at
   the skills root (top-level category folders live here). Override the output
   location with `--output-dir <path>`.

2. **Category mapping.**
   Categories come from the top-level subfolders of `--skills-dir`.  The script
   maps folder names to display labels automatically; add to `_CATEGORY_LABELS`
   in `generate_catalogue.py` to override any label.

3. **Extraction rules.**
   The script reads each `SKILL.md`:
   - *Name* — YAML frontmatter `name`, falling back to the directory name.
   - *Challenge* — first sentence of the `## Purpose` section, or first bullet
     of `## When to use this skill`, or a generic fallback.
   - *Solution* — YAML frontmatter `catalogue_one_liner`, then `description`
     (first ~250 chars), then `## Purpose` content.

4. **Templates.**
   `templates/catalog-index.html` is the HTML shell; the script injects
   `{{SKILL_COUNT}}` and `{{SKILL_SECTIONS}}`.  The Markdown output is built
   entirely in code.

5. **Idempotent.** Running the script twice with the same input produces
   identical output. Safe to re-run whenever the skill set changes.
