# Rule: Invariants present for lifecycle concepts

**Scanner:** Manual review

Every concept that has a populated `lifecycle:` block must also have an `invariants:` field with at least one declarative constraint or an explicit `(none yet)` placeholder. Stateless concepts must have `invariants: (none)` or a value. Passing means every CRC block has an invariants field. Failing means a block with a lifecycle has no invariants field at all.

## DO

- Add at least one invariant tied to the lifecycle for stateful concepts.

  **Example (pass):**
  ```
  Condition
      ...
      lifecycle:
          states: inactive, active, superseded, resolved
          ...
      invariants:
          - a condition already present in the supersession chain is overridden by the more severe one, never duplicated
          - a combined condition is removed entirely when its source effect ends
  ```

- Use `(none yet)` when the lifecycle is clear but invariants are not yet enumerable.

  **Example (pass):**
  ```
  Check Result
      ...
      lifecycle:
          states: pending, succeeded, failed
          ...
      invariants: (none yet)
  ```

- Use `(none)` for stateless concepts with no always-true constraints.

  **Example (pass):**
  ```
  Difficulty Class
      ...
      lifecycle: (stateless)
      invariants: (none)
  ```

## DO NOT

- Write a lifecycle block and omit the `invariants:` field entirely.

  **Example (fail):** A CRC block ends after `lifecycle: states: ...` with no `invariants:` line — reader cannot tell whether constraints were considered.

- Duplicate lifecycle transitions as pseudo-invariants.

  **Example (fail):** `invariants: must transition from inactive to active before resolving` — that is a transition rule, not a declarative constraint on what must always be true.

**Source:** Engagement convention (class-responsibility-collaborator skill).
