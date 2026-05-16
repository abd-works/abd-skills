# Hi-fi — {{SCREEN_NAME}}

> **Companion to** `docs/ux/hi-fi.tldr` / `hi-fi.svg`. This markdown is the structured spec for the canvas — it carries the committed aesthetic direction, typography and colour roles, density, and spacing scale. Author or update **this file first**, then drive the canvas from it. After the canvas is updated, sync any change back into this file so the two never diverge.

## Metadata

| Field | Value |
| --- | --- |
| Screen | {{SCREEN_NAME}} (must match the lo-fi screen name verbatim) |
| Lo-fi reference | `docs/ux/lo-fi.tldr` (companion `docs/ux/lo-fi.md`) |
| Design tokens / brand guide | {{TOKENS_OR_BRAND_PATH_OR_NONE}} |
| Canvas (`.tldr`) | `docs/ux/hi-fi.tldr` |
| Canvas (`.svg`) | `docs/ux/hi-fi.svg` |
| Last canvas update | {{ISO_DATE}} |

## Description

{{ONE_PARAGRAPH_DESCRIPTION}}

One paragraph: what this screen looks like under this direction, who it's for, what the visual decisions communicate.

---

## Aesthetic direction (committed, single)

- **Name:** {{DIRECTION_NAME}} (e.g. `editorial`, `brutalist`, `playful`, `industrial`)
- **Adjectives:** {{three or four adjectives}}
- **Rationale:** {{ONE_OR_TWO_SENTENCES}}

---

## Typography roles

Every text element on the canvas maps to one of these roles. No one-off styles.

| Role | Family | Weight | Size / line-height | Tracking | Notes |
| --- | --- | --- | --- | --- | --- |
| display | {{FAMILY}} | {{WEIGHT}} | {{SIZE}}/{{LH}} | {{TRACKING}} | |
| heading | | | | | |
| body | | | | | |
| label | | | | | |
| microcopy | | | | | |

---

## Colour roles

Every coloured element on the canvas maps to one of these roles. Colour is never the only signal for meaning.

| Role | Value | Notes |
| --- | --- | --- |
| surface | {{HEX}} | background |
| ink | {{HEX}} | primary text |
| ink-muted | {{HEX}} | secondary text |
| accent | {{HEX}} | primary action |
| warning | {{HEX}} | always paired with text/icon |
| error | {{HEX}} | always paired with text/icon |
| success | {{HEX}} | always paired with text/icon |

---

## Density and spacing scale

- **Density:** {{compact | comfortable | spacious}}
- **Spacing scale:** {{e.g. 4, 8, 12, 16, 24, 32, 48}} (every gap, padding, margin on the canvas is one of these values)

---

## Carried over from lo-fi (unchanged)

Regions, affordances, labels, and AC carry over from the lo-fi spec without changes. If anything in this list needs to change, **stop**, fix it in `abd-lo-fi` (or further upstream), and rerun this skill.

- Regions: {{see docs/ux/lo-fi.md}}
- Affordances and labels: {{see docs/ux/lo-fi.md}}
- Acceptance criteria: {{see docs/ux/lo-fi.md}}

---

## Accessibility notes (hi-fi level)

- Contrast: body / label text against surface meets at least 4.5:1.
- State cues: every coloured state (error, warning, success, focus) is paired with text or icon.
- Focus and hover styles: noted on the canvas; full implementation deferred to `abd-interface-design`.

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| {{ISO_DATE}} | initial | First draft. |
