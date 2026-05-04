# Rule: One behavior per line

**Scanner:** Manual review

Each bullet in a domain sketch concept block must express exactly one behavior, one responsibility, or one interaction. Do not merge multiple behaviors onto a single line. Lines that combine a state description with its triggered action, or that chain two interactions together with a colon or semicolon, must be split.

## DO

- Write one behavior per bullet.

  **Example (pass):**
  ```
  - may be *ongoing* for a target *character*
  - requires a *resistance check* at the end of each *ongoing target*'s turn until ended
  ```

  **Example (pass):**
  ```
  - *supersedes* a less severe *condition* from the same source — removing the lesser
  - is *superseded by* a more severe *condition* that overrides it
  ```

## DO NOT

- Merge a state with its triggered behavior on one line.

  **Example (fail):** `- may be **ongoing** for a target *character*: requires a *resistance check* at the end of each of the target's turns until ended`
  → Split into two lines: the `is ongoing` state and the `requires resistance check` behavior.

- Chain two distinct interactions with a colon, semicolon, or "and."

  **Example (fail):** `- is resolved by rolling a d20 and comparing the roll total to the difficulty class, producing a check result`
  → Split: resolution behavior on one line; result production on the same line only if the result is the direct and only output of that single behavior (see behavior-result-on-same-bullet rule).

## Note on behavior-result-on-same-bullet

When a single behavior directly and exclusively produces one result, the result may stay on the same line:

  **Example (pass):** `- is resolved by *rolling* a *d20*, adding *trait rank* and *circumstance modifier* and comparing to the *difficulty class*, producing a *check result*`

This is the only exception — it applies when the result is the sole output of the behavior, not a separate triggered action.

**Source:** Engagement convention (domain-sketch skill).
