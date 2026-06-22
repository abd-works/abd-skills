---
name: abd-kanban-handoff
catalog_garden_tier: practice
catalog_garden_order: 55
catalogue_one_liner: >-
  Delivery handoff from board, artifacts, and chat ? where shaping/discovery/increments stand and what to do next.
description: >-
  Produce a delivery handoff capturing completed stages, scope progress, and next recommended pull. Use when passing kanban delivery context to a fresh agent session.
argument-hint: "What will the next session focus on? (optional)"
---

# abd-kanban-handoff

## Purpose

Let a fresh agent resume delivery without re-reading the repo ? by capturing where things stand and what to pull next.

---

## Output

```text
<workspace>/docs/kanban/handoffs/handoff-abd-kanban-<slug>-<YYYY-MM-DD>.md
<workspace>/docs/kanban/handoffs/handoff-latest.md   ? same content, stable path
```

`<slug>` = short project name from ticket lineage or workspace folder name. Create the folder if missing.

---

## Process

### 1. Resolve kanban board

kanban board: `<workspace>/docs/kanban/`

Read when present:

| File | What to use it for |
| --- | --- |
| `board.json` | Active/backlog/done/archived tickets, `skill_progress`, `stage`, `scope_level`, scatter lineage |
| `kanban.json` | Stage order, scope per stage, `stage_work_required` (ground truth for "what's left") |
| `metrics-log.jsonl` | Tail ~50 lines for recent skill_done / scatter / agent events |
| `action-state.json` | Manual mode pending intents (if present under planning root) |

### 2. Infer progress

Evidence priority (highest wins on conflict unless user overrode in chat):

1. **User statements in the current chat** ? explicit reset, skip, "done", policy decisions
2. **`board.json`** ? skill with both `execution_status: done` and `review_status: done` = complete
3. **`kanban.json`** ? required skills per stage
4. **Artifact presence** under `docs/end-to-end/` and `docs/increments/` ? infers work happened even without kanban

Stage ? scope (typical new build):

| Stage | Scope |
| --- | --- |
| context | all (optional) |
| shaping | all |
| discovery | increment |
| exploration | increment |
| specification | sprint |
| engineering | sprint |

**Stage complete on board:** every required skill in `kanban.json` has `execution_status: done` AND `review_status: done`.

**Stage complete without board:** infer from artifact presence; mark confidence high / medium / low.

**Increment folders** (`docs/increments/<n>-<slug>/`) = discovery scatter likely happened. One row per increment in the handoff table showing deepest stage with evidence.

### 3. Merge chat context

Capture from the current conversation:

- What the user asked for this session
- Fixes or policy decisions made
- Explicit "done" / "skip" / "reset" statements about skills or stages
- Next session focus (from argument or user message)

### 4. Write handoff document

Use [`templates/handoff-document.md`](templates/handoff-document.md). Reference artifact paths; do not paste full deliverables. Redact API keys, passwords, PII.

Save to both dated and `handoff-latest.md` paths.

### 5. Tell the user

Reply with the **full path** to the handoff file and a **three-line resume**: current stage, active tickets/skills, recommended next pull.

---

## Where to start (handoff must answer)

| Situation | Start here |
| --- | --- |
| Board active ticket with `in_progress` skill | Resume that ticket + skill; same role agent |
| Board ticket, all skills done, same scope next stage | Advance ticket stage |
| Shaping artifacts done, no increment folders | Run discovery or scatter from thin-slicing |
| Increment folders, exploration partial | Next increment or next exploration skill per `kanban.json` |
| User next-session focus (argument) | Align resume point to that focus; note delivery debt separately |

---

## Suggested skills

| Situation | Skills |
| --- | --- |
| Board / kanban board setup | `abd-kanban`, `abd-kanban-planning` |
| Resume agent pull | kanban-lead / role `AGENT.md` under `practices/kanban/agents/` |
| Missing shaping/discovery artifacts | Stage practice skills (`abd-story-mapping`, `abd-thin-slicing`, ?) |
| Increment exploration+ | `abd-domain-language`, `abd-story-acceptance-criteria`, ? per stage |
| Commits | `commit-msg` |

---

## Validate

- [ ] kanban board path resolved; board.json read or skip reason documented
- [ ] Handoff states stage ? scope status and per-increment folder progress
- [ ] **Where to start** is explicit (next stage, ticket id, or skill name)
- [ ] Chat-only decisions included; no secret leakage
- [ ] File saved under `<workspace>/docs/kanban/handoffs/` (dated + `handoff-latest.md`); path given to user
