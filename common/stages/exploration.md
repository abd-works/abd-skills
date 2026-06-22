# Exploration

**Pull:** When a ticket is `stage: exploration` and active, agents pull skills from `kanban.json` for this stage.
**Prior:** [discovery.md](discovery.md) · **Follow-on:** [specification.md](specification.md)

## Purpose

Deepen the **current increment** (medium scope): conceptual domain model, behavioral acceptance criteria, lo-fi UX mockups, and architecture specification **document** for mechanisms needed in the slice.

## Outcomes

- solution tests
- business logic
- user experience
- tech design

## Team role

**Product Owner** (default for AC). Extension skills assign **Business Expert** (domain model — before AC), **UX Designer**, or **Engineer** per slot.

## Practice skills

When running the full exploration pass, default skill order: **domain (model) → story (AC) → UX → architecture**.

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Domain-driven design** | `abd-domain-model` | Business Expert | Increment conceptual model from discovery Domain Language **before** AC |
| 1b | **Domain-driven design** | `drawio-domain-sync` | Business Expert | **Background** after domain model — `domain-model-class-diagram.drawio` |
| 2 | **Story-driven delivery** | `abd-story-acceptance-criteria` | Product Owner | WHEN/THEN AC using UL terms |
| 2b | **Story-driven delivery** | `drawio-story-sync` | Product Owner | **Background** after AC + graph sync — `acceptance-criteria.drawio` |
| 3 | **User experience design** | `abd-ux-mockup` | UX Designer | Lo-fi wireframes after IA and AC |
| 4 | **Architecture-centric engineering** | `abd-architecture-specification` | Engineer | **Document mode** — conditional; run when increment needs mechanism sections not yet in `architecture-specification.md` |

### Conditional: `abd-architecture-specification` (document mode)

**Run when:** AC and blueprint imply cross-cutting mechanisms not yet in `docs/increments/<n>-<slug>/exploration/architecture/architecture-specification.md` (or assigned named spec).

**Skip when:** Every mechanism the increment needs is already documented — assign existing sections; mark `skill_progress` done with skip notes.

**Before writing:** List mechanisms from AC + `docs/end-to-end/discovery/architecture/architecture-blueprint.md`; discover existing sections in increment `exploration/` subfolders or `end-to-end/exploration/` after prior roll-ups.

## Entry conditions

- [Discovery](discovery.md) exit gate passed.
- Target increment / slice identified in `story-graph.json`.

## Expected outputs

Under **`docs/increments/<n>-<slug>/exploration/`** with four concern subfolders (`domain/`, `stories/`, `ux/`, `architecture/`) — same layout as `end-to-end/exploration/`. One canonical file per type per subfolder; merge sprint/story/scenario as sections. See [artifact-layout.md](../artifact-layout.md).

- `domain/domain-model.md`, `domain.json`, `stories/acceptance-criteria.md`, `ux/mockups.md` (+ `.drawio`), `architecture/architecture-specification.md` when assigned.
- **`docs/end-to-end/discovery/stories/story-graph.json`** — `acceptance_criteria[]` populated on every in-scope story (sync from `acceptance-criteria.md` via `md_acceptance_criteria_to_story_graph.py`; see [artifact-layout.md](../artifact-layout.md)).

## Exit gate

1. Graph valid when AC ran; scanners green for each assigned skill.
2. Every in-scope story has ≥1 WHEN/THEN AC in **`story-graph.json`** (not only in markdown) when AC skill ran.
3. Mockups match IA and exercise AC when UX skill ran.
4. Architecture specification doc ran for undocumented mechanisms, or skill marked skipped with rationale when all mechanisms already exist.
5. **Ripple check:** domain ↔ AC ↔ UX ↔ architecture doc aligned.
6. User confirmed at checkpoint.

## Handoff to next stage

Pass to [specification.md](specification.md):

- AC, mockup, UL, and specification artifact paths.
- Scope of stories ready for specification.
