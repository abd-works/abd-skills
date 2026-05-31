# Delivery stages

Canonical stage definitions for the kanban lead and team members. Source of truth for entry conditions, exit gates, practice skills, and team roles per skill.

**Pull model:** Agents pull eligible skills on active tickets in **every stage** — same algorithm, downstream first. See [../agents/reference/pull-model.md](../agents/reference/pull-model.md).

**Bootcamp reference:** [AI-Augmented Delivery Bootcamp — Five Families × Five Stages](https://forge.abdworks.net/abd-ai-augmented-bootcamp/#/22/1)

## Stages (bootcamp order)

| # | Stage | File | Follow-on |
| --- | --- | --- | --- |
| 1 | **Shaping** | [shaping.md](shaping.md) | → [discovery.md](discovery.md) |
| 2 | **Discovery** | [discovery.md](discovery.md) | → [exploration.md](exploration.md) |
| 3 | **Exploration** | [exploration.md](exploration.md) | → [specification.md](specification.md) |
| 4 | **Specification** | [specification.md](specification.md) | → [engineering.md](engineering.md) |
| 5 | **Engineering** | [engineering.md](engineering.md) | → next increment / [discovery.md](discovery.md) refresh |

## Skill families (default executor role)

Four **families** organize packages under `skills/`. Each has a **default** executor role — stage files override when cross-family (see [team-roles.md](../roles/team-roles.md)).

| Family | Default role | Playbook |
| --- | --- | --- |
| **Story-driven delivery** | Product Owner | [product-owner.md](../roles/product-owner.md) |
| **Domain-driven design** | Business Expert | [business-expert.md](../roles/business-expert.md) |
| **User experience design** | UX Designer | [ux-designer.md](../roles/ux-designer.md) |
| **Architecture-centric engineering** (`architecture-centric-engineering/`) | Engineer | [engineer.md](../roles/engineer.md) |

Role index: [team-roles.md](../roles/team-roles.md)

## Cross-artifact updates

Any output in one family can force an update in another. After each skill, the kanban lead checks ripple triggers before opening the next skill:

| When this changes… | Review / update… |
| --- | --- |
| Domain terms, UL, CRC, object model | Story map labels, AC, scenarios, architecture component names |
| Story map (add/rename/split stories) | Domain terms, IA screen lists, slice assignments, AC scope |
| UX IA or mockups | AC (interaction-level), interface design, story coverage on screens |
| Architecture blueprint / template / reference | Domain boundaries, test layout, module structure, SLOs |
| AC or scenarios | Mockups, CRC, tests, code, **`story-graph.json`** (`acceptance_criteria[]`, `scenarios[]`) |

Log conflicts in `docs/corrections-log.md`; do not advance the slot until assigned ripple updates are scoped or waived at checkpoint.

## Layered context (bootcamp)

| Scope | Depth | Artifact root |
| --- | --- | --- |
| Whole solution | Shaping, Discovery | `docs/end-to-end/shaping/`, `docs/end-to-end/discovery/` — write directly |
| Whole solution | Exploration, Spec, Eng | `docs/end-to-end/{exploration,specification,engineering}/` — filled on increment roll-up |
| Increment (in flight) | Exploration → Engineering | `docs/increments/<n>-<slug>/{exploration,specification,engineering}/` |

**Canonical paths:** [artifact-layout.md](../artifact-layout.md)
