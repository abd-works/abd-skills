# Executor workflow (shared)

**When:** your agent is an **executor** (`slot_type: executor`).

Announce each step. Do not run scanner validation — that is the matching **reviewer** agent's job.

## Skills

| Skill | Use |
| --- | --- |
| `skill-helpers/` | workspace paths |
| Practice skill `SKILL.md` + `rules/` | read to **author** |
| `story-graph-ops` | update graph after draft confirmed |
| `execute-skill-using-skills-rules` / scanners | **no** — deferred to reviewer |
| `track_task` | optional |

**Executors produce; reviewers validate.**

Stage definitions: [../../content/stages/README.md](../../content/stages/README.md)

## Checkpoint protocol

When a step says **CHECKPOINT**:

1. **Present** state and flag unknowns.
2. **Stop** and wait.
3. **On response:** confirm → proceed · correct → log in `docs/corrections-log.md` per `execute-skill-using-skills-rules` **before** fixing · question → answer, re-present.

---

### Step 1 — Claim skill from board

Read `board.json` and `system-of-work.json`. Find next eligible skill per [work-queue.md](work-queue.md):

- Match your `team-role`
- Skill `status: to_do`
- Prior skills in stage order are done
- Downstream stage priority

Claim: set `status: in_progress`, `agent: <your-role>`, `start: <now>`.

Announce: ticket ID, lineage, stage, skill name, scope level.

### Step 2 — Sync with workspace

Scan for existing artifacts (`story-graph.json`, domain docs, prior stage outputs). Flag conflicts with ticket scope.

### Step 3 — Read practice skill (authoring)

Read the assigned practice skill's `SKILL.md` and bundled **rules** — templates, vocabulary, formatting, quality bar for **building**.

The skill name comes from the ticket's `skills` key you claimed.

Announce skill name and that rules were loaded for authoring. Do not run scanners.

### Step 4 — Produce draft

Produce the deliverable to disk. Quick author sanity pass only — not formal rule/scanner review.

**CHECKPOINT.** Present draft summary and unknowns. Wait for confirm before Step 5.

### Step 5 — Update story graph

If this skill produces graph content, update `story-graph.json` via `story-graph-ops` after checkpoint confirm. Otherwise skip.

### Step 6 — Mark done and pull next

Update `board.json`:

- Set skill `status: done`, `end: <now>`
- The matching reviewer agent will pick up review work

Announce: skill complete on ticket.

**Pull next eligible skill** per [work-queue.md](work-queue.md). If nothing available, report idle.

**When blocked:** set skill `status: blocked` — kanban lead handles in scan cycle.
