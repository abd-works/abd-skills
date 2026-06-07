---
scanner: ~
---
# Rule: Coverage boundary stated before estimates begin

The estimation session file must declare which **bootcamp delivery stages** the estimate covers before any items are estimated. Without a coverage boundary, estimates from different sessions or teams are not comparable. Stage definitions: [`../../../reference/stages/README.md`](../../../reference/stages/README.md).

**Default (included unless opted out):** exploration (AC), specification, engineering (ATDD + implementation), regression testing.

**Not default (opt in):** shaping, discovery, exploration extras (UX mockup, arch template), engineering `abd-interface-design` implementation pass, user testing / UAT.

Passing means the session file has an explicit coverage boundary checklist in the scope section. Failing means estimates exist but the reader cannot tell which stages are included.

## DO

- State the coverage boundary as a checklist of bootcamp stages, marking each as included or excluded, in the session scope section.

  **Example (pass):**

  - [ ] **Shaping** *(not needed — outline map exists)*
  - [ ] **Discovery** *(map and slices complete)*
  - [x] **Exploration** — acceptance criteria
  - [ ] **Exploration** — UX mockups, architecture template *(deferred)*
  - [x] **Specification**
  - [x] **Engineering** — Class Model, ATDD, production code
  - [x] **Regression testing**
  - [ ] **User testing / UAT** *(Increment 2)*

  A reader knows exactly which stages are covered.

- Add a brief reason when opting a default stage out or a non-default stage in, so the decision is traceable.

  **Example (pass):** "[ ] Regression testing *(existing suite stable; negligible effort this increment)*" — the team actively decided to exclude it and said why.

## DO NOT

- Leave coverage boundary blank, vague, or as a free-text summary that does not name the specific stages.

  **Example (fail):** Scope section says "**Coverage boundary:** Standard" or "Development + testing" — does not map to bootcamp stages.

- Use legacy stage names (prioritization, story definition, acceptance tests as a stage, code) instead of bootcamp names.

  **Example (fail):** "[x] Story mapping" and "[x] Acceptance tests stage" — use **Discovery** and **Engineering (ATDD)** instead.

- Assume coverage carries over from a previous session without restating it.

  **Example (fail):** Session file references "same as last sprint's estimation" with no checklist — the session file must stand alone.

**Source:** Engagement convention; bootcamp stages in `../../../reference/stages/`.
