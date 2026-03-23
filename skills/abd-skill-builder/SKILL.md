---
name: abd-skill-builder
description: Portable standards, templates, and scaffold for skills.sh-style packages — aligns with Operator checks (Python compile validity, build.py, scanners) and the layout rules in this skill’s library. **Rule-bound automation** defaults to **`rules/scanners.json`** + **`operator.build_pipeline`** + **`operator.scanners`** per **`parts/library/rules-and-automated-checks.md`**.
---

# Abd skill builder (standards + scaffold)

This skill is the **agent-portable** home for **repository skill standards** and a **CLI scaffold** that emits a compliant directory tree.

## Relationship to `agentic-skill-builder`

| Piece | Role |
|-------|------|
| **`agentic-skill-builder`** (Python package) | **Orchestration** (ingest → strategize → … → **operator** → expert). Structural validation is **`operator.run_operator()`** — not the graph’s optional builder stub. |
| **`operator.run_operator()`** | The **structural gate**: `SKILL.md`, `skill-config.json`, Python compile check on configured paths, `scripts/build.py`, scanners, optional `rules/scanners.json` bindings. |
| **This skill (`abd-skill-builder`)** | **Normative docs** under **`content/parts/library/`**, **templates**, and **`scripts/scaffold_skill.py`** so agents/humans can **create a skill from scratch** without hand-copying the toy fixture. |

Use **`content/parts/library/builder-vs-operator.md`** for **scaffold/generation** vs **Operator validation**.

## When to use

- Starting a **new** skill under `agilebydesign-skills/skills/`.
- Auditing an existing skill against **§3** directory and operator rules.
- Feeding **standards** into prompts without pasting long excerpts.

## Commands

```bash
# Emit a new skill skeleton (SKILL.md, skill-config, conf/, content/, scripts/, rules/)
python scripts/scaffold_skill.py --name my-skill --out /path/to/my-skill

# Build AGENTS.md + content/built/ (static_built)
python scripts/build.py
```

- **Workspace and config:** **`parts/phases/workspace-and-config.md`** (phase document under **`parts/phases/`**)
- **Delivery / merge order / `content/built/`:** **`README.md`** (section *Delivery & merge order*)
- **Full §3 (all tables and subsections):** **`parts/library/skill-standards-section-3.md`** — **what** to put where (stages/phases/steps, process tables, optional domain+story-map pattern, rule naming, static vs dynamic assembly).
- **Index + Operator checklist:** **`parts/library/skill-repo-standards.md`**
- **Authoring checklist** (human + AI — rules/scanners, library, cross-cutting concepts, delivery mode, `test/` folder, sign-off): **`parts/library/authoring-checklist.md`** — norms are worked in **`<skill>/docs/skill-plan.md`** under **## Authoring checklist** (scaffold injects; not kept under **`abd-skill-builder/docs/`**).
- **Plan skill migration** (**1b** — inventory + **standards-delta** + user picks **IDs**): **`parts/phases/plan-migrate.md`**
- **Migrate existing skill** (**2b** — execute **1b**): **`parts/phases/migrate.md`**
- **Team process plate** (rich **`process.md`** like **abd-maps-models-specs**): **`templates/process-team.md.template`** — see **`parts/library/process-approach.md`** (*Team process plate*).
- **Rules in AI-chat phase bundles:** declare **`phase_rules`** and optional **`every_phase_rules`** in **`skill-config.json`** (rule file stem = basename without `.md`). **`scripts/instructions.py`** inlines them in **`phase_bundle`** order; see **`parts/library/process-approach.md`** (*Default `phase_bundle` order*). Scaffold template: **`templates/skill-config.json.template`**.
- **Phase markdown files:** use **descriptive kebab-case slugs** (`story-map.md`, `terms-mechanisms.md`) — **not** `phase-00-…` filenames or `# Phase N —` H1 titles. Pipeline order lives in **`process.md`** (# column) and **`build.py`**’s merge list (§3.1 table + naming bullets in **`skill-standards-section-3.md`**).

## See also

- **`../agentic-skill-builder/README.md`** — Python package that runs **`operator.run_operator()`** against a skill directory.
