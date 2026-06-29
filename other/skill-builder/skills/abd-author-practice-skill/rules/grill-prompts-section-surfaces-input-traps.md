# Rule: Input traps reference surfaces input ambiguities

**Purpose:** Before an agent generates anything for a practice skill, it must know the assumptions, ambiguities, and missing context that commonly produce bad output for that specific method. Those traps live in **`reference/input-traps.md`** — a silent pre-flight check in **every** run. They are **not** grill questions and **not** inlined in `SKILL.md`.

## DO

- Ship **`reference/input-traps.md`** for every practice skill that produces stakeholder-facing artifacts from ambiguous input.

  **Example (pass):** `practices/story-driven-delivery/skills/abd-story-mapping/reference/input-traps.md` lists at least three bold-labeled traps specific to story mapping.

- List at least three input traps that are **specific to this skill's method**. Each trap is bold-labeled and names one real failure mode or ambiguity — not generic checklist items.

- Ship **`reference/grill-me.md`** separately for grill interview questions — see rule **Grill me reference holds interview questions**.

- Keep **`SKILL.md` thin** — index sections point to `reference/input-traps.md` and `reference/grill-me.md`; no inlined trap or grill lists.

## DO NOT

- Omit `reference/input-traps.md` when the skill produces artifacts from ambiguous human input.

- Use `input-traps.md` as grill questions — grilling uses **`reference/grill-me.md`** only.

- Inline trap lists in `SKILL.md` under `## Grill me` or `## Grill prompts`.

- Conflate input traps with grill-me — different files, different jobs.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
