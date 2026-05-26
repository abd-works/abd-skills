# Delivery war room — role agent autostart

Eight **persistent role agents** pull work from the **Kanban board** (`board.json`). Open the agent matching your role — not one chat per slot.

Kanban model: `delivery/content/kanban.md`

| You are | Agent |
| --- | --- |
| Product Owner executor | `delivery/agents/product-owner/AGENT.md` |
| Product Owner reviewer | `delivery/agents/product-owner-reviewer/AGENT.md` |
| Business Expert executor | `delivery/agents/business-expert/AGENT.md` |
| Business Expert reviewer | `delivery/agents/business-expert-reviewer/AGENT.md` |
| UX Designer executor | `delivery/agents/ux-designer/AGENT.md` |
| UX Designer reviewer | `delivery/agents/ux-designer-reviewer/AGENT.md` |
| Engineer executor | `delivery/agents/engineer/AGENT.md` |
| Engineer reviewer | `delivery/agents/engineer-reviewer/AGENT.md` |

Shared queue rules: `delivery/agents/_shared/work-queue.md`

## 1) Workspace

Bootstrap must include **`workspace`** — the engagement root.

## 2) Kanban board

Read `docs/planning/delivery-war-room/board.json` and `manifest.md`.

Each **run** = one **ticket** in **one column**: `backlog` · `in_progress` · `review` · `done` · `blocked` · `stalled`.

Stage flow on a ticket: **in_progress → review → done** (no Ready).

## 3) Claim next slot

1. Read **`board.json`** — find tickets in your column (`in_progress` for executors, `review` for reviewers).
2. Resolve `active_slot` or smallest eligible `slot-NN-start.md` for your `team-role` and `slot_type`.
3. Verify `depends_on` satisfied and no conflicting claim.
4. Write `slot-NN-claim.md` before starting.

Cross-run: separate tickets can be active (e.g. Run 5 engineering + Run 6 exploration). See `_shared/work-queue.md`.

## 4) Handoff

Read `slot-NN-start.md`. Executors → `_shared/executor-workflow.md`. Reviewers → prior executor artifacts only.

## 5) Mid-slot checkpoint

Waived when `manifest.md` `checkpoint_policy: on_block_only`.

## 6) Story graph update

After confirmation, update via `story-graph-ops` when the skill produces graph content.

## 7) When done

Write `slot-NN-finished.md`. Remove claim. Claim next eligible slot. Delivery lead re-syncs **`board.json`**.

## 8) When blocked or stalled

**Blocked:** write `slot-NN-blocked.md` — ticket column `blocked`. Clear via `slot-NN-answer.md`.

**Stalled:** claim open past `stall_timeout_minutes` — delivery lead nudges; ticket column `stalled` on sync.
