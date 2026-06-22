---
name: abd-domain-code
catalog_garden_tier: practice
catalog_garden_order: 5
catalogue_one_liner: >-
  Turn domain knowledge into tested, running code — no infrastructure, pure business logic.
description: >-
  Generate tested pure-domain code — classes, operations, invariants — with no infrastructure coupling. Use when domain concepts are ready and need test-driven implementation.
context-perspective: domain
context-fidelity:
  - level: engineering
    mode: domain-tdd
---

# abd-domain-code

## Purpose

Turn domain knowledge into tested, running code — pure business logic with no infrastructure coupling — so the domain model is proven executable before integration begins.

---

## Inputs

Use whatever domain artifacts exist — richer inputs produce better output. A **domain specification** , **domain model  , CRC** , **domain terms list**,  **domain glossary** or stories, acceptance criteria, or a plain description and extract what you need as you go.

If **architecture specification** (`architecture-specification.md`exist; read that to understand where domain-layer exists / how to code and test it. If none exists, again infer conventions from the context, language and any existing code.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these common input traps:

- **Invariant gaps** — which business rules feel "obvious" but haven't been stated — and what breaks if the code doesn't enforce them?
- **Behavior ownership** — when two domain objects could reasonably own the same operation, which one actually does — and what's the consequence of getting it wrong?
- **State transition coverage** — which state changes are legal and which aren't — and are we confident we've mapped every transition, including the ones that should be rejected?
- **Domain vs. infrastructure bleed** — where is the boundary between pure domain logic and infrastructure concerns — and what concepts are we tempted to leak across that line?
- **Edge interactions** — what happens at the limits — zero items, maximum quantities, duplicate entries — where domain rules interact in ways nobody explicitly stated?

---

## Agent Instructions

### 1. Read domain context

Use whatever is available in priority order: domain specification → domain model / CRC → domain terms → stories and AC → plain description.
Extract classes, operation signatures, invariants, and relationships from whichever source is richest.

If an architecture reference exists, read the **domain layer** section only — pick up base classes,
exception conventions, and value-object patterns. If none exists, infer sensible conventions from
the language and any existing code.

### 2. Write tests first — follow abd-story-acceptance-test

Read and follow **`abd-story-acceptance-test/SKILL.md`** in full.

Scope the tests to domain behavior only — follow the epic / sub-epic / story / scenario
convention from that skill (one file per sub epic, one class per story, one method per scenario).
- Test invariants, operation outcomes, and state transitions.
- No mocks of infrastructure — use plain in-memory fakes or direct instantiation. validate using rules and scan as per normal use.

### 3. Write production code — follow abd-clean-code

Read and follow **`abd-clean-code/SKILL.md`** in full.

Constraints:
- Every class and operation must trace to something in the domain context.
- Use names verbatim from the domain glossary and specification.
- Raise domain exceptions (not framework errors) for invariant violations.
- No imports from infrastructure, persistence, or web layers.

### 4. Validate

- All tests pass (GREEN).
- No production class imports outside the domain layer.
- Every invariant named in the domain context is enforced in code.
- Run abd-clean-code scanners if available.
