# Rule: Direction stated per dependency — upstream, downstream, or mutual

Every dependency arc must explicitly state the direction of the relationship: which context is upstream (the supplier of data or capability), which is downstream (the consumer), or whether the relationship is mutual. Without direction, the reader cannot tell who depends on whom, who has the power to change the interface, and who bears the translation burden. Failure is a dependency arc with no direction field, or a direction that uses vague language instead of explicitly naming upstream and downstream.

## DO

- State direction using explicit upstream/downstream language that names which context is which.

  **Example (pass):**

  ```
  - Direction: Trading is upstream; Front Page is downstream
  ```

- For mutual relationships where both contexts supply and consume from each other, state "mutual" and explain what flows in each direction.

  **Example (pass):**

  ```
  - Direction: mutual — Inventory pushes stock levels to Order Management; Order Management pushes reservation requests to Inventory
  ```

- For standalone contexts (Separate Ways pattern), the direction is "none" — but this belongs in the Standalone Contexts section, not in a dependency arc.

  **Example (pass):**

  ```
  ## Standalone Contexts

  ### Analytics Warehouse
  Standalone — Separate Ways. No runtime dependency; consumes read-only replicas outside the operational model.
  ```

## DO NOT

- Omit the direction field from a dependency arc.

  **Example (fail):**

  ```
  ### Trading → Invoice
  - Domain mapping: deal identifiers
  - Integration mechanism: Batch
  - Team engagement model: Conformist
  ```

  No direction field — the reader must guess who depends on whom.

- Use vague direction language that does not name the upstream and downstream contexts.

  **Example (fail):**

  ```
  - Direction: one-way
  ```

  "One-way" does not say which context is upstream and which is downstream.

- Use arrow notation in the heading as a substitute for the direction field — the heading is a label, not the specification.

  **Example (fail):**

  ```
  ### Trading → Invoice
  ```

  The arrow in the heading suggests direction, but without an explicit Direction field, a reviewer cannot confirm it was a deliberate choice.
