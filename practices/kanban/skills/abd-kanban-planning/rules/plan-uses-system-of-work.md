---
scanner: plan-shape
---

# Rule: Plans configure the kanban board stage configuration

**Scanner:** `scanners/plan-shape-scanner.py` — rule id `plan-uses-system-of-work`

Every engagement plan must name a **strategy** and produce a **kanban board stage configuration** (stored in `system-of-work.json`) — ordered stages, each with a scope level and stage work required. **Do not** pre-list every skill assignment for every ticket. Agents pull skill work from the kanban board at runtime.

## DO

- Select **one named strategy** from `strategies/` (or define a custom one) and cite it in the plan.
- Write **`kanban.json`** with the kanban board configuration: stages, scope per stage, ordered stage work required with delivery role assignments, strategy (scatter rules, checkpoint policy, autonomy), and team.
- Show the **full kanban board stage configuration table** (stages, scope, skills) for the engagement in the plan.
- When inventing a **new** custom configuration, **CHECKPOINT:** ask the operator whether to add it to `abd-kanban-planning/strategies/` for reuse.

## DO NOT

- Pre-author skill assignments per ticket — agents pull from the kanban board at runtime.
- Use slot files (`slot-NN-start.md`, `slot-NN-finished.md`) — those are removed.
- Treat `system-of-work.json` as a separate domain concept; it is the on-disk representation of the kanban board's stage configuration.
- Duplicate stage skill lists across multiple places — `system-of-work.json` is the single source of truth.

## Example (wrong)

```markdown
## Skills per ticket

| Ticket | Stage | Skill | Agent |
| --- | --- | --- | --- |
| inc-1 | exploration | abd-domain-language | business-expert |
| inc-1 | exploration | abd-acceptance-criteria | product-owner |
```

Pre-assigns skills to specific tickets — duplicates the kanban board; brittle.

## Example (correct)

```markdown
## Strategy: new-thin-slice

**Kanban board stage configuration** (from strategy `new-thin-slice`):

| Stage | Scope | Stage work required (ordered) |
| --- | --- | --- |
| shaping | all | abd-story-mapping (product-owner), abd-thin-slicing (product-owner) |
| discovery | increment | abd-domain-terms (business-expert), abd-story-mapping (product-owner) |
| exploration | increment | abd-domain-language (business-expert), abd-acceptance-criteria (product-owner) |
| engineering | sprint | abd-interface-design (ux-designer), abd-domain-implementation (business-expert), abd-acceptance-test-driven-development (product-owner), abd-clean-code (engineer) |

Stored in `delivery-war-room/system-of-work.json`. Agents pull skill work from any ticket at the matching stage.
```
