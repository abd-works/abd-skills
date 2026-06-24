# Rule: Grill prompts section surfaces input traps

**Purpose:** Before an agent generates anything for a practice skill, it must surface the assumptions, ambiguities, and missing context that most commonly produce bad output for that specific method. The `## Grill prompts` section makes those traps explicit and links to the shared grill-me interview pattern. Every practice `SKILL.md` must have one.

## DO

- Include a `## Grill prompts` section in every practice `SKILL.md`. Place it before `## Agent Instructions`.

  **Example (pass):** The section exists between `## Output file` and `## Agent Instructions`, or between the title block and `## Purpose` when the skill positions it at the top.

- Open the section with exactly this line, before any other content:

  ```
  Read `common/grill-me-with-practice-skill.md` before grilling.
  ```

  **Example (pass):**
  ```markdown
  ## Grill prompts

  Read `common/grill-me-with-practice-skill.md` before grilling.

  Before generating, surface these traps:

  - **Hidden actors** — ...
  ```

- List at least three input traps that are **specific to this skill's method**. Each trap is bold-labeled and names one real failure mode or ambiguity that commonly causes bad output for this practice — not generic checklist items.

  **Example (pass) — abd-story-acceptance-criteria:**
  ```markdown
  - **Hidden actors** — who actually triggers this — is "the user" hiding three different actors with different journeys and different expectations of "done"?
  - **One story or a bundle** — does this story describe one observable interaction, or is it actually three behaviors wearing a trenchcoat?
  - **Unstated negative paths** — what should explicitly NOT happen? Every happy path has a shadow.
  ```

  **Example (pass) — abd-bdd-specification:**
  ```markdown
  - **Scaffold completeness** — is the behavior hierarchy fully approved, or are there blocks with open questions?
  - **Framework choice** — is the target framework confirmed? Jest and Mamba have different nesting syntax.
  - **Hierarchy fidelity** — does every level of the hierarchy have a code equivalent?
  ```

## DO NOT

- Omit the `## Grill prompts` section from a practice `SKILL.md`.

  **Example (fail):** A `SKILL.md` that goes from `## Output file` directly to `## Agent Instructions` with no grill prompts section.

- Omit the `Read \`common/grill-me-with-practice-skill.md\` before grilling.` line, or bury it after other content.

  **Example (fail):**
  ```markdown
  ## Grill prompts

  Before generating, surface these traps:

  - **Hidden actors** — ...

  Read `common/grill-me-with-practice-skill.md` for the full interview pattern.
  ```
  The reference appears after the traps instead of first.

- Use the section to describe how the skill works or what it produces — that belongs in Purpose and Agent Instructions.

  **Example (fail):**
  ```markdown
  ## Grill prompts

  This skill turns a story map into acceptance criteria. Ask the user for the story map path and which stories are in scope.
  ```

- List only generic traps that apply equally to every skill with no traps that name a real failure mode specific to this method.

  **Example (fail):** Three traps that are `"Is your workspace configured?"`, `"Have you read the docs?"`, `"Do you have the right permissions?"` — none of these surface a real input risk for the practice being packaged.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
