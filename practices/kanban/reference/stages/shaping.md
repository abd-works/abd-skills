# Shaping

**Pull:** When a ticket is `stage: shaping` and active, agents pull skills from `kanban.json` for this stage.
**Follow-on:** [discovery.md](discovery.md) · **Index:** [README.md](README.md)

## Purpose

Establish the **whole-solution** view — wide and shallow. Partition the problem space, sketch architecture context, and produce a **story map in outline mode** (epics and major flows only, not full story depth).

Shaping uses the same **`abd-story-mapping`** skill as Discovery but in **outline mode**: actors and epics visible, minimal story detail until Discovery deepens the map.

## Outcomes

- Business Logic
- Solution Behavior
- UI Layout
- Technology Design

## Team role

**Product Owner** (default). Extension skills assign **Business Expert** (domain glossary) or **Engineer** (architecture outline) per slot.

## Practice skills

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Domain-driven design** | `abd-domain-glossary` | Business Expert | Module boundaries + KA-grouped domain terms in one pass |
| 2 | **Story-driven delivery** | `abd-story-mapping` (**outline mode**) | Product Owner | Epic-level map; actors and journeys, not full decomposition |
| 2b | **Story-driven delivery** | `drawio-story-sync` | | **Background** after story-mapping — `story-map.drawio` |
| 3 | **User experience design** | `abd-impact-mapping` | Product Owner | Outcome-first goals, actors, impacts, deliverable options |
| 4 | **Architecture-centric engineering** | `abd-architecture-outline` | Engineer | System context, layering, deployment — no blueprint depth yet |

## Entry conditions

- Workspace is set and accessible.
- At least one context source exists (brief, documents, interviews, existing repo).

## Expected outputs

All artifacts flat under **`docs/end-to-end/shaping/`**. See [artifact-layout.md](../artifact-layout.md).

- `docs/end-to-end/shaping/domain/domain-glossary.md` (or per-module files under `domain/domain-glossary/`) when domain glossary ran.
- `docs/end-to-end/shaping/story-graph.json` (outline depth) when story-mapping ran.
- `docs/end-to-end/shaping/impact-map.md` when impact mapping ran.
- `docs/end-to-end/shaping/architecture-outline.md` (+ diagram) when outline skill ran.

## Exit gate

1. Scanners green for each assigned skill.
2. Outline story map is reviewable left-to-right at epic / sub-epic level.
3. Domain glossary exists with KA-grouped terms when domain glossary ran.
4. Architecture outline exists when assigned — components named, not mechanism internals.
5. User confirmed at checkpoint.

## Handoff to next stage

Pass to [discovery.md](discovery.md):

- Paths to domain glossary, outline map, impact map, and architecture outline artifacts.
- Open questions flagged for full Discovery pass.
- Ripple check: domain glossary vs outline map vs arch outline — reconcile before Discovery slot 1.
