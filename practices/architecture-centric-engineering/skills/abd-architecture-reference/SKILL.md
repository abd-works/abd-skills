---
catalog_garden_tier: practice
catalog_garden_order: 30
name: abd-architecture-reference
description: >-
  Read abd-architecture-template output and produce runnable code files — the
  actual implementation of one architecture mechanism — either from the current
  project's stories or from a built-in hello-world scenario.
---
# abd-architecture-reference

## Purpose

`abd-architecture-template` produces a reference document that specifies *how* a mechanism is structured, what files exist, how types collaborate, and how the flow runs. This skill takes that reference document as its blueprint and produces the **actual runnable code files** that realise the mechanism — domain classes, entry points, and tests — ready to execute.

Two paths are available: use the real project's architecture reference and one in-scope story to generate real implementation files, or use the built-in "Simple Calculator" scenario so any team can see a complete, working three-layer example with zero prior setup.

## When to use

- You have an `architecture-reference.md` (from `abd-architecture-template`) and want the code that implements it.
- A team needs a concrete runnable example to understand what one mechanism looks like end-to-end before building the real thing.
- You want a quick smoke-test: generate the hello-world code, run it with `pytest`, confirm the mechanism works as specified.

---

## Agent Instructions

1. **Choose the implementation mode.** Ask — or infer from context — which of the two modes to use:

   | Mode | When to use |
   |---|---|
   | **Project mode** | A real `architecture-reference.md` is in scope. Generate the files listed in its File Structure block, implementing the walkthrough example. |
   | **Hello-world mode** | No project context is available, or the team wants a standalone runnable example. Use the built-in Simple Calculator scenario described below. |

2. **Read `abd-architecture-template` first.** Open `skills/architecture-centric-engineering/abd-architecture-template/SKILL.md`. The reference document it describes is the contract this skill implements — use its File Structure, Participants, Flow, and Walkthrough sections as the specification for every file you generate.

3. **Hello-world scenario (mode 2).** When no project context exists, generate the files in `templates/hello-world/` using this pre-configured scope:

   - **System:** Simple Calculator — a three-layer CLI app (Presentation → Domain → Infrastructure) written in Python.
   - **Story:** `As a user, when I enter two numbers and an operator, the calculator returns the correct result or a clear error message.`
   - **Mechanism implemented:** Error handling — invalid operator and divide-by-zero are raised at the domain layer, caught once at the presentation boundary, and shown to the user without a traceback.
   - **Files to generate:**
     - `calculator.py` — Domain layer: `Calculator` class + `CalculationError`
     - `cli.py` — Presentation layer: `main()` with the single `try/except`
     - `tests/test_calculator.py` — domain unit tests
     - `tests/test_cli.py` — presentation integration tests
   - Use `templates/hello-world/` as the reference implementation for expected content, naming, and style.

4. **Generate complete, runnable files.** Every file must be syntactically correct and immediately executable. Do not generate stubs, placeholders, or `pass` bodies.

5. **One mechanism per run.** Implement the mechanism covered by the reference document. Do not add extra mechanisms unless the user explicitly asks.

---

## Core concepts

### Reference document as specification

The output of `abd-architecture-template` is the specification for this skill's code. The File Structure block is the list of files to create. The Participants diagram is the type graph to implement. The Flow diagram is the call sequence. The Walkthrough is the acceptance scenario the code must pass.

### Hello-world as calibration

The Simple Calculator scenario is intentionally trivial so the *mechanism* is what the reader learns from, not the domain. A team that understands how error handling works across three Python layers can apply the same pattern to any mechanism in any architecture.

### Project mode as fast-start

In project mode the reference document is already written. This skill reads it, extracts the File Structure and Walkthrough, and generates the matching implementation. The reference document is not modified.

---

## Validate

- Every generated file is syntactically correct Python (or the target language).
- Running `pytest` on the generated test files produces a passing test suite with no errors.
- The domain layer raises typed exceptions; the presentation layer has exactly one `try/except` for each domain exception type.
- No layer swallows an error silently or uses a bare `except Exception`.
- In hello-world mode the generated files match the scenario spec above (three layers, divide-by-zero, unknown operator, stdout output).
- In project mode every file listed in the reference's File Structure block is generated.

---

<!-- execute_rules:bundle_rules:begin -->
<!-- execute_rules:bundle_rules:end -->
