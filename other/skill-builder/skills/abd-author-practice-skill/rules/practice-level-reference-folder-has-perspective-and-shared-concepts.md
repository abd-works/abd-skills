# Rule: Practice-level reference folder has perspective and shared concepts

**Purpose:** A practice family groups related skills under `practices/<family-name>/`. The family-level `reference/` folder is where the fidelity ladder and shared cross-skill concepts live — owned once, linked to by every skill that needs them. Without this, each skill either duplicates the same concept prose or invents its own framing, and the family's coherence is invisible to anyone picking up a single skill.

## DO

- Create `practices/<family-name>/reference/` when authoring or maintaining a practice family.

  **Example (pass):** `practices/behavior-driven-development/reference/` exists alongside the `skills/` and `README.md` at the family root.

- Include a `<family>-perspective.md` file at that level. It must have: the perspective key, what question the practice answers, the owning agent (if one exists), and the fidelity ladder table (fidelity level, skill name, mode).

  **Example (pass):**
  ```markdown
  # BDD Perspective

  **Key:** `engineering`

  **What it answers:** How is behavior discovered, structured, and implemented as tested code?

  **Skills by fidelity:**

  | Fidelity    | Skill                   | Mode            |
  |-------------|-------------------------|-----------------|
  | Exploration | `abd-bdd-behavior`      | bdd-scaffold    |
  | Spec        | `abd-bdd-specification` | bdd-signature   |
  | Engineering | `abd-bdd-development`   | bdd-development |
  ```

- When two or more skills in the family share a concept, vocabulary, or cross-cutting discipline, place it in a shared reference file at the practice level — not duplicated inside each skill's `reference/concepts.md`. Each skill's concepts file may link to the shared file.

  **Example (pass):** `practices/domain-driven-design/reference/oo-concepts.md` is owned once; `abd-domain-language`, `abd-domain-model`, and `abd-domain-specification` each link to it rather than restating OO theory independently.

  **Example (pass):** `practices/story-driven-delivery/reference/handling-incomplete-context.md` is linked from multiple skills rather than copied into each.

## DO NOT

- Omit the practice-level `reference/` folder when the family has two or more skills.

  **Example (fail):** `practices/behavior-driven-development/` contains only `skills/` and `README.md` — no `reference/` folder, so there is no perspective file and no shared concept anchor.

- Put the perspective file inside an individual skill's `reference/` folder.

  **Example (fail):** `practices/behavior-driven-development/skills/abd-bdd-behavior/reference/bdd-perspective.md` — this belongs at the practice level, not inside a single skill.

- Duplicate shared concept prose across multiple skills' `reference/concepts.md` files when a single family-level file would serve all of them.

  **Example (fail):** `abd-bdd-behavior/reference/concepts.md`, `abd-bdd-specification/reference/concepts.md`, and `abd-bdd-development/reference/concepts.md` each contain identical paragraphs explaining what BDD is and how the three phases relate — the same text in three files.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
