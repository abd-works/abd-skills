<!--
  Parameterized SKILL.md skeleton for agilebydesign-skills.
  Canonical copy: skills/abd-practice-skill-builder/abd-author-practice-skill/templates/SKILL_template.md
  Copy to skills/<your-skill>/SKILL.md and replace every {{PLACEHOLDER}}.
  Shape: thin router — purpose, when-to-use, output file, Agent Instructions (read-gates), Validate.
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

## Output file

**Deliverables folder:** `docs/{{SCAFFOLD_PATH}}/` — see [`common/folder-conventions.md`](../../../../common/folder-conventions.md) for the canonical scaffold tree. The user may name a different path; this is the sensible default.

**Where to write the deliverables (`<deliverables-folder>` resolution):**

1. The path the user told you to use.
2. Where the engagement already keeps deliverables (write next to existing phase output).
3. Canonical scaffold path from `common/folder-conventions.md` (see entry for this skill).
4. The workspace root if none of the above applies.

**File names:** `{{OUTPUT_FILE_NAME}}`. Add a `<name>-` prefix only for disambiguation.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these traps:

- **{{GRILL_TRAP_1_LABEL}}** — {{GRILL_TRAP_1_DESCRIPTION}}
- **{{GRILL_TRAP_2_LABEL}}** — {{GRILL_TRAP_2_DESCRIPTION}}
- **{{GRILL_TRAP_3_LABEL}}** — {{GRILL_TRAP_3_DESCRIPTION}}

---

## Agent Instructions

> **MANDATORY — read every file in `rules/` and `reference/` before authoring any artifact. Do not rely on memory or the SKILL body alone.**

### 1. Read context (MANDATORY before starting)

Read every file in **`reference/`** (if the folder exists). These contain concept definitions, examples, and heuristics that govern what good output looks like.

### 2. Generate

Read every file in **`rules/`**. Author to those rules — treat each DO / DO NOT as a shape contract, not a suggestion.

Produce output using every template in **`templates/`**:

| Template | What to produce |
| --- | --- |
| {{TEMPLATE_ROW_1}} | {{TEMPLATE_ROW_1_DESC}} |
| {{TEMPLATE_ROW_2}} | {{TEMPLATE_ROW_2_DESC}} |

{{BUILD_EXTRA_NOTES_OR_DELETE}}

### 3. Validate (MANDATORY — per-rule verdict required)

Re-read every file in **`rules/`**. For **each rule**, emit a verdict:

```
Rule: <rule-filename>  ->  PASS
Rule: <rule-filename>  ->  FAIL  <offending line or reason>
```

**No rule may be silently skipped.** Then run the scanner pass:

```bash
python skills/common/scripts/run_scanners.py \
  --skill-root skills/{{SKILL_FOLDER_NAME}} \
  --workspace <path-to-output>
```

Fix every FAIL and every scanner violation. No "done" until all rules have a PASS verdict and scanners are green.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers, not a second authoring pass.

- **Who is checking:** {{VALIDATE_WHO_LINE}}
- {{VALIDATE_BULLET_1}}
- {{VALIDATE_BULLET_2}}
- {{VALIDATE_BULLET_3}}

{{VALIDATE_CLOSING_PARAGRAPH}}

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
