# Rule: Every SLO row has a named scope and one NFR category

Every row in the SLO matrix must name its **scope** (system, parent epic, epic, or story) and pick exactly one of the six **NFR categories** (Performance & Scalability, Availability & Reliability, Security & Compliance, Usability & Accessibility, Maintainability & Supportability, Interoperability & Compatibility). Scope is what makes the right level of investment go to the right operations: read-mostly catalogue browsing does not need order-placement durability, and the matrix should make that distinction visible. Failing means a row with no scope, a row scoped to "the system" when it really applies to one epic, a row that picks two categories, or a row that picks a category outside the six.

## DO

- Name the scope in the row's Scope column using one of: `system`, `parent epic: {name}`, `epic: {name}`, `story: {name}`.

  **Example (pass):** Scope cell reads `parent epic: Orders` — the row applies to every story under the Orders parent epic but does not impose itself on Catalogue or Reporting.

- When a parent-epic-level target genuinely overrides the system default, write the row at parent-epic scope and let the matrix make the override visible.

  **Example (pass):** System availability SLO = 99.9%. Orders parent-epic availability SLO = 99.95% (tighter). Both rows present; readers see Orders is intentionally tighter.

- Pick exactly one NFR category from the canonical six. If a target genuinely spans two categories, split it into two rows.

  **Example (pass):** "Time-to-revoke a leaked token" is **Security & Compliance**. The fact that fast revocation is also a *performance* concern does not change the category — the SLI is a security indicator.

## DO NOT

- Omit the scope column or leave it blank.

  **Example (fail):** A row with SLI "Catalogue cache hit rate" but no Scope cell — readers cannot tell whether this applies to the whole system or just one epic.

- Scope every row to "system" because "everything matters to everyone".

  **Example (fail):** Order durability, catalogue cache hit rate, and reporting job throughput all scoped to `system`. The matrix becomes a list of generic numbers and loses the criticality signal.

- Pick a category outside the canonical six ("Performance and Security", "Other", "Cross-cutting").

  **Example (fail):** Category column reads "Performance & Security" — pick one. The architecture mechanism that *implements* the target may span both, but the SLI itself measures one.

- Scope a row to a story when its parent epic's SLO already covers it.

  **Example (fail):** Twenty stories each get their own story-scoped latency row that is identical to the parent epic's row. The matrix bloats; readers cannot find the genuinely story-specific targets. Story-scoped rows exist only when the target differs materially from the parent epic.

**Source:** Practice-skill authoring convention (abd-service-level-objectives); scope and category are how the matrix stays browsable and actionable.
