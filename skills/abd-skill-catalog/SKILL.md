---
name: abd-skill-catalog
description: >-
  Scan the agilebydesign-skills repository (root skills/ and agents/), then
  regenerate a reader-facing Markdown outline plus a small multi-page HTML
  site. Each skill and agent entry includes a short **summary** paragraph (for
  tables and cards) plus a longer **description** from `## Purpose` when
  present. Optional repository layout summarizes files (with links) and common
  folders in one line each.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
---

# ABD Skill & Agent Catalogue

Maintain a browsable catalogue of **practice skills** under the repo root
`skills/` and **agents** under `agents/`, aligned with the tone of
`agents/abd-skill-builder/docs/process-outline.md` and the compact HTML chrome
used under `agents/abd-skill-builder/docs/overview/`.

## When to use this skill

- You added, renamed, or retired a skill or agent and the catalogue is stale.
- You need a stakeholder-facing index of what each skill and agent is for.
- You want both Markdown (diffable, review in Git) and HTML (quick browse).

## What it produces

| Artifact | Format | Location (default) |
| --- | --- | --- |
| **Outline** | Markdown | `abd-skill-catalog/outline.md` (repository root) |
| **Site hub** | HTML | `abd-skill-catalog/catalog/index.html` |
| **Skills grid** | HTML | `abd-skill-catalog/catalog/skills.html` |
| **Agents grid** | HTML | `abd-skill-catalog/catalog/agents.html` |
| **Skill detail pages** | HTML | `abd-skill-catalog/catalog/skill/<dir>.html` (one per skill; cards link here) |
| **Agent detail pages** | HTML | `abd-skill-catalog/catalog/agent/<dir>.html` (one per agent; cards link here) |

Each catalogue entry includes:

- **Summary** — one paragraph for summary tables and HTML cards: YAML
  `description`, else flattened `## Purpose`, else opening text after the H1.
- **Description** — expanded purpose text from `## Purpose` when present, else
  YAML `description` or body excerpt (used in the outline detail sections).
- **Repository layout** — top-level files with a one-line blurb and relative
  link; common directories get **one** folder-level summary plus **each file
  directly in that folder** listed with the same blurb + link pattern (one
  directory level deep, not recursive into subfolders).
- **Detail pages** — full description, an ASCII package diagram inside a
  `<pre>` (same spirit as `agents/abd-skill-builder/docs/overview/` capability
  pages), and a contents list with links into the repository.

## Agent instructions

1. **Regenerate on command.** From the **agilebydesign-skills** repository root,
   run:

   ```bash
   python skills/abd-skill-catalog/scripts/generate_abd_catalog.py
   ```

   Options:

   - `--repo-root <path>` — defaults to the parent of the repo `skills/`
     directory (detected from this script location).
   - `--output-dir <path>` — overrides `<repo-root>/abd-skill-catalog` if you need a different folder.

2. **Discovery rules.**

   - **Skills:** every immediate child of `skills/` that contains `SKILL.md`.
     (Skips plain files and folders without `SKILL.md`.)
   - **Agents:** every immediate child of `agents/` that contains one of
     `AGENT.md`, `AGENTS.md`, or `SKILL.md` (first match in that order).

3. **Extraction (skills).** Same heuristics as `skill-garden-catalogue`:

   - *Name* — YAML `name`, else directory name.
   - *Summary* — YAML `description` when present, else first paragraph of
     `## Purpose`, else text between H1 and the first `##` heading.
   - *Description* — full `## Purpose` body when present, else YAML
     `description`, else beginning of the markdown body.

4. **Extraction (agents).**

   - *Name* — YAML `name` if present, else markdown H1 heading text.
   - *Summary / Description* — prefer `## Purpose` when present; otherwise derive
     from the opening sections (`## Introduction`, first paragraphs). YAML
     `description` feeds the summary when present.

5. **Templates.** HTML shell and CSS live under
   `skills/abd-skill-catalog/templates/` and are copied with token replacement.
   Edit those files to change branding or layout without touching Python.

6. **Idempotent.** Running the script twice with the same tree overwrites the
   same outputs deterministically.
