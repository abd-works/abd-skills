# Rule: Subtypes use Child : Parent on the name line

**Scanner:** Manual review

When a concept is a specialization of another, its CRC block name line must use `Child : Parent` notation. The block states only delta responsibilities — what the subtype adds or overrides beyond the base. Passing means subtypes are correctly notated and carry only deltas. Failing means subtypes use the wrong format or duplicate base responsibilities.

## DO

- Use `Child : Parent` on the name line for subtypes.

  **Example (pass):**
  ```
  Saving Throw : Check
      responsible: adds an ability-score basis and proficiency eligibility on top of the base check resolution
      not_responsible: does not own the generic pass/fail resolution — that is inherited from Check
      collaborators: Ability Score, Proficiency
  ```

- State only delta responsibilities that the subtype adds beyond what the parent already owns.

  **Example (pass):** Parent `Check` owns resolution; subtype `Saving Throw : Check` adds only "adds an ability-score basis."

## DO NOT

- Use the Object Sketch English heading form in CRC blocks.

  **Example (fail):** `Saving Throw *is a type of* Check` — CRC uses `:` notation, not the sketch's English form.

- Use code-style inheritance syntax.

  **Example (fail):** `SavingThrow extends Check` or `class SavingThrow(Check)`

- Duplicate base responsibilities in the subtype block.

  **Example (fail):** Subtype repeats "resolves whether an attempted action succeeds or fails" — that belongs on the parent `Check` only.

**Source:** Engagement convention (class-responsibility-collaborator skill).
