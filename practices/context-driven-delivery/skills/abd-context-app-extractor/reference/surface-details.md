# Surface Details

Detailed guidance for each supported surface type. Read the section that matches your target.

---

## Web — Playwright

**Requires:** Node.js, `@playwright/test` installed in the target project.

### Key capabilities

| Capability | Purpose |
|---|---|
| `page.ariaSnapshot()` | Produces the WAI-ARIA tree as YAML — the primary capture format. See `reference/aria-capture-format.md` for what the output contains and why it is preferred over DOM scraping. |
| `page.screenshot({ fullPage: true })` | Visual record of each view — supplements the ARIA tree, does not replace it |
| `page.goto()` / `page.click()` | Navigate to each route and open dialogs and modals |

### Assumptions the template makes

- A `playwright.config.ts` with `baseURL` set and, optionally, `storageState` for pre-authenticated sessions.
- A running dev or test server, or a `webServer` entry in `playwright.config.ts`.

### Running

```bash
npx playwright test extract.spec.ts --reporter=line
```

### Template

See `templates/web/extract.spec.ts`. Fill in `APP_NAME`, `PERSONA`, and the `PAGES` array. Each `PAGES` entry needs a `slug`, a `url`, and an optional `setup` function that opens modals or navigates nested flows.

---

## Desktop — pywinauto (Windows)

**Requires:** Python 3.9+, `pywinauto`, `Pillow`.

```bash
pip install pywinauto Pillow
```

### Primary path — UIA (preferred)

pywinauto uses the Windows UI Automation (UIA) API — the Windows equivalent of WAI-ARIA. It returns a named element tree (roles, names, values) without pixel-level fragility.

| Capability | Purpose |
|---|---|
| `app.window().print_control_identifiers()` | Dumps the UIA tree to a string — the Windows equivalent of `page.ariaSnapshot()`. Save as `aria.yaml`. See `reference/aria-capture-format.md`. |
| `app.window().capture_as_image()` | Full-window screenshot — supplements the UIA tree, does not replace it |
| `element.click()` / `element.type_keys()` | Navigation and interaction |

### Fallback — pyautogui (pixel)

Use pyautogui only when the application does not expose UIA (legacy Win32 without accessibility, games, Electron with accessibility disabled). Capture screenshots with `pyautogui.screenshot()`. The template includes a `UIA_AVAILABLE` flag to switch between paths.

### Running

```bash
python scripts/extract.py
```

### Template

See `templates/desktop/extract.py`. Fill in `APP_NAME`, `PERSONA`, `APP_EXE`, and the `PAGES` list. Each page entry defines navigation steps (click sequences or keyboard shortcuts) that bring the application to that view.

---

## Microservices — httpx + HAR recorder

**Requires:** Python 3.9+, `httpx`, `PyYAML`.

```bash
pip install httpx pyyaml
```

### What the extractor does

1. Calls each known endpoint with representative inputs.
2. Records request + response as `.har` files under `docs/extracted-context/api-extraction/har/`.
3. Reconstructs an `openapi.yaml` from the collected traces.

### For gRPC services

```bash
grpcurl -plaintext localhost:50051 describe    # list services and message types
grpcurl -plaintext localhost:50051 list        # list available methods
```

Pipe the output to a file and treat it as the equivalent of `openapi.yaml` for downstream domain modelling.

### Template

See `templates/microservices/extract.py`. Fill in `APP_NAME`, `BASE_URL`, authentication details, and the `ENDPOINTS` list. Each endpoint entry specifies the HTTP method, path, and a sample request body.
