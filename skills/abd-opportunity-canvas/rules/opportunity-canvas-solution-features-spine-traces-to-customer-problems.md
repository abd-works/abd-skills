# Rule: Solution Features spine traces to Customer Problems with a UVP

**Scanner:** Manual review

The canvas passes the spine check when **Solution Features** states a Unique Value Proposition and its major features can each be traced to at least one named segment or problem in **Customer Problems** — and every named segment in Customer Problems is addressed by at least one feature. Failing means features appear with no stated problem, a named segment has no solution addressing their need, or Solution Features is a feature list with no UVP.

## DO

- Include a UVP in Solution Features and write each feature so it is clear which problem or segment from Customer Problems it addresses.

  **Example (pass):** `SOLUTION_FEATURES: UVP — a booking slot the dealer can rely on. Live bay calendar (addresses: coordinator need for real-time bay visibility — Customer Problems row 1); push notification on change (addresses: fleet manager need for booking confirmation — Customer Problems row 2).`

## DO NOT

- List features in Solution Features with no UVP and no link to a Customer Problems segment or requirement.

  **Example (fail):** `SOLUTION_FEATURES: Calendar view, notification system, reporting dashboard.` — no UVP, no problem linked, no segment referenced.

- Name a customer segment in Customer Problems and leave it without any coverage in Solution Features.

  **Example (fail):** `CUSTOMER_PROBLEMS: Fleet managers — need bulk booking confirmation` with no feature for fleet managers in Solution Features — the segment is named but the solution ignores them.

**Source:** Agile by Design Opportunity Canvas — Customer Problems and Solution Features spine.
