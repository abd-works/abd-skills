---
name: abd-architecture-code
description: >-
  Generate tests and production code from a named architecture spec, using domain and story context to instantiate the spec's patterns. Use when writing code for a story that has a named spec (e.g. specs/mern, specs/hero-vtt).
---
# abd-architecture-code

## Purpose

Generate **executable tests and production code** from a resolved architecture spec plus domain and story context — instantiating that spec's `template/`, `templates/`, `rules/`, and **Testing Architecture**. Orchestrates **`abd-story-acceptance-test`** (RED) and **`abd-clean-code`** (GREEN).

---

## Core concepts

### `<spec-root>`

The architecture spec **directory path resolved in step 0** (user path, story-map node, or project default). **Not hardcoded in this skill.** Every file name, folder, test tier, helper layout, and production layer placement is read from **`<spec-root>`** — `architecture-specification.md`, `rules/`, `templates/tests/`, and `example/tests/` when present.

### Orchestration

| Phase | Skill | Output |
| --- | --- | --- |
| Setup | **`track_task`** | **`progress/`** checklists — one row per spec testing tier and production layer |
| RED | **`abd-story-acceptance-test`** | Acceptance tests per **`<spec-root>`** Testing Architecture |
| GREEN | **`abd-clean-code`** | Production code per **`<spec-root>`** `template/` patterns |

**`<spec-root>` overrides** generic paths in downstream skills (e.g. when `abd-story-acceptance-test` says "follow host project conventions").

### Per-scenario increment

Work **one scenario at a time** within each layer: write test → run RED → write code → run GREEN → fix → next scenario. Do not batch all tests then all code.

**Layer order** — read from **`<spec-root>` Testing Architecture** first. When the spec is silent, default: domain → server → client → E2E (or spec-equivalent tier names).

Continue through deploy and verify until the story works end-to-end in a running solution — not when unit tests alone pass.

The companion **abd-architecture-specification** skill shows the *parameterized template shape*; this skill shows *filled-in output* — see **`reference/example.ts`** for a concrete Recipients module merged from `mern-domain-first-specification`.

---

## Agent Instructions

> **MANDATORY gates — do not generate any artifact until every gate passes. Use the AskQuestion tool when a required input is missing.**

### 0. Required inputs — resolve or ask

Gather **all** of these before reading the spec or writing a line of code.

| Input | Required | Resolution order | If missing |
| --- | --- | --- | --- |
| **Architecture spec** | Yes | User path; story-map node `architecture-spec`; project `docs/architecture/specification/<name>/` | **AskQuestion** — which spec directory? Record as **`<spec-root>`** for all following steps. |
| **Domain context** | Yes | `domain-specification.md` (preferred) → `domain-model.md` | **AskQuestion** — which domain artifact? |
| **Story scope** | Yes | Story specification (preferred) → acceptance criteria on the story | **AskQuestion** — which story / spec / AC file? |
| **UX context** | When UI | `ux-specification.md` + mockup for the increment/flow | **AskQuestion** — which UX artifact? |
| **Story hierarchy** | Yes | `story-graph.json` or story map for epic / sub-epic names | **AskQuestion** — which increment / epic? |
| **Shape reference** | No | **`reference/example.ts`** in this skill — concrete instantiated module (catalog hero); not a template | — |

**Story scope priority**

1. **Story specification** — Given/When/Then scenarios with real domain values (e.g. `*-specification-by-example.md`, `abd-story-specification` output).
2. **Acceptance criteria** — WHEN/THEN/AND/BUT on the story (`abd-story-acceptance-criteria` output).
3. Neither found → **AskQuestion** before proceeding.

**Domain context priority**

1. **`domain-specification.md`** — class model, operations, stereotypes.
2. **`domain-model.md`** — typed domain surface.
3. Neither found → **AskQuestion** before proceeding.

### 1. Read context — `<spec-root>` is law

**MANDATORY — read from the resolved `<spec-root>` before any generation:**

| Artifact | Path inside `<spec-root>` | Governs |
| --- | --- | --- |
| Architecture doc | `architecture-specification.md` (or `archiecture-specification.md`) | Mechanisms, participants, **Testing Architecture**, layer order |
| Rules | `rules/*.md` | DO / DO NOT for every generated file |
| Working example | `template/` | Canonical runnable code — match structure and naming exactly |
| Scaffolds | `templates/` | Parameterized files to instantiate (including `templates/tests/` when present) |
| Examples | `example/` when present | Worked domain + story + test mapping |

The resolved spec's **Testing Architecture** section, **`templates/tests/`**, and **`example/tests/`** (when present) dictate how **every test tier** is created. Do not invent folders, file names, test tiers, or layer order not derivable from **`<spec-root>`**.

Also read (outside `<spec-root>`):

- **Domain artifact** resolved in step 0 — class names, operations, field names, invariants.
- **Story artifact** resolved in step 0 — scenarios, acceptance criteria, actors.
- **UX artifact** when the story has screens — controls, test ids, navigation, states (client + E2E tests assert against these).
- **`reference/example.ts`** in this skill — optional concrete output shape (catalog hero); the companion **abd-architecture-specification** skill shows the parameterized template.
- **Existing project tests** — use only as a secondary reference **after** confirming they match `<spec-root>` rules; repo drift is not authority.

### 1b. Test layout inventory — mandatory gate before RED

**Do not write any scenario test or production code until this gate passes.**

All steps read from **`<spec-root>`** — never from agent memory of another project or stack.

1. Read **Testing Architecture** in `<spec-root>/architecture-specification.md` (or typo filename) — extract: story-artifact → test-artifact mapping, tier names, helper layout, layer order, slug rules.
2. Read test-related rules under `<spec-root>/rules/` (e.g. `test-story-driven.md`, `use-thorough-e2e-tests.md`, or spec-equivalents) — extract mandatory tier count and naming patterns.
3. List every **lowest-level sub-epic** in scope from `story-graph.json` / story map.
4. For each sub-epic, **derive** the full tier file set and helper set by substituting epic/sub-epic slugs into `<spec-root>/templates/tests/` paths (or mirror `<spec-root>/example/tests/` when templates are absent).
5. Create empty scaffolds on disk from those templates **before** the first RED scenario.
6. Publish the inventory in chat — one row per sub-epic, columns = each tier and helper path **as defined by this spec** (not a fixed column set from this skill).
7. If the project already has tests, compare structure to the inventory; reconcile drift before adding scenarios.

**Named spec overrides downstream defaults:** when **`abd-story-acceptance-test`** says "follow host project conventions", **`<spec-root>` Testing Architecture** wins.

See **`rules/scaffold-test-layout-before-scenarios.md`**.

### 1c. Layer progress checklist — mandatory (`track_task`)

**Do not start step 3 until this gate passes.** Persist session progress with **`track_task`** — not in chat alone.

1. **Resolve workspace** — **`skill-config.json` → `workspace.active_skill_workspace`**, or **`python skill-helpers/scripts/get_workspace.py`** from the agilebydesign-skills repo root; if unset, ask the user to set workspace first.
2. **Create progress tree** — **`<active_skill_workspace>/abd-architecture-code/progress/`** (do not overwrite existing checklists unless the user asks to reset).
3. **Derive layers from `<spec-root>`** — same source as step **1b**: **Testing Architecture** tier names, production layer mapping, and layer order. Default only when the spec is silent: domain → server → client → E2E.
4. **Write `process-checklist.md`** — one `- [ ]` line per workflow phase:

   ```markdown
   - [ ] 0 — Resolve inputs (<spec-root>, domain, story, UX, hierarchy)
   - [ ] 1 — Read context; derive test + production layer inventory
   - [ ] 1b — Scaffold test layout on disk
   - [ ] 1c — Layer progress checklist created
   - [ ] 3 — Generate tests and production (all spec layers)
   - [ ] 4 — Deploy and verify end-to-end
   - [ ] 4a — All spec-mandated test suites executed (full run, all pass)
   - [ ] 5 — Validate rules and scanners
   ```

5. **Write `<scope-slug>-layers-checklist.md`** — **`<scope-slug>`** = increment, epic, or story scope label from step **0**. For **each lowest-level sub-epic** in scope, list **every testing tier and production layer** from the spec **in order**. **Three checkboxes per layer** (tests require both scenario runs and a full tier execution):

   ```markdown
   ## <sub-epic-slug>

   ### <LayerName> (tests — <tier> per <spec-root>)
   - [ ] Scenarios — each RED then GREEN (executed, not merely written) — `<test-tier-path-from-1b-inventory>`
   - [ ] Tier suite — full test run executed, all pass — `<same-path>` via `<spec test command>`

   ### <LayerName> (production — <spec-root> layer)
   - [ ] Minimum code green for those scenarios — `<production-path-pattern-from-spec>`
   ```

   After all sub-epics, add **## Test execution — all tiers in scope** — one `- [ ]` line per **distinct test runner or tier** **`<spec-root>/rules/`** mandates (domain, server, client, E2E, etc.), with the command and scope path. Tick only after a **full run** passes — not a single scenario file in isolation when the spec requires the whole tier or suite.

   ```markdown
   ## Test execution — all tiers in scope

   - [ ] Execute `<tier-or-runner-name>` — `<command>` — all tests in scope pass
   ```

   Repeat for each layer the spec names (names, paths, and commands come from **`<spec-root>`**, not from this example).

6. **Tick step 0 and 1b items** — flip matching lines in **`process-checklist.md`** to `- [x]` for work already completed before this step.
7. **Publish summary in chat** — table: sub-epic × layer × scenario-run × tier-executed × production checkbox (paths and commands from inventory).

**During step 3** — after the **per-layer gate** passes (every scenario **executed** RED then GREEN, **full tier suite executed** for that layer, **and** production green), flip **all three** lines for that sub-epic × layer to `- [x]` before opening the next layer. **During step 4** — run and tick **Test execution — all tiers in scope** and **`- [ ] 4a`** only when every listed suite has been **executed** with all tests passing. **During step 4–5** — tick remaining **`process-checklist.md`** lines when each phase completes.

**Resume** — read **`progress/`** first; first unchecked `- [ ]` in the layers file is next unless the user names a step.

See **`rules/track-layer-completion-checklist.md`**.

### 2. Downstream skills — mandatory, not optional

| Phase | Skill | When |
| --- | --- | --- |
| **RED — tests** | **`abd-story-acceptance-test`** | Always, for every layer's tests |
| **GREEN — production** | **`abd-clean-code`** | Always, for every production file |

**`abd-story-acceptance-test`**

- **MUST** read and follow that skill's `SKILL.md`, `rules/`, `reference/`, and matching language template.
- **Input:** story specification scenarios when available; acceptance criteria when not.
- **Plus (overrides generic output paths):** **`<spec-root>` Testing Architecture** — tier names, helper layout, test doubles, story-hierarchy → file mapping (read from the resolved spec, not assumed).
- **File unit** = whatever the resolved spec maps to the lowest story artifact (often sub-epic → file; hero-vtt and others differ — read the table in `<spec-root>`).
- **Helpers** = whatever count and naming `<spec-root>` defines per file unit — shared across stories in that unit, not one helper file per story.
- Complete step **1b** (test layout inventory) before declaring file / class / method hierarchy.

**`abd-clean-code`**

- **MUST** read and follow that skill's `SKILL.md` and `rules/` when writing production code.
- **Input:** failing tests from step 3; domain artifact for names and behaviour.
- **Plus:** the named spec's `template/` patterns — constructor injection, layer placement, mechanism boundaries.

If either skill package is not available in the workspace, **AskQuestion** — do not improvise test or production structure.

### 3. Generate — layer order, one scenario at a time

Work **one layer at a time**, and within each layer work **one scenario at a time**. The unit of progress is a single scenario (one `it` / `test` method) — not a whole story file, not a whole layer.

**Default layer order** — read from **`<spec-root>` Testing Architecture** first; use this table only when the spec does not name an order:

| Order | Production layer | Test layer (typical) |
| --- | --- | --- |
| **1** | Domain / shared | Domain unit tests |
| **2** | Server / API / persistence adapter | Server / HTTP adapter tests |
| **3** | Client / presentation | Client / UI adapter tests |
| **4** | — (full stack) | E2E / browser tests |

Tier file names, extensions, and helper suffixes come from **`<spec-root>/templates/tests/`** and **`example/tests/`** — not from examples in this skill prose.

**Per-scenario loop (mandatory — repeat for every scenario in story order)**

```
  ┌─────────────────────────────────────────────────────────────┐
  │  1. WRITE TEST   one scenario in the current tier's file    │
  │                  extend sub-epic helpers if needed           │
  │  2. RUN          confirm RED — fails for the right reason   │
  │  3. WRITE CODE   minimum production code to satisfy it      │
  │  4. RUN          confirm GREEN — this scenario passes        │
  │  5. FIX          if fail → fix code or test; re-run until OK  │
  │  6. NEXT TEST    only then add the next scenario              │
  └─────────────────────────────────────────────────────────────┘
```

1. **Write test** — run **`abd-story-acceptance-test`** for **one scenario** in the current tier's existing sub-epic file; add one `it` / `test` method; extend that sub-epic's tier helper — do not create new test files named after stories.
2. **Run (RED)** — execute the suite; confirm this scenario **fails for the right reason** (missing behaviour, not a typo or wiring mistake).
3. **Write code** — run **`abd-clean-code`**; add the **minimum** production code that scenario requires — no ahead-of-scope methods.
4. **Run (GREEN)** — execute again; this scenario **must pass** before any new test is written.
5. **Fix** — if it still fails, fix production code or test setup; re-run until green. Do not skip to the next scenario while this one is red.
6. **Next test** — pick the next scenario in story order; return to step 1.

When every scenario in the current layer is green, move to the next layer and restart the per-scenario loop there.

**Per-layer gate (mandatory)**

- Do not start the next layer until **every scenario in the current tier has been executed** RED then GREEN, the **full tier test suite has been executed** and passes, **and** production for that layer is green.
- After the gate passes, **check off** that layer's scenario-run, tier-executed, and production lines in **`<scope-slug>-layers-checklist.md`** (step **1c**) before opening the next spec layer.
- Do not write multiple scenario tests upfront and implement code in bulk — that violates the increment rule.

**DO NOT**

- Start RED without completing steps **1b** (inventory + scaffolds) and **1c** (**`track_task`** layer checklist on disk).
- Name test files after **stories** or **scenarios** when **`<spec-root>`** maps a higher story artifact (e.g. sub-epic) → file.
- Ship a story-hierarchy unit with only some tiers when **`<spec-root>/rules/`** mandates all tiers for that unit.
- Batch-write all test methods for a story, then all production code.
- Write production code before the scenario's test method exists.
- Move to the next scenario while the current one is still failing.
- Skip a layer or reorder layers contrary to the spec's Testing Architecture.
- Mark a layer done in chat without updating **`progress/`** checklists.
- Start the next spec layer while any scenario-run, tier-executed, or production checkbox for the current layer is still `- [ ]`.
- Mark tests done without **executing** them — writing test methods or seeing one scenario pass is not enough; run the full tier and every spec-mandated suite.
- Implement production files not required by the current scenario — but **test tier files** for each sub-epic must exist upfront even if scenarios are filled incrementally.
- Use live/production seam types in unit or adapter tests when the spec designates fakes or mocks.

### 4. Deploy and verify — working solution required

The per-scenario loop continues through integration. After each layer's scenarios are green, and again when all layers are done:

1. **Install** dependencies (`npm install`, `pip install`, or equivalent per spec) — fix resolution errors immediately.
2. **Execute** every test tier **`<spec-root>/rules/`** and scripts require (unit, adapter, E2E, etc.) — **run the full suite**, not a single file in isolation when the spec mandates the whole tier; fix regressions before proceeding. Passing one runner when the spec mandates another is **not** done. Tick **Test execution — all tiers in scope** and **`- [ ] 4a`** in **`progress/`** only after every listed command has been run and all tests pass.
3. **Start** composition roots (dev server, app host) per spec — verify boot without errors.
4. **Smoke the flow** — walk the story's happy path in the running app (or E2E suite) to confirm the deployed solution actually works, not just that unit tests pass in isolation.
5. **Fix** any integration, wiring, or runtime failures; re-run affected scenarios; repeat until the story works end-to-end.

Do not proceed to validation until install succeeds, all tiers are green, the app runs, and the story flow works in the deployed environment.

When step **4** completes, tick **`- [ ] 4 — Deploy and verify end-to-end`** and **`- [ ] 4a — All spec-mandated test suites executed (full run, all pass)`** in **`process-checklist.md`**. Every line under **Test execution — all tiers in scope** must be `- [x]`.

### 5. Validate — per-rule verdict required

Re-read every file in the spec's `rules/` and this skill's `rules/`. Run spec scanners when present:

```bash
python foundational/skill-helpers/skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root <spec-root> \
  --workspace <path-to-generated-code>
```

For each rule emit:

```
Rule: <rule-filename>  ->  PASS
Rule: <rule-filename>  ->  FAIL  <offending line or reason>
```

Fix every FAIL before declaring done.

When step **5** completes, tick **`- [ ] 5 — Validate rules and scanners`** and **`- [ ] 3 — Generate tests and production (all spec layers)`** in **`process-checklist.md`**. Every line in **`<scope-slug>-layers-checklist.md`** must be `- [x]`.

---

## Validate

**Goal:** Inspect generated artifacts as a reviewer against the named spec and downstream skills.

- **Inputs gated** — **`<spec-root>`**, domain artifact, story scope, story hierarchy, and UX (when UI) resolved or explicitly chosen via AskQuestion; no silent assumptions.
- **Test layout scaffolded** — step 1b inventory derived from **`<spec-root>`**; every story-hierarchy unit has all spec-mandated tier files + helpers before scenarios were added.
- **Layer progress tracked** — step 1c **`track_task`** checklists exist; every spec testing tier and production layer has an explicit `- [x]` when done; **every test tier and spec-mandated suite was executed** (full run, all pass); **`progress/`** matches actual layer gates (not chat-only claims).
- **Skills invoked** — `abd-story-acceptance-test` for tests; `abd-clean-code` for production; both rule sets followed with **`<spec-root>`** overriding generic test paths.
- **Spec is law** — file layout, mechanism participants, test tiers, and helpers match **`<spec-root>`** `architecture-specification.md`, `template/`, and `templates/`.
- **Layer order** — domain → server → client → E2E (or spec-equivalent order); each layer green before the next.
- **One scenario at a time** — test → code → fix → pass → next test; no batched test-then-code dumps.
- **Tests first** — RED before GREEN for every scenario; no production code without a failing test first.
- **Story scope** — code and tests implement only what the current scenario requires.
- **Deployed and working** — install succeeds; full suite green; app boots; story flow verified in the running solution.
- **Rules pass** — every spec rule and skill rule has an explicit PASS verdict.
