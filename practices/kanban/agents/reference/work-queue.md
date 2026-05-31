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
   - All prior skills have `execution_status: done` **AND** `review_status: done` (or conditional skip).
   - That skill's `role` matches your `delivery-role`.
   - No claim yet, or `execution_status` is `not_started`.

   **Conditional skills** — assess skip vs run before claiming ([Conditional skills](#conditional-skills)).

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

2. Update `docs/planning/delivery-war-room/heartbeat-<your-role>.json`:

   ```json
   {"agent_role":"<your-role>","ts":"<ISO 8601>","status":"ready"}
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

## Conditional skills

Some stage skills are **listed on every ticket** but run **only when scope needs them**. Do not leave them `not_started` indefinitely — assess at claim time, then either execute or skip.

| Skill | Stage | Run when | Skip when |
| --- | --- | --- | --- |
| `abd-architecture-template` | exploration | Increment needs **new** mechanism sections not in `docs/increments/<n>-<slug>/exploration/architecture/architecture-template.md` | All mechanisms documented — assign existing; skip |
| `abd-architecture-reference` | specification | Sprint needs **new** reference or **missing** code per inventory | Reference + code exist — update `docs/increments/<n>-<slug>/specification/architecture-reference-assignment.md` only; skip |

**Skip protocol:**

1. List mechanisms from AC, UL, `docs/end-to-end/discovery/architecture/architecture-blueprint.md`.
2. Discover existing sections in `docs/increments/<n>-<slug>/exploration/{domain,stories,ux,architecture}/` or `docs/end-to-end/exploration/` subfolders as appropriate.
3. If **all** mechanisms are satisfied by assign → skip execution.
4. Update `skill_progress` for that skill:
   - `execution_status: done`, `review_status: done`
   - `agent` / `reviewer`: your role
   - `notes`: `"skipped — mechanisms already documented for scope"` (or list assign paths)
5. Proceed to the next skill in stage order.

If **any** mechanism needs create → run `abd-architecture-template` normally (create only missing sections).

For **`abd-architecture-reference`**, before starting: list mechanisms from CRC/spec; check reference sections and File Structure paths on disk. If reference **assign** and code **assign** for all → skip with assignment table path in notes. If reference exists but code missing → run and create **code only**. If reference missing → run template first or create reference section, then code.

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
