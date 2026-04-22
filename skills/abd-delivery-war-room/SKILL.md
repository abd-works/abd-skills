---
name: abd-delivery-war-room
description: >-
  Experimental **file-based war room** for handoffs between `abd-delivery-lead` and
  `abd-team-member`: `delivery-war-room/` under the engagement workspace with
  `INSTRUCTIONS.md`, `manifest.md`, and `slot-NN-start.md` / `slot-NN-finished.md`.
  **Not wired into the delivery-lead or team-member agents** until re-integrated from
  first principles. Use this skill only when you explicitly opt in to the war-room
  pattern and copy the templates below into the engagement.
---

# abd-delivery-war-room

> **Status:** Parked here for redesign. The canonical **orchestration** agents do **not** reference this skill yet.

## Purpose

Reduce repeated paste handoffs between orchestrator and team-member threads by keeping **state on disk** under the engagement root.

## Workspace layout (recommended folder name)

Use **`delivery-war-room/`** (new engagements). Older experiments may still use `delivery-chamber/`; the mechanics are the same.

```text
<workspace>/delivery-war-room/
  INSTRUCTIONS.md       # team member reads first — copy from § INSTRUCTIONS template below
  manifest.md           # ordered slots for the cycle
  slot-01-start.md
  slot-01-finished.md
  slot-02-start.md
  slot-02-finished.md
  …
```

Two-digit slot numbers (`01`, `02`, …).

## Resuming

If the war-room folder, `agile-delivery-plan.md`, and `abd-delivery-lead/progress/delivery-plan-checklist.md` exist, a delivery-lead session can **read disk** and continue from the first unchecked checklist line. Infer slot completion from `slot-NN-finished.md`—do not ask “is it done?” when the files already say so.

## Delivery lead — start of a cycle

1. Create `<workspace>/delivery-war-room/`.
2. Copy the **INSTRUCTIONS template** (below) to `INSTRUCTIONS.md`.
3. Write `manifest.md` (goal, ordered slots, file naming).
4. Write **only** `slot-01-start.md` first (full handoff: `team-role`, `workspace`, scope, `story-graph-ops`, corrections pointer). Do not add `slot-02-start.md` until `slot-01-finished.md` exists (unless you override).

## Team member — autostart

If `delivery-war-room/INSTRUCTIONS.md` exists at the workspace root:

1. Read `INSTRUCTIONS.md` → resolve absolute `workspace` (parent of `delivery-war-room/`).
2. Read `manifest.md`, pick active `NN` (smallest slot with `slot-NN-start.md` present and `slot-NN-finished.md` absent).
3. Read `slot-NN-start.md` for role and scope, then continue per `abd-team-member/AGENT.md` from Step 1 (classic bootstrap).

If no slot qualifies, stop until the lead adds a start file.

## Team member — when finished

Write `slot-NN-finished.md` with: timestamp (optional), artifacts touched, stage complete line, and optional **`## For delivery lead`** / **`## For operator`** (thread routing: ping lead thread, then open next team-member chat when disk is ready).

## Delivery lead — chaining slots

After validating slot NN, read `slot-NN-finished.md`, then create `slot-(NN+1)-start.md` when the plan continues.

## Paste blocks (optional)

Replace `<ABSOLUTE_WORKSPACE>` with the engagement root (folder that contains `delivery-war-room/`).

**A) First `abd-delivery-lead` chat**

```text
workspace: <ABSOLUTE_WORKSPACE>
Use the war room on disk (delivery-war-room/). Follow agents/abd-delivery-lead/AGENT.md from Step 1.

context: <optional>
```

**B) First `abd-team-member` chat** (after `INSTRUCTIONS.md`, `manifest.md`, `slot-01-start.md` exist)

```text
Engagement workspace (Cursor root):
<ABSOLUTE_WORKSPACE>

Follow agents/abd-team-member/AGENT.md.

If ./delivery-war-room/INSTRUCTIONS.md exists, read it first (workspace + active slot + slot-NN-start.md), then Step 1 onward.
```

## Limits

- Cursor cannot spawn chats for you; someone still opens **New chat** for each agent.
- This skill does **not** change exit gates in `stages/*.md`; align any “who accepts” policy in your own engagement notes until agents adopt this again.

---

## INSTRUCTIONS template (`delivery-war-room/INSTRUCTIONS.md`)

Copy verbatim into each engagement (edit nothing unless you extend the protocol):

```markdown
# Delivery war room — team member autostart

## 1) Engagement root (`workspace`)

The engagement root is the directory that **contains** this `delivery-war-room` folder. Resolve to an **absolute** path. Use it as `workspace` for all paths, scanners, and `story-graph-ops`.

## 2) Cycle context

Read `delivery-war-room/manifest.md`.

## 3) Active slot (`NN`)

Find the smallest two-digit `NN` such that `slot-NN-start.md` exists and is non-empty, and `slot-NN-finished.md` does not exist. That is the active slot. If none, report no pending work.

## 4) Handoff

Read `delivery-war-room/slot-NN-start.md` for `team-role`, scope, stage, skills, corrections.

Then run `agents/abd-team-member/AGENT.md` from Step 1 with the resolved `workspace` and `team-role`.

## 5) When done

Write `delivery-war-room/slot-NN-finished.md` with artifact paths and stage complete (or blocked).
```

---

## Historical note

Earlier iterations lived under `agents/abd-delivery-lead/delivery-chamber-protocol.md` and `delivery-chamber/` in engagements. That coupling has been **removed** from the agents pending a clean redesign.
