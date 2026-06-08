# Specification

**Pull:** When a ticket is `stage: specification` and active, agents pull skills from `kanban.json` for this stage â€” same [
**Prior:** [exploration.md](exploration.md) Â· **Follow-on:** [engineering.md](engineering.md) Â· **Index:** [README.md](README.md)

## Purpose

Translate exploration artifacts into a conceptual **domain model**, **concrete specification-by-example** scenarios, and production-grade **UX specification**. Narrow scope â€” story-level depth.

## Team role

**Product Owner** (default for spec-by-example). Extension skills assign **Business Expert** (domain model â€” before spec) or **UX Designer** per slot.

## Practice skills

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Domain-driven design** | `abd-domain-model` | Business Expert | Conceptual domain model from Domain Language â€” before spec-by-example |
| 1b | **Domain-driven design** | `drawio-domain-sync` | | **Background** after domain model â€” `domain-model-class-diagram.drawio` |
| 2 | **Story-driven delivery** | `abd-specification-by-example` | Product Owner | Given/When/Then with real values; tables name domain model concepts |
| 2b | **Story-driven delivery** | `drawio-story-sync` | | **Background** after spec + graph scenario merge â€” refresh `acceptance-criteria.drawio` |
| 3 | **User experience design** | `abd-ux-specification` | UX Designer | **Spec pass** â€” author `interface-design.md` from lo-fi mockups |

## Entry conditions

- [Exploration](exploration.md) exit gate passed.
- Stories have AC; Domain Language complete; mockups available when UX skill is assigned.

## Expected outputs

Under **`docs/increments/<n>-<slug>/specification/`** (flat). One canonical file per type. See [artifact-layout.md](../artifact-layout.md).

- `domain-model.md`, `specification-by-example.md`, `interface-design.md` when assigned.
- **`docs/end-to-end/discovery/stories/story-graph.json`** â€” `scenarios[]` / `scenario_outlines[]` populated on every in-scope story when spec-by-example ran (sync from `specification-by-example.md` via story-graph-ops; see [artifact-layout.md](../artifact-layout.md)).

## Exit gate

1. Graph valid; scanners green for each assigned skill.
2. Domain model (`domain-model.md`) exists and aligns with Domain Language when `abd-domain-model` ran; domain model complete **before** spec-by-example.
3. Scenarios trace to AC with concrete values when spec skill ran; **`scenarios` in `story-graph.json` must be non-empty** for in-scope stories (markdown alone is not enough); table names/columns match domain model when outlines used.
4. **Ripple check**.
5. User confirmed at checkpoint.

## Handoff to next stage

Pass to [engineering.md](engineering.md):

- Scenario paths, interface spec, domain model paths.
- Test and implementation scope for the slice.
