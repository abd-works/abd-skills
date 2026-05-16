# Lo-fi — {{SCREEN_NAME}}

> **Companion to** `docs/ux/lo-fi.tldr` / `lo-fi.svg`. This markdown is the structured spec for the canvas. Author or update **this file first**, then drive the canvas from it. After the canvas is updated, sync any change back into this file so the two never diverge.

## Metadata

| Field | Value |
| --- | --- |
| Screen | {{SCREEN_NAME}} (must match the screen name on the initial IA verbatim) |
| Initial IA | `docs/ux/initial-ia.tldr` (companion `docs/ux/initial-ia.md`) |
| Story map | {{STORY_MAP_PATH}} |
| Ubiquitous language | {{UBIQUITOUS_LANGUAGE_PATH}} |
| Acceptance criteria | {{ACCEPTANCE_CRITERIA_PATH}} |
| Canvas (`.tldr`) | `docs/ux/lo-fi.tldr` |
| Canvas (`.svg`) | `docs/ux/lo-fi.svg` |
| Mode | {{interactive | headless}} |
| Last canvas update | {{ISO_DATE}} |

## Description

{{ONE_PARAGRAPH_DESCRIPTION}}

One paragraph: what this screen is for, what the user does on it, what stories live here.

---

## Regions (from initial IA)

Copy the region list from the initial IA for this screen.

- {{REGION_1}}
- {{REGION_2}}
- {{REGION_3}}

---

## Affordances per region

Every affordance traces back to an AC clause or a UL term. Add the trace in the `Trace` column.

### {{REGION_NAME}}

| Affordance | Label (UL or AC, verbatim) | Trace |
| --- | --- | --- |
| {{TYPE: input/button/list/message area/...}} | {{LABEL_VERBATIM}} | {{AC clause id or UL term}} |

<!-- duplicate the ### block for each region -->

---

## In-scope stories

User-visible stories plus grouped system stories for this screen.

- {{USER_STORY_TITLE}}
- {{USER_STORY_TITLE}}
- (system) {{SYSTEM_STORY_TITLE}}

---

## Ubiquitous language excerpt (verbatim, screen-scope only)

Only terms whose stories appear on this screen. Copy term + definition character-for-character from the UL file.

- **{{TERM}}** — {{DEFINITION_VERBATIM}}
- **{{TERM}}** — {{DEFINITION_VERBATIM}}

---

## Acceptance criteria (verbatim)

Every AC for every in-scope story, character-for-character, with original story headings, numbering, and `WHEN/THEN/AND/BUT` keywords.

### {{STORY_HEADING_VERBATIM}}

1. {{AC_CLAUSE_VERBATIM}}
2. {{AC_CLAUSE_VERBATIM}}

<!-- duplicate for each in-scope story -->

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| {{ISO_DATE}} | initial | First draft. |
