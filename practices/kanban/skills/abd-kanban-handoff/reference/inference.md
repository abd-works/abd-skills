# Delivery progress inference

Evidence priority when building an **abd-kanban-handoff** (highest wins on conflict unless user overrode in chat):

1. **User statements in the current chat** (reset board, deleted deliverables, “story mapping is fine”, etc.)
2. **`board.json`** — `skill_progress` with both `execution_status` and `review_status` done = skill complete for that ticket
3. **`kanban.json`** — required skills per stage (ground truth for “what’s left” on a ticket at a stage)
4. **`summarize_delivery_progress.py` output** — merged board + artifact scan
5. **Artifact presence** under `docs/end-to-end/` and `docs/increments/` — infers work happened **even without kanban**
6. **`metrics-log.jsonl` tail** — corroboration only

---

## Stage × scope model (abd-kanban)

Canonical stage order (typical new build):

| Stage | Scope level | Scatter trigger to next |
| --- | --- | --- |
| context | all | (optional) |
| shaping | all | → discovery when stage complete |
| discovery | increment | thin-slicing defines increment folders |
| exploration | increment | → specification when increment exploration done |
| specification | sprint | scatter from increment ticket |
| engineering | sprint | complete → archive |

**Ticket `scope_level`:** `all` | `increment` | `sprint` | `story` — must match the stage’s configured scope.

**Stage complete (on board):** every **required** skill in `kanban.json` for that stage has `execution_status: done` **and** `review_status: done` on the ticket.

**Stage complete (no board):** infer from canonical artifacts listed below; mark confidence **high / medium / low** in the handoff.

---

## Board.json signals

For each ticket in `active`, `backlog`, `done`, `archived`:

- **`stage`** + **`scope_level`** — where the ticket sits in the pipeline
- **`skill_progress`** — per-skill execution/review; `in_progress` = live work
- **`stage_history`** — completed prior stages with timestamps
- **`scatter_from` / `scatter_to`** — parent archived, children created
- **`lineage`** — project → increment → sprint → story labels

**Manual mode:** `board_mode: manual` — intents in `action-state.json`; do not assume automatic pull.

---

## Artifact signals (no kanban or stale board)

### Whole-solution — `docs/end-to-end/`

| Stage folder | Strong “started” signals | Strong “shaping/discovery pass done” signals |
| --- | --- | --- |
| `shaping/` | any `.md` / `story-graph.json` | `module-partition.md`, `impact-map.md`, `architecture-outline.md`, story map outline |
| `discovery/stories/` | `story-map.md` | `thin-slicing.md`, full `story-graph.json` |
| `discovery/domain/` | `domain-terms.md` | file populated, not stub |
| `discovery/ux/` | `information-architecture.md` | — |
| `discovery/architecture/` | `architecture-blueprint.md` | `service-level-objectives.md` |
| `exploration/` | any subfolder content | roll-up from increments (often sparse until increments finish) |
| `specification/` | `crc.md` | `specification-by-example.md`, `architecture-reference.md` |
| `engineering/` | `object-model.md` | `src/` activity in workspace |

### Per-increment — `docs/increments/<n>-<slug>/`

Folder existence ⇒ **increment identified in thin-slicing** (discovery scatter likely).

| Subfolder | Stage work |
| --- | --- |
| `exploration/domain/`, `stories/`, `ux/`, `architecture/` | exploration skills for that increment |
| `specification/` | CRC, spec-by-example, interface-design, arch-reference |
| `engineering/` | object-model, ATDD, clean-code / `src/` |

Handoff table: one row per increment folder with **highest stage folder that has non-empty canonical files**.

---

## Increments “without kanban”

When the team delivered **without** war-room files:

1. List `docs/increments/*/` directories (pattern `<n>-<slug>`).
2. For each, note deepest stage with evidence (exploration > specification > engineering).
3. Compare to `docs/end-to-end/discovery/stories/thin-slicing.md` — increments named there but missing folders = **not started**.
4. State **recommended next**: usually lowest-numbered or highest-priority increment with incomplete exploration per thin-slicing order.

---

## Where to start (handoff must answer)

Pick **one** primary resume point:

| Situation | Start here |
| --- | --- |
| Board active ticket with `in_progress` skill | Resume that ticket + skill; same role agent |
| Board ticket, all skills done, same scope next stage | Advance ticket stage or run kanban lead scatter |
| Shaping artifacts done, no increment folders | Run discovery on `project-all` or scatter from thin-slicing |
| Increment folders, exploration partial | Next increment or next exploration skill per `kanban.json` |
| User next-session focus (argument) | Align resume point to that focus; note delivery debt separately |

Include **two-pass complete** reminder: `board_skill.py complete` twice per skill (work done → review done) when using executor workflow.
