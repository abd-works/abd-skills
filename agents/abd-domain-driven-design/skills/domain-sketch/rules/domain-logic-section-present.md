# Rule: Domain logic section present with testable bullets

**Scanner:** Manual review

After domain-sketch enrichment, the module file must contain a `## Domain logic` section with at least one prose bullet. Each bullet is a testable observation about business behavior, rules, interactions, or constraints — grounded in the source. Passing means the section exists with real bullets. Failing means the section is missing or contains only headings with no content.

## DO

- Include a `## Domain logic` section with short prose bullets describing business behavior.

  **Example (pass):**
  ```
  ## Domain logic

  - A shipment may leave the warehouse only after payment has cleared.
  - Delivery is confirmed when the carrier posts a terminal scan or the customer signs.
  ```

- Write each bullet as a testable observation a non-technical person can validate against the source.

  **Example (pass):** "A check result must equal or exceed the DC to succeed." — concrete, testable.

## DO NOT

- Omit the `## Domain logic` section entirely.

  **Example (fail):** File jumps from Key Abstractions content directly to `### Concept` blocks with no domain logic section.

- Include domain logic bullets that are implementation design rather than business behavior.

  **Example (fail):** "Use a strategy pattern for check resolution." — implementation, not domain behavior.

**Source:** Engagement convention (domain-sketch skill).
