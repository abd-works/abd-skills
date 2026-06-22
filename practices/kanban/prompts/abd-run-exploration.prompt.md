---
description: >-
  Run all Exploration stage skills (executor + reviewer) for the active increment.
agent: agent
---

Read `common/stages/exploration.md` and `practices/kanban/reference/artifact-layout.md`.

**Before starting:** run `/keyquestions` to confirm which skills are in scope and which are HIL checkpoints.

For each skill in the stage's default order:
1. **Execute** - follow `practices/kanban/reference/agent-workflow/executor-workflow.md`.
2. **Review** - a separate agent of the same role follows `practices/kanban/reference/agent-workflow/reviewer-workflow.md`. Log all corrections with `/corrections-log` before re-executing.
3. **Pause** - if this skill is an HIL checkpoint (per `/keyquestions`), present the outcome and wait. Do not proceed until the user confirms.

Continue until all skills pass review and the exit gate is met.
If the user provided text after the command, treat it as the increment or slice focus.