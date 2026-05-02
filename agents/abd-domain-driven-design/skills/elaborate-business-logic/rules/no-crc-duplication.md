---
---

# Rule: No CRC duplication

The business-logic section must not duplicate CRC "Responsible for" or "Collaborators" prose. Only lifecycle and invariant elaboration belongs here. Passing means the business-logic content adds new lifecycle and invariant detail without restating CRC responsibilities. Failing means CRC text has been copied or paraphrased into the business-logic section.

## DO

- Reference a CRC concept by name and add only lifecycle states, transitions, and invariants.

  **Example (pass):**
  ```
  ### Power Level
  #### State / lifecycle
  States: base, shifted
  Transitions: base → shifted (power-level shift applied), shifted → base (shift expires)
  #### Invariants
  - Effective power level must never drop below 0.
  ```

- Keep CRC responsibilities in the CRC section and elaborate only the state/invariant dimension here.

  **Example (pass):** The CRC says "Responsible for: tracking current power level and applying shifts." The business-logic section adds lifecycle states and invariants without repeating that sentence.

## DO NOT

- Copy or paraphrase CRC "Responsible for" lines into the business-logic section.

  **Example (fail):**
  ```
  ### Power Level
  Responsible for tracking current power level and applying shifts.
  #### State / lifecycle
  ...
  ```

- Reproduce collaborator lists from the CRC.

  **Example (fail):**
  ```
  ### Attack
  Collaborates with: Target Defence, Damage, Effect
  #### State / lifecycle
  ...
  ```
