---

name: abd-delivery-war-room

description: >-

  File-based Kanban war room for `delivery-lead` and eight persistent role agents:

  `delivery-war-room/` under the engagement workspace is the **authoritative source of

  all delivery progress** — board.json, checklist, manifest, slots, claims, and run log.

  Read this skill before Step 2.

---



# abd-delivery-war-room



## Purpose



Single on-disk home for **progress** and **handoffs**. Models delivery as a **Kanban board** ([`../../content/kanban.md`](../../content/kanban.md)). The delivery lead, **eight persistent role agents**, and operator all read and write here.

**Planning is not Kanban.** The narrative plan (`agile-delivery-plan.md`), run catalog, system of work, and slot starts are authored by **delivery-lead** using **`abd-delivery-planning`** and this skill. **`sync_kanban_board.py`** only writes **`board.json`** — it reads slot/run state and must not create planning artifacts.



## Kanban model



| Concept | Implementation |

| --- | --- |

| **Work ticket** | One **run** from `run-catalog.json` |

| **Backlog** | Not-started run tickets — **only** backlog column in the engagement |

| **Stage flow** | Per ticket, per stage: **`in_progress` → `review` → `done`** |

| **Between stages** | Ticket stays in **`done`** until next stage pulls to **`in_progress`** |

| **Blocked / stalled** | `slot-NN-blocked.md`; claim timeout → **`stalled`** |

| **No Ready** | No ready column; no per-stage backlog after pull |



Rule: [`rules/kanban-ticket-columns.md`](rules/kanban-ticket-columns.md)



## Role agents (eight)



| Executor | Reviewer |

| --- | --- |

| `product-owner` | `product-owner-reviewer` |

| `business-expert` | `business-expert-reviewer` |

| `ux-designer` | `ux-designer-reviewer` |

| `engineer` | `engineer-reviewer` |



Agents are **instantiated once** per engagement as **isolated subagents**. Bootstrap payload only — slot scope lives in `slot-NN-start.md`; ticket column in **`board.json`**.



## Progress authority



| What | Where | Who updates |

| --- | --- | --- |

| **Kanban board snapshot** | **`board.json`** | **`sync_kanban_board.py` only** (read-only for planning) |

| Narrative plan | `abd-delivery-lead/agile-delivery-plan.md` | **delivery-lead** + **`abd-delivery-planning`** |

| System of work + run catalog | `system-of-work.json`, `run-catalog.json`, `run-state.json` | **delivery-lead** (Step 2b) |

| Slot starts (per run) | `runs/run-NN/<stage>/slot-NN-start.md` | **delivery-lead** via **`generate_run_slots.py`** when a run opens |

| Orchestration + run/stage checkboxes | `delivery-plan-checklist.md` | **delivery-lead** (`generate_delivery_checklist.py --sync-only`) |

| Slot completion | `slot-NN-finished.md` | Role agent |

| Active claim | `slot-NN-claim.md` | Role agent (removed on finish) |

| Slot schedule / policy | `manifest.md`, `system-of-work.json`, `slot-NN-start.md` | Delivery lead |

| Audit trail | `run-log.jsonl` | Delivery lead |

| Blockers | `slot-NN-blocked.md`, `slot-NN-answer.md` | Role agent / operator |

| Stalls | `board.json` column + optional `slot-stalled.md` | Sync script / delivery lead |



**Resume rule:** read **`board.json`** first, then checklist `<!-- resume: slot NN -->`. Role agents pull from ticket column matching their role.



## Bootcamp alignment



| Stages | `shaping` → `discovery` → `exploration` → `specification` → `engineering` |

| Roles | `product-owner`, `business-expert`, `ux-designer`, `engineer` (+ matching `*-reviewer` agents) |

| Slot types | `executor` · `reviewer` (same `team-role` for both in a pair) |



Stage gates: [`../../content/stages/README.md`](../../content/stages/README.md).



## Workspace layout



```text

<workspace>/docs/planning/

  abd-delivery-lead/

    agile-delivery-plan.md

  delivery-war-room/

    board.json                 # Kanban snapshot — sync_kanban_board.py ONLY

    system-of-work.json        # stage order + skill order (delivery-lead, Step 2b)

    run-catalog.json           # planned runs — no slot rows (delivery-lead, Step 2b)

    run-state.json             # slots_generated, next_slot_id (updated at run open)

    delivery-plan-checklist.md

    INSTRUCTIONS.md

    manifest.md

    profile.md

    run-log.jsonl

    runs/

      run-01/

        discovery/

          slot-05-start.md

          slot-05-finished.md

      run-02/

        exploration/

          slot-19-start.md

        specification/

        engineering/

```



### Sync commands



```bash

python skill-helpers/skills/track_task/scripts/generate_delivery_checklist.py --sync-only --workspace <workspace>

python delivery/skills/abd-delivery-war-room/scripts/sync_kanban_board.py --workspace <workspace>

```



Run **both** after every stage exit gate and run complete.



## Delivery lead — start of a cycle (Step 2b)



After plan CHECKPOINT approval — **delivery-lead** writes planning artifacts; then syncs the board:

1. Create `<workspace>/docs/planning/delivery-war-room/` if missing.
2. Copy **`templates/INSTRUCTIONS.md`** → `INSTRUCTIONS.md`.
3. Write **`system-of-work.json`** and **`run-catalog.json`** from the approved plan (named systems of work; each run with scope, stages, `system_of_work` ref). Initialize **`run-state.json`**.
4. Write `manifest.md`, `profile.md` (policy, wip, cross-run rules — **not** a full pre-authored slot list for every future run).
5. Regenerate **`delivery-plan-checklist.md`**.
6. Initialize `run-log.jsonl`.
7. **Open the first run(s):** `python delivery/skills/abd-delivery-war-room/scripts/generate_run_slots.py --workspace <ws> --run N` — materialize slots **only for runs that start now**. Do **not** pre-generate all Runs 2–10 at plan approval.
8. Copy `wip_policy` from `manifest.md` into `board.json`.
9. Run **`sync_kanban_board.py`** → initial **`board.json`** (reflect only — does not create plan or slots).
10. Start the **agent scan loop** (Step 4 in delivery-lead AGENT.md).

When inventing a **new** custom system of work, **CHECKPOINT:** ask whether to save it under **`abd-delivery-planning/strategies/`**.



## Role agent — autostart



1. Read `INSTRUCTIONS.md`, **`board.json`**, your role `AGENT.md`.

2. **Claim** next slot per [`../../agents/_shared/work-queue.md`](../../agents/_shared/work-queue.md) — pull from ticket column.

3. Read `slot-NN-start.md` → executor or reviewer workflow.

4. On finish → `slot-NN-finished.md` → claim again until no eligible work.



## Role agent — when finished



- **Executor slots** — `templates/slot-finished.md`; moves ticket toward **review** on sync.

- **Reviewer slots** — `templates/slot-finished-reviewer.md`; moves ticket toward **done** or next **in_progress** on sync.



## Reviewer slots



When `slot_type: reviewer`: read prior executor output → scanners → exit-gate review → reviewer finished file. No new stage artifacts.



### Scanner infrastructure failure — chain stop



Same as `delivery-lead/AGENT.md` **Scanner infrastructure gate**. Ticket column **`blocked`** until fixed.



## Delivery lead — monitoring



After slots complete: append **`run-log.jsonl`**, run **checklist sync** + **`sync_kanban_board.py`**. Add rework slot starts when reviewers fail.



## Templates



Copy from `templates/`: `INSTRUCTIONS.md`, `manifest.md`, `profile.md`, `board.json`, `system-of-work.json`, `run-catalog.json`, `run-state.json`, `slot-start.md`, …

Scripts (delivery-lead invokes; Kanban sync does **not**):

```bash
python delivery/skills/abd-delivery-war-room/scripts/migrate_slot_layout.py --workspace <ws>
python delivery/skills/abd-delivery-war-room/scripts/generate_run_slots.py --workspace <ws> --run N
python delivery/skills/abd-delivery-war-room/scripts/sync_kanban_board.py --workspace <ws>
```



## Limits



- Exit gates remain in `stages/*.md`; war room records Kanban state, it does not replace stage definitions.

- **`board.json`** is generated by **`sync_kanban_board.py`** (delivery-lead) — Kanban **reads** it only.
- **`sync_kanban_board.py`** must not create `agile-delivery-plan.md`, `run-catalog.json`, `system-of-work.json`, or `slot-NN-start.md`.
- **Kanban UI** (`abd-delivery-agent-kanban`): read-only except **`wip-policy.json`** (agent pool +/−).


