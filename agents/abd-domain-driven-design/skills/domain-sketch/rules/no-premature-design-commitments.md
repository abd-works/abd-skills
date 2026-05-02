# Rule: No premature design commitments

**Scanner:** Manual review

The module file at `state: domain-sketch` must contain no DDD stereotypes, operation signatures, cardinality notation, lifecycle tables, or structural classification labels. The object sketch is a plain-English domain model — design decisions belong to later skills. Passing means the file stays at the concept level. Failing means design-level notation has leaked in.

## DO

- Keep concept blocks in plain English — intent paragraphs, prose behaviors, prose collaborations.

  **Example (pass):** "depends on Payment Clearance for the all-clear to ship" — prose collaboration.

- Record modeling choices in `#### Decisions made` as plain-English statements.

  **Example (pass):** "Shipment Lifecycle owns the exit gate, not Payment Clearance — payment is a prerequisite, not an orchestrator."

## DO NOT

- Add DDD stereotypes like `<<Entity>>`, `<<Value Object>>`, `<<Service>>`, `<<Aggregate>>`.

  **Example (fail):** `### Shipment <<Entity>>` or `<<Aggregate Root>>` anywhere in the sketch.

- Include operation signatures like `release(payment: Payment): void`.

  **Example (fail):** A behavior line includes `checkPayment(orderId: UUID): Boolean`.

- Add cardinality notation like `1..*`, `0..1`, or relationship arrows.

  **Example (fail):** "Shipment 1..* --> LineItem" in a collaboration line.

- Include lifecycle state tables with transition matrices.

  **Example (fail):** A table of states and transitions — that belongs to class-responsibility-collaborator.

- Use `Shape hint:` labels to classify concepts structurally.

  **Example (fail):** `Shape hint: orchestration object` — this is jargon that tells the reader nothing they can't see from the behaviors and collaborations.

**Source:** Engagement convention (domain-sketch skill).
