---
description: Fix wrong output — log the correction on disk and iterate until right
agent: agent
---

We fixed something a skill priduced. Log the error and the fix so we can correct the skill later

1. **Fix the deliverable first** — do not touch sources, rules, or prompts yet.
2. **Log on disk in the same turn:**
   - **If a CDD session is active** (a `cdd-session-journal.md` exists in `docs/cdd-sessions/<date>-<topic>/`): append to the `## Corrections` section of that journal. Format per the `abd-context-driven-delivery` skill: DO / DO NOT + Example (wrong) + Example (correct).
   - **Otherwise:** find or create `skill-errors-log.md` inside the skill being corrected. Append: DO / DO NOT (forward-looking) + Example (wrong). Leave Example (correct) blank.
3. **Re-generate and iterate** until actually satisfied.
4. Only improve the source skill if the user explicitly asks — promote session-local corrections to changes only on request.
