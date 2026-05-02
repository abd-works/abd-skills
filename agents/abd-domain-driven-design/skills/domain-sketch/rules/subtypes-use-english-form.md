# Rule: Subtypes use English heading form with delta only

**Scanner:** Manual review

Subtype concepts must use the English heading form (`### [Subtype] *is a type of* [Base]`), not code notation. Subtype blocks carry only delta behaviors and collaborations — shared behavior stays on the base concept. Passing means every subtype uses the English form and adds only what is new. Failing means a subtype uses code notation or duplicates base behavior.

## DO

- Use the English heading form with italicized "is a type of."

  **Example (pass):** `### International Shipment *is a type of* Shipment Lifecycle`

- Include only delta behaviors and collaborations — what the subtype adds beyond the base.

  **Example (pass):** Base owns "gates warehouse exit"; subtype adds "collects customs commodity codes" — no repetition.

## DO NOT

- Use code-style notation for generalization.

  **Example (fail):** `### InternationalShipment : Shipment` or `### InternationalShipment extends Shipment`

- Duplicate base behaviors in the subtype block.

  **Example (fail):** Subtype repeats "gates warehouse exit until payment clearance is on record" — that belongs on the base only.

**Source:** Engagement convention (domain-sketch skill).
