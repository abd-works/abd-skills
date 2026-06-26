# Rule: tool-hierarchy

**Artifact:** The extraction script (`extract.spec.ts` or `extract.py`) and the YAML front matter `tool:` field in `extraction-overview.md`.

When multiple tools are available for a surface, the semantic-tree tool must be chosen as the primary mechanism. Pixel-based tools are fallbacks only — they produce screenshots but no structured data, forcing downstream skills to operate without the ARIA/UIA tree.

## DO

- Choose Playwright as the primary tool when the target is a web application, regardless of whether a raw HTTP client or a pixel-based tool is also installed.

  **Example (pass):** Target is a Next.js app. `extraction-overview.md` has `tool: playwright`. The script calls `page.ariaSnapshot()` for every page. A pixel screenshot library is present in `devDependencies` but not used in the extraction script.

- Choose pywinauto (UIA path) as the primary tool when the target is a Windows desktop application that exposes a UIA accessibility tree.

  **Example (pass):** `extract.py` imports `pywinauto` and calls `window.print_control_identifiers()`. The `UIA_AVAILABLE = True` flag is set. pyautogui is imported but only activated when `UIA_AVAILABLE` is `False`.

- Document the fallback reason in a code comment when pyautogui or a non-semantic tool is used as primary.

  **Example (pass):** `# UIA not available — Electron app has accessibility disabled. Falling back to pyautogui for screenshot-only capture.`

## DO NOT

- Use pyautogui as the primary capture method for a Windows desktop application without first confirming that pywinauto's UIA API fails for that target.

  **Example (fail):** `extract.py` imports only `pyautogui` and `extraction-overview.md` has `tool: pyautogui` for a WPF application — WPF exposes full UIA; pywinauto would have worked and produced a structured tree.

- Record `tool: playwright` in `extraction-overview.md` but use Puppeteer or raw `fetch` calls in the actual script.

  **Example (fail):** Front matter says `tool: playwright` but the script is a Node `fetch` loop writing raw JSON responses — no ARIA tree is captured, which misrepresents the extraction and leaves downstream skills without layout or interaction data.

**Source:** Engagement convention (abd-context-app-extractor authoring, 2026-06-25); pywinauto UIA documentation.
