# Rule: One aesthetic direction, committed and named on the canvas

**Scanner:** AI review

Every hi-fi mockup names its aesthetic direction in a short on-canvas note, and applies that direction consistently across typography, colour, hierarchy, and density. "Vaguely modern", "default shadcn", "generic AI", or mixing two directions in one screen is a fail — not because those are bad aesthetics, but because they are not chosen aesthetics.

## DO

- Write a `Direction:` note on the canvas with a name and three or four adjectives.

  **Example (pass):**
  ```
  Direction: editorial / serif headlines, generous white space,
             neutral palette, single warm accent
  ```

- Make every visual decision serve the named direction.

  **Example (pass):** The named direction is `editorial` — the display font is a serif, headlines are large with generous line-height, the palette is restrained, and the primary action uses the one named accent.

- When offering options to the user, present them as named directions.

  **Example (pass):** "Two options: (1) editorial — serif, calm, neutral; (2) playful — rounded sans, saturated palette, generous motion cues. Pick one before we proceed."

## DO NOT

- Leave the direction implicit.

  **Example (fail):** No `Direction:` note on the canvas, and the visual decisions look like a mix of two or three aesthetics.

- Mix directions in one screen.

  **Example (fail):** Brutalist heavy black headlines paired with playful pastel buttons and editorial serif body copy.

- Ship a default-look mockup.

  **Example (fail):** A grey-on-grey card with a generic primary-blue button, no named direction, no rationale — the visual equivalent of saying "just make it look professional".
