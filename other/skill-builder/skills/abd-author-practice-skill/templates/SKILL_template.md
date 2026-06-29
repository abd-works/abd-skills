<!--
  Parameterized SKILL.md skeleton for agilebydesign-skills.
  Canonical copy: skills/abd-practice-skill-builder/abd-author-practice-skill/templates/SKILL_template.md
  Copy to skills/<your-skill>/SKILL.md and replace every {{PLACEHOLDER}}.
  Shape: thin router — purpose, when-to-use, Agent Instructions (mandatory skill-workflow read-gates). Optional human index sections (Read, Input traps, Grill me, Generate, Validate) — one ref per section; link all paths as [`path`](path); § names plain (headings in skill-workflow).
  Rules live in rules/*.md only. Concept teaching lives in reference/*.md only. Nothing inlined here.
-->

---
name: {{SKILL_NAME}}
description: >-
  {{SKILL_DESCRIPTION_WHAT_IT_PRODUCES}}. Use when {{SKILL_DESCRIPTION_USE_WHEN_SITUATION}}.
---
# {{SKILL_DISPLAY_NAME}}

## Purpose

{{SKILL_PURPOSE_ONE_PARAGRAPH}}

**Authoring note:** Write **one** paragraph only — **why** this packaged practice exists, **who** it helps, **what** becomes possible when the method is used well, and **how** this page supports that — in plain language. Do **not** put repository paths, `Manual:`, which template to copy, hub retrieval filenames, scanner wiring, or other **package / agent mechanics** here; those belong in **Prerequisites** and **Build**.

---

## Example: how the opening can read (fictional practice)

**For authors only:** Mirror this for **tone and depth**, then **delete this whole section** from the **`SKILL.md`** you ship so practitioners see one real practice, not a sample.

### Purpose (illustrative — replace `{{SKILL_PURPOSE_ONE_PARAGRAPH}}`)

Release train planning helps teams sequence work across fixed dates so dependencies and scope stay honest before anyone commits. This skill packages that facilitation pattern so product owners and delivery leads can run the same conversations (with or without an agent) and leave with a comparable, board-ready plan.

### When to use this skill (illustrative — replace the bullets under `{{WHEN_TO_USE_BULLET_*}}`)

Load this skill when **any** of the following apply:

- You have a backlog slice and need to **map it to calendar milestones** without hiding risk.
- Stakeholders are **trading scope for date** and need a **single shared picture** of what can ship when.
- You are **standing up a release train** and want **one** method page instead of ad hoc slide decks.

---

## When to use this skill

Load this skill when **any** of the following apply:

- {{WHEN_TO_USE_BULLET_1}}
- {{WHEN_TO_USE_BULLET_2}}
- {{WHEN_TO_USE_BULLET_3}}
- {{WHEN_TO_USE_BULLET_4}}

## Agent Instructions

**MANDATORY:** [`common/skill-workflow.md`](../../../../common/skill-workflow.md) — read in full; complete § Read-gates before generating or validating.

## Read

§ Read-gates — all of [`rules/`](rules/), [`reference/`](reference/), [`templates/`](templates/).

## Input traps

[`reference/input-traps.md`](reference/input-traps.md) — pre-flight in every run, not grill-only.

## Grill me

[`reference/grill-me.md`](reference/grill-me.md) — only when the invocation includes "grill me".

## Generate

[`reference/generate.md`](reference/generate.md) when present; otherwise [`rules/`](rules/) + [`templates/`](templates/).

## Output

[`reference/output.md`](reference/output.md) — only when the skill breaks the default `docs/` path.

## Validate

§ Validate output + practice `validate-checklist.md` when the family ships one.

## Diagram workflow

[`reference/diagram-workflow.md`](reference/diagram-workflow.md) — only when the skill produces diagram outputs.

---

## Deploy

This skill ships IDE-deployable files under **`ide-files/`**. Deploy them to any project:

```powershell
.\agents\abd-practice-skill-builder\skills\abd-author-practice-skill\scripts\Deploy-SkillOutputs.ps1 -SkillPath skills/{{SKILL_FOLDER_NAME}} -ProjectRoot <target-project> -Force
```

Default **`-IDE Cursor`**. Use **`-IDE Both`** when the target project should also receive **`.vscode/*.instructions.md`** and **`.github/prompts/*.prompt.md`**.

After editing `.mdc` or `.instructions.md`, validate parity (use an **absolute** `--workspace` path):

```bash
python skills/common/scripts/run_scanners.py \
  --skill-root skills/abd-practice-skill-builder/abd-author-practice-skill \
  --workspace /absolute/path/to/repo/skills/{{SKILL_FOLDER_NAME}}
```
