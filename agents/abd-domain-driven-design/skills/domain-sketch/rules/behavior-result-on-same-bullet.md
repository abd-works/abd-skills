# Rule: Behavior and its produced result on the same bullet

**Scanner:** Manual review

When a behavior bullet directly produces a result, the result must appear on the same bullet as the behavior — not as a separate bullet immediately following it. Passing means cause and effect are combined on one line. Failing means a bullet describes a behavior and the next bullet says only "produces a [result]" or "returns a [result]."

## DO

- Combine a behavior and its immediate output on the same bullet using ", producing a [result]" or a similar connective phrase.

  **Example (pass):** `- is resolved by *rolling* a *d20*, adding the *trait rank* and the *circumstance modifier* and comparing the *roll total* to the *difficulty class*, producing a *check result*`

- Use a separate bullet for a result only when the result has its own standalone significance not already captured on the behavior bullet.

  **Example (pass):** `- accumulates *degrees of failure*` and separately `- a third *degree of failure* means death` — the second is a threshold rule, not just "produces a result."

## DO NOT

- Write a behavior bullet and then immediately follow it with a standalone "produces a [result]" bullet.

  **Example (fail):**
  ```
  - is resolved by *rolling* a *d20*, comparing the *roll total* to the *difficulty class*
  - produces a *check result*
  ```
  The second bullet adds nothing the first does not imply — merge them.

- Split cause and effect across two bullets when the result has no content of its own beyond being the output.

  **Example (fail):** `- applies the *modifier* to the *roll*` followed by `- returns the *modified total*` — the return is part of the behavior, not a separate fact.

**Source:** Correction log entry — domain-sketch skill (check-resolution engagement).
