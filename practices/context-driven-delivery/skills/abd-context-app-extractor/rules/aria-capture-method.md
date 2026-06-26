# Rule: aria-capture-method

**Artifact:** `pages/<slug>/aria.yaml` inside `docs/extracted-context/app-extraction/`.

`aria.yaml` must contain a role-labelled semantic tree — not absent, not a raw HTML dump, not a flat list of element attributes. A reviewer can open the file and immediately read structural meaning from it.

## DO

- Contain indented, role-labelled nodes where every entry names a role and an accessible name.

  **Example (pass):**
  ```yaml
  - main:
    - heading "Sign in" [level=1]
    - textbox "Email address"
    - button "Sign in"
  ```
  Roles (`main`, `heading`, `textbox`, `button`) and names (`"Sign in"`, `"Email address"`) are both present. The tree is readable without the screenshot.

- Be present alongside `screenshot.png` in every `pages/<slug>/` folder.

  **Example (pass):** `pages/03-campaigns-list/` contains both `aria.yaml` and `screenshot.png`. A downstream skill can choose the representation it needs.

## DO NOT

- Contain raw HTML, CSS selectors, or a flat attribute list instead of a role-labelled tree.

  **Example (fail):**
  ```yaml
  - tag: input
    class: form-control
    aria-label: Email address
  - tag: button
    class: btn btn-primary
    text: Sign in
  ```
  This is a DOM dump, not an ARIA tree — roles and nesting are absent; it cannot support layout or interaction analysis.

- Be absent when the surface supports semantic-tree capture.

  **Example (fail):** `pages/02-dashboard/` contains only `screenshot.png`. The view was captured visually but not semantically — downstream analysis has no structured data to work from.

**Source:** WAI-ARIA Standard; `reference/aria-capture-format.md`.
