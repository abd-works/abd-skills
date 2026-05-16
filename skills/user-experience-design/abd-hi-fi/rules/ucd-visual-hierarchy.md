# Rule: Visual hierarchy makes the primary action and reading order unmistakable

**Scanner:** AI review

The most important affordance on the screen — the one the acceptance criteria describe as the primary outcome — is visually unmistakable: largest active element, highest contrast against the surface, most space around it. The reading order through the screen matches the user-flow order established in the lo-fi.

## DO

- Make the primary action the heaviest visual element.

  **Example (pass):** `Continue` on the `game directory prompt` is a filled accent button, the largest interactive element, surrounded by white space; `Browse...` is an outline secondary button beside the input; everything else is body or label weight.

- Use scale, contrast, and spacing together for hierarchy, not just colour.

  **Example (pass):** Display headline > body > label > microcopy, with explicit size, weight, and spacing differences declared in the typography roles. Removing colour from the screen would still leave the hierarchy readable.

- Place affordances in reading order top-to-bottom and left-to-right (LTR) so the eye-path matches the AC flow.

  **Example (pass):** Heading → explanatory body → input → error region → primary action. The user reads the AC flow without scrolling or skipping.

## DO NOT

- Show two equally-weighted primary actions.

  **Example (fail):** Two filled accent buttons of identical prominence — `Continue` and `Cancel` — when only `Continue` is the primary outcome described by AC.

- Lean on colour alone to establish hierarchy.

  **Example (fail):** Same-size, same-weight buttons, distinguished only by hue. In greyscale, the hierarchy disappears.

- Bury the primary action below the fold or behind secondary content.

  **Example (fail):** `Continue` placed under a block of decorative imagery the AC do not require.
