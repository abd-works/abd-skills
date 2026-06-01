---
description: >-
  Kanban-aware session handoff: infer delivery progress from board, artifacts, and chat;
  write resume doc under docs/planning/handoffs/ in the engagement workspace.
mode: agent
---

Run the **`abd-kanban-handoff`** skill (`practices/kanban/skills/abd-kanban-handoff/SKILL.md`).

1. Resolve engagement workspace (`python foundational/skill-helpers/scripts/get_workspace.py` or user path).
2. Run `practices/kanban/skills/abd-kanban-handoff/scripts/summarize_delivery_progress.py` on that workspace.
3. Reconcile with **this conversation** (chat overrides stale disk).
4. Write the handoff to `<workspace>/docs/planning/handoffs/` (dated file + `handoff-latest.md`) using `templates/handoff-document.md`.
5. Reply with the file path and a three-line **where to start** summary.

If the user provided text after the command, use it as **next session focus**.

Do not duplicate full deliverables — reference paths only. Redact secrets.
