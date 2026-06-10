# Kanban Board



---

## Core concepts

- **kanban board** — blueprint of ordered stages, each with a scope level and stage work required, governing ticket flow live with tickets flowing through stages
- **ticket** — a unit of work at the scope level its current stage requires, carrying lineage, priority, and skill progress entries created as work starts
- **board position** — backlog, the stage a ticket currently occupies (queue, in progress, or done within that stage), or complete
- **scatter** — when scope changes between stages, child tickets are created at the finer scope and the parent follows them on the board; no scatter when scope stays the same
- **lineage** — every ticket carries its ancestry: project > increment > sprint > story

## Kanban board
The kanban board defines an ordered sequence of stages, the scope level each stage operates at, and the practice skills each stage requires. `kanban.json` is the authority — tickets carry only a `skill_progress` map, never a skill list. When scope changes between stages, the ticket **scatters**: children are created at the finer scope and the parent follows them on the board. When scope stays the same, the ticket advances. Multiple tickets can be active across stages simultaneously.
The *kanban board* defines an ordered set of *stages* — each with a *scope level* and *stage work required* — and runs live with *tickets* flowing through *stages*.

- **ticket** — scope unit at the level its current stage requires (all, increment, sprint, story)
- **backlog** — ordered; only decomposed JIT; hierarchy from story map + thin-slicing
- **stage in progress** — tickets at a stage where skill work is underway
- **stage done** — all skills in stage complete; ticket awaits pickup to the next stage
- **team** — executor/reviewer pair counts per delivery role configured on the board; one integer per role

## Kanban board stage configuration

The *kanban board* is the single source of truth for which *skills* each *stage* requires. This configuration defines:

1. **Stages** — ordered sequence (shaping → discovery → exploration → specification → engineering)
2. **Scope per stage** — what granularity tickets live at (all, increment, sprint, story)
3. **Stage work required per stage** — ordered list of practice skills to execute, with delivery role assignment

When scope changes between stages (e.g. shaping at "all" → discovery at "increment"), completing one stage **scatters** the ticket into children at the finer scope.

### Kanban board shape

```json
{
  "schema": "abd-kanban-board/v1",
  "definitions": {
    "default-new-build": {
      "label": "Default new build",
      "strategy": {
        "scatter_rules": {
          "all_to_increment": "one ticket per increment from thin-slicing; scatter all",
          "increment_to_sprint": "group 3-4 stories per sprint; scatter next 1-2 increments JIT"
        },
        "checkpoint_policy": "per_skill",
        "autonomy": "moderate"
      },
      "team": { "product-owner": 1, "business-expert": 1, "ux-designer": 1, "engineer": 1 },
      "stages": [
        {
          "name": "exploration",
          "scope": "increment",
          "stage_work_required": [
            { "skill": "abd-domain-language", "role": "business-expert" },
            { "skill": "abd-story-acceptance-criteria", "role": "product-owner" },
            { "skill": "abd-ux-mockup", "role": "ux-designer" },
            { "skill": "abd-architecture-specification", "role": "engineer", "run_when": "increment_needs_undocumented_mechanisms" }
          ]
        }
      ]
    }
  }
}
```

### Default new build

Practice skills per stage — from `reference/stages/`. Background (`drawio-*`), optional (`abd-thin-slicing`), and support (context/RAG) skills are omitted from the board catalog; add them per engagement when needed.

- **Shaping** (scope: all) — `abd-domain-glossary`, `abd-story-mapping` (outline), `abd-impact-mapping`, `abd-architecture-outline`
- **Discovery** (scope: all) — `abd-story-mapping` (full), `abd-domain-language`, `abd-information-architecture`, `abd-architecture-blueprint`
- **Exploration** (scope: increment) — `abd-domain-model`, `abd-story-acceptance-criteria`, `abd-ux-mockup`, `abd-architecture-specification` document mode (conditional — when increment needs undocumented mechanisms)
- **Specification** (scope: sprint) — `abd-domain-specification`, `abd-story-specification`, `abd-ux-specification` (spec pass), `abd-architecture-specification` template mode
- **Engineering** (scope: sprint) — `abd-ux-specification` (implementation pass), `abd-domain-code`, `abd-story-acceptance-test`, `abd-clean-code`, `abd-architecture-code` (conditional — when a named architecture spec is assigned)

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
    "abd-story-acceptance-criteria": { "execution_status": "in_progress", "agent": "product-owner", "start": "...", "end": null, "review_status": null }
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

### Ticket lifecycle

1. **Backlog** — enters backlog at priority from story map
2. **Stage in progress** — at least one skill started by an agent
3. **Stage done** — all skills executed and reviewed; waits for pickup to next stage
4. **Scatter** (if scope changes) — children created at finer scope; parent follows them on the board
5. **Continue** (if next stage has same scope) — ticket advances to next stage, skill progress cleared
6. **Complete** — final stage done; ticket archived with full timing data

## Scattering

When a ticket completes a stage and the **next stage's scope** is finer than the current stage's scope, the ticket **scatters**:

- **Discovery (all) → Exploration (increment)** — project ticket scatters; children created from thin-slicing increments in story map
- **Exploration (increment) → Specification (sprint)** — increment ticket scatters; children created from stories grouped into sprints by kanban lead / strategy

### Scatter mechanics

1. Child tickets are **created** at the finer scope level, entering the backlog for the next stage
2. Children carry **lineage** from the parent (e.g. `["Project", "Increment 1", "Sprint 1"]`)
3. Children are ordered by priority from the story map
4. The parent **follows its children** on the board — it remains visible alongside them
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
- **Board state** — managed by the kanban app → `board.json`
- **Scatter** — triggered by kanban lead; app creates children and parent follows them on the board
- **Metrics** — computed by the kanban app → `metrics-log.jsonl`

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

The kanban app computes:

- Cycle time per stage, per scope level
- Bottleneck detection (which stage/skill accumulates in-progress work)
- Throughput (tickets completed per unit time)

Board UI (read-only live view): `practices/kanban/apps/abd-delivery-agent-kanban/` — `npm install && npm run dev` → http://localhost:3000/board

## Limits

- `kanban.json` is the **single source of truth** for which skills a stage requires — tickets never duplicate that list.
- Tickets carry only a `skill_progress` map (lazily populated when agents start work); no `skills` key.
- Scatter logic is deterministic from the kanban board scope transitions and story map structure.
