---
scanner:
---
# Rule: No premature infrastructure in building-blocks output

The building-blocks classification is a **design-level** artifact — it records architectural intent (identity, boundaries, immutability, communication contracts) but does not prescribe implementation technology. Passing means the document stays in domain language and design constraints. Failing means it names database tables, message brokers, framework annotations, REST endpoints, or specific persistence strategies.

## DO

- Use domain language and DDD pattern vocabulary only: Entity, Value Object, Aggregate root, boundary, invariant, Domain Event, Service.

  **Example (pass):** "**Protected invariants:** When a change to the Order boundary is committed, the total must equal the sum of line amounts." — design constraint, no tech.

- Describe lifecycle in terms of domain state transitions, not persistence mechanisms.

  **Example (pass):** "**Lifecycle:** Created at patient admission, transitions through Active → Discharged → Archived." — domain states, not DB row states.

- Describe event contracts in terms of trigger, payload, and consumer — not transport mechanisms.

  **Example (pass):** "**Payload:** patient ID, discharge reason, discharge timestamp." — what the event carries, not how it's serialized or transported.

## DO NOT

- Name database tables, columns, or storage engines in the building-blocks output.

  **Example (fail):** "**Lifecycle:** Inserted into the `patients` table with status column set to 'ACTIVE'."

- Prescribe message queue topics, REST endpoints, or framework annotations.

  **Example (fail):** "**Consumers:** Subscribes to `order.confirmed` Kafka topic." — names the transport; should just say "Inventory service reacts."

- Add implementation patterns (Repository, Factory, DTO, Controller) to the stereotype classification — those come later.

  **Example (fail):** "**Stereotype:** Entity with JPA @Entity annotation and Spring Data Repository." — implementation detail, not design intent.

**Source:** Practice convention — building blocks classify design intent before implementation decisions; Kept chunk #1 (Evans: "A Model Expressed in Software" separates model from implementation paradigm).
