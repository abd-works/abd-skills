# Generate — abd-domain-glossary

Follow every file in `rules/`; fill `templates/module-file-template.md` to match its headings, tables, and fields exactly.

## Output shape

| Template | Deliverable |
| --- | --- |
| `templates/module-file-template.md` | `domain/domain-glossary.md` (default) or one file per module under `domain/domain-glossary/` for large systems |

Every `Source:` reference must point to a real file on disk at an exact location. See practice [`source-traceability.md`](../../../reference/source-traceability.md).

## Quality bar

- Single-noun module names, no kind-mixing
- Every KA intro opens with "*KAName* is …"
- `#### Decisions made` under each `## KA` — why these terms belong together
- Every `### term` has behavioral bullets; references at KA level under `### KA References`
- Boundary terms carry `*(owned by: Module)*`
- Domain terms *italicized* throughout
