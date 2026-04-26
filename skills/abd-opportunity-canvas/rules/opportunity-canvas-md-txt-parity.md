# Rule: Markdown and plain-text canvases match for one engagement

**Scanner:** Manual review

When both **`templates/opportunity-canvas.md`** and **`templates/opportunity-canvas.txt`** are produced for the same workshop, they must describe one opportunity, not two. **Passing** means the **`OPPORTUNITY:`** title matches, the eight ABD row blocks match (from `CUSTOMER_PROBLEMS:` through `COST_DRIVERS:`), the same **`ALTERNATIVES:`** intent, and the same count of **`ASSUMPTION:`** lines with the same **validate by** meaning. **Failing** means divergent scope, an extra path only in one file, or missing rows or assumptions in one.

## DO

- Keep the filled **Template** section in **`.md`** and **`.txt`** aligned: same **`OPPORTUNITY:`** string, same eight ABD blocks, and the same **number** of **`ASSUMPTION:`** lines with the same validation intent.

  **Example (pass):** Both files start with `OPPORTUNITY: Fleet same-day scheduling` and list the same `SOLUTION_FEATURES:` and two `ASSUMPTION:` lines with matching validate-by outcomes.

## DO NOT

- Ship one file with content another omits when both purport to be the same engagement snapshot.

  **Example (fail):** **`opportunity-canvas.md`** adds a third `ASSUMPTION:` absent from **`opportunity-canvas.txt`**.

**Source:** Engagement (paired-artifact parity). One workshop should yield one shared picture of the opportunity.
