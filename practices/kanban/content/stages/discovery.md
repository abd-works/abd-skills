# Discovery

**Prior:** [shaping.md](shaping.md) · **Follow-on:** [exploration.md](exploration.md) · **Index:** [README.md](README.md)

## Purpose

Transform shaped context into a **full** product definition: domain vocabulary, complete story map, UX information architecture, architecture blueprint, and **thin slices last**. Uses **`abd-story-mapping` in full mode** (not outline — see [shaping.md](shaping.md)).

Discovery focuses on **what you are working on** — end-to-end scope and the lenses (domain, story, UX, architecture) aligned before slice ordering and before Exploration deepens a slice.

## Team role

**Product Owner** (default). Extension skills assign **Business Expert**, **UX Designer**, or **Engineer** per slot.

## Practice skills

When running the full discovery pass, default skill order: **domain → story → UX → architecture → thin slicing (last)**.

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Domain-driven design** | `abd-domain-terms` | Business Expert | Extract and group terms before full map |
| 2 | **Domain-driven design** | `abd-ubiquitous-language` | Business Expert | Key abstractions and behavior sketches |
| 3 | **Domain-driven design** | `drawio-domain-sync` | Business Expert | Optional domain diagram from vocabulary |
| 4 | **Story-driven delivery** | `abd-story-mapping` (**full mode**) | Product Owner | Full map decomposed to testable stories |
| 5 | **User experience design** | `abd-information-architecture` | UX Designer | Screen inventory, navigation, content model |
| 6 | **Architecture-centric engineering** | `abd-architecture-blueprint` | Engineer | System components and mechanisms |
| 7 | **Architecture-centric engineering** | `abd-service-level-objectives` | Engineer | NFR/SLO targets when assigned |
| 8 | **Story-driven delivery** | `abd-thin-slicing` | Product Owner | Vertical slice ordering **after** map, IA, and blueprint align |
| 9 | **Story-driven delivery** | `drawio-story-sync` | Product Owner | Increment diagram after thin-slicing |

## Entry conditions

- [Shaping](shaping.md) exit gate passed, **or** operator waives shaping for brownfield with existing map.
- Workspace and context sources available.

## Expected outputs

- Domain: `domain-terms` / `ubiquitous-language` artifacts; optional domain `.drawio`.
- Story: `story-graph.json`, `story-map.md`, `thin-slicing.md`; optional story `.drawio`.
- UX: `information-architecture.md` + `.drawio` under `docs/ux/`.
- Architecture-centric engineering: `architecture-blueprint.md`, SLO doc when assigned; paired diagrams per skill.

## Exit gate

1. `story-graph.json` passes `story_graph_cli.py read` when story work ran.
2. Scanners green for **each assigned skill**.
3. Full-mode map: epics → sub-epics → stories; verb–noun naming; actors assigned.
4. IA, domain, and blueprint consistent with each other — **ripple check** per [README.md](README.md) **before** thin-slicing.
5. Every story assigned to a slice when thin-slicing ran.
6. User confirmed at checkpoint.

## Handoff to next stage

Pass to [exploration.md](exploration.md):

- All artifact paths; recommended first slice for exploration.
- Ripple flags for any cross-family mismatches found during discovery.
