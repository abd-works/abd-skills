# Rule: Input traps reference surfaces input ambiguities

**Purpose:** Before an agent generates anything for a practice skill, it must know the assumptions, ambiguities, and missing context that commonly produce bad output for that specific method. Those traps live in **`reference/input-traps.md`** — not in `SKILL.md` and not in grill-me. Grill mode uses them as interview questions; direct generation uses them as a pre-flight check.

## DO

- Ship **`reference/input-traps.md`** for every practice skill that produces stakeholder-facing artifacts from ambiguous input.

  **Example (pass):** `practices/story-driven-delivery/skills/abd-story-mapping/reference/input-traps.md` lists at least three bold-labeled traps specific to story mapping.

- List at least three input traps that are **specific to this skill's method**. Each trap is bold-labeled and names one real failure mode or ambiguity — not generic checklist items.

  **Example (pass):**
  ```markdown
  # Input traps — abd-story-acceptance-criteria

  - **Hidden actors** — who actually triggers this — is "the user" hiding three different actors?
  - **One story or a bundle** — does this story describe one observable interaction, or three behaviors wearing a trenchcoat?
  - **Unstated negative paths** — what should explicitly NOT happen?
  ```

- Keep **`SKILL.md` thin** — no `## Grill prompts` section with inlined traps. Read order is [`common/skill-workflow.md`](../../../../common/skill-workflow.md) § Read-gates; grill mechanics are [`common/grill-me-with-practice-skill.md`](../../../../common/grill-me-with-practice-skill.md).

## DO NOT

- Omit `reference/input-traps.md` when the skill produces artifacts from ambiguous human input.

  **Example (fail):** A practice skill with only `reference/concepts.md` and no input-traps file — agents have no method-specific ambiguity checklist.

- Inline trap lists in `SKILL.md` under `## Grill prompts`.

  **Example (fail):** Ten bold-labeled traps copied into `SKILL.md` instead of `reference/input-traps.md`.

- Conflate input traps with grill-me — traps apply in **all modes**; grill-me is only the interview pattern that turns unresolved traps into questions.

- List only generic traps with no method-specific failure modes.

  **Example (fail):** `"Is your workspace configured?"`, `"Have you read the docs?"` — not input risks for this practice.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
