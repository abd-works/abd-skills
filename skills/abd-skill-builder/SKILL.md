---
name: abd-skill-builder
description: Portable standards, templates, and scaffold for skills.sh-style packages — aligns with structural validation (Python compile validity, build.py, scanners) and the layout rules in this skill’s library. **Rule-bound automation** defaults to **`rules/scanners.json`** + **`build.build_pipeline`** + **`build.scanners`** per **`parts/library/rules-and-scanners.md`**.
---

# Abd skill builder (standards + scaffold)

This skill is the **portable** home for **repository skill standards** and a **CLI scaffold** that emits a compliant directory tree.

**Model:** run **`scaffold_skill.py`** to copy the scaffold into a new folder, then **author** the skill with a human or AI using the library and phase docs. Validate with **`python scripts/base/build.py`** and the configured compile/scanner steps. **No** separate orchestration stack lives in this repo.

| Piece | Role |
|-------|------|
| **Structural validation** | The **gate** on a skill package: `SKILL.md`, `skill-config.json`, Python compile check on configured paths, `scripts/base/build.py`, scanners, optional `rules/scanners.json` bindings. |
| **This skill (`abd-skill-builder`)** | **Normative docs** under **`content/parts/library/`**, **`skill-scaffold/`**, and **`scripts/scaffold_skill.py`** so you can **create a skill from scratch** without hand-copying the toy fixture. |

Use **`Skill structure and concepts.md`** for repo map, pipeline, and checklist norms; **`rules-and-scanners.md`** for merge, compile paths, scanners, and **`build.build_pipeline`**.

## When to use

- Starting a **new** skill under `agilebydesign-skills/skills/`.
- Auditing an existing skill against **§3** directory and validation rules.
- Feeding **standards** into prompts without pasting long excerpts.

## Commands

```bash
# Emit a new skill skeleton (SKILL.md, skill-config.json, content/, scripts/, rules/)
python scripts/scaffold_skill.py --name my-skill --out /path/to/my-skill

# Build AGENTS.md + content/built/ (static_built)
python scripts/base/build.py
```

- **Workspace and config:** **`parts/phases/workspace-and-config.md`** (phase document under **`parts/phases/`**)
- **Delivery / merge order / `content/built/`:** **`README.md`** (section *Delivery & merge order*)
- **Repo map, §3 layout (tables), checklists:** **`content/parts/library/skill-structure-and-concepts.md`** and **`content/parts/library/base/checklist.md`** — where things go; stages/phases/steps; process tables; how checklist files are created (stable **`library/base/`** vs workspace **`progress/`**).
- **Plan skill migration** (**1b** — inventory + **standards-delta** + user picks **IDs**): **`parts/phases/plan-migrate.md`**
- **Migrate existing skill** (**2b** — execute **1b**): **`parts/phases/migrate.md`**
- **Team process plate** (rich **`process.md`** like **abd-maps-models-specs**): **`parts/library/process-phases.md`** (*Team process plate*, process table columns, IDE usage, `generate.py` / `build.py`).
- **Rules in AI-chat phase bundles:** declare **`phase_rules`** and optional **`every_phase_rules`** in **`skill-config.json`** (rule file stem = basename without `.md`). **`scripts/instructions.py`** inlines them in **`phase_bundle`** order; see **`parts/library/process-phases.md`** (*Default `phase_bundle` order*). Scaffold starts from **`skill-scaffold/skill-config.json`**.
- **Phase markdown files:** use **descriptive kebab-case slugs** (`story-map.md`, `terms-mechanisms.md`) — **not** `phase-00-…` filenames or `# Phase N —` H1 titles. Pipeline order lives in **`process.md`** (# column) and **`build.py`**’s merge list (§3.1 table + naming bullets in **`Skill structure and concepts.md`**).

## See also

- **`README.md`** — delivery merge order, junction install, quick start.
