# Generate — abd-domain-model

Follow every file in `rules/`; fill templates exactly.

## Read context

Read these files before generating:

- **`reference/concepts.md`** — domain model format: class blocks, constructor, properties, methods, collaborators, invariants, subtypes, and the consistent file shape.
- **`../../reference/oo-concepts.md`** — OO fundamentals (what is a class, decomposing responsibilities, relationships, inheritance and subtypes).

## Output shape

| Template | Deliverable |
| --- | --- |
| `templates/domain-model-template.md` | The domain model file with typed class blocks under each KA. |
| `templates/domain.json` | Domain JSON with class names, property names (camelCase), and inheritance. |

The file is **not** an in-place enrichment of the domain-language file. It is a fresh artifact in the same flat heading shape every other DDD phase skill uses.

## Quality bar

Every behavior bullet from the Domain Language maps to at least one property or method. Properties are typed — never raw `String`; use domain types, constrained enums, or typed primitives. Methods use type-only params (no param names). Hidden collaborators (not in params or return) listed underneath methods, indented, before invariants. No `+` prefix. No stereotypes. No `List<T>` or `Dictionary<K,V>`. No `Interaction:` blocks. Subtype blocks carry only deltas. State marker set to `domain-model`.
