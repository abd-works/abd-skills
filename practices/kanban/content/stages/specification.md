# Specification

**Prior:** [exploration.md](exploration.md) · **Follow-on:** [engineering.md](engineering.md) · **Index:** [README.md](README.md)

## Purpose

Define stories with **domain model** cards that supply concepts for outline **example tables**, then **concrete specification-by-example** scenarios, production-grade **interface design** intent, scenario **walkthrough**, and **architecture reference** for mechanisms used in the slice. Narrow scope — story-level depth.

## Team role

**Product Owner** (default for spec-by-example). Extension skills assign **Business Expert** (domain model — before spec; walkthrough — after spec), **UX Designer**, or **Engineer** per slot.

## Practice skills

When running the full specification pass, default skill order: **domain (domain model) → story (spec) → domain (walkthrough) → UX → architecture**.

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Domain-driven design** | `abd-domain-model` | Business Expert | domain model cards + `domain.json` — concepts for spec outline tables |
| 2 | **Story-driven delivery** | `abd-story-specification` | Product Owner | Given/When/Then with real values; tables name domain model concepts |
| 3 | **Domain-driven design** | `abd-domain-walk` | Business Expert | Walk spec scenarios through the domain model — every step maps to a concept |
| 4 | **User experience design** | `abd-interface-design` | UX Designer | **Spec pass** — author `interface-design.md` from lo-fi mockups |
| 5 | **Architecture-centric engineering** | `abd-architecture-reference` | Engineer | Deep mechanism reference for Engineering |

## Entry conditions

- [Exploration](exploration.md) exit gate passed.
- Stories have AC; mockups available when interface skill is assigned.
- **domain model** (and `domain.json`) complete **before** spec-by-example when outline / example tables are in scope.

## Expected outputs

- domain model artifacts + `domain.json` when domain model ran — table names and columns trace to domain model concepts.
- Scenario files + graph references (outline tables validated against domain model / `domain.json`).
- Scenario walkthrough markdown when walkthrough ran.
- Interface spec / component notes when UX skill ran.
- Architecture reference sections when assigned.

## Exit gate

1. Graph valid; scanners green for each assigned skill.
2. domain model concepts and `domain.json` exist **before** outline spec tables when both domain model and spec ran.
3. Scenarios trace to AC with concrete values when spec skill ran; table names/columns match domain model when outlines used.
4. Walkthrough maps every scenario step to domain model concepts when walkthrough ran.
5. Reference docs match template from exploration when arch skill ran.
6. **Ripple check** per [README.md](README.md).
7. User confirmed at checkpoint.

## Handoff to next stage

Pass to [engineering.md](engineering.md):

- Scenario paths, interface spec, domain model, reference doc paths.
- Test and implementation scope for the slice.
