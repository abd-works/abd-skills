# Work queue — role agents

Delivery **executor** and **reviewer** agents are **persistent by role**. The kanban lead instantiates each role agent **once** at engagement bootstrap; agents **pull skill-level work** from active tickets on the Kanban board.

## Board model

Board state lives in `<workspace>/docs/planning/delivery-war-room/board.json`.

Each ticket in `active` has a `skills` object with per-skill progress. Agents claim skills matching their role.

## Role agents

| Agent | Pulls |
| --- | --- |
| `product-owner` | `role: product-owner`, `slot_type: executor` → skills on active tickets |
| `product-owner-reviewer` | same role, review on completed executor skills |
| `business-expert` | `role: business-expert`, executor |
| `business-expert-reviewer` | reviewer |
| `ux-designer` | `role: ux-designer`, executor |
| `ux-designer-reviewer` | reviewer |
| `engineer` | `role: engineer`, executor |
| `engineer-reviewer` | reviewer |

Agents are **not stage-locked**. They claim eligible skills across all stages, prioritizing downstream work first.

Shared workflows: [executor-workflow.md](executor-workflow.md) · [reviewer-workflow.md](reviewer-workflow.md)

## Bootstrap (once per engagement)

Every role agent session receives **only** this bootstrap payload from the kanban lead:

- **`workspace`** — engagement root (required)
- **`team-role`** — fixed by which agent you are
- **`slot_type`** — `executor` or `reviewer` (fixed)

If `workspace` is missing, ask once and stop.

## Claim next skill (pull from board)

After finishing work — or on first turn:

1. Read **`board.json`** and `system-of-work.json`.

2. Find **active tickets** with skills matching your `team-role`:
   - **Executor** → skills where `role` matches and `status: to_do`
   - **Reviewer** → skills where `role` matches, `status: done`, and `review_status: null`

3. **Skill order gate**: a skill is only claimable when ALL prior skills in the stage's ordered list (from `system-of-work.json`) have `status: done`. Skills execute in order.

4. **Stage priority (downstream first):**

   | Priority | Stage |
   | --- | --- |
   | 1 (highest) | `engineering` |
   | 2 | `specification` |
   | 3 | `exploration` |
   | 4 | `discovery` |
   | 5 | `shaping` |
   | 6 (lowest) | `context` |

   Within the same stage: **highest-priority ticket** (lowest `priority` number).

5. If nothing qualifies, report **no pending work for this role**.

## Claiming (avoid double work)

Before starting work on a skill, update `board.json`:

- Set skill `status: in_progress` (executor) or `review_status: in_progress` (reviewer)
- Set `agent: <your-role>` or `reviewer: <your-role>`
- Set `start: <ISO 8601>` or `review_start: <ISO 8601>`

## Completing work

When finished:

- Set skill `status: done`, `end: <ISO 8601>` (executor)
- Set `review_status: done`, `review_end: <ISO 8601>` (reviewer)
- Or `review_status: failed` if rework needed (reviewer)

Then immediately pull next eligible skill.

## Rework

When a reviewer marks `review_status: failed`:

- The skill's `status` resets to `to_do` (executor must redo)
- The executor agent will pick it up on next pull cycle
- Corrections should be logged in `docs/corrections-log.md`

## Autostart

If `INSTRUCTIONS.md` exists in the war room:

1. Resolve `workspace`.
2. Read `board.json`, `system-of-work.json`.
3. Claim next eligible skill per algorithm above.
4. Execute per workflow.
5. On finish → claim again until no eligible work.

## Blocked

If an agent cannot proceed:

- Set skill `status: blocked` with a note
- Report to kanban lead (will appear in scan cycle)
- Stop claiming until unblocked
