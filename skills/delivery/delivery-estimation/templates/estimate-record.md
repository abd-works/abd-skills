# Estimate Record

## Item

- **Scope item:** {{ITEM_NAME}}
- **Scope level:** {{LEVEL — epic | feature | story | thin slice}}
- **Source:** {{WHERE_THIS_ITEM_LIVES — e.g. "story map, Increment 1, epic: Browse Catalog"}}

## Estimate

- **Category:** {{CHOSEN_CATEGORY}}
- **Coverage:** {{STAGES_CHECKED_IN_SESSION — e.g. "AC def, spec def, dev, story test, regression test (per session coverage)"}}

## Contributing-factor breakdown

Score or note each factor from the session catalog for **this specific item**. Do not copy-paste generic scores — each item's factors should reflect its reality.

| Factor | Score / Note |
| --- | --- |
| {{FACTOR_1_NAME}} | {{SCORE_OR_NOTE_FOR_THIS_ITEM}} |
| {{FACTOR_2_NAME}} | {{SCORE_OR_NOTE_FOR_THIS_ITEM}} |
| {{FACTOR_N_NAME}} | {{SCORE_OR_NOTE_FOR_THIS_ITEM}} |

## Team vote

- **Round 1:** {{VOTES — e.g. "Sarah: M, Marcus: XL, Priya: M, Tomás: L"}}
- **Divergence discussion:** {{WHAT_THE_OUTLIERS_SAID — or "No divergence" if unanimous}}
- **Round 2 (if needed):** {{VOTES_AFTER_DISCUSSION — or "N/A"}}
- **Final consensus:** {{FINAL_CATEGORY}}

## Discussion notes

{{FREE_TEXT — what the team talked about, risks surfaced, assumptions made, open questions}}

## Emergent scope

Record any backlog changes that surfaced during estimation of this item. Use the downstream skill shown to action each one.

- **New AC** → `abd-acceptance-criteria`: {{DESCRIPTION}}
- **New story / epic** → `abd-story-mapping`: {{DESCRIPTION}}
- **Split** → `abd-story-mapping` (epic → sub-epics/stories) or `abd-thin-slicing` (story → thin slices): {{DESCRIPTION}}
- **Merge** → `abd-story-mapping`: {{DESCRIPTION}}
- **Open question**: {{DESCRIPTION}}

Persist structural changes (new items, splits, merges) to `story-graph.json` via `story-graph-ops`.

If none: "**Emergent scope:** None — estimation confirmed existing scope is sufficient."

## Follow-up

- **Needs further work:** {{YES/NO}}
- **Action:** {{WHAT — e.g. "Spike shelter API contract" or "Decompose into sub-stories" or "None"}}

---

## Example: Submit Adoption Application (filled)

### Item

- **Scope item:** Submit Adoption Application
- **Scope level:** Story
- **Source:** Story map, Increment 1, epic: Adopt a Pet

### Estimate

- **Category:** L
- **Coverage:** AC def, spec def, development, story testing, regression testing (per session coverage)

### Contributing-factor breakdown

| Factor | Score / Note |
| --- | --- |
| Technical complexity | High — shelter API integration, form validation, multi-step submission flow |
| Domain uncertainty | Medium — adoption rules understood but shelter-side validation rules not yet documented |
| External dependencies | High — shelter API contract not finalized; payment gateway for adoption fee |
| Skill gaps | Medium — team has not used the shelter SDK before; payment SDK is familiar |
| Testing depth | High — integration tests needed for shelter API; mock strategy TBD |
| Data migration | Low — no legacy data involved for this story |

### Team vote

- **Round 1:** Sarah: L, Marcus: XL, Priya: M, Tomás: L
- **Divergence discussion:** Marcus (XL): "We have no API contract yet — could be a week just figuring out the integration." Priya (M): "The form and frontend are straightforward; only the API call is unknown." Team agreed the API uncertainty is real but bounded — a spike would reduce it to M. Estimated as L with a spike flagged.
- **Round 2:** Sarah: L, Marcus: L, Priya: L, Tomás: L
- **Final consensus:** L

### Discussion notes

The shelter API is the main risk. Marcus has seen similar integrations take longer than expected when the contract is unclear. Team agreed to spike the API contract before committing. If the spike reveals the API is well-documented and stable, this drops to M. If the API requires custom adapter work, it stays L or needs decomposition.

Priya raised that the form should validate pet availability before submission — if the pet was adopted between browse and submit, the application should fail gracefully.

### Emergent scope

- **New story** → `abd-story-mapping`: Handle shelter API timeout gracefully (error state, retry, user message)
- **New AC** → `abd-acceptance-criteria`: Adoption application must validate pet availability before submission
- **Split** → `abd-thin-slicing`: If spike reveals adapter work, split this story into two thin slices — (1) submit with mock shelter API, happy path only; (2) integrate real shelter API with error handling
- **Open question:** Does the shelter API support idempotent submission? If not, we need duplicate-detection logic.

### Follow-up

- **Needs further work:** Yes
- **Action:** Spike the shelter API contract (half-day timebox). Re-estimate after spike if the category changes.
