# Rule: extraction-overview-shape

**Artifact:** `docs/extracted-context/app-extraction/extraction-overview.md`.

`extraction-overview.md` is the master index for a completed extraction. Downstream skills (abd-story-mapping, abd-ux-mockup, abd-domain-model) open this file to understand the full scope of what was captured. This rule checks that the file is present, correctly structured, and complete.

## DO

- Include YAML front matter with at least `app`, `surface`, `tool`, and `extraction_date` fields before any markdown content.

  **Example (pass):**
  ```yaml
  ---
  app: PML Vouchera
  surface: web
  tool: playwright
  persona: Campaign Manager
  extraction_date: 2026-06-25
  pages_dir: ./pages/
  ---
  ```

- Add one `## <slug>` section per captured page, using the exact same slug as the corresponding `pages/<slug>/` folder.

  **Example (pass):**
  ```markdown
  ## 01-login

  url_or_view: /login
  user_intent: Authenticate to access the application
  domain_focus: Authentication, Session
  ux_focus: Form layout, error states
  aria_snapshot: ./pages/01-login/aria.yaml
  screenshot: ./pages/01-login/screenshot.png
  ```

- Include `url_or_view`, `user_intent`, `aria_snapshot`, and `screenshot` fields in every section — these are the minimum required for downstream consumption.

  **Example (pass):** All four fields present and pointing to existing files under `./pages/<slug>/`.

## DO NOT

- Omit the YAML front matter entirely or leave required fields (`app`, `surface`, `tool`) blank.

  **Example (fail):** File begins with `# Extraction Overview` with no `---` front matter block — abd-story-mapping cannot determine the surface or tool without these fields.

- Have a `## <slug>` section with no `aria_snapshot` or `screenshot` reference.

  **Example (fail):**
  ```markdown
  ## 02-dashboard

  url_or_view: /dashboard
  user_intent: View key metrics
  ```
  Missing `aria_snapshot` and `screenshot` — downstream skills cannot find the capture files.

- Include sections for pages whose `pages/<slug>/` folder does not exist on disk.

  **Example (fail):** Section `## 05-settings` appears in `extraction-overview.md` but `pages/05-settings/` is absent — the index is out of sync with the actual captures and will produce broken links.

**Source:** Engagement convention (abd-context-app-extractor authoring, 2026-06-25).
