# Rule: Implementation-level accessibility meets the host project's floor

**Scanner:** AI review

The running screen is keyboard reachable, focus is visible, inputs have programmatic labels, errors are programmatically associated with their inputs, state changes are announced where appropriate, and meaning is never conveyed by colour alone. If the host project declares an accessibility standard (typically WCAG 2.2 AA for web), the screen meets it without silencing the accessibility checker.

## DO

- Pair every input with a programmatic label, not just a placeholder.

  **Example (pass):** `<label for="coh-game-directory-path">COH game directory path</label> <input id="coh-game-directory-path" ...>`.

- Associate error messages with their inputs.

  **Example (pass):** `<input aria-describedby="path-error">` and the error region has `id="path-error"` and the verbatim AC error copy.

- Make focus visible on every interactive element.

  **Example (pass):** A focus ring is declared in the styles (matching the hi-fi accent role or an explicit focus role) and is not removed by `outline: none` without a replacement.

- Make the screen keyboard reachable in reading order.

  **Example (pass):** Tab order: heading skip → input → Browse → error region (when present) → Continue. Matches the visual reading order.

## DO NOT

- Communicate state through colour alone.

  **Example (fail):** A red border on the input with no text or icon nearby that says "error".

- Remove focus styles globally.

  **Example (fail):** `*:focus { outline: none; }` with no replacement focus style.

- Use a placeholder as the only label.

  **Example (fail):** `<input placeholder="COH game directory path" />` with no `<label>` or `aria-label`.

- Silence the accessibility checker rather than fix the violation.

  **Example (fail):** `axe.disableRule(...)` for a rule the implementation actually violates.
