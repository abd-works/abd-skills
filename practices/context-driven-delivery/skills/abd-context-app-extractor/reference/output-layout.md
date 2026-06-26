# Output Layout

## Folder structure

```
docs/extracted-context/
  app-extraction/
    extraction-overview.md        ← master log
    pages/                        ← one folder per captured view
      01-login/
        screenshot.png            ← full-page / full-window screenshot
        aria.yaml                 ← WAI-ARIA tree (web) or UIA tree (desktop) — see reference/aria-capture-format.md
      02-dashboard/
        screenshot.png
        aria.yaml
      03-campaigns-list/
        screenshot.png
        aria.yaml
      03b-campaign-create-modal/  ← modal is a separate slug with b/c suffix
        screenshot.png
        aria.yaml
  api-extraction/                       ← microservices surface only
    openapi.yaml                  ← reconstructed spec from HAR traces
    har/
      <endpoint>.har              ← raw network traces (one file per endpoint)
```

## extraction-overview.md schema

### YAML front matter

```yaml
---
app: <application name>
surface: web | desktop | microservice
tool: playwright | pywinauto | pyautogui | httpx
persona: <the role used during extraction, e.g. "Campaign Manager">
extraction_date: YYYY-MM-DD
pages_dir: ./pages/
---
```

### Per-page sections

Each captured page gets one `## <slug>` section:

```markdown
## 01-login

url_or_view: /login
user_intent: Authenticate to access the application
domain_focus: Authentication, Session
ux_focus: Form layout, error states
notes: Captures both empty and filled-with-error states
aria_snapshot: ./pages/01-login/aria.yaml
screenshot: ./pages/01-login/screenshot.png
```

**Required fields:** `url_or_view`, `user_intent`, `aria_snapshot`, `screenshot`.  
**Optional fields:** `domain_focus`, `ux_focus`, `notes`, `network_summary`.

## Slug naming convention

A slug is a short, human-readable identifier for a page or view:

- **Format:** `<two-digit-sequence>-<kebab-name>` — for example `01-login`, `03-campaigns-list`.
- **Modals and drawers:** Add a letter suffix on the parent slug — `03b-campaign-create-modal`, `03c-campaign-delete-confirm`.
- **Never use:** `step-001`, `page-1`, or any sequence-only name without a meaningful label.

The sequence prefix ensures lexical sort matches traversal order; the kebab label makes the folder readable at a glance in any file explorer.

## Downstream consumers

| Skill | What it reads |
|---|---|
| abd-story-mapping | `extraction-overview.md` — proposes epics and features from `user_intent` and `domain_focus` |
| abd-ux-mockup | `pages/*/aria.yaml` — generates wireframes from the ARIA/UIA tree |
| abd-domain-model | `domain_focus` tags across all pages — identifies domain concepts |
