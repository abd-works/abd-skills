---
name: abd-delivery-war-room
description: >-
  File-based war room for `delivery-lead` and `delivery-team-member`:
  `delivery-war-room/` under the engagement workspace is the **authoritative source of
  all delivery progress** — orchestration checklist, manifest, slots, and run log.
  Read this skill before Step 2.
---

# abd-delivery-war-room

## Purpose

Single on-disk home for **progress** and **handoffs**. The delivery lead, team members, and operator all read and write here.

## Progress authority

| What | Where | Who updates |
| --- | --- | --- |
| Orchestration + run/stage checkboxes | `delivery-plan-checklist.md` | Delivery lead (`generate_delivery_checklist.py --sync-only` after each gate) |
| Slot completion | `slot-NN-finished.md` | Team member |
| Active slot / run policy | `manifest.md`, `slot-NN-start.md` | Delivery lead |
| Audit trail (checklist sync source) | `run-log.jsonl` | Delivery lead |
| Blockers | `slot-NN-blocked.md`, `slot-NN-answer.md` | Team member / operator |

**Resume rule:** read the war room first. **`<!-- resume: slot NN next -->`** in the checklist (set by sync) + `slot-NN-finished.md` on disk. First unchecked **run/stage** block ≈ orchestration position.

**Per-stage checklist:** sync ticks the whole stage block when the lead appends `stage_exit_gate` to `run-log.jsonl` — not per-slot manual edits.

## Bootcamp alignment

| Stages | `shaping` → `discovery` → `exploration` → `specification` → `engineering` |
| Roles | `product-owner`, `business-expert`, `ux-designer`, `engineer`, `reviewer` |
| Family packages | `story-driven-delivery/`, `domain-driven-design/`, `user-experience-design/`, `architecture-centric-engineering/` |

Stage gates and skill order: [`../../content/stages/README.md`](../../content/stages/README.md).

## Workspace layout

```text
<workspace>/docs/planning/
  abd-delivery-lead/
    agile-delivery-plan.md          # narrative plan (strategy, runs, slots in tables)
    agile-delivery-plan.changelog.md
  delivery-war-room/                # ← authoritative progress
    delivery-plan-checklist.md      # generated; orchestration + run/stage checkboxes
    INSTRUCTIONS.md                 # team member autostart
    manifest.md
    profile.md
    run-log.jsonl
    slot-01-start.md
    slot-01-finished.md
    …
```

Regenerate + sync after plan confirm or revision; **sync-only** after every stage gate:

```bash
python skill-helpers/skills/track_task/scripts/generate_delivery_checklist.py --workspace <workspace>
python skill-helpers/skills/track_task/scripts/generate_delivery_checklist.py --sync-only --workspace <workspace>
```

## Delivery lead — start of a cycle

1. Create `<workspace>/docs/planning/delivery-war-room/`.
2. Copy **`templates/INSTRUCTIONS.md`** → `INSTRUCTIONS.md`.
3. Write `manifest.md`, `profile.md`.
4. Regenerate **`delivery-plan-checklist.md`** into the war room (from `agile-delivery-plan.md`).
5. Initialize `run-log.jsonl`.
6. Write **only** `slot-01-start.md` first.

## Team member — autostart

If `INSTRUCTIONS.md` exists:

1. Read `INSTRUCTIONS.md` → read `workspace` from the active `slot-NN-start.md`.
2. Read `manifest.md`, pick active `NN` (smallest slot with start present, finished absent).
3. Read `slot-NN-start.md`, then continue per `delivery-team-member/AGENT.md` Step 1.

## Team member — when finished

Write `slot-NN-finished.md` with: timestamp, artifact paths, scanner results, stage-complete status.

- **Executor slots** — use `templates/slot-finished.md`.
- **Reviewer slots** — use `templates/slot-finished-reviewer.md` (findings only; no new artifacts).

## Reviewer slot

When `team-role: reviewer` in the slot start file:

1. Read the **prior executor** `slot-NN-finished.md` and every artifact path listed.
2. Run scanners via `execute-skill-using-skills-rules` — record pass/fail per skill (**reviewer scanned**). Use `--language` when the skill requires it.
3. Validate exit-gate items from `stages/<stage>.md` — record pass/fail and findings (**reviewer reviewed**).
4. Write reviewer `slot-MM-finished.md`. Do not produce new stage artifacts.

### Scanner infrastructure failure — chain stop

If scanners **crash**, **fail to import**, or report **false clean** (see `delivery-lead/AGENT.md` **Scanner infrastructure gate**):

- Reviewer finished file: **Overall gate FAIL**, blockers = scanner infrastructure.
- Delivery lead **must not** open the next slot until infra is fixed and scanners re-run successfully.
- Fixes target skill packages (`scanners/`, imports, `__main__`), workspace tooling (root configs, `package.json`, test scripts), or env deps (`tree-sitter` for MERN) — **not** deferral to a later increment.

**Scanner obviously not relevant (narrow exception):** After scanners execute, a rule may be skipped only when obviously inapplicable to this slot — document **Scanner exception** in the reviewer finished file (see `delivery-lead/AGENT.md`). Infra failures are never eligible.

If findings require **artifact** fixes (scanners executed, rules failed, no valid exception), stop. The delivery lead logs corrections, authors a **rework** executor slot; after rework PASS, append to `run-log.jsonl` and run **checklist sync**.

## Delivery lead — chaining slots

After validating slot NN: append `slot_complete` (and `stage_exit_gate` when the stage closes) to **`run-log.jsonl`**, run **`generate_delivery_checklist.py --sync-only`**, then create `slot-(NN+1)-start.md`.

## Templates

Copy from `templates/` into the engagement war room: `INSTRUCTIONS.md`, `manifest.md`, `profile.md`, `slot-start.md`, `slot-finished.md`, `slot-finished-reviewer.md`, `slot-blocked.md`, `slot-answer.md`.

## Limits

- Cursor cannot spawn chats for you; someone still opens **New chat** for each agent.
- Exit gates remain in `stages/*.md`; war room records state, it does not replace stage definitions.
