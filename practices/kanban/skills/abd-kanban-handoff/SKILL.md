---
name: abd-kanban-handoff
catalog_garden_tier: practice
catalog_garden_order: 55
catalogue_one_liner: >-
  Delivery handoff from board, artifacts, and chat — where shaping/discovery/increments stand and what to do next.
description: >-
  Compact the session into a kanban-aware handoff: infer completed stages, scopes, increments, and skills from
  board.json (when present), war-room files, docs/end-to-end and docs/increments artifacts, and conversation.
  Use when the user types /abd-kanban-handoff or wants the next agent to resume delivery without re-discovering progress.
argument-hint: "What will the next session focus on? (optional)"
---

# abd-kanban-handoff

## Purpose

Produce a **delivery resume document** so a fresh agent knows **where JIT kanban delivery left off** — which **stages** and **scopes** (all → increment → sprint → story) have advanced, which **increments** have material under `docs/increments/`, and what to run next — without re-reading the whole repo or chat.

Works **with or without** a live board UI: when `board.json` is missing or stale, infer progress from **artifact presence** and **chat** per [reference/inference.md](reference/inference.md).

Like generic **handoff**: suggested skills, redact secrets, optional user focus argument — but the body is structured for **abd-kanban** / war-room / pull-model continuity, and the file is saved **in the engagement workspace** (not OS temp).

---

## Output file

**Folder (create if missing):**

```text
<workspace>/docs/planning/handoffs/
```

**Filename:** `handoff-abd-kanban-<slug>-<YYYY-MM-DD>.md` — `<slug>` = short project name from ticket lineage or workspace folder name.

**Also write (overwrite each run):** `handoff-latest.md` in the same folder so the next agent can open a stable path without hunting by date.

---

## When to apply

- User types **`/abd-kanban-handoff`** or asks for a **kanban handoff** / **delivery handoff**
- End of a war-room session before switching agents or repos
- Before adding UI or board features — next agent needs current **stage × scope × increment** picture

**Do not** use for non-delivery work (generic chat handoff → use `handoff` skill).

---

## Process

### 1. Resolve engagement workspace

From **agilebydesign-skills repo root**:

```powershell
python foundational/skill-helpers/scripts/get_workspace.py
```

If unset, ask the user or use the project named in chat. All paths below are `<workspace>/…`.

### 2. Run delivery progress summary (machine evidence)

```powershell
python practices/kanban/skills/abd-kanban-handoff/scripts/summarize_delivery_progress.py --workspace <absolute-workspace>
```

Optional JSON for merging:

```powershell
python practices/kanban/skills/abd-kanban-handoff/scripts/summarize_delivery_progress.py --workspace <path> --format json
```

Read the script output first; then **reconcile** with conversation (chat wins on conflicts the user stated explicitly).

### 3. Read war room when present

Under `docs/planning/kanban/` or `docs/planning/delivery-war-room/`:

| File | Use |
| --- | --- |
| `board.json` | Active/backlog/done/archived tickets, `skill_progress`, `stage`, `scope_level`, scatter lineage |
| `kanban.json` | Stage order, scope per stage, `stage_work_required` |
| `metrics-log.jsonl` | Recent `skill_done`, scatter, agent events (tail ~50 lines) |
| `action-state.json` | Manual mode pending intents (if under planning root) |

### 4. Infer without board (artifact-only delivery)

Follow [reference/inference.md](reference/inference.md): scan `docs/end-to-end/<stage>/` and `docs/increments/<n>-<slug>/` for canonical files from [../../reference/artifact-layout.md](../../reference/artifact-layout.md).

**DO** treat increment folders as evidence that **shaping/discovery scatter happened** even if `board.json` was never committed.

**DO NOT** mark a stage “complete” from artifacts alone when chat says work was abandoned or reset.

### 5. Merge chat context

From the current conversation, capture:

- What the user asked for this session (e.g. manual mode UI, review visibility)
- Fixes or policy decisions (e.g. two-pass `complete`, no orphan release in manual scan)
- Explicit “done” / “skip” / “reset” statements about skills or stages
- **Next session focus** — from `/abd-kanban-handoff` argument or user message

### 6. Write handoff document

Save under the engagement workspace:

```text
<workspace>/docs/planning/handoffs/handoff-abd-kanban-<slug>-<YYYY-MM-DD>.md
<workspace>/docs/planning/handoffs/handoff-latest.md   # same content, stable name
```

Create `docs/planning/handoffs/` if it does not exist.

Use [templates/handoff-document.md](templates/handoff-document.md). **Reference** artifact paths; do not paste full deliverables.

Redact API keys, passwords, PII.

### 7. Tell the user

Reply with the **full path** to the handoff file and a **three-line resume**: current stage, active tickets/skills, recommended next pull.

---

## Suggested skills (always include section)

Tailor from inferred **next stage** and gaps:

| Situation | Skills |
| --- | --- |
| Board / war room setup | `abd-kanban`, `abd-kanban-planning` |
| Resume agent pull | `abd-kanban` + kanban-lead / role `AGENT.md` under `practices/kanban/agents/` |
| Missing shaping/discovery artifacts | Stage practice skills (`abd-story-mapping`, `abd-thin-slicing`, …) |
| Increment exploration+ | `abd-domain-language`, `abd-acceptance-criteria`, … per stage |
| UI / board app | `abd-interface-design`, `abd-acceptance-criteria` (app AC in engagement repo) |
| Commits | `commit-msg` |
| Checkbox session tracking | `track_task` |

---

## References

- [reference/inference.md](reference/inference.md) — evidence priority, stage/scope/increment rules
- [reference/war-room-paths.md](reference/war-room-paths.md) — path resolution
- [templates/handoff-document.md](templates/handoff-document.md) — output skeleton
- Kanban domain: `practices/kanban/reference/kanban-board.md`, `artifact-layout.md`
- Pull model: `practices/kanban/agents/reference/pull-model.md`, `executor-workflow.md`

---

## Validate

- [ ] Workspace resolved; script run or skip reason documented
- [ ] Handoff states **stage × scope** status and **per-increment** folder progress when increments exist
- [ ] **Where to start** is explicit (next stage, ticket id, or skill name)
- [ ] Chat-only decisions included; no secret leakage
- [ ] File saved under `<workspace>/docs/planning/handoffs/` (dated + `handoff-latest.md`); path given to user
