# Phase: Scaffold

For an **existing** skill tree (not greenfield), use **[`migrate.md`](migrate.md)** instead: produce a **delta report**, then **only fix** what the user selects.

## Steps (greenfield)

1. **Authoring checklist:** Open **[`../library/authoring-checklist.md`](../library/authoring-checklist.md)** (in **abd-skill-builder**; copy into **your new skill** as `docs/authoring-checklist.md` — scaffold does this). Work **A → B → C** (ask questions, AI suggestions, check boxes) for build intent, rules/scanners, library, cross-cutting concepts, **`delivery.mode`**, then operator sign-off.
2. Choose a **skill id** (directory name; kebab-case recommended).
3. Run `python scripts/scaffold_skill.py --name <id> --out <parent>/<id>`.
4. Edit `conf/build-strategy.json` — set **`skill_purpose`** (required for `strategy_complete` in the delivery graph). Add other keys from the template as needed; they are **separate fields**, not part of the **`skill_purpose`** string.
5. Flesh out **`content/parts/process.md`** and phase files. For a **rich** process doc (outcome, principles, inputs/outputs, staged tables like **abd-maps-models-specs**), copy/adapt **`content/parts/templates/process-team.md.template`** (team process plate) from **abd-skill-builder**; see **`library/process-approach.md`** → *Team process plate*. Add rules and scanners as needed (see checklist §2–5).
6. Add tests under **`test/`** (scaffold emits **`test/README.md`**); put fixtures in **`test/fixture/…`** and any **`active_skill_workspace`** under **`test/<name>/`** per **[`../library/skill-repo-standards.md`](../library/skill-repo-standards.md)**.
7. Run `python scripts/build.py`, then `agentic-skill-builder run --skill-path <path>` or equivalent Operator checks.

## Anchor

This phase **writes** the skill tree and **establishes** the operator contract — no domain modeling yet.
