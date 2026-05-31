---
catalog_garden_tier: practice
catalog_garden_order: 30
name: abd-architecture-reference
description: >-
  Assign or produce runnable implementation from architecture reference —
  reuse existing reference sections and code when already present; create
  only missing mechanisms or files. Use when you have or need an
  architecture-reference.md and want code that matches it, or when a team
  needs a concrete runnable example of a mechanism end-to-end.
---
# abd-architecture-reference

## Purpose

`abd-architecture-template` produces (or assigns) reference sections that specify *how* a mechanism is structured. This skill **assigns** existing reference and code when already present, or **creates** missing reference sections and implementation files.

Two paths remain: **project mode** (real reference + stories) and **hello-world mode** (calibration only when no project reference exists).

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` and `reference/concepts.md` before starting.**

### 1. Resolve — assign or create

Follow the **assign before create** workflow in `reference/concepts.md`:

### 2. Choose implementation mode

| Mode | When to use |
|---|---|
| **Project mode** | A project reference exists (assigned or just created). Implement from File Structure and Walkthrough. |
| **Hello-world mode** | No project reference and no in-scope ticket — calibration only. |

Do **not** use hello-world mode when the project already has `docs/architecture/architecture-reference.md`.

### 3. Read template output

Use assigned or newly created reference sections as the contract — File Structure, Participants, Flow, Walkthrough.

### 4. Hello-world scenario (mode 2 only)

   - **System:** Simple Calculator — a three-layer CLI app (Presentation → Domain → Infrastructure) in Python.
   - **Story:** `As a user, when I enter two numbers and an operator, the calculator returns the correct result or a clear error message.`
   - **Mechanism:** Error handling — invalid operator and divide-by-zero raised at domain, caught once at presentation boundary.
   - **Files:** `calculator.py` (Domain), `cli.py` (Presentation), `tests/test_calculator.py`, `tests/test_cli.py`.
   - Use `templates/hello-world/` as the reference implementation.

5. **Generate missing files only.** Every new file must be syntactically correct and immediately executable. No stubs or placeholder bodies.

6. **One mechanism per run** unless the ticket scope explicitly lists multiple.

---

## Core concepts

See **`reference/concepts.md`** for assign-before-create workflow, reference-as-specification, and project vs hello-world mode.

---

## Validate

- **Assignment table** present — every mechanism in scope has reference and code disposition (assign or create).
- Every **newly created** file is syntactically correct (target language).
- Running the test suite produces passing results for new code with no errors.
- The domain layer raises typed exceptions; the presentation layer has exactly one catch boundary.
- No layer swallows an error silently or uses a bare `except Exception`.
- In hello-world mode the generated files match the scenario spec.
- In project mode every **missing** file listed in the reference's File Structure is generated; assigned paths are left unchanged.

---
