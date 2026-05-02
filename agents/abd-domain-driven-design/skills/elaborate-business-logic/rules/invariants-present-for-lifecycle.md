---
---

# Rule: Invariants present for lifecycle concepts

Every concept that has a **State / lifecycle** block must also have at least one **Invariant** line or an explicit "(none yet)" placeholder. Passing means every lifecycle block is paired with invariant coverage. Failing means a lifecycle block exists with no invariant section at all.

## DO

- Add at least one invariant tied to the lifecycle.

  **Example (pass):**
  ```
  ### Character
  #### State / lifecycle
  States: active, staggered, incapacitated, dying, dead
  ...
  #### Invariants
  - Damage condition must equal the highest single penalty applied, not the sum.
  - A character cannot transition to dying unless incapacitated first.
  ```

- Use "(none yet)" when the lifecycle is clear but invariants are not yet enumerable.

  **Example (pass):**
  ```
  ### Initiative Entry
  #### State / lifecycle
  States: waiting, acting, delayed, done
  ...
  #### Invariants
  (none yet)
  ```

## DO NOT

- Write a lifecycle block and omit the invariant section entirely.

  **Example (fail):**
  ```
  ### Attack
  #### State / lifecycle
  States: declared, rolled, resolved
  Transitions: declared → rolled, rolled → resolved
  ```
  No `#### Invariants` heading follows — reader cannot tell whether invariants were considered.

- Duplicate lifecycle transitions as pseudo-invariants.

  **Example (fail):** "Must transition from declared to rolled before resolved" — that is a transition rule, not a declarative constraint.
