# Templates — authoring instructions

These files are **instructions for what to write**, not copy-paste starters. Each one explains the purpose, required fields, and authoring decisions for its counterpart in a built skill.

The filled scaffold versions — the actual ready-to-edit files dropped into a new skill — live in **`skill-scaffold/`** (sibling of this folder).

| File | What it documents |
|------|-------------------|
| [`abd-config.json.template.md`](abd-config.json.template.md) | How to fill `conf/abd-config.json` — workspace routing keys |
| [`process.md.template`](process.md.template) | How to write a minimal `content/parts/process.md` |
| [`process-team.md.template`](process-team.md.template) | How to write a rich multi-stage `process.md` with outcome, principles, and per-stage tables |
| [`skill-config.json.template`](skill-config.json.template) | How to fill every field in `skill-config.json` |
| [`skill-plan.md.template`](skill-plan.md.template) | How to fill `docs/skill-plan.md` — the Stage 1 planning document |

## Relationship to skill-scaffold/

`skill-scaffold/` contains the actual scaffold files with real structure and inline comments. `templates/` tells you **why** each field or section exists and what decisions to make when filling it in.

Read the relevant `templates/` doc first to understand the shape, then edit the corresponding file in your new skill (copied from `skill-scaffold/`).
