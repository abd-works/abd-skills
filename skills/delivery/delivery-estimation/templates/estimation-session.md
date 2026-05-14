# Estimation Session

## Session metadata

- **Date:** {{DATE}}
- **Facilitator:** {{FACILITATOR_NAME}}
- **Participants:** {{PARTICIPANT_LIST}}

## Scope

- **Granularity:** {{SCOPE_LEVEL — epic | sub-epic | story | thin slice}}
- **Source:** {{WHERE_THE_BACKLOG_COMES_FROM — story map, sprint backlog, feature list, etc.}}

### Coverage boundary

Check each stage included in this session's estimates. Defaults are pre-checked; opt in or out as the team agrees.

- [ ] Story mapping — placing items in the backlog hierarchy *(not default)*
- [x] Acceptance criteria definition — writing WHEN/THEN AC
- [x] Specification definition — specification-by-example scenarios
- [x] Development — implementing production code
- [x] Story testing — acceptance tests / system integration tests
- [x] Regression testing — running and maintaining the regression suite
- [ ] User testing — end-user / UAT validation *(not default)*

## Contributing-factors catalog

List every factor the team agreed drives effort for this session. Score each factor per item using whatever scale the team chose (High / Medium / Low, 1–5, or notes).

| # | Factor | Description |
| --- | --- | --- |
| 1 | Technical complexity | How many moving parts, unfamiliar APIs, or non-trivial algorithms |
| 2 | Domain uncertainty | How well the team understands the business rules and edge cases |
| 3 | External dependencies | Waiting on other teams, third-party services, or vendor deliverables |
| 4 | Skill gaps | Whether the team has done this kind of work before |
| 5 | Integration surface | Number and complexity of integration points with other systems |
| 6 | Testing depth | Amount of test coverage expected (unit, integration, E2E, manual) |
| {{N}} | {{TEAM_ADDED_FACTOR}} | {{FACTOR_DESCRIPTION}} |

## Estimation-category scheme

- **Scheme:** {{SCHEME_NAME — e.g. T-shirt (XS/S/M/L/XL), Fibonacci-like (1/2/3/5/8/13), S/M/L/XL}}
- **Split threshold:** {{THRESHOLD — e.g. "> 5 points" or "> 8 days" or "> L". Default for stories: > 5 points / > 8 days. Items above this trigger a proactive split suggestion.}}

| Category | Rough meaning in this team's context |
| --- | --- |
| {{CATEGORY_1}} | {{WHAT_IT_MEANS — e.g. "< 1 day of pair work"}} |
| {{CATEGORY_2}} | {{WHAT_IT_MEANS}} |
| {{CATEGORY_3}} | {{WHAT_IT_MEANS}} |
| {{CATEGORY_4}} | {{WHAT_IT_MEANS}} |
| {{CATEGORY_5}} | {{WHAT_IT_MEANS — optional, only if scheme uses 5+ categories}} |

## Items estimated

Priority order is agreed before estimation begins. AI suggests an initial order; the team reorders before starting.

| Priority | Scope item | Category | Split? | Notes |
| --- | --- | --- | --- | --- |
| 1 | {{ITEM_NAME}} | {{CATEGORY}} | {{YES/NO — was the team split?}} | {{BRIEF_NOTE}} |
| 2 | {{ITEM_NAME}} | {{CATEGORY}} | {{YES/NO}} | {{BRIEF_NOTE}} |

## Session summary

- **Total items estimated:** {{COUNT}}
- **Items flagged for follow-up:** {{LIST_OF_ITEMS_NEEDING_SPIKE_OR_DECOMPOSITION}}
- **New stories or AC discovered:** {{COUNT_AND_BRIEF_DESCRIPTION}}
- **Session duration:** {{TIME}}

---

## Example: Pet Store adoption flow (filled)

### Session metadata

- **Date:** 2026-05-14
- **Facilitator:** Sarah (delivery lead)
- **Participants:** Sarah, Marcus (backend), Priya (frontend), Tomás (QA)

### Scope

- **Granularity:** Story
- **Source:** Story map, Increment 1 (Browse and Adopt a Pet)

#### Coverage boundary

- [ ] Story mapping *(not needed — map already complete)*
- [x] Acceptance criteria definition
- [x] Specification definition
- [x] Development
- [x] Story testing (acceptance tests / system integration tests)
- [x] Regression testing
- [ ] User testing *(deferred to Increment 2 UAT pass)*

### Contributing-factors catalog

| # | Factor | Description |
| --- | --- | --- |
| 1 | Technical complexity | Moving parts, unfamiliar APIs, non-trivial algorithms |
| 2 | Domain uncertainty | How well we understand the adoption rules and edge cases |
| 3 | External dependencies | Third-party shelter API, payment gateway |
| 4 | Skill gaps | First time using the shelter integration SDK |
| 5 | Testing depth | Unit + integration tests; E2E deferred to later increment |
| 6 | Data migration | Legacy pet records need transformation |

### Estimation-category scheme

- **Scheme:** T-shirt (S / M / L / XL)
- **Split threshold:** > L (any item estimated XL triggers a split discussion; default guideline for stories is > 5 points or > 8 days, which maps to XL in this session's scheme)

| Category | Rough meaning |
| --- | --- |
| S | < 1 day of pair work, well-understood, no dependencies |
| M | 1–2 days, some complexity or one dependency |
| L | 3–5 days, multiple factors at play or significant uncertainty |
| XL | > 5 days, needs decomposition before committing |

### Items estimated

AI suggested order: Submit Adoption Application (highest risk), Receive Adoption Confirmation, Track Application Status, Browse Available Pets, View Pet Details. Team moved Browse first since it unblocks all other items, kept Submit second. Final agreed order below.

| Priority | Scope item | Category | Split? | Notes |
| --- | --- | --- | --- | --- |
| 1 | Browse Available Pets | S | No | Straightforward list + filter; API already spiked; unblocks everything else |
| 2 | Submit Adoption Application | L | Yes | Shelter API integration unknown; Priya voted M, Marcus voted XL — resolved after discussing API contract |
| 3 | View Pet Details | S | No | Single-page read; depends on Browse |
| 4 | Track Application Status | M | No | Polling shelter API; complexity in status mapping |
| 5 | Receive Adoption Confirmation | M | Yes | Payment gateway timing uncertain; team added "payment latency" as contributing factor mid-session |

### Session summary

- **Total items estimated:** 5
- **Items flagged for follow-up:** Submit Adoption Application — spike the shelter API contract before committing to L
- **New stories or AC discovered:** 2 — "Handle shelter API timeout gracefully" (new story); "Adoption application must validate pet availability before submission" (new AC on Submit Adoption Application)
- **Session duration:** 45 minutes
