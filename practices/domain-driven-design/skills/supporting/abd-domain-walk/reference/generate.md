# Generate — abd-domain-walk

Follow every file in `rules/`; fill templates exactly.

## Read context

Read these files before generating:

- **`reference/concepts.md`** — prerequisites, the consistent scenario/walk shape, and the flat heading structure.

## Output shape

| Template | Deliverable |
| --- | --- |
| `templates/domain-walkthrough-scaffold.md` | The walkthrough file with scenarios grouped under KAs, pseudocode walks, references, and decisions. |

## Scenarios per KA

Cover at minimum one happy path, one failure or edge path, one path involving cooperation or shared resources. Use real domain values, not placeholders. Every pseudocode line that performs domain logic must trace to a class and operation in the prior-phase file.
