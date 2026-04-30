---
scanner: resolutions-before-abstractions
---

# Rule: Resolutions before abstractions

Every `## Module:` section (or the flat file when no modules exist) must have a `### Resolutions` block before the first `### Key Abstraction:`. This documents the settle pass — merges, splits, promotions, demotions, and closure of identification-phase tensions. Passing means `### Resolutions` appears and precedes the first abstraction. Failing means it is missing or appears after.

## DO

- Place `### Resolutions` immediately after the module heading (and optional one-liner) but before the first `### Key Abstraction:`.

  **Example (pass):**
  ```
  ## Module: [Funds Transfer]

  ### Resolutions

  - **Merge / Split / Promotion / Demotion:** None.
  - **Wire Transfer vs Funds Transfer:** Closed — both retained. Evidence: …

  ### Key Abstraction: Funds Transfer
  ```

- In flat files (no `## Module:`), place `### Resolutions` under the H1 / front matter, before the first `### Key Abstraction:`.

  **Example (pass):** `### Resolutions` at line 8, first `### Key Abstraction:` at line 15.

- State explicitly when no structural moves occurred: "None" or "No merges, splits, promotions, or demotions."

  **Example (pass):** `- **Merge / Split / Promotion / Demotion:** None (two abstractions retained as-is).`

## DON'T

- Omit `### Resolutions` entirely from a module section.

  **Example (fail):** `## Module: [Payments]` followed directly by `### Key Abstraction: Payment` with no Resolutions block between them.

- Place `### Resolutions` after one or more `### Key Abstraction:` sections.

  **Example (fail):** Two Key Abstractions listed, then `### Resolutions` appears at the bottom of the module.

- Leave draft `Tension:` lines unaddressed — every tension from identification must be closed in Resolutions or listed under `### Deferred tensions`.

  **Example (fail):** `Tension: Possible merge with Settlement` on a Key Abstraction but no mention of it in `### Resolutions` or `### Deferred tensions`.
