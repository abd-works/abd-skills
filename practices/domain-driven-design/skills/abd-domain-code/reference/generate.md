# Generate — abd-domain-code

Follow every file in `rules/`; fill templates exactly.

## Inputs

Use whatever domain artifacts exist — richer inputs produce better output. A **domain specification**, **domain model / CRC**, **domain terms list**, **domain glossary**, stories, acceptance criteria, or a plain description — extract what you need as you go.

If **architecture specification** (`architecture-specification.md`) exists, read that to understand where the domain layer lives and how to code and test it. If none exists, infer conventions from the context, language, and any existing code.

## 1. Read domain context

Use whatever is available in priority order: domain specification → domain model / CRC → domain terms → stories and AC → plain description.

Extract classes, operation signatures, invariants, and relationships from whichever source is richest.

If an architecture reference exists, read the **domain layer** section only — pick up base classes, exception conventions, and value-object patterns. If none exists, infer sensible conventions from the language and any existing code.

## 2. Write tests first — follow abd-story-acceptance-test

Read and follow **`abd-story-acceptance-test/SKILL.md`** in full.

Scope the tests to domain behavior only — follow the epic / sub-epic / story / scenario convention from that skill (one file per sub epic, one class per story, one method per scenario).

- Test invariants, operation outcomes, and state transitions.
- No mocks of infrastructure — use plain in-memory fakes or direct instantiation. Validate using rules and scan as per normal use.

## 3. Write production code — follow abd-clean-code

Read and follow **`abd-clean-code/SKILL.md`** in full.

Constraints:

- Every class and operation must trace to something in the domain context.
- Use names verbatim from the domain glossary and specification.
- Raise domain exceptions (not framework errors) for invariant violations.
- No imports from infrastructure, persistence, or web layers.

## 4. Validate

- All tests pass (GREEN).
- No production class imports outside the domain layer.
- Every invariant named in the domain context is enforced in code.
- Run abd-clean-code scanners if available.
