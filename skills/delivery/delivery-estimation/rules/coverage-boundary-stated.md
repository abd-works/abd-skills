---
scanner: ~
---
# Rule: Coverage boundary stated before estimates begin

The estimation session file must declare which delivery stages the estimate covers before any items are estimated. Without a coverage boundary, estimates from different sessions or teams are not comparable, and team members may be sizing different things under the same number. The skill defines seven standard stages with defaults; the session must show which are checked in and which are out.

Default stages (included unless opted out): acceptance criteria definition, specification definition, development, story testing, regression testing. Non-default stages (excluded unless opted in): story mapping, user testing.

Passing means the session file has an explicit coverage boundary checklist in the scope section. Failing means estimates exist but the reader cannot tell which stages are included.

## DO

- State the coverage boundary as a checklist of delivery stages, marking each as included or excluded, in the session scope section.

  **Example (pass):**

  - [ ] Story mapping *(not needed — map already complete)*
  - [x] Acceptance criteria definition
  - [x] Specification definition
  - [x] Development
  - [x] Story testing (acceptance tests / system integration tests)
  - [x] Regression testing
  - [ ] User testing *(deferred to Increment 2 UAT pass)*

  A reader knows exactly which stages are covered.

- Add a brief reason when opting a default stage out or a non-default stage in, so the decision is traceable.

  **Example (pass):** "[ ] Regression testing *(existing regression suite is stable; regression effort is negligible this increment)*" — the team actively decided to exclude it and said why.

## DO NOT

- Leave coverage boundary blank, vague, or as a free-text summary that does not name the specific stages.

  **Example (fail):** Scope section says "**Coverage boundary:** Standard" or "Development + testing" — does "testing" include story testing, regression, user testing, or all three?

- Assume coverage carries over from a previous session without restating it.

  **Example (fail):** Session file has no coverage boundary but references "same as last sprint's estimation" — the session file must stand alone.

**Source:** Engagement convention (delivery-estimation requirements — "be specific on estimate what is covered"; stages: story mapping not default, AC def, spec def, dev, story test, regression test default, user test not default).
