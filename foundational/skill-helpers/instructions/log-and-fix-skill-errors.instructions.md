---
applyTo: "**"
---
# Correction process (always-on)

**Triggers:** output is wrong **or** user corrects how you work (process, norms, behavior).

## Where the corrections log lives — on disk, not chat

- Use the log **inside the skill or target being corrected** (`<target-skill>/skill-errors-log.md`). Append to an existing one, or create it there from `instructions/templates/skill-errors-log.md`.
- Write the entry **in the same turn** as you fix or acknowledge the problem. Chat is not the record.
- Process corrections count — if the user corrects how you work, log those too.

## Fix the output first

Do **not** touch sources, rules, or prompts until the deliverable is confirmed right.

1. **Identify** — note the problem; open the on-disk log.
2. **Log (initial)** — append an entry: **DO / DO NOT** (altered future behavior) + **Example (wrong)**. Leave **Example (correct)** blank.
3. **Re-generate** — apply the correction; expect multiple turns.
4. **Review** — refine and re-log; repeat until actually satisfied.
5. **Confirm** — fill **Example (correct)**, set Status to `confirmed`.

## Log entry fields

| Field | Content |
| --- | --- |
| **Context** | What produced the output — omit if obvious |
| **DO / DO NOT** | Forward-looking. Mistake belongs in Example (wrong) only. |
| **Example (wrong)** | What the output actually did |
| **Example (correct)** | Fill only after confirmed |
| **Likely source** | `prompt gap` · `instruction not read` · `edge case` · `automation gap` · `unclear expectation` |

Duplicate violation → add another **Example (wrong)** to the same entry.

## Improve the source — only when the user asks

Read the full log, find root causes, **propose** fixes — do not implement without explicit go-ahead.
