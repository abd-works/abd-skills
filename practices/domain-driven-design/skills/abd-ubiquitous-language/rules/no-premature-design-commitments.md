# Rule: No premature design commitments

**Scanner:** Python — `no-premature-design-commitments-scanner.py`

The ubiquitous-language file contains no UML stereotypes, operation signatures, typed properties, cardinality notation, or structural classification labels. Design decisions belong to later skills. Passing means every concept block is plain prose. Failing means the file uses any of the forbidden notations.

## DO

- Keep concept blocks in plain English — verb-led prose bullets and `**Invariant:**` lines.

  **Example (pass):**
  ```
  ### check
  - is resolved by *rolling* a *d20*, comparing the *roll total* to the *difficulty class*
  - **Invariant:** shape is always *roll total* versus *difficulty class*
  ```

## DO NOT

- Add DDD stereotype tags.

  **Example (fail):** `### <<Entity>> Check`, `### <<ValueObject>> Rank`

- Include operation signatures.

  **Example (fail):** `release(payment: Payment): void`

- Add cardinality notation.

  **Example (fail):** `Check 1..* Modifier`

- Use typed properties.

  **Example (fail):** `- difficulty: int`

- Use `Shape hint:` or `Tension:` labels.

  **Example (fail):** `Shape hint: Aggregate root`

**Source:** Inherited from abd-ubiquitous-language — no premature design commitments.
