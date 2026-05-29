---
name: abd-kanban
description: >-
  JIT Kanban board for kanban-lead and role agents.
  delivery-war-room/ under the engagement workspace is the authoritative source of
  all delivery progress — board.json, system-of-work.json, metrics, and ticket history.
  Tickets flow through stages, scatter at scope boundaries, and agents pull skill-level
  work without pre-authored slot files.
---

# abd-kanban

## Purpose

Single on-disk home for **progress** and **handoffs**. Models delivery as a **JIT Kanban board** where work tickets flow through stages defined by a **system of work**, scatter into finer-grained tickets at scope boundaries, and role agents pull skill-level tasks from active tickets.

## Core concepts

| Concept | Definition |
| --- | --- |
| **System of work** | Static definition: ordered stages, each with a scope level and ordered skills |
| **Work ticket** | A unit of work at the scope defined by its current stage (all, increment, sprint, story) |
| **Backlog** | Ordered list of tickets awaiting their next stage — hierarchy from story map |
| **Scatter** | When a ticket completes a stage whose next stage has finer scope, it decomposes into child tickets |
| **Lineage** | Every ticket carries its ancestry: project > increment > sprint > story |
| **Skill progress** | Each ticket tracks per-skill status (to_do, in_progress, done) within its current stage |

## Kanban model

| Concept | Implementation |
| --- | --- |
| **Work ticket** | Scope unit at the level its stage requires (all, increment, sprint, story) |
| **Backlog** | Ordered; only decomposed JIT; hierarchy from story map + thin-slicing |
| **Active** | Tickets with at least one skill in_progress |
| **Done** | All skills in stage complete; awaiting scatter or next stage pull |
| **Blocked** | Ticket with a blocker that prevents progress |

Rule: [`rules/kanban-ticket-columns.md`](rules/kanban-ticket-columns.md)

## System of work

The system of work is a **static, reusable definition** that drives all ticket flow. It defines:

1. **Stages** — ordered sequence (context → shaping → discovery → exploration → specification → engineering)
2. **Scope per stage** — what granularity tickets live at (all, increment, sprint, story)
3. **Skills per stage** — ordered list of practice skills to execute, with default role assignment

When scope changes between stages (e.g. shaping at "all" → discovery at "increment"), completing one stage **scatters** the ticket into children at the finer scope.

Template: [`templates/system-of-work.json`](templates/system-of-work.json)

### Default new build

| Stage | Scope | Skills (ordered) |
| --- | --- | --- |
| Context (optional) | all | convert-to-markdown, semantic-context-chunker, chunk-markdown, embed-vectors |
| Shaping | all | story-mapping, thin-slicing |
| Discovery | increment | domain-terms, UL, architecture-blueprint, IA |
| Exploration | increment | UL-refresh, acceptance-criteria, ux-mockup, arch-template |
| Specification | sprint | CRC, spec-by-example, scenario-walkthrough, interface-design, arch-reference |
| Engineering | sprint | interface-design, object-model, ATDD, clean-code |

## Tickets

A ticket is the **unit of Kanban flow**. Its scope matches the system of work's scope for the current stage.

### Ticket shape

```json
{
  "ticket_id": "inc-1",
  "lineage": ["Project Name", "Increment 1"],
  "scope_level": "increment",
  "stage": "exploration",
  "priority": 1,
  "skills": {
    "abd-ubiquitous-language": { "status": "done", "role": "business-expert", "agent": "business-expert", "start": "...", "end": "...", "review_status": "done", "reviewer": "business-expert-reviewer", "review_start": "...", "review_end": "..." },
    "abd-acceptance-criteria": { "status": "in_progress", "role": "product-owner", "agent": "product-owner", "start": "...", "end": null, "review_status": null, "reviewer": null, "review_start": null, "review_end": null },
    "abd-ux-mockup": { "status": "to_do", "role": "ux-designer", "agent": null, "start": null, "end": null, "review_status": null, "reviewer": null, "review_start": null, "review_end": null },
    "abd-architecture-template": { "status": "to_do", "role": "engineer", "agent": null, "start": null, "end": null, "review_status": null, "reviewer": null, "review_start": null, "review_end": null }
  },
  "entered_stage": "2026-05-28T10:00:00Z",
  "completed_stage": null,
  "scatter_from": "project-all",
  "scatter_to": []
}
```

### Skill status flow

Each skill within a ticket follows: **to_do → in_progress → done**

Each skill also has a review cycle: **review_status: null → in_progress → done** (or **failed** → rework)

A ticket's stage is **done** when ALL skills have `status: done` AND `review_status: done`.

### Ticket lifecycle

1. **Created** — enters backlog at priority from story map
2. **Active** — at least one skill claimed by an agent (in_progress)
3. **Stage done** — all skills executed and reviewed
4. **Scatter** (if next stage has finer scope) — parent archived, children enter backlog
5. **Continue** (if next stage has same scope) — ticket enters next stage, skills reset to to_do per system of work
6. **Complete** — final stage done; ticket archived with full timing data

## Scattering

When a ticket completes a stage and the **next stage's scope** is finer than the current stage's scope, the ticket **scatters**:

| Transition | Scatter source | Children created from |
| --- | --- | --- |
| Shaping (all) → Discovery (increment) | Project ticket | Thin-slicing increments from story map |
| Exploration (increment) → Spec (sprint) | Increment ticket | Stories grouped into sprints by kanban lead / strategy |

### Scatter mechanics

1. Parent ticket is **archived** (moved to `archived` with start/end timestamps)
2. Child tickets are **created** at the finer scope level, entering the backlog for the next stage
3. Children carry **lineage** from the parent (e.g. `["Project", "Increment 1", "Sprint 1"]`)
4. Children are ordered by priority from the story map
5. **JIT rule**: only scatter the next N items unless user or strategy says otherwise

### When scope stays the same

Discovery (increment) → Exploration (increment): no scatter. The same ticket moves to the next stage; its skills are populated from the system of work for that stage.

## Backlog

The backlog is **ordered** and **hierarchical**:

- Order comes from story map priority + thin-slicing
- Hierarchy comes from the story map structure (epics → sub-epics → stories)
- Only decomposed as far as needed (JIT)
- Delivery lead or user can pre-decompose ("divide increment 1 into 3 sprints")
- Items not yet scattered stay at their parent scope level until their turn

## Role agents (eight)

| Executor | Reviewer |
| --- | --- |
| `product-owner` | `product-owner-reviewer` |
| `business-expert` | `business-expert-reviewer` |
| `ux-designer` | `ux-designer-reviewer` |
| `engineer` | `engineer-reviewer` |

Agents are **instantiated once** per engagement as **isolated subagents**. They pull skill-level work from active tickets. An agent claims a skill on a ticket when:

1. The skill's `role` matches the agent's `team-role`
2. The skill's `status` is `to_do` (executor) or skill is `done` and `review_status` is null (reviewer)
3. Prior skills in the stage's ordered list are done (skills execute in order)

## Progress authority

| What | Where | Who updates |
| --- | --- | --- |
| **Kanban board** | **`board.json`** | **`sync_kanban_board.py`** (from ticket state) |
| **System of work** | `system-of-work.json` | **kanban-lead** at setup |
| **Strategy** | `strategy.md` | **kanban-lead** at setup |
| **Ticket state** | `board.json` tickets array | Role agents (skill progress) + kanban-lead (scatter, stage transitions) |
| **Metrics** | `board.json` metrics + `metrics-log.jsonl` | **`track_metrics.py`** |
| **Audit trail** | `metrics-log.jsonl` | Delivery lead |
| **Blockers** | ticket `blocked` status | Role agent / operator |

## Workspace layout

```text
<workspace>/docs/planning/
  delivery-war-room/
    board.json                 # Kanban state — tickets, backlog, active, done, archived
    system-of-work.json        # Stage + scope + skill definitions
    strategy.md                # Active strategy (scope progression, scatter rules)
    manifest.md                # Engagement policy, wip_policy, autonomy
    metrics-log.jsonl          # Timestamped events (skill start/end, stage transitions, scatters)
    INSTRUCTIONS.md            # Agent bootstrap instructions
```

## Delivery lead — setup

After strategy selection:

1. Create `<workspace>/docs/planning/delivery-war-room/` if missing.
2. Copy **`templates/INSTRUCTIONS.md`** → `INSTRUCTIONS.md`.
3. Write **`system-of-work.json`** from strategy (or custom).
4. Write `strategy.md` with scope progression rules, scatter heuristics, sprint grouping.
5. Write `manifest.md` with wip_policy, autonomy, checkpoint policy.
6. Initialize **`board.json`** with first ticket (scope: all, stage: shaping).
7. Initialize `metrics-log.jsonl`.
8. Start the **agent scan loop**.

## Delivery lead — scan cycle

Each tick:

1. Read `board.json` — active tickets, backlog, wip_policy.
2. **Detect completed skills** — mark reviewed skills done, check if stage is complete.
3. **Stage transitions** — if all skills done on a ticket, either scatter or advance to next stage.
4. **Scatter** — run `scatter_ticket.py` when scope changes; archive parent, create children in backlog.
5. **Pull from backlog** — move next-priority tickets from backlog to active (respecting WIP).
6. **Bottleneck analysis** — which stage/skill has the most waiting work? Report to operator.
7. **Agent pool** — spawn/scale agents per `wip_policy`.
8. **Sync** — write `board.json`, append `metrics-log.jsonl`.

## Role agent — work cycle

1. Read `board.json` and `manifest.md`.
2. Find active tickets with a skill matching your `team-role` and `slot_type`.
3. **Priority**: rightmost stage first (engineering > spec > explore > discovery > shaping).
4. Claim the skill (set `status: in_progress`, `agent: <role>`, `start: <now>`).
5. Execute the practice skill per executor or reviewer workflow.
6. Mark done (`status: done`, `end: <now>`).
7. Pull next eligible skill.

## Metrics and tracking

Every ticket carries timing data:

- **Per skill**: start, end, review_start, review_end
- **Per stage**: entered_stage, completed_stage
- **Per ticket**: created, archived (when scattered or complete)
- **Lineage** enables rollup: total increment time, total project time, stage cycle times

The kanban lead uses `track_metrics.py` to compute:

- Cycle time per stage, per scope level
- Bottleneck detection (which stage/skill accumulates WIP)
- Throughput (tickets completed per unit time)

## Sync commands

```bash
python kanban/skills/abd-kanban/scripts/sync_kanban_board.py --workspace <workspace>
python kanban/skills/abd-kanban/scripts/scatter_ticket.py --workspace <workspace> --ticket <id>
python kanban/skills/abd-kanban/scripts/track_metrics.py --workspace <workspace>
```

## Templates

Copy from `templates/`: `INSTRUCTIONS.md`, `manifest.md`, `board.json`, `system-of-work.json`, `ticket.json`.

## Limits

- Exit gates remain in `stages/*.md`; war room records Kanban state, it does not replace stage definitions.
- System of work defines skill order; agents follow it without pre-authored assignments.
- Scatter logic is deterministic from the system of work scope transitions and story map structure.
