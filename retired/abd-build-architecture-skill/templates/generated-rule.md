<!--
  Template: ONE rule file in a generated architecture-implementation skill.
  This is the OUTPUT of abd-build-architecture-skill, copied per principle
  from the architecture reference.

  Naming: rules/<principle-slug>.md
  The basename describes the VALID state the rule guards
  (e.g. maintain-layer-purity.md, handle-errors-at-boundary.md).
  Delete this comment block before shipping.
-->

---
{{# Add `scanner: <stem>` ONLY if scanners/<stem>-scanner.py exists in the generated skill. Otherwise omit the YAML block entirely. #}}
---

### Rule: {{Principle title as a positive outcome}}

{{One-or-two-paragraph statement of pass and fail for this principle, taken from the reference's "Principle:" line plus a sentence on what failure looks like in real code. Avoid jargon the reference does not use. Cite the source mechanism inline so a reviewer can find it: "from the {{MechanismName}} section of inputs/architecture-reference.md".}}

#### DO

- {{Forward-looking instruction tied directly to the principle.}}

  **Example (pass):**

  ```{{language}}
  {{Code that follows the reference's named pattern.}}
  ```

- {{Second forward-looking instruction (often: where the pattern lives in the folder tree).}}

  **Example (pass):** {{Concrete file path or test helper invocation showing the pattern in context.}}

#### DO NOT

- {{The anti-pattern named in the reference walkthrough.}}

  **Example (fail):**

  ```{{language}}
  {{Code that violates the principle — typically the "WRONG" example from the reference walkthrough.}}
  ```

- {{A common drift the reference does not name but that the generating agent has seen before.}}

  **Example (fail):** {{Concrete failing fragment with one sentence of why it fails.}}

**Source:** `inputs/architecture-reference.md` — section "Mechanism: {{MechanismName}}", under "Principles & Patterns".
