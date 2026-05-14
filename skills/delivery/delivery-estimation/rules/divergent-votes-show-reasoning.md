---
scanner: ~
---
# Rule: Divergent votes show reasoning not just final category

When team votes on an estimate diverge (not unanimous on the first round), the estimate record must capture **what the disagreement was about** — whose votes differed, what each outlier said, and how the team resolved it. The estimate record exists so future readers (and re-estimation sessions) can understand **why** a number landed where it did. Passing means a reader can reconstruct the conversation from the record. Failing means the record shows a final category with no trace of the disagreement that preceded it.

## DO

- Name the voters and their categories in each round, and quote or paraphrase what the outliers said during the divergence discussion.

  **Example (pass):**

  - **Round 1:** Sarah: L, Marcus: XL, Priya: M, Tomás: L
  - **Divergence discussion:** Marcus (XL): "We have no API contract yet — could be a week just figuring out the integration." Priya (M): "The form and frontend are straightforward; only the API call is unknown."
  - **Round 2:** Sarah: L, Marcus: L, Priya: L, Tomás: L
  - **Final consensus:** L

- Record "No divergence" explicitly when the vote was unanimous — do not leave the field blank.

  **Example (pass):** "**Round 1:** All four voted S. **Divergence discussion:** No divergence. **Final consensus:** S"

## DO NOT

- Record only the final category without showing votes or discussion.

  **Example (fail):** "**Final consensus:** L" — no vote rounds, no names, no discussion. A future reader has no idea whether this was unanimous or contentious.

- Show that votes diverged but omit the reasoning.

  **Example (fail):** "**Round 1:** votes ranged from M to XL. **Round 2:** all voted L." — who said what and why is missing; the record does not explain the resolution.

**Source:** Engagement convention (delivery-estimation rough requirements — "team vote", "user can tweak, new data added to contributing factor").
