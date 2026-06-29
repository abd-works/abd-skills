# Generate — abd-domain-specification

Follow every file in `rules/`; fill templates exactly.

## Read context

Read these files before generating:

- **`reference/concepts.md`** — typed notation: properties, operations, object initialisation, relationships (aggregation/composition/association), collections, inheritance, invariants, interactions, entities and value objects, and the consistent file shape.
- **`../../reference/oo-concepts.md`** — OO fundamentals (what is a class, decomposing responsibilities, relationships, inheritance and subtypes).

## Output shape

| Template | Deliverable |
| --- | --- |
| `templates/domain-specification-scaffold.md` | The domain specification file with typed class blocks under each KA. |
| `templates/domain.json` | Domain JSON with class names, property names (camelCase), and inheritance. |

The file is **not** an in-place enrichment of the domain model file. It is a fresh artifact in the same flat heading shape every other DDD phase skill uses.

## Quality bar

Every property is typed and justified by a domain responsibility. Every operation is a fully typed signature. Every class has object initialisation decided. Composition/aggregation properties carry stereotypes. Subtype blocks carry only deltas. Operations with inherent complexity have `Interaction:` blocks. No operation carries multiple invariants without an `Interaction:`. Variable names in interactions use domain language. State marker set to `domain-specification`.
