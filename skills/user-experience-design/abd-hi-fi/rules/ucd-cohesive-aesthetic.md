# Rule: Typography, colour, and density are role-driven and consistent

**Scanner:** AI review

The hi-fi mockup declares typography roles and colour roles on the canvas with explicit values, and uses only those roles for every element on the screen. Density and a small spacing scale are declared and used consistently. One-off type styles, ad-hoc colours, or improvised spacing values are a fail because they break the committed direction.

## DO

- Declare typography roles with explicit values and reuse them.

  **Example (pass):**
  ```
  Typography roles:
    display   — serif, 32/40, weight 600
    body      — sans, 16/24, weight 400
    label     — sans, 14/20, weight 500, +0.2 tracking
    microcopy — sans, 13/18, weight 400
  ```
  Every text element on the screen maps to one of these roles.

- Declare colour roles with explicit values and reuse them.

  **Example (pass):**
  ```
  Colour roles:
    surface   — #FAFAF7
    ink       — #1A1A1A
    ink-muted — #6B6B6B
    accent    — #B85C38
    error     — #B23A48
  ```
  Every coloured element on the screen maps to one of these roles.

- Pick one density and one spacing scale and stick to it.

  **Example (pass):** Density `comfortable`, spacing scale `4, 8, 12, 16, 24, 32, 48`. Every gap, padding, and margin on the canvas is one of those values.

## DO NOT

- Use a typography style that is not in the declared roles.

  **Example (fail):** A one-off `serif, 18px, italic` for a single subhead — the role table does not include it.

- Use a colour that is not in the declared roles.

  **Example (fail):** A `#3366CC` link colour that does not map to any declared role.

- Mix densities or improvise spacing values.

  **Example (fail):** Compact stacks in the input area, spacious stacks in the prompt area, and `13px` and `27px` spacings used inconsistently with no entry on the scale.
