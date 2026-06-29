# Story-Driven Delivery — Skill Extensions

Read this file when any **story-driven-delivery** practice skill tells you to. It extends the shared workflow in [`common/skill-workflow.md`](../../../../common/skill-workflow.md) (also linked as [`../skill-rule-workflow.md`](../skill-rule-workflow.md) after deploy).

---

## Output file resolution (deliverables)

Follow [`common/skill-workflow.md`](../../../../common/skill-workflow.md) § Output file resolution first.

**SDD default scaffold:** `docs/stories/` — see [`common/folder-conventions.md`](../../../../common/folder-conventions.md) § Stories for per-skill paths (`story-map/`, `acceptance-criteria/`, `specification/`).

| Skill | Default file | Scaffold subfolder |
| --- | --- | --- |
| `abd-story-mapping` | `story-map.md` | `docs/stories/story-map/` |
| `abd-thin-slicing` | `thin-slicing.md` | `docs/stories/story-map/` |
| `abd-story-acceptance-criteria` | `acceptance-criteria.md` | `docs/stories/acceptance-criteria/` |
| `abd-story-specification` | `specification-by-example.md` | `docs/stories/specification/` |
| `abd-story-acceptance-test` | language test-discovery names | project `tests/` tree (see skill) |

Add a `<name>-` prefix only when disambiguation is needed.

**Machine-readable graph:** `story-graph.json` lives beside the story map (`docs/stories/story-map/story-graph.json` by default). Load **story-graph-ops** whenever you create or change the graph file.

---

## Read-gates

Follow [`common/skill-workflow.md`](../../../../common/skill-workflow.md) § Read-gates.

**Also read before generating:**

| File | When |
| --- | --- |
| [`../../reference/handling-incomplete-context.md`](../../reference/handling-incomplete-context.md) | Any SDD skill — gap discipline |
| [`../../reference/new-vs-existing-system.md`](../../reference/new-vs-existing-system.md) | Any SDD skill — spec-first vs reverse-engineering mode |
| [`domain-input-priority.md`](./domain-input-priority.md) | AC, specification, acceptance-test skills |
| [`diagram-workflow.md`](./diagram-workflow.md) | Skills with a `## Diagram workflow` section |

---

## Validate output

Follow [`common/skill-workflow.md`](../../../../common/skill-workflow.md) § Validate output.

**Also apply** [`validate-checklist.md`](./validate-checklist.md) — shared SDD review items every skill adds on top of its own `## Validate` section.
