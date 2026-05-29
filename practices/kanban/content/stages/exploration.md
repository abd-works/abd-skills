# Exploration

**Prior:** [discovery.md](discovery.md) · **Follow-on:** [specification.md](specification.md) · **Index:** [README.md](README.md)

## Purpose

Deepen the **current increment** (medium scope): ubiquitous language refresh, behavioral acceptance criteria, lo-fi UX mockups, and architecture **template** for mechanisms needed in the slice.

## Team role

**Product Owner** (default for AC). Extension skills assign **Business Expert** (UL — typically before AC), **UX Designer**, or **Engineer** per slot.

## Practice skills

When running the full exploration pass, default skill order: **domain (UL) → story (AC) → UX → architecture**.

| Order | Family | Skill | Role | Notes |
| --- | --- | --- | --- | --- |
| 1 | **Domain-driven design** | `abd-ubiquitous-language` | Business Expert | UL refresh for the increment **before** AC |
| 2 | **Domain-driven design** | `drawio-domain-sync` | Business Expert | Optional domain diagram refresh |
| 3 | **Story-driven delivery** | `abd-acceptance-criteria` | Product Owner | WHEN/THEN AC using UL terms |
| 4 | **Story-driven delivery** | `drawio-story-sync` | Product Owner | Exploration / AC diagrams when assigned |
| 5 | **User experience design** | `abd-ux-mockup` | UX Designer | Lo-fi wireframes after IA and AC |
| 6 | **Architecture-centric engineering** | `abd-architecture-template` | Engineer | Mechanism patterns for the slice — not full reference yet |

## Entry conditions

- [Discovery](discovery.md) exit gate passed.
- Target increment / slice identified in `story-graph.json`.

## Expected outputs

- UL updates when assigned (before AC in a full pass).
- AC in graph + `acceptance-criteria.md`; optional exploration `.drawio`.
- UX mockup `.drawio` + companion markdown when assigned.
- Architecture template sections for assigned mechanisms.

## Exit gate

1. Graph valid when AC ran; scanners green for each assigned skill.
2. Every in-scope story has ≥1 WHEN/THEN AC when AC skill ran.
3. Mockups match IA and exercise AC when UX skill ran.
4. **Ripple check:** domain ↔ AC ↔ UX ↔ arch template aligned per [README.md](README.md).
5. User confirmed at checkpoint.

## Handoff to next stage

Pass to [specification.md](specification.md):

- AC, mockup, UL, and template artifact paths.
- Scope of stories ready for specification.
