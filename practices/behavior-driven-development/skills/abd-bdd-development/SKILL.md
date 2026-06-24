---
name: abd-bdd-development
catalog_garden_tier: practice
catalog_garden_family: behavior-driven-development
catalog_garden_order: 43
catalogue_one_liner: >-
  Replace BDD signature markers with real test logic and then implement the minimal production code to make them pass.
description: >-
  Complete the RED-GREEN cycle: implement test bodies then write minimal production code until every test passes. Use when the test structure is in place and you are ready to implement and drive production code from failing tests.
context-perspective: engineering
context-fidelity:
  - level: engineering
    mode: bdd-development
---
# abd-bdd-development

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these traps:

- **Signature completeness** — are all `// BDD: SIGNATURE` markers present and accounted for? Implementing half a signature file means the RED pass is partial and the structure looks done when it is not.
- **Test isolation** — does each test arrange its own state, or is state leaking between tests through shared objects? Shared objects between tests cause brittle tests that fail in order-dependent ways.
- **Observable behavior vs. internals** — are assertions checking what the system does (output, state change visible through the public API), or what is inside the implementation (private fields, internal method calls)? Testing internals means the test breaks when refactoring, not when the behavior breaks.
- **Mock boundaries** — are mocks placed at the module boundaries your architecture defines, or are domain classes being mocked? Mocking domain logic means you are not testing the domain.
- **Code minimalism** — is the production code adding features the tests do not require? Any code without a failing test behind it is untested risk.

---

## Purpose

Complete a BDD test file by replacing `// BDD: SIGNATURE` markers with Arrange-Act-Assert test bodies, then implement production code until every test passes. This is the engineering phase of BDD — the work is real, runnable, and RED before it goes GREEN.

The discipline is tight: tests observe **behavior through the public API**; assertions check what the system produces or changes; production code does only what the failing tests demand.

---

## When to use

- You have a test file with `// BDD: SIGNATURE` markers and want to implement the tests.
- You are in the RED-GREEN-REFACTOR cycle and need to write production code driven by failing tests.
- You want to implement a module with test coverage that matches the BDD hierarchy.

**Not this skill when:**
- Signatures are not yet written → use `abd-bdd-specification` first.
- You want to write new tests from scratch without an existing BDD hierarchy → use `abd-story-acceptance-test`.
- You are generating acceptance tests for E2E → use `abd-story-acceptance-test` with the Playwright template (E2E uses the spec approach by default; see `reference/concepts.md` — Testing layer selection).

---

## Output files

- **Test file:** `{domain-name}.test.ts` (Jest/TypeScript) or `{domain-name}_spec.py` (Mamba/Python) — existing file with signatures replaced.
- **Helper file (when needed):** `{domain-name}-helper.ts` / `{domain-name}_helper.py` — shared factory functions and `beforeEach` setup extracted when used by more than one test.
- **Production code:** `{domain-name}.ts` / `{domain-name}.py` — minimal module implementing the behavior under test.

**Resolution:** production code goes in the layer's conventional module location. If the project has a `src/features/{name}/` structure, the module goes there. Follow the project's established convention.

---

## Agent Instructions

Read every file in `rules/` and `reference/` before generating or validating.

### 1. Read context

- **`../../../reference/bdd-concepts.md`** — shared BDD theory: what the hierarchy is, observable behavior, domain practice alignment.
- **`reference/concepts.md`** — development-phase specifics: RED-GREEN-REFACTOR, Arrange-Act-Assert, mock boundaries, code minimalism.
- **`reference/examples.md`** — worked test-to-code examples in both Jest and Mamba.
- **`reference/diagnose.md`** — flip to diagnose mode when a test keeps failing after 2 fix attempts.
- The existing signature file — scan for all `// BDD: SIGNATURE` markers to know the full scope.

### 2. Implement tests

**Before writing any test body:**

1. **Confirm framework** — Jest or Mamba; inherit from the signature file.
2. **Scan signatures** — list all `it` blocks still containing `// BDD: SIGNATURE`; report the count to the user.
3. **Identify shared setup** — look for `beforeEach` opportunities (e.g., instantiating the same object in multiple tests). Extract to `beforeEach` or a factory function before implementing.

**Build rules:**

- Replace `// BDD: SIGNATURE` with an **Arrange-Act-Assert** body:
  ```
  // Arrange — set up preconditions and inputs
  // Act — call the production code under test
  // Assert — check the observable outcome
  ```
- **One assertion per behavior** — each `it` tests one observable outcome.
- Call production code directly — let tests fail naturally if the code does not exist yet (that is the RED phase).
- Mock **only at module boundaries** defined by the architecture — external services, infrastructure adapters, framework internals. Do not mock domain classes you are testing.
- Extract shared setup to `beforeEach` when the same arrangement appears in three or more sibling tests.
- Extract shared helpers to `{domain-name}-helper.ts` when they are reused across describe blocks or files.

**Template table:**

| Template | What to produce |
|---|---|
| `templates/tests.ts` | Jest/TypeScript test implementation |
| `templates/tests.py` | Mamba/Python test implementation |

### 3. Implement production code

After all test bodies are written and the tests are RED:

1. **Write the minimal code** that makes each failing test GREEN — nothing more.
2. Start with functions or simple objects before introducing classes.
3. Let the tests drive when a class or abstraction is needed — they will tell you by failing in a way that a function cannot satisfy.
4. Follow `abd-clean-code` rules for production modules.

**Build rules:**

- Do not add properties, parameters, or behaviors that no test demands.
- Do not add configuration or options not tested.
- Do not add error handling paths with no failing test.
- When a test requires a class, create one; when a function suffices, use a function.

**Template table:**

| Template | What to produce |
|---|---|
| `templates/code.ts` | Minimal TypeScript production module |
| `templates/code.py` | Minimal Python production module |

### 4. Diagnose — flip immediately when tests keep failing

If a test fails after **2 or more consecutive fix attempts** — stop. You are spinning.

Read `reference/diagnose.md` immediately. Do not attempt a third fix without a hypothesis. Build a hypothesis list, instrument one variable at a time, and fix the root cause.

**Do not move to the next test until the spinning test is GREEN.**

### 5. Validate

Read every rule in `rules/` and emit per-rule verdicts:

```
Rule: observable-behavior       ->  PASS
Rule: context-sharing           ->  PASS
Rule: layer-isolation           ->  PASS
Rule: code-minimalism           ->  PASS
Rule: oo-api-design             ->  PASS
```

---

## Principles

### 1. Observable Behavior

Tests prove what the system does, not how it does it. Assertions check outputs, state changes, and effects visible through the public API — not private fields or internal method invocations.

**DO:**
- Assert on the value returned: `expect(result.email).toBe('test@example.com')`
- Assert on state change visible through the API: `expect(character.wounds).toBe(3)`
- Assert on the effect produced: `expect(repository.save).toHaveBeenCalledWith(expectedEntity)`

**DON'T:**
- Access private fields: `expect(service._cache).not.toBeNull()`
- Assert on internal method calls: `expect(service._validate).toHaveBeenCalled()`
- Spy on the object under test: `jest.spyOn(character, 'applyDamage')`

### 2. Context Sharing

Tests within a describe block often need the same object in the same initial state. Extract that setup to `beforeEach` rather than duplicating it in every `it` body. Factory functions create test data without hard-coding the same literal values everywhere.

**DO:**
```typescript
describe('Character that has been created', () => {
  let character: Character;

  beforeEach(() => {
    character = new Character({ name: 'Test', stats: defaultStats() });
  });

  it('should have initial stats assigned', () => {
    expect(character.stats.strength).toBe(10);
  });
});
```

**DON'T:**
```typescript
it('should have initial stats assigned', () => {
  const character = new Character({ name: 'Test', stats: defaultStats() }); // duplicate
  expect(character.stats.strength).toBe(10);
});

it('should have zero starting wounds', () => {
  const character = new Character({ name: 'Test', stats: defaultStats() }); // duplicate again
  expect(character.wounds).toBe(0);
});
```

### 3. Layer Isolation

Each test targets one layer of the architecture. Tests mock at the boundaries that layer uses to talk to the next layer — not inside the layer being tested.

**DO:**
- Mock the external service adapter when testing the service layer.
- Mock the repository when testing business logic.
- Test the domain class without mocks (it has no external boundary).

**DON'T:**
- Mock the domain class you are testing (`jest.mock('../Character')` when the test IS for Character).
- Cross layer boundaries silently (e.g., unit test that also writes to the real database).
- Use `jest.fn()` for internal domain methods.

### 4. Code Minimalism

Production code grows only when tests demand it. Any code without a failing test behind it is untested and out of scope.

**DO:**
- Write the simplest code that makes the failing test pass.
- Prefer a function over a class until a test demands class behavior (state, inheritance, interface).
- Return only what the test expects.

**DON'T:**
- Add properties not tested: `this.createdAt = new Date()` when no test checks `createdAt`.
- Add overloads, configuration options, or alternative paths not covered by a test.
- Pre-emptively design for future requirements.

```typescript
// DON'T: over-engineered
class User {
  constructor(
    public email: string,
    public role: string = 'user',
    public permissions: string[] = [],   // not tested
    public preferences: Record<string, unknown> = {} // not tested
  ) {}
}

// DO: minimal — only what the tests demand
function createUser(data: { email: string; name: string }) {
  if (!data.email.includes('@')) throw new Error('Invalid email');
  return { email: data.email, name: data.name, isActive: true };
}
```

### 5. OO API Design

When tests drive a class-based API, the class should manage its own state, initialize completely on construction, expose state through properties, and use the closest domain object for each operation.

**DO:**
- Initialize fully on construction — no `load()` call needed after `new`.
- Use properties for state access; methods for actions that change state.
- Place operations on the object that owns the concept in the domain model.
- Use simple, direct verb names: `build()`, `save()`, `validate()`.

**DON'T:**
- Require setup calls after construction: `agent.loadConfiguration()`.
- Name methods with verbose action descriptions: `executesBuilderMethod()`.
- Place operations on a parent object when they belong to a child domain object.
- Pass internal state as parameters when the object should manage it.

---

## Validate

**Goal:** Inspect the generated test file and production code as a reviewer.

- **No signatures remain** — zero `// BDD: SIGNATURE` markers in the final file.
- **RED before GREEN** — tests were written before production code; each assertion is specific enough to fail for the right reason.
- **Observable behavior** — assertions check public outputs or public state changes; no private field access.
- **Context shared correctly** — `beforeEach` used for shared object setup; factory functions for test data; no copy-pasted arrangement code.
- **Layer isolation correct** — mocks at architecture boundaries only; no mocking of the object under test.
- **Code minimalism** — production code has no methods, properties, or behaviors without a corresponding passing test.
- **Per-rule verdict** — enumerate every rule in `rules/` and emit `Rule: <name> -> PASS` or `Rule: <name> -> FAIL <reason>`.
