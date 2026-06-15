# Kanban war room — role agent autostart

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

Read `docs/planning/kanban/board.json` and `system-of-work.json`.

Each **ticket** is in one list: `backlog` · `active` · `done` · `archived`.

**Skills are defined in `system-of-work.json`** — not on the ticket. The ticket only carries a `progress` map (lazily populated when agents claim).

## 3) Claim next skill

1. Read **`system-of-work.json`** — find the skill list for the ticket's current stage.
2. Read **`board.json`** — find active tickets where a skill matching your role has no progress entry or is `to_do`.
3. Check **skill order**: prior skills in the stage (from system of work) must be done before you can claim the next.
4. Priority: **downstream stage first** (engineering > spec > explore > discovery > shaping).
5. Claim: write a `progress` entry on the ticket — `status: in_progress`, `agent: <your-role>`, `start: <now>`.

See `_shared/work-queue.md` for full algorithm.

## 4) Execute

Executors → `_shared/executor-workflow.md`. Reviewers → `_shared/reviewer-workflow.md`.

## 5) When done

Mark progress entry `status: done`, `end: <now>`. Pull next eligible skill.

## 6) When blocked

Set progress entry `status: blocked` — kanban lead handles in scan cycle.
