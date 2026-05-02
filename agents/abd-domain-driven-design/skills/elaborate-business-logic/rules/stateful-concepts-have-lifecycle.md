---
---

# Rule: Stateful concepts have lifecycle blocks

Every CRC concept whose responsibilities or mechanics imply state changes, threshold ladders, supersession, or spend/recover must have either a **State / lifecycle** block or an explicit "(stateless — no lifecycle block)" note. Passing means no stateful concept is left without coverage. Failing means a concept with state-shaped mechanics has neither a lifecycle block nor a stateless annotation.

## DO

- Add a State / lifecycle block for concepts with state-shaped mechanics.

  **Example (pass):**
  ```
  ### Power Attack
  #### State / lifecycle
  States: available, committed, resolved
  Transitions: available → committed (player declares), committed → resolved (attack roll completes)
  Terminal: resolved
  ```

- Add an explicit stateless note for concepts that appear in CRC but have no lifecycle.

  **Example (pass):**
  ```
  ### Damage Bonus
  (stateless — no lifecycle block)
  ```

## DO NOT

- Omit a concept that has state-shaped mechanics without any annotation.

  **Example (fail):** The CRC lists "Condition" with responsibilities "applies modifiers while active, removed when duration expires" but the business-logic section has no entry for Condition.

- Assume a concept is stateless without checking its mechanics bullets.

  **Example (fail):** "Effect" has mechanics "activates on trigger, expires after duration" but is silently skipped — no lifecycle block, no "(stateless)" note.
