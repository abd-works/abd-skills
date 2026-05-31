# Exploration

**Pull:** When a ticket is `stage: exploration` and active, agents pull skills from `kanban.json` for this stage — same [pull-model](../../agents/reference/pull-model.md) as all stages.
**Prior:** [discovery.md](discovery.md) · **Follow-on:** [specification.md](specification.md) · **Index:** [README.md](README.md)

## Purpose

Deepen the **current increment** (medium scope): ubiquitous language, behavioral acceptance criteria, lo-fi UX mockups, and architecture **template** for mechanisms needed in the slice.

## Team role

**Product Owner** (default for AC). Extension skills assign **Business Expert** (ubiquitous language — before AC), **UX Designer**, or **Engineer** per slot.

## Practice skills

When running the full exploration pass, default skill order: **domain (UL) → story (AC) → UX → architecture**.

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Domain-driven design** | `abd-ubiquitous-language` | Business Expert | Increment vocabulary **before** AC |
| 2 | **Domain-driven design** | `drawio-domain-sync` | Business Expert | **Background** after UL — class diagram beside `ubiquitous-language.md` |
| 3 | **Story-driven delivery** | `abd-acceptance-criteria` | Product Owner | WHEN/THEN AC using UL terms |
| 3b | **Story-driven delivery** | `drawio-story-sync` | Product Owner | **Background** after AC + graph sync — `acceptance-criteria.drawio` |
| 4 | **Story-driven delivery** | `drawio-story-sync` | Product Owner | Optional — refresh exploration diagrams when assigned separately |
| 5 | **User experience design** | `abd-ux-mockup` | UX Designer | Lo-fi wireframes after IA and AC |
| 6 | **Architecture-centric engineering** | `abd-architecture-template` | Engineer | **Conditional** — run only when the increment needs mechanism template sections not yet documented; otherwise mark skill skipped (see below) |

### Conditional: `abd-architecture-template`

**Run when:** AC and blueprint imply cross-cutting mechanisms not yet in `docs/increments/<n>-<slug>/exploration/architecture/architecture-template.md`.

**Skip when:** Every mechanism the increment needs is already documented — assign existing sections; mark `skill_progress` done with skip notes.

**Before writing:** List mechanisms from AC + `docs/end-to-end/discovery/architecture/architecture-blueprint.md`; discover existing sections in increment `exploration/` subfolders or `end-to-end/exploration/` after prior roll-ups.

## Entry conditions

- [Discovery](discovery.md) exit gate passed.
- Target increment / slice identified in `story-graph.json`.

## Expected outputs

Under **`docs/increments/<n>-<slug>/exploration/`** with four concern subfolders (`domain/`, `stories/`, `ux/`, `architecture/`) — same layout as `end-to-end/exploration/`. One canonical file per type per subfolder; merge sprint/story/scenario as sections. See [artifact-layout.md](../artifact-layout.md).

- `domain/ubiquitous-language.md`, `stories/acceptance-criteria.md`, `ux/mockups.md` (+ `.drawio`), `architecture/architecture-template.md` when assigned.
- **`docs/end-to-end/discovery/stories/story-graph.json`** — `acceptance_criteria[]` populated on every in-scope story (sync from `acceptance-criteria.md` via `md_acceptance_criteria_to_story_graph.py`; see [artifact-layout.md](../artifact-layout.md)).

## Exit gate

1. Graph valid when AC ran; scanners green for each assigned skill.
2. Every in-scope story has ≥1 WHEN/THEN AC in **`story-graph.json`** (not only in markdown) when AC skill ran.
3. Mockups match IA and exercise AC when UX skill ran.
4. Architecture template ran for undocumented mechanisms, or skill marked skipped with rationale when all mechanisms already exist.
5. **Ripple check:** domain ↔ AC ↔ UX ↔ arch template aligned per [README.md](README.md).
6. User confirmed at checkpoint.

## Handoff to next stage

Pass to [specification.md](specification.md):

- AC, mockup, UL, and template artifact paths.
- Scope of stories ready for specification.
