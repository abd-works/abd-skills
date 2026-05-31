# Specification

**Pull:** When a ticket is `stage: specification` and active, agents pull skills from `kanban.json` for this stage — same [pull-model](../../agents/reference/pull-model.md) as all stages.
**Prior:** [exploration.md](exploration.md) · **Follow-on:** [engineering.md](engineering.md) · **Index:** [README.md](README.md)

## Purpose

Define stories with **CRC** cards that supply concepts for outline **example tables**, then **concrete specification-by-example** scenarios, production-grade **interface design** intent, and **architecture reference** for mechanisms used in the slice. Narrow scope — story-level depth.

## Team role

**Product Owner** (default for spec-by-example). Extension skills assign **Business Expert** (CRC — before spec), **UX Designer**, or **Engineer** per slot.

## Practice skills

When running the full specification pass, default skill order: **domain (CRC) → story (spec) → UX → architecture**.

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Domain-driven design** | `abd-class-responsibility-collaborator` | Business Expert | CRC cards + `domain.json` — concepts for spec outline tables |
| 1b | **Domain-driven design** | `drawio-domain-sync` | Business Expert | **Background** after CRC — `crc-class-diagram.drawio` |
| 2 | **Story-driven delivery** | `abd-specification-by-example` | Product Owner | Given/When/Then with real values; tables name CRC concepts |
| 2b | **Story-driven delivery** | `drawio-story-sync` | Product Owner | **Background** after spec + graph scenario merge — refresh `acceptance-criteria.drawio` |
| 3 | **User experience design** | `abd-interface-design` | UX Designer | **Spec pass** — author `interface-design.md` from lo-fi mockups |
| 4 | **Architecture-centric engineering** | `abd-architecture-reference` | Engineer | **Conditional** — assign reference + code when already present; create only missing files |

### Conditional: `abd-architecture-reference`

**Run when:** Sprint scope needs reference sections or implementation files not yet on disk (per assign/create inventory in `abd-architecture-reference`).

**Skip when:** All in-scope mechanisms have complete reference sections **and** production/test files from the reference File Structure already exist — record assignment table (or point to existing `*-architecture-reference-assignment.md`) and mark skill done.

**Not the same as template:** Exploration/template documents mechanisms; specification/reference **implements** from them — but skip when a prior pass or brownfield already produced both reference and code.

## Entry conditions

- [Exploration](exploration.md) exit gate passed.
- Stories have AC; mockups available when interface skill is assigned.
- **CRC** (and `domain.json`) complete **before** spec-by-example when outline / example tables are in scope.

## Expected outputs

Under **`docs/increments/<n>-<slug>/specification/`** (flat). One canonical file per type. See [artifact-layout.md](../artifact-layout.md).

- `crc.md`, `domain.json`, `specification-by-example.md`, `interface-design.md`, `architecture-reference.md` when assigned.
- **`docs/end-to-end/discovery/stories/story-graph.json`** — `scenarios[]` / `scenario_outlines[]` populated on every in-scope story when spec-by-example ran (sync from `specification-by-example.md` via story-graph-ops; see [artifact-layout.md](../artifact-layout.md)).

## Exit gate

1. Graph valid; scanners green for each assigned skill.
2. CRC concepts and `domain.json` exist **before** outline spec tables when both CRC and spec ran.
3. Scenarios trace to AC with concrete values when spec skill ran; **`scenarios` in `story-graph.json` must be non-empty** for in-scope stories (markdown alone is not enough); table names/columns match CRC when outlines used.
4. Reference docs match template from exploration when arch skill ran.
5. **Ripple check** per [README.md](README.md).
6. User confirmed at checkpoint.

## Handoff to next stage

Pass to [engineering.md](engineering.md):

- Scenario paths, interface spec, CRC, reference doc paths.
- Test and implementation scope for the slice.
