---
description: Fix the skill source based on what went wrong — do NOT touch the output
---

Something went wrong and the skill itself needs fixing. Run the source-fix process now.

**Do NOT re-generate output. Do NOT iterate on the deliverable. Fix the skill.**

1. **Read the corrections log** — open `<target-skill>/skill-errors-log.md`. Read all entries as a set, not just the latest.
2. **If no log exists** — infer the problem from the conversation: what did the skill produce, what was wrong, what should it have done instead.
3. **Find the root cause** in the skill source:
   - `rules/*.md` — missing or wrong rule
   - `SKILL.md` — bad instruction, missing step, wrong guidance
   - `ide-files/*.mdc` / `*.instructions.md` / `*.prompt.md` — stale or incorrect IDE surface
   - `templates/` — wrong template shape
   - `scripts/` — broken or missing script logic
   - `scanners/` — scanner not catching the violation, or firing incorrectly
4. **Fix it** — propose the changes. If the user confirms or says to go ahead, make the edits immediately.
5. **Log what you changed** — append to `<target-skill>/skill-errors-log.md`: what the root cause was, what you changed, and mark the entry `confirmed`.

**Do not produce new output. Do not run the skill again. The fix is the deliverable.**
