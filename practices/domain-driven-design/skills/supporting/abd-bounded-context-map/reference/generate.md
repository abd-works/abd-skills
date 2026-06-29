# Generate — abd-bounded-context-map

Follow every file in `rules/`; fill templates exactly.

## Read context

Read these files before generating:

- **`reference/concepts.md`** — bounded contexts, context maps, the three dimensions per dependency, relationship patterns (Shared Kernel, Customer/Supplier, Conformist, ACL, Open Host/Published Language, Separate Ways), and boundary heuristics.

## Output shape

| Template | Deliverable |
| --- | --- |
| `templates/bounded-context-map-template.md` | A single `bounded-context-map.md` — inventory of bounded contexts, dependency arcs with three dimensions each, decisions and tensions. |

## Quality bar

Every bounded context has an owning team and scope description. Every dependency arc fills all three dimensions — domain mapping, integration mechanism, and team engagement model. Every relationship uses a named pattern from the DDD/ABD catalogue. Direction is explicit on every arc. No orphan contexts.
