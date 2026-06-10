# Discovery

**Pull:** When a ticket is `stage: discovery` and active, agents pull skills from `kanban.json` for this stage.
**Prior:** [shaping.md](shaping.md) · **Follow-on:** [exploration.md](exploration.md) · **Index:** [README.md](README.md)

## Purpose

Transform shaped context into a **full** product definition: domain vocabulary, complete story map, UX information architecture, architecture blueprint, and **thin slices last**. Uses **`abd-story-mapping` in full mode** (not outline — see [shaping.md](shaping.md)).

Discovery focuses on **what you are working on** — end-to-end scope and the lenses (domain, story, UX, architecture) aligned before slice ordering and before Exploration deepens a slice.

## Outcomes

- Business Logic
- Solution Behavior
- UI Layout
- Technology Design

## Team role

**Product Owner** (default). Extension skills assign **Business Expert**, **UX Designer**, or **Engineer** per slot.

## Practice skills

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Story-driven delivery** | `abd-story-mapping` (**full mode**) | Product Owner | Full map decomposed to testable stories |
| 1b | **Story-driven delivery** | `drawio-story-sync` | | **Background** after full story-mapping — `story-map.drawio` |
| 2 | **Domain-driven design** | `abd-domain-language` | Business Expert | Shared vocabulary for the whole solution before slice work |
| 3 | **User experience design** | `abd-information-architecture` | UX Designer | Screen inventory, navigation, content model |
| 4 | **Architecture-centric engineering** | `abd-architecture-blueprint` | Engineer | System components and mechanisms |
| 5 | **Story-driven delivery** | `abd-thin-slicing` | Product Owner | Vertical slice ordering **after** map, IA, and blueprint align |
| 5b | **Story-driven delivery** | `drawio-story-sync` | | **Background** after thin-slicing — `thin-slicing.drawio` |

## Entry conditions

- [Shaping](shaping.md) exit gate passed, **or** operator waives shaping for brownfield with existing map.
- Workspace and context sources available.

## Expected outputs

All artifacts under **`docs/end-to-end/discovery/`** in four subfolders. See [artifact-layout.md](../artifact-layout.md).

- **Stories** (`stories/`): `story-graph.json`, `story-map.md`, `thin-slicing.md`; optional `thin-slicing.drawio`.
- **Domain** (`domain/`): `domain-language.md` when domain language ran.
- **UX** (`ux/`): `information-architecture.md` + `.drawio`.
- **Architecture** (`architecture/`): `architecture-blueprint.md`, `ADR-*.md` when assigned.

## Exit gate

1. `story-graph.json` passes `story_graph_cli.py read` when story work ran.
2. Scanners green for **each assigned skill**.
3. Full-mode map: epics → sub-epics → stories; verb—noun naming; actors assigned.
4. IA, domain, and blueprint consistent with each other — **ripple check** **before** thin-slicing.
5. Every story assigned to a slice when thin-slicing ran.
6. User confirmed at checkpoint.

## Handoff to next stage

Pass to [exploration.md](exploration.md):

- All artifact paths; recommended first slice for exploration.
- Ripple flags for any cross-family mismatches found during discovery.
