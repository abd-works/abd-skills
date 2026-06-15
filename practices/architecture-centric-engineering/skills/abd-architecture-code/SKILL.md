---
name: abd-architecture-code
description: >-
  Generate tests and production code from a named architecture spec, using domain and story context to instantiate the spec's patterns. Use when writing code for a story that has a named spec (e.g. specs/mern, specs/hero-vtt).
---
# abd-architecture-code

## Purpose

Given a **named architecture spec**, **domain context**, and **story scope**, generate executable tests then production code that instantiates the spec's `template/`, `templates/`, `rules/`, and **Testing Architecture** section. This skill orchestrates **`abd-story-acceptance-test`** (RED) and **`abd-clean-code`** (GREEN) inside the spec's file layout and layer order.

**One scenario at a time: write test → write code → fix → pass → next test.** Work in small increments within each layer — never batch all tests then all code. Domain layer first, server second, client third, E2E last — matching the spec's testing architecture when tier names differ. Continue until the solution is installed, deployed, and working end-to-end.

---

## Agent Instructions

> **MANDATORY gates — do not generate any artifact until every gate passes. Use the AskQuestion tool when a required input is missing.**

### 0. Required inputs — resolve or ask

Gather **all** of these before reading the spec or writing a line of code.

| Input | Required | Resolution order | If missing |
| --- | --- | --- | --- |
| **Architecture spec** | Yes | User path; story-map node `architecture-spec`; project `docs/architecture/` | **AskQuestion** — which spec directory? |
| **Domain context** | Yes | `domain-specification.md` (preferred) → `domain-model.md` | **AskQuestion** — which domain artifact? |
| **Story scope** | Yes | Story specification (preferred) → acceptance criteria on the story | **AskQuestion** — which story / spec / AC file? |

**Story scope priority**

1. **Story specification** — Given/When/Then scenarios with real domain values (e.g. `*-specification-by-example.md`, `abd-story-specification` output).
2. **Acceptance criteria** — WHEN/THEN/AND/BUT on the story (`abd-story-acceptance-criteria` output).
3. Neither found → **AskQuestion** before proceeding.

**Domain context priority**

1. **`domain-specification.md`** — class model, operations, stereotypes.
2. **`domain-model.md`** — typed domain surface.
3. Neither found → **AskQuestion** before proceeding.

### 1. Read context — spec is law

**MANDATORY — read before any generation:**

| Artifact | Path inside spec | Governs |
| --- | --- | --- |
| Architecture doc | `architecture-specification.md` (or `archiecture-specification.md`) | Mechanisms, participants, **Testing Architecture**, layer order |
| Rules | `rules/*.md` | DO / DO NOT for every generated file |
| Working example | `template/` | Canonical runnable code — match structure and naming exactly |
| Scaffolds | `templates/` | Parameterized files to instantiate for the story |
| Examples | `example/` when present | Worked domain + story mapping |

The spec's **example**, **template**, and **Testing Architecture** section dictate how **every layer** — including all test tiers — is created. Do not invent folders, file names, test tiers, or layer order not derivable from the spec.

Also read:

- **Domain artifact** resolved in step 0 — class names, operations, field names, invariants.
- **Story artifact** resolved in step 0 — scenarios, acceptance criteria, actors.

### 2. Downstream skills — mandatory, not optional

| Phase | Skill | When |
| --- | --- | --- |
| **RED — tests** | **`abd-story-acceptance-test`** | Always, for every layer's tests |
| **GREEN — production** | **`abd-clean-code`** | Always, for every production file |

**`abd-story-acceptance-test`**

- **MUST** read and follow that skill's `SKILL.md`, `rules/`, `reference/`, and matching language template.
- **Input:** story specification scenarios when available; acceptance criteria when not.
- **Plus:** the named spec's **Testing Architecture** — tier names, helper layout, test doubles, folder mapping from story hierarchy.
- Declare file / class / method hierarchy per that skill before writing code.

**`abd-clean-code`**

- **MUST** read and follow that skill's `SKILL.md` and `rules/` when writing production code.
- **Input:** failing tests from step 3; domain artifact for names and behaviour.
- **Plus:** the named spec's `template/` patterns — constructor injection, layer placement, mechanism boundaries.

If either skill package is not available in the workspace, **AskQuestion** — do not improvise test or production structure.

### 3. Generate — layer order, one scenario at a time

Work **one layer at a time**, and within each layer work **one scenario at a time**. The unit of progress is a single scenario (one `it` / `test` method) — not a whole story file, not a whole layer.

**Default layer order** (use unless the spec's Testing Architecture names tiers differently — then map to the spec's order):

| Order | Production layer | Test layer (typical) |
| --- | --- | --- |
| **1** | Domain / shared | Domain unit tests |
| **2** | Server / API / persistence adapter | Server / HTTP adapter tests |
| **3** | Client / presentation | Client / UI adapter tests |
| **4** | — (full stack) | E2E / browser tests |

Examples of spec-specific tier names: `shared/` + `*_server.test.ts` + `*_client.test.tsx` + `*_e2e.spec.ts` (MERN); `Module.HeroVirtualTabletop` + `Module.UnitTest` (hero-vtt). **Follow the spec's Testing Architecture table and `template/tests/` layout**, not a generic test folder.

**Per-scenario loop (mandatory — repeat for every scenario in story order)**

```
  ┌─────────────────────────────────────────────────────────────┐
  │  1. WRITE TEST   one scenario method + helpers it needs     │
  │  2. RUN          confirm RED — fails for the right reason   │
  │  3. WRITE CODE   minimum production code to satisfy it      │
  │  4. RUN          confirm GREEN — this scenario passes        │
  │  5. FIX          if fail → fix code or test; re-run until OK  │
  │  6. NEXT TEST    only then add the next scenario              │
  └─────────────────────────────────────────────────────────────┘
```

1. **Write test** — run **`abd-story-acceptance-test`** for **one scenario** in the current layer; add one `it` / `test` method and only the helpers that scenario needs.
2. **Run (RED)** — execute the suite; confirm this scenario **fails for the right reason** (missing behaviour, not a typo or wiring mistake).
3. **Write code** — run **`abd-clean-code`**; add the **minimum** production code that scenario requires — no ahead-of-scope methods.
4. **Run (GREEN)** — execute again; this scenario **must pass** before any new test is written.
5. **Fix** — if it still fails, fix production code or test setup; re-run until green. Do not skip to the next scenario while this one is red.
6. **Next test** — pick the next scenario in story order; return to step 1.

When every scenario in the current layer is green, move to the next layer and restart the per-scenario loop there.

**Per-layer gate (mandatory)**

- Do not start the next layer until **all scenarios** in the current layer pass.
- Do not write multiple scenario tests upfront and implement code in bulk — that violates the increment rule.

**DO NOT**

- Batch-write all test methods for a story, then all production code.
- Write production code before the scenario's test method exists.
- Move to the next scenario while the current one is still failing.
- Skip a layer or reorder layers contrary to the spec's Testing Architecture.
- Implement methods, files, or test tiers not required by the current scenario or spec templates.
- Use live/production seam types in unit or adapter tests when the spec designates fakes or mocks.

### 4. Deploy and verify — working solution required

The per-scenario loop continues through integration. After each layer's scenarios are green, and again when all layers are done:

1. **Install** dependencies (`npm install`, `pip install`, or equivalent per spec) — fix resolution errors immediately.
2. **Execute** the full test suite per spec scripts (`npm test`, `scripts/test.sh`, etc.) — fix any regressions before proceeding.
3. **Start** composition roots (dev server, app host) per spec — verify boot without errors.
4. **Smoke the flow** — walk the story's happy path in the running app (or E2E suite) to confirm the deployed solution actually works, not just that unit tests pass in isolation.
5. **Fix** any integration, wiring, or runtime failures; re-run affected scenarios; repeat until the story works end-to-end.

Do not proceed to validation until install succeeds, all tiers are green, the app runs, and the story flow works in the deployed environment.

### 5. Validate — per-rule verdict required

Re-read every file in the spec's `rules/` and this skill's `rules/`. Run spec scanners when present:

```bash
python foundational/skill-helpers/skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root <path-to-named-spec> \
  --workspace <path-to-generated-code>
```

For each rule emit:

```
Rule: <rule-filename>  ->  PASS
Rule: <rule-filename>  ->  FAIL  <offending line or reason>
```

Fix every FAIL before declaring done.

---

## Validate

**Goal:** Inspect generated artifacts as a reviewer against the named spec and downstream skills.

- **Inputs gated** — architecture spec, domain artifact, and story scope resolved or explicitly chosen via AskQuestion; no silent assumptions.
- **Skills invoked** — `abd-story-acceptance-test` for tests; `abd-clean-code` for production; both rule sets followed.
- **Spec is law** — file layout, mechanism participants, test tiers, and helpers match `architecture-specification.md`, `template/`, and `templates/`.
- **Layer order** — domain → server → client → E2E (or spec-equivalent order); each layer green before the next.
- **One scenario at a time** — test → code → fix → pass → next test; no batched test-then-code dumps.
- **Tests first** — RED before GREEN for every scenario; no production code without a failing test first.
- **Story scope** — code and tests implement only what the current scenario requires.
- **Deployed and working** — install succeeds; full suite green; app boots; story flow verified in the running solution.
- **Rules pass** — every spec rule and skill rule has an explicit PASS verdict.
