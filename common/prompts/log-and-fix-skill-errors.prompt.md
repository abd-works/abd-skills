---
description: Fix wrong output — log the correction on disk and iterate until right
agent: agent
---

Something I produced is wrong. Follow the correction process:

1. **Fix the deliverable first** — do not touch sources, rules, or prompts yet.
2. **Log on disk in the same turn** — find or create `skill-errors-log.md` inside the skill being corrected. Append: DO / DO NOT (forward-looking) + Example (wrong). Leave Example (correct) blank.
3. **Re-generate and iterate** until actually satisfied.
4. Only improve the source if the user explicitly asks.
