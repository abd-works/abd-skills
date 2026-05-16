# lo-fi prompt template

Fill the slots between `{{` and `}}` with verbatim excerpts from the inputs, then paste the filled prompt into the `abd-canvas` chat panel (interactive mode) or POST it to the canvas agent endpoint (headless mode). The agent will draw the wireframe.

---

```
SCREEN: {{SCREEN_NAME}}

This screen is part of the initial IA at:
{{INITIAL_IA_PATH}}

Its regions (from the initial IA) are:

{{REGIONS_FROM_INITIAL_IA}}

Stories grouped under this screen on the initial IA:

{{IN_SCOPE_STORIES}}

---

UBIQUITOUS LANGUAGE — verbatim from the UL file, screen-scope only
(Only terms whose stories appear on this screen.)

{{UBIQUITOUS_LANGUAGE_EXCERPT}}

---

ACCEPTANCE CRITERIA FOR THIS SCREEN — verbatim from the AC file
(Every AC for every in-scope story, character-for-character, including
WHEN / THEN / AND / BUT keywords and the original numbering.)

{{ACCEPTANCE_CRITERIA_EXCERPT}}

---

DRAW THIS SCREEN

Lay out the screen as a lo-fi wireframe:

- Use the regions from the initial IA above as the container structure.
- Place affordances inside the correct regions, labelled with UL terms
  (verbatim) or AC copy (verbatim). No invented labels.
- For every AC clause, ensure the screen renders the region or affordance
  it implies. The primary action sits in the user's eye-path; required
  feedback (errors, validation messages, status) has a labelled region.
- Attach the verbatim ACCEPTANCE CRITERIA block to the canvas beside the
  layout so reviewers can read both at once.
- This is a lo-fi pass: no colour decisions, no typography decisions, no
  brand polish, no production code, no ARIA roles. Structural labels and
  layout only.
```

---

## Slot reference

| Slot | Source | Notes |
| --- | --- | --- |
| `{{SCREEN_NAME}}` | initial IA | Exact screen name as it appears on `initial-ia.tldr`. |
| `{{INITIAL_IA_PATH}}` | engagement | e.g. `<engagement>/docs/ux/initial-ia.tldr`. |
| `{{REGIONS_FROM_INITIAL_IA}}` | initial IA | The region list for this screen, verbatim. |
| `{{IN_SCOPE_STORIES}}` | story map | User-visible stories on this screen + grouped system stories. |
| `{{UBIQUITOUS_LANGUAGE_EXCERPT}}` | UL file | Terms (name + full definition) for in-scope stories only, verbatim. |
| `{{ACCEPTANCE_CRITERIA_EXCERPT}}` | AC file | Every AC for every in-scope story, character-for-character. |
