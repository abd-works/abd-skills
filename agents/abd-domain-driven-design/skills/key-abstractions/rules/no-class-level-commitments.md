---
scanner: no-class-level-commitments
---

# Rule: No class-level commitments

The module file at `state: key-abstractions` must contain no stereotypes, typed properties, method signatures, cardinality arrows, or other class-level notation. The key-abstractions step adds verbatim source extracts — it does not introduce modeling decisions. Passing means the file stays at the enrichment level. Failing means class-level decisions have leaked in.

## DO

- Keep behavioral lines as plain prose bullets — observations about what the term means and how it works.

  **Example (pass):**
  ```
  - A check is d20 + trait rank (plus modifiers) vs DC; equal or above is success.
  ```

- Keep `Owned by:` fields on boundary terms as simple module names.

  **Example (pass):** `Owned by: Power`

## DO NOT

- Use UML stereotype tags like `<<Entity>>`, `<<ValueObject>>`, `<<Service>>`, `<<Event>>`, `<<Aggregate>>`.

  **Example (fail):** `<<Entity>> with lifecycle states` anywhere in the file.

- Add typed properties like `amount: Decimal`, `status: String`, or `checkId: UUID`.

  **Example (fail):** A behavioral line includes `rollResult: Int` or `dc: Integer`.

- Include method signatures like `resolve(modifier, dc) -> Result`.

  **Example (fail):** `Operations: roll(d20) -> int, compare(result, dc) -> bool`

- Use cardinality notation like `1..*`, `0..1`, or relationship arrows.

  **Example (fail):** `Check 1..* --> Condition` in any section.

- Commit to super/sub hierarchies or Entity/ValueObject distinctions.

  **Example (fail):** `Condition <<extends>> BasicCondition` — this belongs to later skills.
