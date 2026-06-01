# Handoff — abd-kanban delivery resume

**Generated:** <ISO date>  
**Workspace:** `<absolute-path>`  
**Saved to:** `<workspace>/docs/planning/handoffs/handoff-abd-kanban-<slug>-<YYYY-MM-DD>.md` (and `handoff-latest.md`)  
**Next session focus:** <from user argument or "not specified">

---

## Executive resume (3 lines)

1. **Pipeline position:** <e.g. shaping complete; discovery not started / increment 1 in exploration>
2. **Live work:** <ticket id, skill, role, or "none — board idle">
3. **Start here:** <one concrete next action>

---

## Delivery pipeline status

| Stage | Scope | Board / artifact confidence | Status |
| --- | --- | --- | --- |
| context | all | | not started / in progress / done |
| shaping | all | | |
| discovery | increment | | |
| exploration | increment | | |
| specification | sprint | | |
| engineering | sprint | | |

**Scatter:** <e.g. project-all archived → inc-1, inc-2 in backlog / or "not yet scattered">

---

## Board snapshot (if `board.json` exists)

**Configuration:** `<stage_configuration>` · **Mode:** `<board_mode>`

### Active tickets

| ticket_id | stage | scope | skills in progress | skills done |
| --- | --- | --- | --- | --- |
| | | | | |

### Backlog / done / archived counts

- Backlog: <n> · Done column: <n> · Archived: <n>

---

## Increments (artifact view)

| Increment folder | Lineage label | Deepest evidence | Notes |
| --- | --- | --- | --- |
| `docs/increments/1-<slug>/` | | exploration / specification / engineering / empty | |

**Thin-slicing source:** `<path to thin-slicing.md or "missing">`

---

## Session context (from chat)

<Decisions, fixes, and user corrections not visible on disk — bullet list>

---

## War room paths

| Item | Path |
| --- | --- |
| War room | `<path>` |
| Board | `<path>/board.json` |
| Kanban config | `<path>/kanban.json` |

---

## Open / risks

- <blocked items, manual intents pending, stale board vs artifacts>

---

## Suggested skills

| Skill | When |
| --- | --- |
| | |

---

## Commands cheat sheet

```powershell
python foundational/skill-helpers/scripts/get_workspace.py
python practices/kanban/skills/abd-kanban-handoff/scripts/summarize_delivery_progress.py --workspace "<workspace>"
python practices/kanban/skills/abd-kanban/scripts/board_skill.py pull --workspace "<workspace>" --role <role>
```
