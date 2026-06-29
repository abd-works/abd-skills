# Rule: Grill me reference holds interview questions

**Purpose:** Grill mode asks the user questions one at a time before generating. Interview questions live in **`reference/grill-me.md`** — not in `SKILL.md`, not in `input-traps.md`, not in `common/grill-me-with-practice-skill.md` (mechanics only).

## DO

- Ship **`reference/grill-me.md`** for every practice skill that supports grill mode.

  **Example (pass):** `reference/grill-me.md` opens with a link to `common/grill-me-with-practice-skill.md` for mechanics, then lists method-specific questions to ask one at a time.

- List at least three interview questions specific to this skill's method — phrased to ask the user, not as silent pre-flight checks.

- Point **`SKILL.md` § Grill me** at **`reference/grill-me.md`** only.

## DO NOT

- Put grill questions in **`reference/input-traps.md`** — traps are pre-flight checks in every run.

- Put question lists in **`common/grill-me-with-practice-skill.md`** — that file is shared mechanics only.

- Inline grill questions in **`SKILL.md`**.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
