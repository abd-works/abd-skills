# Specification

**Prior:** [exploration.md](exploration.md) · **Follow-on:** [engineering.md](engineering.md) · **Index:** [README.md](README.md)

## Purpose

Define stories with **CRC** cards that supply concepts for outline **example tables**, then **concrete specification-by-example** scenarios, production-grade **interface design** intent, scenario **walkthrough**, and **architecture reference** for mechanisms used in the slice. Narrow scope — story-level depth.

## Team role

**Product Owner** (default for spec-by-example). Extension skills assign **Business Expert** (CRC — before spec; walkthrough — after spec), **UX Designer**, or **Engineer** per slot.

## Practice skills

When running the full specification pass, default skill order: **domain (CRC) → story (spec) → domain (walkthrough) → UX → architecture**.

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Domain-driven design** | `abd-class-responsibility-collaborator` | Business Expert | CRC cards + `domain.json` — concepts for spec outline tables |
| 2 | **Story-driven delivery** | `abd-specification-by-example` | Product Owner | Given/When/Then with real values; tables name CRC concepts |
| 3 | **Domain-driven design** | `abd-scenario-walkthrough` | Business Expert | Walk spec scenarios through CRC — every step maps to a concept |
| 4 | **User experience design** | `abd-interface-design` | UX Designer | **Spec pass** — author `interface-design.md` from lo-fi mockups |
| 5 | **Architecture-centric engineering** | `abd-architecture-reference` | Engineer | Deep mechanism reference for Engineering |

## Entry conditions

- [Exploration](exploration.md) exit gate passed.
- Stories have AC; mockups available when interface skill is assigned.
- **CRC** (and `domain.json`) complete **before** spec-by-example when outline / example tables are in scope.

## Expected outputs

- CRC artifacts + `domain.json` when CRC ran — table names and columns trace to CRC concepts.
- Scenario files + graph references (outline tables validated against CRC / `domain.json`).
- Scenario walkthrough markdown when walkthrough ran.
- Interface spec / component notes when UX skill ran.
- Architecture reference sections when assigned.

## Exit gate

1. Graph valid; scanners green for each assigned skill.
2. CRC concepts and `domain.json` exist **before** outline spec tables when both CRC and spec ran.
3. Scenarios trace to AC with concrete values when spec skill ran; table names/columns match CRC when outlines used.
4. Walkthrough maps every scenario step to CRC concepts when walkthrough ran.
5. Reference docs match template from exploration when arch skill ran.
6. **Ripple check** per [README.md](README.md).
7. User confirmed at checkpoint.

## Handoff to next stage

Pass to [engineering.md](engineering.md):

- Scenario paths, interface spec, CRC, reference doc paths.
- Test and implementation scope for the slice.
