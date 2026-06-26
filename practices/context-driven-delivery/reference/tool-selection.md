# Tool Selection

Choose the tool based on the **surface type** of the target application. Semantic-tree tools are always preferred over pixel-based fallbacks.

> **Shared reference** — this file is used by both `abd-context-app-extractor` and `abd-stub-external-dependencies`. Changes here apply to both skills.

## Surface-to-tool matrix

| Surface | Primary tool | Fallback |
|---|---|---|
| Web (browser) | Playwright (`page.ariaSnapshot()`) | Puppeteer |
| Windows desktop — Win32 / WPF / WinForms / UWP | pywinauto (UIA) | pyautogui |
| macOS desktop | pyautogui | AppleScript |
| REST / GraphQL microservice | httpx + HAR recorder | requests |
| gRPC microservice | grpcurl + proto reflection | — |

## Identifying the surface from the repo

Examine the target repository for these indicators before choosing a tool:

- `package.json` containing `@playwright/test` or a `playwright.config.ts` → **web**
- `.exe`, `.app`, WinForms / WPF project files, or a Windows application manifest → **Windows desktop**
- `openapi.yaml`, `.proto` files, or a Dockerfile that exposes a port with no UI → **microservice**
- Multiple indicators → run a **separate extraction per surface** and place outputs in `from-application/` and `from-api/` respectively.

## Why semantic trees first

Playwright's `page.ariaSnapshot()` and pywinauto's UIA tree give you a structured, role-labelled description of layout, data, and interactions in a single call — without brittle CSS selectors or image matching. The ARIA/UIA tree is the complete authoritative record of what is on screen; screenshots are the visual supplement, not the primary source.

## Setup commands

### Web — Playwright
```bash
npx playwright --version           # confirm installation
cp <skill>/templates/web/extract.spec.ts <repo>/tests/extract.spec.ts
```

### Windows desktop — pywinauto
```bash
pip install pywinauto Pillow
cp <skill>/templates/desktop/extract.py <repo>/scripts/extract.py
```

### Microservices — httpx
```bash
pip install httpx pyyaml
cp <skill>/templates/microservices/extract.py <repo>/scripts/extract.py
```
