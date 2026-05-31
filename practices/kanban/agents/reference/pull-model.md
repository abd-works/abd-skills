# Pull model — all stages, all roles

**Every delivery agent pulls. Nothing is assigned by ticket or stage. The kanban board is the queue.**

| Who | Pulls what | Does NOT |
| --- | --- | --- |
| **business-expert** | Next eligible BE skill on any **active** ticket, any **stage** | Pull backlog tickets; wait for spawn |
| **product-owner** | Next eligible PO skill — same rules | Same |
| **ux-designer** | Next eligible UX skill — same rules | Same |
| **engineer** | Next eligible engineer skill — same rules | Same |
| **kanban-lead** | Backlog → active; stage advance; scatter; spawn/re-spawn pull agents | Execute practice skills |

**One executor session per role** executes **and** reviews each skill. **Do not spawn `*-reviewer` agents.**

---

## Stages (all use the same pull algorithm)

Stage names and skills come from **`kanban.json`** for the engagement — not from memory.

Typical PawPlace / new-build order (downstream = last in list):

| Scan priority | Stage | Scope | Example skills (role) |
| --- | --- | --- | --- |
| 5 (first) | `engineering` | sprint | interface-design (UX), object-model (EN), ATDD (EN), clean-code (EN) |
| 4 | `specification` | sprint | CRC (BE), spec-by-example (PO), interface-design (UX), arch-reference (EN) |
| 3 | `exploration` | increment | UL (BE), AC (PO), ux-mockup (UX), arch-template (EN, conditional) |
| 2 | `discovery` | all/increment | domain-terms (BE), story-mapping (PO), IA (UX), blueprint (EN) |
| 1 (last) | `shaping` | all | module-partition (BE), story-mapping (PO), impact-mapping (UX), arch-outline (EN) |

Optional **`context`** stage (convert/chunk/embed) appears in some configs — include it when present in `kanban.json`, scanned after shaping (lowest downstream priority).

**Rule:** Read `kanban.json` → `definitions.<config>.stages[]` → scan stages in **reverse array order** (last stage first).

---

## Eligibility (one algorithm — every stage)

For your `delivery-role`, on each pull scan:

1. Read `board.json` (`active` only) and `kanban.json`.
2. Build stage list from config; iterate **from last stage to first**.
3. For each stage name, consider every active ticket where `ticket.stage === stage name`.
4. For that ticket, walk `stage_work_required` **in order**. Find the **first** skill where:
   - All **prior** skills have `execution_status: done` **and** `review_status: done` (or skipped per conditional rules).
   - This skill's `role` matches your delivery role.
   - This skill is not started, or is `not_started` / no `skill_progress` entry.
   - **Conditional skills** (`abd-architecture-template`, `abd-architecture-reference`): eligible only after **conditional gate** (below) — not merely because priors are done.
5. Pick the winning skill: **lowest stage scan order that found a match** (downstream wins), then **lowest ticket `priority`**.
6. **Conditional gate first** (template / arch-reference only): run assign/create inventory per [work-queue.md](work-queue.md#conditional-skills) **before** `in_progress`. If skip applies → mark `done` + notes; pull again. If run applies → set `in_progress`, then author.
7. **Other skills:** claim with `in_progress` on `board.json` before any authoring.

### Conditional gate — not automatic

| Skill | Run only when | Skip (mark done, no authoring) when |
| --- | --- | --- |
| `abd-architecture-template` | Increment scope needs **new** mechanism sections not in `docs/increments/<n>-<slug>/exploration/` | Every in-scope mechanism already documented — assign existing sections only |
| `abd-architecture-reference` | Sprint needs **new** reference sections or **missing** code files per inventory | Every mechanism has reference **assign** and code **assign** — update `docs/increments/<n>-<slug>/specification/architecture-reference-assignment.md` only |

**DO NOT** treat arch-reference as the default next specification skill. Discovery/exploration companions often **assign** reference; spec stage then assigns code paths or skips entirely.

**Kanban-lead:** Count engineer eligibility when priors are done and the conditional skill is unset — executors run the gate on pull. **DO NOT** put `abd-architecture-reference` or a ticket id in spawn prompts.

**Same algorithm** for shaping through engineering. No stage-specific exceptions.

---

## Continuous pull (delivery roles — mandatory)

**Turn 1 — before any skill:**

1. [session-bootstrap.md](session-bootstrap.md) — paths, heartbeat.
2. Arm **`AGENT_LOOP_TICK_<role>`** pull loop (30s, `notify_on_output`).
3. Run pull scan **immediately** (do not wait for first tick).

**Every wake (tick or after skill complete):**

1. Pull scan (algorithm above).
2. **Work found** → execute + review per [executor-workflow.md](executor-workflow.md) → write board → **pull again** (same turn if possible, else next tick).
3. **No work** → append `agent_ready` once per idle period → heartbeat `status: ready` → **keep pull loop running** → end turn; next tick re-scans.

**DO NOT** exit after one skill. **DO NOT** exit after one empty scan. **DO NOT** move backlog → active.

---

## Kanban lead — every scan cycle

After [session-bootstrap.md](session-bootstrap.md) loop is armed, each Step 3 cycle:

### A — Flow tickets

- Stage complete → advance or scatter.
- `agent_ready` in last 20 lines of `metrics-log.jsonl` → pull next backlog ticket to **active** for that role.

### B — Ensure pull agents exist (all roles)

For **each** role in `kanban.json` `team` (business-expert, product-owner, ux-designer, engineer):

1. Run eligibility algorithm **for that role** across all active tickets (same as pull-model).
2. Count `eligible_skills` and `in_progress` claims for that role.
3. If `eligible_skills > 0` and live agents `< team[role]`:
   - Spawn executor subagent (`run_in_background: true`) with bootstrap + **continuous pull** instructions.
4. If heartbeat stale (>2 min) and `eligible_skills > 0` → re-spawn.
5. If `agent_ready` and backlog has tickets that would give that role work → pull to active **before** expecting poll to succeed.

**DO NOT** spawn `*-reviewer` agents. **DO NOT** assign a skill to an agent in spawn prompt — agents **pull** themselves.

### C — End turn

Update `heartbeat-kanban-lead.json`. Wait for next `AGENT_LOOP_TICK_kanban_lead`.

---

## What “Done column” means (not a pull queue)

Tickets in a stage **Done** column are either:

- **Archived parent** (exploration complete, scattered) — children in active/backlog hold the work.
- **Active ticket** waiting on **another role's** skill — your role pulls only when **your** skill is next in order.

Done ≠ “pick me up” for every role. **Pull scan** decides.

---

## Failure modes (DO NOT)

| Symptom | Cause | Fix |
| --- | --- | --- |
| Agent idle, work on board | Exited after one skill / no pull loop | Arm pull loop; re-spawn with pull-model |
| Wrong stage scanned | Hardcoded stage list | Read stages from `kanban.json` reverse order |
| PO spawned while UL in review | Missing review gate on prior skill | Prior skill needs execution + review done |
| Lead ran once | No notify_on_output on lead loop | session-bootstrap |
| Reviewer agents spawned | Legacy pattern | One executor; execute + review in one pass |
| Arch-ref runs on every sprint | Priors done treated as eligible; spawn named skill | Conditional gate on pull; skip when assign-only; lead spawn without skill name |
