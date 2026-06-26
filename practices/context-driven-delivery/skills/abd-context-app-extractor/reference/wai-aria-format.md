# WAI-ARIA Format (Web)

**Full spec:** https://www.w3.org/TR/wai-aria/  
**Authoring practices guide:** https://www.w3.org/WAI/ARIA/apg/

## What it is

WAI-ARIA (Accessible Rich Internet Applications) is the W3C standard that assigns semantic meaning to browser UI. It describes every visible element in terms of three vectors:

- **Role** — what the element is (`button`, `textbox`, `dialog`, `main`, `navigation`)
- **Properties** — static identity and relationships (`aria-label`, `aria-describedby`)
- **States** — live interaction flags (`aria-expanded`, `aria-disabled`, `aria-haspopup`)

This makes the ARIA tree the authoritative semantic record of a web view — richer than a screenshot, more stable than CSS selectors.

## How it is captured

Playwright exposes the browser's accessibility tree directly via `page.ariaSnapshot()`. No parsing required — the method returns a YAML string ready to write to `aria.yaml`.

## Output format

`aria.yaml` for a web surface is a Playwright ARIA snapshot — indented YAML with role-labelled nodes:

```yaml
- document:
  - main:
    - heading "Sign in" [level=1]
    - textbox "Email address"
    - textbox "Password"
    - button "Sign in"
    - link "Forgot password?"
  - dialog "Session expired" [modal=true]:
    - paragraph "Your session has timed out."
    - button "OK"
```

Each line: `- <role> "<accessible name>" [<state>=<value>]`

## What it does not capture

- Visual styling (colour, font, spacing) — use the screenshot
- Canvas-drawn content and PDF embeds — absent or degraded
- Network payloads — add `network_summary` to the overview entry if API shape matters
