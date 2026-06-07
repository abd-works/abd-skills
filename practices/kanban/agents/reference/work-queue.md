# Work queue — agents

**Shared kanban concepts**: [../../reference/kanban-board.md](../../reference/kanban-board.md) · [../../reference/agents-and-skills.md](../../reference/agents-and-skills.md)

**Canonical pull rules:** [pull-model.md](pull-model.md) — all stages, all roles, continuous pull.

Delivery agents are **persistent by delivery role**. They **pull skill-level work** from **active** tickets on `board.json` — **every stage**, downstream first. The kanban lead pulls **tickets** (backlog → active); agents pull **skills**.

Each agent **executes and reviews** in a single session — **no separate reviewer agents**. See [executor-workflow.md](executor-workflow.md).

Agents are **not stage-locked**. They start work on eligible skills across all stages, prioritizing downstream work first.

## Bootstrap (once per engagement)

**Turn 1:** Read [session-bootstrap.md](session-bootstrap.md) before anything else.

Every agent session receives **only** this bootstrap payload from the kanban lead:

- **`workspace`** — engagement root (required)
- **`delivery-role`** — fixed by which agent you are

If `workspace` is missing, ask once and stop.

On first turn: resolve war room paths, write heartbeat (`status: working`), read board + kanban.json, then scan for eligible work.

On first turn: resolve war room paths, write heartbeat (`status: working`), read board + kanban.json, **arm continuous pull loop** per [pull-model.md](pull-model.md), then run pull scan immediately.

## Start next skill (pull from board)

**Read [pull-model.md](pull-model.md) eligibility algorithm.** Summary:

After finishing work — or on first turn — or on every pull-loop tick:

1. Read **`board.json`** (`active` tickets only) and **`kanban.json`**.

2. Load stage order from `kanban.json` → `definitions.<stage_configuration>.stages[]` (or `definitions` entry matching `board.json` / war room config). Scan stages **in reverse array order** (last stage = downstream = scan first).

3. For each stage, for each **active** ticket where `ticket.stage` matches that stage name, walk that stage's `stage_work_required` in order. Find the **next** skill where:
   - All prior skills have `execution_status: done` **AND** `review_status: done`.
   - That skill's `role` matches your `delivery-role`.
   - No claim yet, or `execution_status` is `not_started`.

4. **Pick one claim:** downstream stage wins; within a stage, lowest `priority` ticket wins.

5. If nothing qualifies on **active** tickets → [When idle — signal and poll](#when-idle--signal-and-poll). **Keep the pull loop running.**

**DO NOT** use a hardcoded stage list. **DO NOT** skip shaping, discovery, exploration, specification, or engineering — the same pull rules apply to every stage defined in `kanban.json`.

## When idle — signal and keep pulling

Agents pull **skills** on **active** tickets only. **Backlog → active** is kanban-lead's job. When no eligible skill is found, **do not exit** — signal `agent_ready` and **keep the pull loop running**.

### 1. Signal ready to kanban lead

After marking a skill done (or on bootstrap when no work is found):

1. Append to `docs/planning/delivery-war-room/metrics-log.jsonl`:

   ```json
   {"event":"agent_ready","timestamp":"<ISO 8601>","agent_role":"<your-role>","reason":"no_eligible_skill_on_active_tickets"}
   ```

2. Update heartbeat via `board_skill.py ready` (preferred) or write `heartbeat-<role>[-N].json` with `status: ready`.

   ```bash
   python practices/kanban/skills/abd-kanban/scripts/board_skill.py ready \
     --workspace <workspace> --role <your-role> [--instance N]
   ```

3. Announce in chat: **`<role> ready — no eligible skill on active tickets; polling board (downstream first).`**

**Do not** move tickets between `backlog` and `active` yourself.

### 2. Keep pulling (loop must stay armed)

**Turn 1:** Arm `AGENT_LOOP_TICK_<role>` per [pull-model.md](pull-model.md) and [session-bootstrap.md](session-bootstrap.md). **Do not** arm the loop only after going idle — arm it before the first pull scan.

On each tick:

1. Re-read `board.json` and `kanban.json`.
2. Run [Start next skill](#start-next-skill-pull-from-board) (all stages, downstream first).
3. **Work found** → claim, execute, review, mark done → **pull again** (same wake or next tick).
4. **Still nothing** → refresh heartbeat `ts`; end turn; loop fires again in 30s.

After **10** consecutive idle ticks, report: **`No pending work for <role> after polling — kanban lead should pull backlog tickets to active.`** Keep loop armed unless operator says stop.

### 3. What you poll vs what the lead does

| You (team member) | Kanban lead |
| --- | --- |
| Poll **active** tickets for next **skill** | Pull **backlog → active** when roles are ready |
| Append `agent_ready` to metrics log | Reads `agent_ready`, respects WIP, pulls tickets |
| Update your heartbeat | Spawns or nudges agents |

## Starting work (avoid double work)

Before starting work on a skill, update `board.json`:

- Set `execution_status: in_progress`
- Set `agent: <your-role>`
- Set `start: <ISO 8601>`

## Completing work

When the execute + review pass finishes (see [executor-workflow.md](executor-workflow.md) Step 7):

- Set `execution_status: done`, `end: <ISO 8601>`
- Set `review_status: done`, `reviewer: <your-role>`, `review_start: <ISO 8601>`, `review_end: <ISO 8601>`

Both execution and review are marked done in one update. The next skill's agent can start immediately.

Then pull next eligible skill.

## Architecture skills

`abd-architecture-specification` and `abd-architecture-specification` are **always eligible** when prior skills are done — same as any stage skill. Kanban never auto-skips them; the **skill run** decides quick vs long pass.

**On every claim:**

1. Read mechanisms in scope from the ticket's **architecture blueprint** (and AC / UL as needed).
2. Check existing reference sections and `docs/planning/delivery-war-room/mechanism-registry.json`.
3. **Quick pass** — every mechanism already documented → emit the **mapping document only** (template assignment table or `architecture-reference-assignment.md`), mark skill done.
4. **Long pass** — one or more mechanisms missing → create only gaps; update the registry for new **create** rows; emit the mapping document.

| Skill | Mapping artifact | Registry update |
| --- | --- | --- |
| `abd-architecture-specification` | Mechanism assignments table (assign \| create per mechanism) | After each **create** row |
| `abd-architecture-specification` | `docs/increments/<ticket>/…/architecture-reference-assignment.md` | After each new reference section |

Full workflow: each skill's `reference/concepts.md`.

## Rework

When the review pass (Step 6) reveals a **substantive** issue the agent cannot fix mechanically:

- Log in `docs/corrections-log.md`
- Flag to kanban lead — the lead decides whether to re-run the skill or adjust scope
- The skill's `execution_status` resets to `not_started`

**Simple issues** are fixed in place during the review pass — no rework cycle.

## Autostart

If `INSTRUCTIONS.md` exists in the war room:

1. Read [session-bootstrap.md](session-bootstrap.md) and complete delivery-role first turn.
2. Start next eligible skill per algorithm above (downstream first).
3. Execute + review per [executor-workflow.md](executor-workflow.md).
4. On finish → signal ready if idle → arm poll loop per [When idle — signal and poll](#when-idle--signal-and-poll) until work found or poll limit reached.

## Blocked

If an agent cannot proceed:

- Add a note to the ticket describing the blocker
- Report to kanban lead (will appear in scan cycle)
- Stop starting new work until unblocked
