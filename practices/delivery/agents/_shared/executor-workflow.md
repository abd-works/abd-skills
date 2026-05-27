# Executor workflow (shared)

**When:** your agent is an **executor** (`slot_type: executor`).

Announce each step (e.g. `[Executor Step 1 — Set up]`). Do not run scanner validation — that is the matching **reviewer** agent's job.

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

### Step 1 — Set up

Read your role playbook under `../../content/roles/`. Read **`skills:`** from `slot-NN-start.md` — that names the **one practice skill** for this slot (resolve to `<workspace>/.cursor/skills/<skill-name>`). **`team-role`** only filters which slots you claim; do not guess the skill from the playbook alone.

Announce: slot **NN**, team-role, workspace, **practice skill from slot start**, run scope.

### Step 2 — Sync with workspace

Scan for existing artifacts (`story-graph.json`, domain docs, prior stage outputs). Flag conflicts with task scope.

### Step 3 — Read practice skill (authoring)

Read the assigned practice skill's `SKILL.md` and bundled **rules** — templates, vocabulary, formatting, quality bar for **building**.

Announce skill name and that rules were loaded for **authoring**. Do not run scanners.

### Step 4 — Produce draft

Produce the deliverable to disk. Quick author sanity pass only — not formal rule/scanner review.

**CHECKPOINT.** Present draft summary and unknowns. Wait for confirm before Step 5.

### Step 5 — Update story graph

If this skill produces graph content, update `story-graph.json` via `story-graph-ops` after checkpoint confirm. Otherwise skip.

### Step 6 — Finish executor slot

Write `docs/planning/delivery-war-room/slot-NN-finished.md` using `slot-finished.md` template:

- Artifact paths produced
- `scanner_validation: deferred to reviewer slot`
- Stage skill unit complete from executor side

Remove `slot-NN-claim.md`. **Claim the next eligible slot** per [work-queue.md](work-queue.md). Ticket column updates on **`sync_kanban_board.py`** (executor finish → toward **review**).

**When blocked:** write `slot-NN-blocked.md` — ticket column **`blocked`**. **When stalled:** delivery lead handles; column **`stalled`** on sync.

Announce: **Executor slot NN complete** — ticket moves toward **review** on board sync.
