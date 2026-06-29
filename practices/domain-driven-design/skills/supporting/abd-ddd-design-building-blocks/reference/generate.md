# Generate — abd-ddd-design-building-blocks

Follow every file in `rules/`; fill templates exactly.

## Read context

Read these files before generating:

- **`reference/concepts.md`** — all building block stereotypes (Entity, Value Object, Aggregate, Repository, Factory, Service, Domain Event, Specification), cross-aggregate consistency, the business questions each stereotype surfaces, and source-fidelity guidance.
- **`reference/examples.md`** — a worked domain model before-and-after example showing building blocks applied to an Order domain.

## Output shape

| Template | Deliverable |
| --- | --- |
| `templates/ddd-building-blocks-template.md` | The building-blocks portrait for every concept — stereotypes, identity rules, aggregate boundaries, events, services, with business questions and rationale. |

## Quality bar

Every concept from the input model appears with at least one stereotype facet or an explicit Unresolved note. Every stereotype records the business question asked and the answer given. Concepts may express multiple stereotypes (Entity + Aggregate Root + emits Events). Write at the same fidelity as the input source (domain model notation, typed notation, or plain-English concept blocks). Include the source model and show DDD annotations layered on top.
