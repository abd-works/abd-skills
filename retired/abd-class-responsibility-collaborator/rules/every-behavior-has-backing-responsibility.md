# Rule: Every Domain Language behavior has a backing responsibility

**Scanner:** Manual review

Each behavior bullet in the Domain Language must be traceable to at least one responsibility (property or operation) in the domain model block for the same concept. Behaviors that produce no CRC entry must be explained in the Decisions section.

## DO

- For every behavior bullet, produce at least one property or operation.

  **Example (pass):** Sketch: "makes checks using its traits" → CRC has `traits | Trait`.

  **Example (pass):** Sketch: "carries imposed conditions via its Imposed Conditions collection" → CRC has `imposed conditions | Imposed Conditions`.

  **Example (pass):** Sketch: "has a difficulty ladder" → CRC has `difficulty ladder | Difficulty Ladder`.

## DO NOT

- Leave a behavior bullet with no corresponding CRC entry and no decision note.

  **Example (fail):** Sketch says "has exactly one rank" but no property for `effectiveness rank` appears in the domain model block for `Trait`.

- Map a behavior to a responsibility on the wrong concept.

  **Example (fail):** Sketch says `Trait` "has a difficulty ladder" but the `difficulty ladder` property appears on `Check` instead.

## Note

A responsibility can be either a property (noun phrase) or an operation (verb phrase) — the domain model stage does not require distinguishing between them. What matters is that the behavior has a named responsibility somewhere.

**Source:** Engagement convention (class-responsibility-collaborator skill).
