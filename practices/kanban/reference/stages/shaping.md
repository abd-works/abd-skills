# Shaping

**Pull:** When a ticket is `stage: shaping` and active, agents pull skills from `kanban.json` for this stage — same [pull-model](../../agents/reference/pull-model.md) as all stages.
**Follow-on:** [discovery.md](discovery.md) · **Index:** [README.md](README.md)

## Purpose

Establish the **whole-solution** view — wide and shallow. Partition the problem space, sketch architecture context, and produce a **story map in outline mode** (epics and major flows only, not full story depth).

Shaping uses the same **`abd-story-mapping`** skill as Discovery but in **outline mode**: actors and epics visible, minimal story detail until Discovery deepens the map.

## Team role

**Product Owner** (default). Extension skills assign **Business Expert** (domain partition), **UX Designer** (impact mapping), or **Engineer** (architecture outline) per slot.

## Practice skills

Skill order when running the full shaping pass: **domain → story (outline) → UX → architecture**.

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Domain-driven design** | `abd-domain-partition` | Business Expert | Corpus / module boundaries before detailed mapping |
| 2 | **Domain-driven design** | `abd-bounded-context-map` | Business Expert | Context relationships when multiple modules |
| 3 | **Story-driven delivery** | `abd-story-mapping` (**outline mode**) | Product Owner | Epic-level map; actors and journeys, not full decomposition |
| 3b | **Story-driven delivery** | `drawio-story-sync` | Product Owner | **Background** after story-mapping — `story-map.drawio` ([drawio-sync-background.md](../../agents/reference/drawio-sync-background.md)) |
| 4 | **Idea shaping** | `abd-opportunity-generation` | Product Owner | Optional — frame opportunity and assumptions before Discovery |
| 5 | **User experience design** | `abd-impact-mapping` | UX Designer | Goals → actors → impacts → deliverable options before full IA |
| 6 | **Architecture-centric engineering** | `abd-architecture-outline` | Engineer | System context, layering, deployment — no blueprint depth yet |

## Entry conditions

- Workspace is set and accessible.
- At least one context source exists (brief, documents, interviews, existing repo).

## Expected outputs

All artifacts flat under **`docs/end-to-end/shaping/`**. See [artifact-layout.md](../artifact-layout.md).

- Module-partition / context-map in `docs/end-to-end/shaping/` (`modules/<name>/` only when partition requires it).
- `docs/end-to-end/shaping/story-graph.json` (outline depth) when story-mapping ran.
- Impact map in `docs/end-to-end/shaping/` when `abd-impact-mapping` ran.
- `docs/end-to-end/shaping/architecture-outline.md` (+ diagram) when outline skill ran.

## Exit gate

1. For **each practice skill listed in the slot start file**, `run_scanners.py --skill-root <skill> --workspace <workspace>` exits 0.
2. Outline story map is reviewable left-to-right at epic / sub-epic level.
3. Module or context boundaries are explicit when domain skills ran.
4. Architecture outline exists when assigned — components named, not mechanism internals.
5. User confirmed at checkpoint.

## Handoff to next stage

Pass to [discovery.md](discovery.md):

- Paths to partition, outline map, and architecture outline artifacts.
- Open questions flagged for full Discovery pass.
- Ripple check: domain partition vs outline map vs arch outline — reconcile before Discovery slot 1.
