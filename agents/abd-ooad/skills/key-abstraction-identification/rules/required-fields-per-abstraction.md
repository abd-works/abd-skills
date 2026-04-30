---
scanner: required-fields-per-abstraction
---

# Rule: Required fields per abstraction

Every `### Key Abstraction:` section must carry all four required fields — **Intent**, **Core terms** (bullet list), **Shape hint**, and at least one verbatim extract — so the next skill in the pipeline has a complete, self-contained unit to work from. Passing means every abstraction has all four present and non-empty. Failing means any abstraction is missing a field or has a placeholder-only stub.

## DO

- Include an `Intent:` line with a complete, source-grounded sentence for every Key Abstraction.

  **Example (pass):** `Intent: The atomic operation that moves a specified amount from one account to another.`

- Include a `Core terms` header followed by at least one `- phrase` bullet.

  **Example (pass):**
  ```
  Core terms (absorbed from this module's Core terms list):
  - funds transfer
  - source account / destination account
  ```

- Include a `Shape hint:` line with free-form prose (not a `<<Tag>>`).

  **Example (pass):** `Shape hint: Both noun-shaped and verb-shaped — a thing-with-state and a named procedure.`

- Include at least one `**Extract — …**` block with a verbatim ```` ```source ```` body.

  **Example (pass):** An abstraction with two extracts, one whole and one partial.

## DON'T

- Leave an abstraction with no `Intent:` line or only `Intent: …` / `Intent: {{placeholder}}`.

  **Example (fail):** A `### Key Abstraction: Wire Transfer` section with no `Intent:` line at all.

- Omit `Core terms` entirely or have zero bullet items under the header.

  **Example (fail):** `Core terms:` followed by blank lines and then the next heading.

- Skip the `Shape hint:` or use a stereotype tag instead of prose.

  **Example (fail):** `Shape hint: <<Entity>>` — tags are not allowed at this rung.

- Have a Key Abstraction with zero `**Extract — …**` blocks.

  **Example (fail):** Name + Intent + Core terms + Shape hint present, but no source extracts at all.
