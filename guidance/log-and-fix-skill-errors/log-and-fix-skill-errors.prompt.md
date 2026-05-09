---
description: Fix wrong output and log the correction on disk
---

Something I produced is wrong. Run the correction process now.

1. **Log first** — open or create `skill-errors-log.md` **inside the skill being corrected** (`<target-skill>/skill-errors-log.md`). Append an entry: DO/DO NOT (altered future behavior) + Example (wrong). Leave Example (correct) blank. Entry goes on disk this turn — not in chat.
2. **Fix** — re-generate the deliverable with the correction applied.
3. **Iterate** — repeat until the output is actually right, then fill Example (correct) and mark confirmed.
4. **Source** — only propose source fixes (rules, prompts, skills) if the user explicitly asks.

Log template: `guidance/log-and-fix-skill-errors/templates/skill-errors-log.md`
