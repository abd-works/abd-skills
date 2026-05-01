---
scanner: front-matter-thin
---

# Rule: Front matter is thin

The front matter (everything before the first `## Module:` or `### Key Abstraction:` heading) must contain only source pointer(s) and counts (modules, key abstractions). No per-module descriptions, no per-abstraction summaries, no intent statements, and no term lists belong in the front matter. Passing means the front matter is a few metadata lines. Failing means it contains teaching content that belongs under abstraction headings.

## DO

- Keep front matter to: H1 title, `Source:` line(s), and counts (`Modules: N`, `Key Abstractions: K`).

  **Example (pass):**
  ```
  # Key Abstractions — Payments Domain

  Source: module-partitioning.md at abd-ooad/module-partitioning.md
  Modules: 3     Key Abstractions: 8

  ---
  ```

- Place all abstraction-specific information (intent, terms, extracts) under the appropriate `### Key Abstraction:` heading.

  **Example (pass):** Front matter is 5 lines; first module starts at line 7.

## DON'T

- Put per-abstraction summaries, intent statements, or term listings in the front matter.

  **Example (fail):**
  ```
  # Key Abstractions — Payments Domain

  Source: ...
  Modules: 3     Key Abstractions: 8

  Key abstractions identified:
  - Funds Transfer: moves money between accounts
  - Wire Transfer: variant with caps
  - Settlement: end-of-day reconciliation
  ```
  (The summary list belongs under module/abstraction headings, not here.)

- Include module-level scope notes or descriptions above the first `## Module:` heading.

  **Example (fail):** Two paragraphs explaining the domain before the first module heading — that belongs in the module's optional one-liner or in an external document.
