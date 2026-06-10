---
scanner: ~
---
# Rule: Emergent scope captured during estimation

Estimation forces concrete thinking, and concrete thinking changes the backlog — new acceptance criteria, new stories, splits, merges, and open questions surface when the team actually talks through an item. The estimate record must capture every backlog change so it feeds back into the right downstream skill and gets persisted. If changes only live in someone's memory or a chat thread, they are lost. Passing means any change discovered during estimation of an item is recorded in that item's estimate record with the downstream skill tagged. Failing means the record has a final category but no trace of what the team discovered or changed along the way.

## DO

- Record each backlog change in the estimate record's emergent-scope section, tagged with the downstream skill that actions it.

  **Example (pass):**

  - **New AC** → `abd-story-acceptance-criteria`: Adoption application must validate pet availability before submission
  - **New story** → `abd-story-mapping`: Handle shelter API timeout gracefully
  - **Split** → `abd-thin-slicing`: Split into (1) submit with mock shelter API, happy path; (2) real shelter API with error handling
  - **Open question:** Does the shelter API support idempotent submission?

  Each item is actionable, tagged, and traceable.

- Record splits with what the item was split into and which skill handles the split based on scope type (epic splits use `abd-story-mapping`; story splits use `abd-thin-slicing`).

  **Example (pass):** "**Split** → `abd-thin-slicing`: Story too uncertain — split into two thin slices: (1) happy-path submission, (2) error handling and retry."

- Record merges when the team combines items that are too small or redundant.

  **Example (pass):** "**Merge** → `abd-story-mapping`: Combined 'View Pet Photo' and 'View Pet Details' into single story 'View Pet Details' — photo display is not a separate user action."

- Mark the emergent-scope section as empty ("None") when estimation did not surface anything new — do not omit the section.

  **Example (pass):** "**Emergent scope:** None — estimation confirmed existing scope is sufficient."

## DO NOT

- Omit the emergent-scope section entirely from an estimate record.

  **Example (fail):** Estimate record has Item, Estimate, Factor breakdown, Team vote, Discussion notes — but no emergent-scope section. A reader cannot tell whether nothing was discovered or whether discoveries were lost.

- Capture backlog changes only in discussion notes as unstructured prose, without tagging the downstream skill.

  **Example (fail):** Discussion notes mention "Priya said we should split this" and "Marcus found a new AC about validation" but the emergent-scope section is empty or missing — the changes are buried in narrative without skill tags, and will likely not get actioned.

- Record a split or merge without naming what the item becomes.

  **Example (fail):** "**Split** → `abd-thin-slicing`: Item was too big, split it." — into what? A reader cannot act on this.

**Source:** Engagement convention (delivery-estimation rough requirements — "capture any comments as part of discussion using acceptance criteria, new story", "split items, merge").
