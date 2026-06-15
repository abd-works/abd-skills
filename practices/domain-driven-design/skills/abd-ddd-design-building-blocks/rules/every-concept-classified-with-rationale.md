---
scanner:
---
# Rule: Every concept classified with explicit rationale

Every named concept from the input model (CRC block, object-model class, or ubiquitous-language concept) must appear in the building-blocks output with **at least one** stereotype annotation. A concept may express multiple stereotypes (Entity + Aggregate Root + emits Domain Events) — that is expected and correct. The answer to the business question is **implicit in the model itself** (the stereotype annotation, the `<<identifier>>` properties, the invariants, the boundary membership) — not written out as a separate Q&A block. Passing means no concept is left out and every stereotype annotation is justified by the model structure. Failing means a concept is missing or a stereotype is slapped on with no supporting model content (no identifier properties on an Entity, no invariants on an Aggregate, etc.).

## DO

- Identify **all** stereotype facets that apply to each concept — do not force one-label-per-concept.

  **Example (pass):** `#### **Order** [Entity, Aggregate Root]` with `<<identifier>>` properties, invariants, and boundary members listed — the model shows why it's an Entity (has identifier props) and an Aggregate Root (has boundary members with invariants).

- Support each stereotype annotation with model content that makes it self-evident.

  **Example (pass):** An Entity has `<<identifier>>` properties. An Aggregate has invariants and boundary members. A Repository has store/retrieve/find responsibilities. The model speaks for itself.

## DO NOT

- Leave any source-model concept unaccounted for in the output (even if it is Unresolved, it must appear).

  **Example (fail):** Source CRC has `Appointment`, `Patient`, `Clinic`, `TimeSlot`; output only addresses `Patient` and `Clinic` — two concepts silently dropped.

- Annotate a stereotype with no supporting model content.

  **Example (fail):** `#### **Address** [Entity]` with no `<<identifier>>` properties — nothing in the model justifies why this is an Entity rather than a Value Object.

- Force each concept into exactly one stereotype when it naturally expresses several.

  **Example (fail):** Order listed only as `[Entity]` when it is also the Aggregate Root for OrderLines and emits OrderConfirmed — the model is incomplete.

**Source:** Kept chunks #3, #4, #5 in `inputs/abd-answers-retrieval.md`
