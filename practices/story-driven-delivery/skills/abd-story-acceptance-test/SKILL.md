---
name: abd-story-acceptance-test
catalog_garden_tier: practice
catalog_garden_order: 50
catalogue_one_liner: >-
  Tests first, then code: executable acceptance tests from scenarios, AC, or notes (RED-GREEN-REFACTOR).
description: >-
  Writes executable acceptance tests (RED-GREEN-REFACTOR) from scenarios, acceptance criteria,
  stories, or rough descriptions. Orchestrator pattern: Given-When-Then test methods call helper
  functions; one class per story, one method per scenario. Use when writing acceptance tests,
  turning behavioral context into test code, or driving implementation with tests.
---
# abd-story-acceptance-test

## Purpose

**Write tests first. Write code to pass them.**

This skill creates **executable test files** — in whatever language and framework the project uses — from whatever behavioral context is available: specification scenarios, acceptance criteria, stories, notes, or a rough description of what the system should do. The output is real test code that runs, fails, and drives what gets built.

The workflow is **test-driven**: write a test that expresses the expected behavior, run it to confirm it fails (RED), then implement production code until the test passes (GREEN). Each test is a precise, runnable statement of what the system must do — test methods show the Given-When-Then flow and helper functions do the work.

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

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what ATDD is, test organization, orchestrator pattern, TDD cycle, domain language.
- **`reference/examples.md`** — shape notes + what to notice (same domain as `abd-story-specification` examples).
- **`templates/acceptance-tests-example.py`** — filled Python/pytest example (order + discount outline).

### 2. Generate

Read every file in **`rules/`**; author to those rules.

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

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-story-acceptance-test \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read test files as reviewers.

- **Test structure declared** — file/class/method hierarchy stated before writing code; file named after lowest-level sub-epic, class after story.
- **Orchestrator pattern** — test methods under 20 lines; helpers named with GWT vocabulary; no duplicated helper variants.
- **RED before GREEN** — tests written before production code; assertions are specific enough to fail for the right reasons.
- **Domain language** — class names, method names, and helper names use domain vocabulary from stories/AC.
- **Coverage** — happy path, failure path, and edge cases covered.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
