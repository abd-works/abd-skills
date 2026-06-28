---
name: abd-context-app-sandbox
description: >-
  Identify external service dependencies in a codebase, stub each one at its
  earliest interface boundary, stand up the application in isolation, and
  verify every screen is reachable via a smoke test — ready for abd-context-app-extractor
  or BDD test authoring.
context-fidelity:
  - level: context
---

# Abd-Stub-External-Dependencies

## Purpose

Applications that depend on third-party APIs, SaaS platforms, or external microservices often cannot start in a local or CI environment without live credentials or network access. This skill fixes that by scanning the codebase for external dependencies, distinguishing them from in-repo and peer-repo services that already participate in integration or e2e tests, and placing a stub at the earliest calling point for each true external. The result is an application that starts, navigates to every screen, and leaves a comparable smoke-test record — without touching real external systems or mocking protocol internals.

The stub inventory produced by this skill records every hardcoded value introduced by each stub so that downstream BDD steps (When / And / Then) can reference them explicitly and reviewers can see exactly what assumptions the stubs encode.

---

## When to use this skill

Load this skill when **any** of the following apply:

- The application cannot start or reach its login screen without live third-party API keys, OAuth flows, or external service endpoints.
- You are preparing the application for `abd-context-app-extractor` and need to stand it up in an isolated environment first.
- A CI pipeline fails because external services are unreachable and no stubs exist.
- You have added a new external dependency and need to make its stub explicit and inventoried before running integration or BDD tests.

---

## Output file

**Where to write the deliverables — resolution order:**

1. The path the user explicitly specified.
2. `docs/stubs/` in the target repo, alongside existing test infrastructure.
3. The workspace root if neither applies.

**Canonical layout:**

```
docs/stubs/
  stub-inventory.md     ← classification table, one stub row per external dependency,
                           smoke-test results, and hardcoded value notice
```

---

## Agent Instructions

> **MANDATORY — read every file in `rules/` and every file in `reference/` before authoring any artifact. Do not rely on memory or the SKILL body alone.**

### 1. Read context (MANDATORY before starting — read in full, do not skim)

Read the following files in full before doing anything else:

- **`reference/what-counts-as-external.md`** — definition of external dependency and the peer-repo e2e exclusion
- **`reference/stub-patterns.md`** — boundary identification heuristics, stub shape examples for common service types
- **`reference/complex-stub-strategy.md`** — **MANDATORY** — when stubbing is complex (5+ externals, domain-shaped returns, auth-gated screens, feature-flag-gated flows), do Discovery and Exploration through stories and domain BEFORE writing any stub. Read this file to determine whether to apply the complex strategy.
- **`../../reference/tool-selection.md`** — shared surface-to-tool matrix; use this to choose the smoke-test automation tool after stubs are in place

Do not proceed to step 2 until all required reference files have been read completely.

### 1b. Apply the complex stub strategy if triggered

After reading `reference/complex-stub-strategy.md`, check the trigger condition:

> **Trigger:** Five or more distinct external services, OR any stub must return a nested domain object with more than three fields.

If triggered — **STOP. Do not proceed to Generate (step 2) yet.**

The session checklist **must** include all three of the following discrete steps in
order. They cannot be collapsed, skipped, or combined into a single checkbox:

1. **Story mapping — minimal stub-focus pass** → `docs/stubs/story-map.md`
   Map each user activity to: which external service is called, at which step, and what
   minimum response shape it must return for the activity to advance.

2. **Acceptance criteria — minimal stub-focus pass** → `docs/stubs/acceptance-criteria.md`
   For each activity, write 2–4 plain-language acceptance criteria that name the stub
   value, the observable outcome, and the screen it is visible on.

3. **Domain language — minimal stub-focus pass** → `docs/stubs/domain-glossary.md`
   For each domain term that appears in an external service response, list the minimum
   fields the UI reads, their types, example values, and which component reads them.

Only after all three documents are written, proceed to step 2 (Generate) using the
story map, acceptance criteria, and domain glossary to author stubs with realistic,
domain-shaped return values.

If not triggered — proceed directly to step 2.

### 2. Generate

Read every file in **`rules/`** in full. Treat each DO / DO NOT as a shape contract — not a suggestion:

- **`rules/dependency-is-external-if.md`**
- **`rules/stub-at-boundary-not-internals.md`**
- **`rules/stub-inventory-format.md`**
- **`rules/smoke-test-reachability.md`**

Follow these steps in order:

1. **Enumerate candidates.** List every third-party call site, environment variable that holds an external URL, SDK initialisation, and OAuth client. Collect file path, line number, and service name for each.
2. **Classify each candidate.** Apply `rules/dependency-is-external-if.md`. Mark each as **external** (needs a stub) or **in-scope** (same-repo service or peer-repo e2e participant — skip).
3. **Stub each external at its earliest boundary.** Apply `rules/stub-at-boundary-not-internals.md`. Place the stub at the outermost interface: an HTTP client adapter, an SDK factory, or a module export — not inside an OAuth token exchange or a deep protocol method.
4. **Start the application.** Run the normal dev or test start command. Confirm the process reaches a healthy state (HTTP 200 on the health or root endpoint, the desktop window opens, or the API returns a valid response).
5. **Run a smoke test.** Choose the automation tool from **`../../reference/tool-selection.md`** based on the application surface. Navigate to every significant screen. Record each screen slug and its reachability result.
6. **Complete the stub inventory.** Fill `docs/stubs/stub-inventory.md` from `templates/stub-inventory.md`. For each stub record: service name, boundary point file and symbol, every hardcoded value, and which BDD step phrases (When / And / Then) reference that value.
7. **Notify the AI of hardcoded stub values.** After the inventory is complete, prompt the working AI assistant with the full inventory table so it records these values as known assumptions for future BDD authoring. See the notice at the end of this section.

#### Hardcoded value notice (paste after inventory is complete)

> The following stubs introduce hardcoded values that downstream BDD tests will reference. Record each one as a known assumption so that When / And / Then steps cite the stub inventory rather than inventing new literals that diverge from what the stubs actually encode.

Paste the full `## Hardcoded Value Notice` table from `stub-inventory.md` into that prompt.

### 3. Validate (MANDATORY — per-rule verdict required)

Re-read every file in **`rules/`**. For **each rule**, emit a verdict:

```
Rule: <rule-filename>  ->  PASS
Rule: <rule-filename>  ->  FAIL  <offending line or reason>
```

No rule may be silently skipped. Fix every FAIL before handing off.

---

## Validate

**Goal:** Inspect what was produced — read the artifacts as a reviewer, not a second authoring pass.

- **All external dependencies classified** — every third-party call site, SDK initialisation, and external-URL env-var appears in `stub-inventory.md` either as `external — stubbed` or `in-scope — skipped` with an explicit reason.
- **Stubs are at the outermost boundary** — no stub intercepts OAuth token flows, deep SDK internals, or protocol-layer methods; each stub replaces the top-level adapter, factory, or module export.
- **Application starts cleanly** — the dev or test start command exits successfully; no uncaught errors reference a missing external service.
- **Every screen is reachable** — the smoke test navigated to every significant screen and recorded a PASS; no screen is absent from the inventory without an explicit note.
- **Stub inventory is complete** — `stub-inventory.md` has one row per stub with service, boundary point, hardcoded values, and BDD step references; the Hardcoded Value Notice table is populated.
- **AI notified** — the hardcoded value notice was pasted to the working AI session after inventory was complete.
- **Per-rule verdict** — re-read every `rules/*.md` file and emit a named PASS/FAIL for each.
