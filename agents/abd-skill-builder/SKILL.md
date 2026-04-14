---
name: abd-skill-builder
description: Portable standards, templates, and scaffold for Open Agent Skills packages — library under content/parts/library/, emit via skills/build_skill/scripts/build_skill.py, validate via rules, scanners, build.py. Full validation workflow lives in skills/execute_rules/.
---

# Abd skill builder (standards + scaffold)

This repo is the **portable** home for **skill repository standards** and a **CLI** that emits a compliant tree, plus **phased authoring** merged into **`AGENTS.md`**.

**Model:** emit a new package with **`skills/build_skill/scripts/build_skill.py`**, author using **`content/parts/`** (library + phases + **`process.md`**), then run validation through **`skills/execute_rules/`** (deep rule pass → generate → **`build.py`** / scanners → final AI pass + corrections log). Orchestration for *this* package is **`AGENTS.md`**; discovery is this **`SKILL.md`**. See **`content/parts/library/base/agent-skill-model.md`**.

| Piece | Role |
| --- | --- |
| **Structural + rules validation** | **`skills/execute_rules/SKILL.md`** — gate table, layers, scanners, corrections (the former “everything in root SKILL” validation story). |
| **Normative docs** | **`content/parts/library/`** (e.g. **skill-structure-and-concepts**, **rules-and-scanners**, **critical-quality-steps**). |
| **Emit skeleton** | **`skills/build_skill/scripts/build_skill.py`** → **`skills/build_skill/templates/skill-scaffold/`**. |

## When to use

- New skill under **`agilebydesign-skills`** (or elsewhere).
- Audit against **§3** in **skill-structure-and-concepts**.
- Standards for prompts without pasting long excerpts.

## Commands

```bash
# New skill skeleton (from abd-skill-builder repo root)
python skills/build_skill/scripts/build_skill.py --name my-skill --out /path/to/my-skill

# Merge AGENTS.md / built slices + post-merge pipeline (from target skill root)
python scripts/base/build.py```

**Full validation workflow (deep rules, scanners, final pass):** open **`skills/execute_rules/SKILL.md`**.

## Pointers

- **Workspace:** **`content/parts/phases/workspace-and-config.md`**
- **Delivery / merge:** root **`README.md`**
- **Layout §3:** **`content/parts/library/base/skill-structure-and-concepts.md`**; checklists: **`skills/track_task/`**
- **Rules + scanners:** **`content/parts/library/base/rules-and-scanners.md`**
- **Quality layers + corrections:** **`content/parts/library/base/critical-quality-steps.md`**
- **Builder operations model:** **`content/builder-architecture.md`**

## See also

- **`README.md`** — quick start, junction install.
