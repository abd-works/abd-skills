---
scanner: no-class-level-commitments
---

# Rule: No class-level commitments

Key Abstractions are deliberately uncommitted on every modeling axis except name and intent. The file must contain no stereotypes, typed properties, method signatures, cardinality arrows, or other class-level notation. Passing means the file stays at the identification rung. Failing means class-level decisions have leaked into the file.

## DO

- Use only free-form prose in the Shape hint line — observations like "taxonomy under Funds Transfer" or "value-like — defined entirely by content".

  **Example (pass):** `Shape hint: Taxonomy under Funds Transfer — the module treats it as a specialization with its own cap vocabulary.`

- Record modeling uncertainty as a `Tension:` line, not as a class decision.

  **Example (pass):** `Tension: May settle as a sub-type or a kind-tag on Funds Transfer.`

- Keep Core terms as plain noun phrases — no types, no annotations.

  **Example (pass):**
  ```
  - per-transaction cap
  - daily cap
  - beneficiary-jurisdiction cap
  ```

## DON'T

- Use UML stereotype tags like `<<Entity>>`, `<<ValueObject>>`, `<<Service>>`, `<<Event>>`, `<<Aggregate>>`.

  **Example (fail):** `Shape hint: <<Entity>> with lifecycle states.`

- Add typed properties like `amount: Decimal`, `status: String`, or `transferId: UUID`.

  **Example (fail):** Core terms list includes `transferId: UUID` or `amount: Money`.

- Include method signatures like `execute(from, to, amount) -> Result`.

  **Example (fail):** `Operations: validate(amount) -> bool, execute() -> TransferResult`

- Use cardinality notation like `1..*`, `0..1`, or relationship arrows.

  **Example (fail):** `Funds Transfer 1..* --> Account` in any section of the file.

- Commit to super/sub hierarchies (Entity vs Value Object, parent/child splits).

  **Example (fail):** `Wire Transfer <<extends>> Funds Transfer` — this belongs to a later skill.
