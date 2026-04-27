# Rule: Alternatives are documented as substantially different columns

**Scanner:** Manual review

When alternatives are present on the canvas, each one passes when it is structured as a distinct column that represents a meaningfully different path — a different customer focus, build approach, buy option, or do-nothing scenario — not a minor variation of the main case. Failing means an alternative column is only a tweak on the same solution (different technology, different timeline) rather than a genuinely different strategic option.

## DO

- Document each alternative as a column whose content in at least one key section differs substantially from the main case — different segment focus, different solution approach, different business model, or no build at all.

  **Example (pass):** Main case column: build a self-service scheduling platform for dealer coordinators. Alternative column: integrate with an existing third-party SaaS scheduling tool, different Key Activities (integration vs build), different Cost Drivers (licensing vs engineering), different Increments of Value (configuration milestones vs feature releases).

## DO NOT

- Add an alternative column that only changes a technology choice or delivery detail while keeping the same customer, problem, solution shape, and business case.

  **Example (fail):** Alternative column that swaps React for Angular in Solution Features while all other sections mirror the main case — this is an implementation variant, not a strategic alternative worth modelling.

**Source:** Agile by Design Opportunity Canvas — Alternatives as canvas columns.
