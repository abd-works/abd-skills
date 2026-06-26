# Rule: Rule DOs and DON'Ts must each have examples

**Scanner:** Manual review

Under **`## DO`**, every bullet must be followed by at least one **Example (pass):** with enough quoted or paraphrased content to show the shape, not a one-word stub. Under **`## DO NOT`**, every bullet must be followed by at least one **Example (fail):** the same way, in normal markdown (bullet then example lines). When several bullets share one vague example at the bottom, or examples do not map to a specific bullet, the rule fails.

## DO

- After **each** **`## DO`** bullet, add **Example (pass):** with a concrete fragment, path, or multi-line quote so someone can imitate it.

  **Example (pass):** Bullet: “**DO** include a filled example in each promised template.”  
  **Example (pass):** In **`templates/story-map.md`**, an **Example** section shows a full mini map with real epic titles and user tasks, not only `{{EPIC}}` tokens — enough depth that a complex generation has a clear target.

- After **each** **`## DO NOT`** bullet, add **Example (fail):** showing the violation with the same level of detail.

  **Example (pass):** Correct pairing of a **DO NOT** bullet with a concrete **Example (fail):**

  - **DO NOT** ship a template that is only headings and placeholders.

    **Example (fail):** **`templates/foo.md`** has **## Instructions**, **## Fields**, and fifteen lines of **`{{PLACEHOLDER}}`** but **no** subsection where one row is filled with plausible prose — nothing to copy for tone or depth.

## DO NOT

- Attach **one** **Pass** / **Fail** pair at the end that does not clearly illustrate **each** bullet above.

  **Example (fail):** Three **DO** bullets about templates, retrieval, and **Validate**; only **Pass:** “Opening reads well” — leaves the other bullets without an example.

- Use **Example (fail):** that repeats the bullet with no sample text.

  **Example (fail):** Bullet: “**DO NOT** omit examples.” **Example (fail):** “When examples are missing.” — not a showable artifact.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
