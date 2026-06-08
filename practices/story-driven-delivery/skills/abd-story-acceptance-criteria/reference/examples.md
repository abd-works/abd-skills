# Acceptance Criteria — Example

## Story: Export Report To PDF

**Story type:** user

**Domain terms** (vocabulary for this story's AC — things, state, actions, rules):

- *Report UI* — screen where the user runs the report and starts export
- *Export a PDF* — user-triggered action for this flow
- *Export Job Progress* — visible status while the export runs
- *Filtered Report Data* — row set after filters; input to the PDF
- *Report Export* — the delivered artifact / job outcome the user waits on
- *Download* — completed file handoff to the user
- *Zero Rows* / *Filters* — empty result after filtering; edge case
- *Feedback* / *Nothing To Export* — user-visible outcome when there is nothing to build
- *Report Export Service* — downstream dependency; failure mode
- *Retry* — user-visible recovery path
- *Partial* / *Empty File* — invalid success shapes to reject

1. **WHEN** the user chooses to *Export a PDF* on the *Report UI*
   **THEN** the *Report UI* indicates *Export Job Progress*
   **AND** the system builds a *PDF* from the current *Filtered Report Data*
   **AND** the user gets a normal completed *Download* for that *Report Export*

2. **WHEN** the *Report* has *Zero Rows* after *Filters*
   **THEN** the user sees clear *Feedback* that there is *Nothing To Export*
   **BUT** no *PDF* is created and no *Download* starts

3. **WHEN** the *Report Export Service* is unavailable
   **THEN** the user sees that *Report Export* failed and can *Retry* later
   **BUT** no *Partial* or *Empty File* is treated as a successful *Report Export*
