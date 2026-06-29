---
name: abd-story-acceptance-test
catalog_garden_tier: practice
catalog_garden_order: 50
catalogue_one_liner: >-
  Prove each behavior works before writing production code — tests drive what gets built.
description: >-
  Generate executable acceptance tests from scenarios using the orchestrator pattern. Use when turning behavioral specs into test code or driving implementation test-first.
context-perspective: stories
context-fidelity:
  - level: engineering
    mode: acceptance-tests
---
# abd-story-acceptance-test

## Purpose

Generate executable test files from specification scenarios, acceptance criteria, stories, or rough descriptions using the project's language and framework. Follow RED-GREEN-REFACTOR: write a failing test that expresses expected behavior, implement production code until it passes — one class per story, one method per scenario, Given-When-Then helpers doing the work.

---

## Output file

**Where to write the test files (`<tests-folder>` resolution):**

1. **The path the user told you to use.** If the user names a file or folder, use exactly that.
2. **Where the project already keeps tests.** Look at the workspace; if a `tests/`, `test/`, `spec/`, or language-conventional test folder exists, put new test files in the appropriate subdirectory there.
3. **The workspace root.** If neither applies, write to the workspace root or a sensible language-default location.

Do **not** invent a predetermined folder name. Tests follow the host project's conventions.

**File names:** Use the target language's test-discovery convention (`test_<scenario>.py`, `<Scenario>Test.java`, `*.test.ts`, etc.).

---

## Agent Instructions

Follow `common/skill-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what ATDD is, test organization, orchestrator pattern, TDD cycle, domain language.
- **`reference/examples.md`** — shape notes + what to notice (same domain as `abd-story-specification` examples).
- **`templates/acceptance-tests-example.py`** — filled Python/pytest example (order + discount outline).
- **`reference/diagnose.md`** — when and how to flip into diagnose mode when tests keep failing.

### 2. Generate

**Before writing any code:**
0. **Verify test structure first (Priority 1)** — Trace the story hierarchy, declare file / class / method before writing any code. See **Test organization** in `reference/concepts.md`.
1. **Confirm language and framework** — If not stated, ask. Defaults: pytest (Python), `node:test` (JS/TS), JUnit 5 (Java).
2. **Pick the matching template** from `templates/` — `acceptance-tests.py`, `.js`, or `.java`. Emit code only; omit the `## Instructions` block.

**Build steps:**
3. One file per area, one class per story, one method per scenario. Name helpers with GWT language (`given_*`, `when_*`, `then_*`) matching step text verbatim. Parameterize helpers to prevent sprawl. Extract shared helpers to `tests/<epic_name>/<epic_name>_helper.py` when reused across files.

**Template table:**

| Template | What to produce |
| --- | --- |
| `templates/acceptance-tests.py` | Python/pytest scaffold following orchestrator pattern |
| `templates/acceptance-tests-example.py` | Filled Python/pytest example (see `abd-story-specification` examples) |
| `templates/acceptance-tests.js` | JS/TS test file following orchestrator pattern |
| `templates/acceptance-tests.java` | Java/JUnit5 test file following orchestrator pattern |

### 3. Diagnose — flip immediately when tests keep failing

**If a test fails after 2 or more consecutive fix attempts — stop. You are spinning.**

Do not add a third fix. Flip immediately into diagnose mode:

1. Read **`reference/diagnose.md`** — it maps the full six-phase diagnose discipline onto acceptance test failures.
2. Build or confirm a fast, deterministic feedback loop (the failing test itself — but verify it is clean).
3. Reproduce the failure on demand before touching any code.
4. Write 3–5 ranked, falsifiable hypotheses. Show them before testing any.
5. Instrument one variable at a time; tag every debug log `[DEBUG-<4char>]`.
6. Fix the root cause. Watch the test go GREEN. Remove all instrumentation.

**Do not proceed to the next story until the spinning test is resolved.**

### 4. Validate

Run scanners and emit per-rule verdicts — see `common/skill-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect what was built — read test files as reviewers.

- **Test structure declared** — file/class/method hierarchy stated before writing code; file named after lowest-level sub-epic, class after story.
- **Orchestrator pattern** — test methods under 20 lines; helpers named with GWT vocabulary; no duplicated helper variants.
- **RED before GREEN** — tests written before production code; assertions are specific enough to fail for the right reasons.
- **Domain language** — class names, method names, and helper names use domain vocabulary from stories/AC.
- **Coverage** — happy path, failure path, and edge cases covered.
- **Example data alignment** — every test value traces to a spec Examples table; all values are imported from a shared fixtures/constants file, not typed inline; stubs are configured to receive and return values that match the spec examples exactly.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
