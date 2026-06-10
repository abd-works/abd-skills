# Specification

**Pull:** When a ticket is `stage: specification` and active, agents pull skills from `kanban.json` for this stage.
**Prior:** [exploration.md](exploration.md) · **Follow-on:** [engineering.md](engineering.md) · **Index:** [README.md](README.md)

## Purpose

Translate exploration artifacts into typed **domain specification**, **concrete specification-by-example** scenarios, production-grade **UX specification**, and architecture specification **template** sections. Narrow scope — sprint-level depth.

## Outcomes

- Business Logic
- Solution Behavior
- UI Layout
- Technology Design

## Team role

**Product Owner** (default for spec-by-example). Extension skills assign **Business Expert** (domain specification — before spec) or **UX Designer** per slot.

## Practice skills

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Domain-driven design** | `abd-domain-specification` | Business Expert | Typed Class Model from domain model — before spec-by-example |
| 1b | **Domain-driven design** | `drawio-domain-sync` | | **Background** after domain specification — `class-model-class-diagram.drawio` |
| 2 | **Story-driven delivery** | `abd-story-specification` | Product Owner | Given/When/Then with real values; tables name domain model concepts |
| 2b | **Story-driven delivery** | `drawio-story-sync` | | **Background** after spec + graph scenario merge — refresh `acceptance-criteria.drawio` |
| 3 | **User experience design** | `abd-ux-specification` | UX Designer | **Spec pass** — author `interface-design.md` from lo-fi mockups |
| 4 | **Architecture-centric engineering** | `abd-architecture-specification` | Engineer | **Template mode** — mechanism templates and file layout for engineering |

## Entry conditions

- [Exploration](exploration.md) exit gate passed.
- Stories have AC; domain model complete; mockups available when UX skill is assigned.

## Expected outputs

Under **`docs/increments/<n>-<slug>/specification/`** (flat). One canonical file per type. See [artifact-layout.md](../artifact-layout.md).

- `domain-specification.md`, `story-specification.md`, `interface-design.md`, architecture specification template sections when assigned.
- **`docs/end-to-end/discovery/stories/story-graph.json`** — `scenarios[]` / `scenario_outlines[]` populated on every in-scope story when spec-by-example ran (sync from `story-specification.md` via story-graph-ops; see [artifact-layout.md](../artifact-layout.md)).

## Exit gate

1. Graph valid; scanners green for each assigned skill.
2. Domain specification exists and aligns with domain model when `abd-domain-specification` ran; domain specification complete **before** spec-by-example.
3. Scenarios trace to AC with concrete values when spec skill ran; **`scenarios` in `story-graph.json` must be non-empty** for in-scope stories (markdown alone is not enough); table names/columns match domain specification when outlines used.
4. Architecture specification template sections exist when assigned.
5. **Ripple check**.
6. User confirmed at checkpoint.

## Handoff to next stage

Pass to [engineering.md](engineering.md):

- Scenario paths, interface spec, domain specification paths, architecture reference when in scope.
- Test and implementation scope for the slice.
