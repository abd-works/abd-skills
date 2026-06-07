# Rule: Stateful concepts have lifecycle blocks

**Scanner:** Manual review

Every concept whose responsibilities or sketch behaviors imply state changes, threshold ladders, supersession, or spend/recover must have either a populated `lifecycle:` block or `lifecycle: (stateless)`. Passing means no concept with state-shaped mechanics is left without coverage. Failing means a concept's mechanics imply state but its CRC block has no lifecycle field.

## DO

- Add a populated lifecycle block for concepts with state-shaped mechanics.

  **Example (pass):**
  ```
  Condition
      ...
      lifecycle:
          states: inactive, active, superseded, resolved
          transitions: inactive → active (source effect imposed), active → resolved (source effect ends)
          illegal: resolved → active (cannot re-activate from same source without new imposition)
          terminal: resolved
  ```

- Write `lifecycle: (stateless)` for concepts that appear in CRC but own no state changes.

  **Example (pass):**
  ```
  Difficulty Class
      responsible: holds the numeric threshold an action must meet or exceed to succeed
      ...
      lifecycle: (stateless)
  ```

## DO NOT

- Omit the `lifecycle:` field entirely.

  **Example (fail):** a domain model block for `Condition` ends after `collaborators:` with no `lifecycle:` line — reader cannot tell whether lifecycle was considered.

- Assume a concept is stateless without checking its sketch behavior bullets.

  **Example (fail):** `Condition` has sketch behaviors "applied, superseded, resolved" but is given `lifecycle: (stateless)` without any reasoning.

**Source:** Engagement convention (class-responsibility-collaborator skill).
