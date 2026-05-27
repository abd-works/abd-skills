# Interface design — {{SCREEN_NAME}}

> **Companion to** the committed code under {{IMPLEMENTATION_PATH}} and to `docs/ux/hi-fi.tldr` / `lo-fi.tldr`. This markdown is the structured spec for the implementation — it records the framework decision, the AC → behaviour → test mapping, and the accessibility / performance gates. Author or update **this file first**, then implement the screen. After the screen is implemented (or changed), sync any change back into this file so spec and code never diverge.

## Metadata

| Field | Value |
| --- | --- |
| Screen | {{SCREEN_NAME}} (must match the hi-fi / lo-fi screen name verbatim) |
| Hi-fi reference | `docs/ux/hi-fi.tldr` (companion `docs/ux/hi-fi.md`) |
| Lo-fi reference | `docs/ux/lo-fi.tldr` (companion `docs/ux/lo-fi.md`) |
| Acceptance criteria | {{ACCEPTANCE_CRITERIA_PATH}} |
| Target framework | {{e.g. React, Vue, WPF, SwiftUI}} |
| Host project root | {{ABSOLUTE_PATH}} |
| Implementation path | {{ABSOLUTE_PATH_TO_SCREEN_FOLDER}} |
| Test path | {{ABSOLUTE_PATH_TO_TEST_FOLDER}} |
| Last implementation update | {{ISO_DATE}} |

## Description

{{ONE_PARAGRAPH_DESCRIPTION}}

One paragraph: what this screen does in the running application, what behaviours the user can trigger, how it fits in the host project.

---

## Host project conventions (discovered, not invented)

- **Folder layout:** {{e.g. feature folder under src/screens/}}
- **State management:** {{e.g. Zustand store, MobX, useReducer}}
- **Styling:** {{e.g. CSS modules, Tailwind tokens, styled-components}}
- **Token system:** {{path to the file declaring typography/colour/spacing tokens}}
- **Test framework:** {{e.g. Vitest + RTL, Jest, xUnit}}
- **Lint / format / type gates:** {{e.g. eslint + prettier + tsc --noEmit}}
- **Accessibility check:** {{e.g. axe-core integration in tests}}
- **Performance budget:** {{path to budget config and the relevant caps}}

---

## Carried over from upstream (unchanged)

These are inputs, not decisions. If something is wrong here, fix it in the upstream skill.

- **Regions:** see `docs/ux/lo-fi.md`
- **Affordances and labels (verbatim):** see `docs/ux/lo-fi.md`
- **Acceptance criteria (verbatim):** see `docs/ux/lo-fi.md`
- **Typography roles:** see `docs/ux/hi-fi.md`
- **Colour roles:** see `docs/ux/hi-fi.md`
- **Density and spacing scale:** see `docs/ux/hi-fi.md`

---

## AC → behaviour → test mapping

One row per AC clause. The test name traces back to the story title and clause number so reviewers can match each test to its source.

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| {{STORY_TITLE}} | 1 | {{ONE_LINE_BEHAVIOUR}} | `{{STORY_TITLE}} — AC 1: {{SHORT}}` | pending / passing / failing |
| {{STORY_TITLE}} | 2 | {{ONE_LINE_BEHAVIOUR}} | `{{STORY_TITLE}} — AC 2: {{SHORT}}` | |

---

## Accessibility implementation

| Check | Status | Notes |
| --- | --- | --- |
| Every input has a programmatic label | | `<label for>` or framework equivalent. |
| Focus order matches reading order | | Tab through; describe order. |
| Focus is visible | | Focus ring style declared, not removed. |
| Errors are programmatically associated | | `aria-describedby` or equivalent. |
| State cues are not colour-only | | Text or icon paired with colour. |
| Keyboard reachable | | Every affordance reachable without mouse. |
| Axe (or host equivalent) passes | | No rule silenced. |

---

## Performance constraints

| Constraint | Budget | Current | Notes |
| --- | --- | --- | --- |
| {{e.g. screen bundle size}} | {{e.g. ≤80 KB gzip}} | {{measured}} | |
| {{e.g. initial paint}} | {{e.g. ≤200 ms p75}} | {{measured}} | |
| {{e.g. animation frame budget}} | {{e.g. ≤16 ms/frame}} | {{measured}} | |

If the host project does not declare explicit budgets, record the project's current baseline and a note confirming this screen does not regress it.

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| {{ISO_DATE}} | initial | First draft. |
