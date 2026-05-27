---
scanner:
---
# Rule: Identity test drives Entity vs Value Object

The distinction between Entity and Value Object is decided by asking whether the concept has **identity that transcends its attributes**. An Entity's identity persists even when all its data changes; a Value Object is fully described by its properties and has no independent identity. Passing means every Entity cites an identity reason and every Value Object cites the absence of identity. Failing means the stereotype was assigned by gut feel, by looking at "importance," or by defaulting everything to Entity.

## DO

- Classify as Entity when the concept must be tracked as "that one" over time, even if all attributes change.

  **Example (pass):** "**Identity:** Patient ID — a patient who changes name, address, and insurance is still the same patient. **Rationale:** Two patients with identical demographics are still different people; identity transcends attributes."

- Classify as Value Object when two instances with identical properties are interchangeable — no "which one" question exists.

  **Example (pass):** "**Defining attributes:** amount, currency. **Rationale:** $50.00 CAD is $50.00 CAD — there is no 'that particular fifty dollars' distinct from another fifty dollars with the same amount and currency."

- Prefer Value Object as the default — select Entity only when the concept genuinely requires tracked identity.

  **Example (pass):** A model with 15 concepts classifies 4 as Entities and 8 as Value Objects — the majority are values, entities are the exception, not the rule.

## DO NOT

- Default to Entity because the concept "feels important" or "is a noun" without applying the identity test.

  **Example (fail):** "**Stereotype:** Entity / **Rationale:** Address is an important concept." — importance is not identity; Address with no independent tracking is a Value Object.

- Classify as Value Object without confirming immutability and replaceability.

  **Example (fail):** "**Stereotype:** Value Object" on a concept that the domain experts say must be "updated in place" and "tracked for audit" — those are Entity signals, not Value Object.

- Use "it has attributes" as the reason for Value Object — all concepts have attributes; the question is whether identity exists **beyond** them.

  **Example (fail):** "**Rationale:** It has name, size, and color properties." — Entities also have properties; this does not distinguish.

**Source:** Kept chunks #4, #5, #7 in `inputs/abd-answers-retrieval.md`
