# Rule: Behavior and its produced result on the same bullet

**Scanner:** Manual review

When a behavior bullet directly produces a result, the result appears on the same bullet using a connective phrase like `, producing a *result*`. Passing means every cause-and-effect pair is one bullet. Failing means a behavior is split across two bullets where the second is just "produces a [result]".

## DO

- Combine behavior and its immediate output on the same bullet.

  **Example (pass):**
  ```
  - is resolved by *rolling* a *d20*, comparing the *roll total* to the *difficulty class*,
    producing a *check result*
  ```

## DO NOT

- Split a behavior and its directly-produced result across two bullets.

  **Example (fail):**
  ```
  - is resolved by *rolling* a *d20*, comparing the *roll total* to the *difficulty class*
  - produces a *check result*            ← belongs on the previous bullet
  ```

**Source:** Inherited from abd-domain-language — behavior and produced result on the same bullet.
