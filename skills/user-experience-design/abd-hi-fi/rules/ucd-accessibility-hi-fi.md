# Rule: Hi-fi accessibility — colour is never the only signal, contrast meets the floor

**Scanner:** AI review

At the hi-fi stage, the visual decisions must not compromise accessibility. Colour is never the only signal for state (errors, warnings, success, focus). Text and meaningful UI elements meet a minimum contrast against their surface. Brand-driven aesthetics do not override this; they live inside the constraint.

## DO

- Pair every coloured state cue with a text or icon cue.

  **Example (pass):** An error input shows the `error` colour role on the border *and* a verbatim AC error message in the labelled `validation error area`. Removing the colour still leaves the meaning intact.

- Meet a contrast floor on body and label text against the surface role.

  **Example (pass):** `ink` on `surface` is `#1A1A1A` on `#FAFAF7` — a contrast ratio well above 4.5:1.

- Treat focusable affordances as visible even before code — note that focus and hover states will be designed in `abd-interface-design`.

  **Example (pass):** The hi-fi annotates `Continue` with `focus + hover ring designed at implementation` rather than handwaving them away.

## DO NOT

- Communicate state through colour alone.

  **Example (fail):** A green or red border around an input with no text or icon to identify the state.

- Place body text in a colour that falls below the contrast floor against its surface.

  **Example (fail):** `#9AA0A6` body on a `#FAFAF7` surface — visually fashionable, but well under 4.5:1.

- Mask brand aesthetics as accessibility — for example, claiming a low-contrast palette is "intentional minimalism".
