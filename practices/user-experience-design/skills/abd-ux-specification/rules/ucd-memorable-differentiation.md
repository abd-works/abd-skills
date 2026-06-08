# Rule: The implementation carries the committed aesthetic direction into running code

**Scanner:** AI review

The aesthetic direction committed in `abd-hi-fi` survives into the running code. Typography roles and colour roles are implemented as real tokens, CSS variables, or theme values — not as inline overrides of a default component library. The running screen looks like the hi-fi mockup; it does not look like an untouched off-the-shelf component set.

## DO

- Implement typography roles as project tokens that match the hi-fi role table.

  **Example (pass):** Hi-fi declares `display — serif, 32/40, weight 600`; the implementation has a `display` token (or theme variable) with those exact values, applied wherever the hi-fi shows the display role.

- Implement colour roles as project tokens that match the hi-fi role values.

  **Example (pass):** Hi-fi declares `accent — #B85C38`; the implementation has an `accent` token with that exact value, used by the primary action.

- Open the running screen beside the hi-fi `.svg` and reconcile differences before shipping.

  **Example (pass):** Spacing on the primary action looks tighter in the browser than on the canvas — the implementation adjusts to match the spacing scale value the hi-fi declared.

## DO NOT

- Ship default component-library look-and-feel and call it implementation.

  **Example (fail):** Default shadcn buttons, default Tailwind palette, default font stack, with no mapping to the hi-fi roles.

- Use one-off colours, type styles, or spacings that are not in the role tables.

  **Example (fail):** A `text-blue-500` link colour that does not map to any hi-fi colour role.

- Drift from the hi-fi without raising it as a correction.

  **Example (fail):** The running screen uses a sans-serif display where the hi-fi specified a serif, with no note explaining why. Either fix the implementation or fix the hi-fi explicitly — do not silently diverge.
