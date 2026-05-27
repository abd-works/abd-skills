# Delivery planning strategies

One **`.md`** file per strategy (this README excluded). The delivery lead **matches** engagement context and classified risks to **When to use** in each file, then **adapts** the step table to the workspace.

## Bootcamp stages (canonical names)

Use these stage slugs in plan **Runs** tables. Full entry/exit gates and skill order: [`../../../content/stages/README.md`](../../../content/stages/README.md).

| # | Stage | Default role | Notes |
| --- | --- | --- | --- |
| 1 | **shaping** | Product Owner | Outline map, partition, arch outline, optional impact map |
| 2 | **discovery** | Product Owner | Domain → story (full) → UX IA → blueprint → **thin slicing last** |
| 3 | **exploration** | Product Owner | UL → AC → UX mockup → arch template (per increment) |
| 4 | **specification** | Product Owner | CRC → spec-by-example → walkthrough → interface → arch reference |
| 5 | **engineering** | Multi-role | interface design impl (UX) → object model → ATDD → clean code (Engineer) |

**Not separate stages:** thin slicing (last in discovery). **ATDD** is Engineering step 3 — package in story-driven delivery, **Engineer executes**. Legacy names (`prioritization`, `story definition`, `acceptance tests`, `code`) are deprecated.

## Team roles

Four roles — assign **`team-role`** per slot: **Product Owner**, **Business Expert**, **UX Designer**, **Engineer**. [team-roles.md](../../../content/roles/team-roles.md)

Extension skills in a stage use the matching role (e.g. Business Expert for domain terms in discovery, Engineer for blueprint).

## Strategy table columns

| Column | Content |
| --- | --- |
| **Step** | Order within the strategy (not always one plan run) |
| **Stage** | Bootcamp stage(s) for this step — use `→` for a chain within one run |
| **Intent** | What this step achieves |
| **Scope** | Stories, slice, epic, or area |
| **Checkpoint policy** | Where to stop for review |
| **Rationale** | Concrete outcome when the step completes — not risk-only |

## Catalog

| File | When to use (summary) |
| --- | --- |
| [new-user-story.md](new-user-story.md) | 1–3 stories on an existing solution |
| [new-thin-slice.md](new-thin-slice.md) | Vertical slice on existing product (~5–15 stories) |
| [new-initiative-no-documented-architecture.md](new-initiative-no-documented-architecture.md) | Greenfield; no settled map or architecture |
| [new-initiative-proprietary-technology-risk.md](new-initiative-proprietary-technology-risk.md) | Undocumented proprietary systems / integrations |
| [new-initiative-business-user-experience-risk.md](new-initiative-business-user-experience-risk.md) | UX, domain, ops, and data meaning dominate risk |
| [legacy-migration.md](legacy-migration.md) | Replace system; legacy behavior is truth |
| [regulatory-compliance-heavy.md](regulatory-compliance-heavy.md) | Regulation / compliance dominates |
| [bug-fix.md](bug-fix.md) | Defect or regression; small bounded scope |
| [spike-proof-of-concept.md](spike-proof-of-concept.md) | Answer one question before full delivery |

## Adding a strategy

After a custom engagement, save a new **`<slug>.md`** here using the same six-column step table and **Key constraints** section. Reference bootcamp stages only.
