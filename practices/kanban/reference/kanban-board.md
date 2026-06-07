# Kanban Board

## Core concepts

- **kanban board** — blueprint of ordered stages, each with a scope level and stage work required, governing ticket flow live with tickets flowing through stages
- **ticket** — a unit of work at the scope level its current stage requires, carrying lineage, priority, and skill progress entries created as work starts
- **board position** — backlog, the stage a ticket currently occupies (queue, in progress, or done within that stage), or complete
- **scatter** — when a ticket completes a stage whose next stage has finer scope, it archives itself and creates child tickets at the finer scope level
- **lineage** — every ticket carries its ancestry: project > increment > sprint > story

## Kanban board

The *kanban board* defines an ordered set of *stages* — each with a *scope level* and *stage work required* — and runs live with *tickets* flowing through *stages*.

- **ticket** — scope unit at the level its current stage requires (all, increment, sprint, story)
- **backlog** — ordered; only decomposed JIT; hierarchy from story map + thin-slicing
- **stage in progress** — tickets at a stage where skill work is underway
- **stage done** — all skills in stage complete; ticket awaits pickup to the next stage
- **team** — executor/reviewer pair counts per delivery role configured on the board; one integer per role

## Kanban board stage configuration

The *kanban board* is the single source of truth for which *skills* each *stage* requires. This configuration defines:

1. **Stages** — ordered sequence (context → shaping → discovery → exploration → specification → engineering)
2. **Scope per stage** — what granularity tickets live at (all, increment, sprint, story)
3. **Stage work required per stage** — ordered list of practice skills to execute, with delivery role assignment

When scope changes between stages (e.g. shaping at "all" → discovery at "increment"), completing one stage **scatters** the ticket into children at the finer scope.

### Default new build

- **Context** (optional, scope: all) — convert-to-markdown, semantic-context-chunker, chunk-markdown, embed-vectors
- **Shaping** (scope: all) — module-partition, story-mapping (outline), impact-mapping, architecture-outline
- **Discovery** (scope: increment) — story-mapping (full), domain-terms, IA, architecture-blueprint
- **Exploration** (scope: increment) — UL, acceptance-criteria, ux-mockup, arch-template (when increment needs undocumented mechanisms)
- **Specification** (scope: sprint) — domain model, spec-by-example, interface-design, arch-reference
- **Engineering** (scope: sprint) — interface-design, class-model, ATDD, clean-code

## Tickets

A ticket is the **unit of kanban flow**. Its scope matches the kanban board's scope for the current stage.

### Ticket shape

```json
{
  "ticket_id": "inc-1",
  "lineage": ["Project Name", "Increment 1"],
  "scope_level": "increment",
  "stage": "exploration",
  "priority": 1,
  "created": "2026-05-27T08:00:00Z",
  "skill_progress": {
    "abd-domain-language": { "execution_status": "done", "agent": "business-expert", "start": "...", "end": "...", "review_status": "done", "reviewer": "business-expert-reviewer", "review_start": "...", "review_end": "..." },
    "abd-acceptance-criteria": { "execution_status": "in_progress", "agent": "product-owner", "start": "...", "end": null, "review_status": null }
  },
  "entered_stage": "2026-05-28T10:00:00Z",
  "completed_stage": null,
  "stage_history": [
    { "stage": "discovery", "entered": "2026-05-27T08:00:00Z", "completed": "2026-05-28T10:00:00Z" }
  ],
  "archived": null,
  "scatter_from": "project-all",
  "scatter_to": [],
  "notes": null
}
```

**Skills are NOT declared on the ticket.** The kanban board (`kanban.json`) defines which skills apply for a given stage. The ticket only carries a `skill_progress` map — lazily populated when an agent starts work on a skill.

### Ticket lifecycle

1. **Backlog** — enters backlog at priority from story map
2. **Stage in progress** — at least one skill started by an agent
3. **Stage done** — all skills executed and reviewed; waits for pickup to next stage
4. **Scatter** (if next stage has finer scope) — ticket archives itself, children enter backlog
5. **Continue** (if next stage has same scope) — ticket advances to next stage, skill progress cleared
6. **Complete** — final stage done; ticket archived with full timing data

## Scattering

When a ticket completes a stage and the **next stage's scope** is finer than the current stage's scope, the ticket **scatters**:

- **Shaping (all) → Discovery (increment)** — project ticket scatters; children created from thin-slicing increments from story map
- **Exploration (increment) → Specification (sprint)** — increment ticket scatters; children created from stories grouped into sprints by kanban lead / strategy

### Scatter mechanics

1. Ticket is **archived** (moved to `archived` with start/end timestamps)
2. Child tickets are **created** at the finer scope level, entering the backlog for the next stage
3. Children carry **lineage** from the parent (e.g. `["Project", "Increment 1", "Sprint 1"]`)
4. Children are ordered by priority from the story map
5. **JIT rule**: only scatter the next N items unless user or strategy says otherwise

### When scope stays the same

Discovery (increment) → Exploration (increment): no scatter. The same ticket moves to the next stage; its skill progress is cleared and agents start skills from the kanban board's stage work required.

## Backlog

The backlog is **ordered** and **hierarchical**:

- Order comes from story map priority + thin-slicing
- Hierarchy comes from the story map structure (epics → sub-epics → stories)
- Only decomposed as far as needed (JIT)
- Kanban lead or user can pre-decompose ("divide increment 1 into 3 sprints")
- Items not yet scattered stay at their parent scope level until their turn

## Planning vs board sync

- **Kanban board** (stages, strategy, team) — written by kanban lead + `abd-kanban-planning` + `abd-kanban` → `kanban.json`
- **Board state** — written by `sync_kanban_board.py` + kanban lead scan → `board.json`
- **Scatter** — triggered by kanban lead via `scatter_ticket.py` → `board.json` (archive ticket, create children)
- **Metrics** — written by `track_metrics.py` → `metrics-log.jsonl`

## Multiple tickets in flight

Multiple active tickets across stages is normal:

```text
inc-1 ticket:  active  (engineering, sprint-1)
inc-2 ticket:  active  (exploration)
inc-3 ticket:  backlog (waiting for exploration)
```

## Metrics and tracking

Every ticket carries timing data:

- **Per skill**: start, end, review_start, review_end
- **Per stage**: entered_stage, completed_stage
- **Per ticket**: created, archived (when scattered or complete)
- **Lineage** enables rollup: total increment time, total project time, stage cycle times

The kanban lead uses `track_metrics.py` to compute:

- Cycle time per stage, per scope level
- Bottleneck detection (which stage/skill accumulates in-progress work)
- Throughput (tickets completed per unit time)

Manual sync:

```bash
python .cursor/skills/abd-kanban/scripts/sync_kanban_board.py --workspace <engagement-root>
```

Board UI (read-only live view): `practices/kanban/apps/abd-delivery-agent-kanban/` — `npm install && npm run dev` → http://localhost:3000/board

## Limits

- `kanban.json` is the **single source of truth** for which skills a stage requires — tickets never duplicate that list.
- Tickets carry only a `skill_progress` map (lazily populated when agents start work); no `skills` key.
- Scatter logic is deterministic from the kanban board scope transitions and story map structure.
