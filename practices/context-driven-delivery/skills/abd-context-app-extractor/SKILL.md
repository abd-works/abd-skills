---
name: abd-context-app-extractor
description: >-
  Explore a live application and record structured per-page context ready for
  story mapping, UX mockup, and domain modelling. Use when you have a working
  application and need to extract structured context from it.
context-fidelity:
  - level: context
---

# Abd-Context-App-Extractor

## Purpose

Teams and agents that need to understand an unfamiliar application often lack a shared, structured record of what the app actually does — its screens, its data, its interactions. This skill closes that gap by driving the application with the right automation tool for its surface type (browser, desktop, or API), capturing a structured ARIA or UIA tree and screenshot for each significant view, and writing everything into a folder layout that downstream skills can consume directly. The result is a comparable, repeatable baseline that any practitioner or agent can build from — without manual annotation or screen-by-screen guesswork.

---

## When to use this skill

Load this skill when **any** of the following apply:

- You have a working application and want to understand what it actually does — its screens, its data, its interactions — without reading source code or relying on memory.
- You need a structured, comparable baseline before beginning story mapping, UX modelling, or domain analysis.
- You have been asked to reverse-engineer or document an unfamiliar application without prior documentation.
- Existing context is stale after a significant release and the team needs a fresh capture to reason from.

---

## Output file

**Where to write the deliverables — resolution order:**

1. The path the user explicitly specified.
2. `docs/extracted-context/app-extraction/` in the target repo, alongside its source code.
3. The workspace root if neither applies.

**Canonical layout:**

```
docs/extracted-context/
  app-extraction/
    extraction-overview.md     ← master log: one ## section per captured page
    pages/                     ← one folder per captured view
      <slug>/
        screenshot.png
        aria.yaml
  api-extraction/              ← microservices /services surface only
    openapi.yaml
    har/<endpoint>.har
```

See **`reference/output-layout.md`** for field definitions and the `extraction-overview.md` front-matter schema.

---

## Agent Instructions

> **MANDATORY — read every file in `rules/` and every file in `reference/` before authoring any artifact. Do not rely on memory or the SKILL body alone.**

### 1. Read context (MANDATORY before starting — read in full, do not skim)

Read the following files in full before doing anything else:

- **`../../reference/tool-selection.md`** — surface detection and tool matrix (shared family reference)
- **`reference/output-layout.md`** — folder structure, front-matter schema, slug convention, downstream consumers
- **`reference/surface-details.md`** — deep-dive setup and capabilities for web, desktop, and microservices

Then determine the surface and open the matching capture-format reference:

- Web (Playwright) → **`reference/wai-aria-format.md`** — WAI-ARIA spec summary, `aria.yaml` output format, spec URL
- Windows desktop (pywinauto) → **`reference/uia-tree-format.md`** — UIA spec summary, `aria.yaml` output format, spec URL

Do not proceed to step 2 until all required files have been read completely.

### 2. Generate

Read every file in **`rules/`** in full. Treat each DO / DO NOT as a shape contract — not a suggestion:

- **`rules/page-slug-naming.md`**
- **`rules/aria-capture-method.md`**
- **`rules/extraction-overview-shape.md`**
- **`rules/tool-hierarchy.md`**

Follow these steps in order:

1. **Identify the surface.** Inspect the target repo for indicators. See `reference/tool-selection.md`.
2. **Copy the matching template** from `templates/web/`, `templates/desktop/`, or `templates/microservices/` into the target repo.
3. **Seed the PAGES / ENDPOINTS list** with the obvious entry points (login, home, primary list views).
4. **Run Phase 0 scout** — a thin, fast pass that captures 10–20 representative pages or endpoints.
5. **Present `extraction-overview.md` to the user** and wait for explicit approval before proceeding to deeper capture.
6. **Iterate** — add missing views to the script and re-run only the new captures.
7. **Hand off** — confirm that `extraction-overview.md` and `pages/*/` are present and consumable by the downstream skill.

### 3. Validate (MANDATORY — per-rule verdict required)

Re-read every file in **`rules/`**. For **each rule**, emit a verdict:

```
Rule: <rule-filename>  ->  PASS
Rule: <rule-filename>  ->  FAIL  <offending line or reason>
```

No rule may be silently skipped. Fix every FAIL before handing off.

### 4. Reasonableness review (MANDATORY — AI judgement, no code required)

After extraction completes and all mechanical guards pass, **read every `pages/<slug>/aria.yaml`** and make an AI judgement on each page. This replaces the need to write exhaustive code checks for every possible failure mode.

For each page ask:

- **Does this ARIA represent a real, rendered UI screen for the stated `user_intent`?**
- Are there interactive elements (buttons, inputs, links, headings) consistent with what the intent describes?
- Is there any sign this is the **wrong page** — e.g. a redirect landing, sign-in page when an authenticated page was expected, 404, maintenance screen?
- Is the content **suspiciously sparse** — a single heading, one button, or a known loading/skeleton pattern — suggesting the render was not complete?

Emit a verdict per page:

```
04-my-dashboard     PASS — dashboard shows usage widget, billing summary, nav links
05-my-billing       PASS — billing section has balance, invoice list, payment method card
20-onboarding-number WARN — single input visible; may be mid-redirect; re-check with longer wait
02-sign-up-catalog  FAIL — blank; navigator sent to /my instead of /sign-up (subscriber redirect)
```

**FAIL or WARN** → do not write that page into the final `extraction-overview.md`. Fix the navigation or timing and re-run only the affected pages. A WARN is acceptable if the page is genuinely sparse by design (e.g. a success/done screen) — note the reason.

---

## Validate

**Goal:** Inspect what was extracted — read the artifacts as a reviewer, not a second authoring pass.

- **Extraction overview is present and complete** — `extraction-overview.md` exists, has YAML front matter with `app`, `surface`, and `tool` fields, and has one `## <slug>` section per captured page with all required fields.
- **Slugs are meaningful** — every page folder under `pages/` uses a numbered slug (`01-login`, `03b-campaign-modal`), not a generic `step-003` or `page-1`.
- **Each page folder is complete** — `screenshot.png` and `aria.yaml` are both present under every `pages/<slug>/` folder.
- **Tool match** — the tool used matches the surface type; pixel-only tools (pyautogui) are not used as the primary capture method when semantic tools (pywinauto, Playwright) are available.
- **Per-rule verdict** — re-read every `rules/*.md` file and emit a named PASS/FAIL for each.
- **Reasonableness review passed** — every page in `extraction-overview.md` received a PASS verdict in step 4. No FAIL pages are present in the overview. WARN pages are annotated with an explanation.
