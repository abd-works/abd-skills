---
scanner: plan-shape
---

# Rule: Multi-run plans use a system of work — slots materialize at run open

**Scanner:** `scanners/plan-shape-scanner.py` — rule id `plan-uses-system-of-work`

When an engagement delivers **more than one product increment**, the saved plan names **runs** and a reusable **system of work** (stages, stage order, skill order per stage). **Do not** pre-list every slot for every run in `agile-delivery-plan.md`. Slots are generated when each run **opens** via `generate_run_slots.py` into `delivery-war-room/`.

## DO

- Define **one or more named systems of work** in the plan (`## System of work`) and in `delivery-war-room/system-of-work.json` — from a planning **strategy** or a custom name.
- List **each run** in the plan and in `delivery-war-room/run-catalog.json` with: title, scope, stages, `system_of_work` reference, optional waivers, `opens_after` / `discovery_precompleted` when applicable.
- Show **full skill order per stage** for the **first run** that introduces a system of work (or inline the discovery system for Run 1). Later runs **reference the same name** — do not duplicate the full skill tables.
- At war-room setup (Step 2b): write `system-of-work.json`, `run-catalog.json`, and `run-state.json` — **not** all `slot-NN-start.md` files.
- When a run opens: run `generate_run_slots.py --workspace <root> --run N` to materialize slots; update `run-state.json`.
- When inventing a **new** custom system of work, **CHECKPOINT:** ask the operator whether to add it to `abd-delivery-planning/strategies/` for reuse.

## DO NOT

- Pre-author slot tables for Runs 3–10 in the plan when they share the same system of work as Run 2.
- Use **routine template**, **offset +N**, or **estimated slot ranges** as a substitute for `system-of-work.json` + run open generation.
- Rely on fragile slot-table parsing in `agile-delivery-plan.md` for Kanban sync — `run-catalog.json` + `run-state.json` are authoritative for run membership.

## Example (wrong)

```markdown
## Runs 3–10 — routine template
| Offset | Phase | Role | Skills |
| +0 | exploration | business-expert | abd-ubiquitous-language |
```

(No named system of work; no run-catalog; slots not generated at run open.)

## Example (correct)

```markdown
## System of work — pawplace-increment-vertical

**From strategy:** `new-thin-slice`  
**Stages:** exploration → specification → engineering  
**Skill order:** per `delivery-war-room/system-of-work.json` (same for Runs 2–10)

## Run 2 — Increment 1 (defines reference run)

**system_of_work:** `pawplace-increment-vertical`  
**Stages:** exploration, specification, engineering  
**Scope:** Increment 1 stories …

## Run 8 — Increment 7

**system_of_work:** `pawplace-increment-vertical` (same as Run 2)  
**discovery_precompleted:** true  
**Slots:** materialize at run open (`generate_run_slots.py --run 8`)
```
