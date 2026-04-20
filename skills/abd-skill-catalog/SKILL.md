---
name: abd-skill-catalog
description: >-
  Scan the agilebydesign-skills repository (root skills/ and agents/), then
  regenerate a reader-facing Markdown outline plus a small multi-page HTML
  site. Each skill and agent entry includes a short **summary** paragraph (for
  tables and cards) plus a longer **description** from `## Purpose` when
  present. Detail pages use a **behavior-first ASCII block** (how the skill or
  agent is used, not only a folder tree), then repository layout with links.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
---

# ABD Skill & Agent Catalogue

Maintain a browsable catalogue of **skills** under the repo root
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
| **Outline** | Markdown | `catalog/outline.md` (repository root) |
| **Site hub** | HTML | `catalog/index.html` |
| **Skills grid** | HTML | `catalog/skills.html` |
| **Agents grid** | HTML | `catalog/agents.html` |
| **Hub / grid intros** | HTML fragments | `skills/abd-skill-catalog/templates/intros/*.html` (short lines above grids; optional polish) |
| **Skill detail pages** | HTML | `catalog/skill/<dir>.html` (one per skill; cards link here) |
| **Agent detail pages** | HTML | `catalog/agent/<dir>.html` (one per agent; cards link here) |

Each catalogue entry includes:

- **Summary** — one paragraph for summary tables and HTML cards: YAML
  `description`, else flattened `## Purpose`, else opening text after the H1.
- **Description** (detail page) — `## Purpose` when present, else YAML
  `description`, else **intro after the title** (all paragraphs until the first
  `##` heading, capped). Agents without `## Purpose` no longer embed the entire
  `AGENT.md` in the catalogue; layout matches skills: short prose, then diagram,
  then contents.
- **Repository layout** — top-level files use the file name as the link to the
  repo path, then a one-line blurb; directories render as nested
  **expand/collapse** trees (HTML `<details>` / `<summary>`): subfolders and
  files to a capped depth (folder rows expand/collapse; no separate “open
  folder” link). Each folder row has a small + / minus box on the left of the
  summary so expand/collapse is obvious.
  Known folder names get a fixed purpose line; any folder that contains
  `SKILL.md` (for example nested skills under `agents/.../skills/`) gets its
  summary from that skill’s YAML `description` / `## Purpose`. The first few
  nesting levels default to **expanded** so typical trees show files without
  extra clicks (still collapsible).
- **Detail pages** — description block as above, then a `<pre>` ASCII block that
  explains **how the package works** (orchestration, skills loaded, main
  artifacts), followed by a short **repo-root tree** for orientation. Agents
  with a distinctive flow (for example **`abd-delivery-lead`**) can register a
  tailored block in `_AGENT_CATALOG_FLOW` in `generate_abd_catalog.py`; others
  get a sensible default from the entry file name + kind. Then the expandable
  **Contents** tree lists files with links. Repo links use `target="_blank"` so
  the catalogue page stays open while `.md` and other files open in another tab.

## Agent instructions

1. **Regenerate on command.** From the **agilebydesign-skills** repository root,
   run:

   ```bash
   python skills/abd-skill-catalog/scripts/generate_abd_catalog.py
   ```

   Options:

   - `--repo-root <path>` — defaults to the parent of the repo `skills/`
     directory (detected from this script location).
   - `--output-dir <path>` — overrides `<repo-root>/catalog` if you need a different folder.

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

5. **Catalogue intros (review with an AI or editor).** The opening paragraphs
   on the hub, skills grid, and agents grid are **not** meant to stay as
   throwaway strings in code. They live as HTML in
   `skills/abd-skill-catalog/templates/intros/`:

   - `catalog-hub-intro.html` — hub intro; may use `{{OUTLINE_HREF}}` for the
     outline link (substituted at build time).
   - `catalog-skills-intro.html` — short line above the skills grid (detail
     pages hold the full explanation).
   - `catalog-agents-intro.html` — short line above the agents grid.

   Whenever catalogue behaviour or layout changes—or on a periodic pass—**have
   an AI review these three files** so they stay accurate and in the tone you
   want (they can stay minimal; behaviour details belong on detail pages). The
   script falls back to minimal built-in HTML only if a fragment is missing.

6. **Agent ASCII flows (optional).** For agents where the generic flow blurb is
   not enough, add a `_AGENT_CATALOG_FLOW` entry in
   `scripts/generate_abd_catalog.py` keyed by the agent directory name (under
   `agents/`). Use `abd-delivery-lead` as the pattern: workspace and plan file →
   planning skill → `stages/` roles and gates → bootstrap `abd-team-member` with
   the stage role → validation and supporting skills. Keep it ASCII-only and
   compact; the **Contents** tree below still lists every file with links.

7. **Templates (layout).** HTML shells and CSS live under
   `skills/abd-skill-catalog/templates/` (excluding `intros/`, which are prose
   fragments) and are merged with token replacement. Edit those files to
   change branding or layout without touching Python.

8. **Idempotent.** Running the script twice with the same tree overwrites the
   same outputs deterministically.
