---
scanner: ~
---
# Rule: Large stories proactively trigger split suggestion

When estimating at story level and the consensus category crosses the session's split threshold, the facilitator (or agent) must proactively suggest decomposition before recording the estimate. The default thresholds are > 5 points (point-based schemes) or > 8 days (day-based schemes, where "days" means the full story lifecycle through acceptance testing, not just coding). The threshold is a conversation trigger, not an automatic split — the team can keep the story whole if they justify it. Passing means every story above the threshold has either been split or has a recorded justification for staying whole. Failing means large stories are silently accepted without the question being raised.

## DO

- Surface the split question whenever a story's consensus category crosses the session's declared split threshold.

  **Example (pass):** Story lands at XL in a session where the threshold is > L. Facilitator says: "This crossed our split threshold — can we break it into independently deliverable pieces?" Team discusses and splits into two thin slices via `abd-thin-slicing`.

- Record a justification when the team decides to keep a large story whole despite crossing the threshold.

  **Example (pass):** Estimate record notes: "Crossed split threshold (XL > L). Team decided to keep whole — the shelter API integration cannot be meaningfully separated into independent slices until the spike completes. Will re-estimate after spike."

- Define the split threshold as part of session setup and record it in the session file's category-scheme section.

  **Example (pass):** Session file says: "**Split threshold:** > L (any item estimated XL triggers a split discussion)."

## DO NOT

- Silently accept a story estimate above the split threshold without raising the decomposition question.

  **Example (fail):** Story lands at 8 points in a session with a > 5 threshold. The estimate is recorded as 8 with no mention of whether splitting was considered — a reader cannot tell if the team consciously accepted the size.

- Treat the threshold as an automatic split without team discussion.

  **Example (fail):** Story lands at XL, agent immediately splits it into three thin slices without asking the team — the threshold is a prompt for conversation, not a mandate.

**Source:** Engagement convention (delivery-estimation requirements — "if the estimation is too large and we are doing stories, proactively suggest to break it up"; guidelines: > 5 points, > 8 days covering story through acceptance test).
