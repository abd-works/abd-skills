---
name: abd-architecture-code
description: >-
  Generate tests and production code from a named architecture spec, using domain and story context to instantiate the spec's patterns. Use when writing code for a story that has a named spec (e.g. specs/mern, specs/hero-vtt).
---
# abd-architecture-code

## Purpose

Given a named architecture spec and story scope with domain context, generate acceptance tests then production code that follows the spec's instructions, templates, file layout, and rules. Use when writing code for a story that has a named spec, adding a feature module to an existing codebase, or reviewing generated code for architecture compliance.

The companion **abd-architecture-specification** skill shows the *parameterized template shape*; this skill shows *filled-in output* — see **`reference/example.ts`** for a concrete Recipients module merged from `mern-domain-first-specification`.

---

## Agent Instructions

> **MANDATORY — read the named spec's `architecture-specification.md`, every file in its `rules/`, and its `template/` before generating any artifact.**

### 1. Read context

Gather these inputs before writing anything:

| Input | Where it comes from |
| --- | --- |
| **Spec** | User-supplied path to spec — `architecture-specification.md` within it |
| **Spec rules** | `rules/*.md` inside the spec — DO / DO NOT norms every generated file must pass |
| **Spec template** | `template/` inside the spec — canonical working code; match its structure and naming |
| **Spec templates** | `templates/` inside the spec — parameterized scaffold; instantiate for the story |
| **Shape reference** | **`reference/example.ts`** in this skill — concrete instantiated module (catalog hero); not a template |
| **Story scope** | User-supplied stories, acceptance criteria, and/or scenarios |
| **Domain context** | User-supplied domain class names, field names, key operations |

If the spec path or domain context is missing, ask before generating.

### 2. Ask — what to generate

Ask the user: tests only, code only, or both?

### 3. Generate — tests first

#### 3a. Acceptance tests

Follow **`abd-story-acceptance-test`** for test structure (one class per story, one method per scenario, orchestrator pattern, GWT helpers). Also follow the spec's testing architecture — tiers, test doubles, and naming conventions as shown in the spec's `template/`.

Produce tests before production code. Do not move to 3b until the test structure is correct.

#### 3b. Production code

Instantiate the spec's `templates/` scaffold for the story's domain names. Follow the spec's file layout exactly:

- Name every file after the pattern shown in `template/` (parameterized names from `templates/`).
- Wire interfaces through constructor injection as the spec requires.
- Implement only the behaviour the story's acceptance criteria describe — no extra methods.

### 4. Install and run — green bar required

After generating tests and code:

1. **Install** all dependencies — run `npm install` (or equivalent) at the project root. Fix any protocol or resolution errors (e.g. `workspace:*` in npm projects).
2. **Execute** the test suite — run `npm test`. If tests fail to load (missing packages, wrong extensions, bad imports), fix the infrastructure and re-run.
3. **Fix** assertion failures revealed by running — wrong API paths, response shape mismatches, missing test setup. Iterate until the suite is green.
4. **Start** the dev server if the spec includes composition roots — verify it boots without errors.

Do not proceed to validation until the test bar is green.

### 5. Validate — per-rule verdict required

Re-read every file in the spec's `rules/`. For each rule emit:

```
Rule: <rule-filename>  ->  PASS
Rule: <rule-filename>  ->  FAIL  <offending line or reason>
```

Fix every FAIL before declaring done.

---

## Validate

**Goal:** Inspect what was generated — read the artifacts as a reviewer against the spec.

- **Runnable** — `npm install` succeeds, `npm test` executes all suites, dev server starts without errors.
- **Green bar** — all tests pass; no skipped suites due to missing deps or config.
- **Spec alignment** — every generated file matches the mechanism, participants, and file layout in `architecture-specification.md`.
- **Tests first** — acceptance tests exist and are structurally correct before production code is reviewed.
- **Rules pass** — every rule in the spec's `rules/` has an explicit PASS verdict; no silent skips.
- **Template fidelity** — generated structure matches the spec's `template/` — same folder layout, naming conventions, test tier separation.
- **Story scope** — generated code implements only what the story's acceptance criteria describe; no speculative methods.
- **Constructor injection** — every class that crosses a mechanism boundary receives its dependencies via constructor; no static calls, no `new` of concrete seam types inside domain classes.
