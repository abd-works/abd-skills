# Delivery war room — role agent autostart

Eight **persistent role agents** pull skill-level work from tickets on the **Kanban board** (`board.json`). Open the agent matching your role.

| You are | Agent |
| --- | --- |
| Product Owner executor | `kanban/agents/product-owner/AGENT.md` |
| Product Owner reviewer | `kanban/agents/product-owner-reviewer/AGENT.md` |
| Business Expert executor | `kanban/agents/business-expert/AGENT.md` |
| Business Expert reviewer | `kanban/agents/business-expert-reviewer/AGENT.md` |
| UX Designer executor | `kanban/agents/ux-designer/AGENT.md` |
| UX Designer reviewer | `kanban/agents/ux-designer-reviewer/AGENT.md` |
| Engineer executor | `kanban/agents/engineer/AGENT.md` |
| Engineer reviewer | `kanban/agents/engineer-reviewer/AGENT.md` |

Shared queue rules: `kanban/agents/_shared/work-queue.md`

## 1) Workspace

Bootstrap must include **`workspace`** — the engagement root.

## 2) Board state

Read `docs/planning/delivery-war-room/board.json` and `system-of-work.json`.

Each **ticket** is in one list: `backlog` · `active` · `done` · `archived`.

Each ticket tracks **per-skill progress** (to_do, in_progress, done + review status).

## 3) Claim next skill

1. Read **`board.json`** — find active tickets with skills matching your role.
2. Check **skill order**: prior skills in the stage must be done before you can claim the next.
3. Priority: **downstream stage first** (engineering > spec > explore > discovery > shaping).
4. Claim: set skill `status: in_progress`, `agent: <your-role>`, `start: <now>`.

See `_shared/work-queue.md` for full algorithm.

## 4) Execute

Executors → `_shared/executor-workflow.md`. Reviewers → `_shared/reviewer-workflow.md`.

## 5) When done

Mark skill `status: done`, `end: <now>`. Pull next eligible skill.

## 6) When blocked

Set skill `status: blocked` — kanban lead handles in scan cycle.
