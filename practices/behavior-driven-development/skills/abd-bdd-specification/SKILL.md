---
name: abd-bdd-specification
catalog_garden_tier: practice
catalog_garden_family: behavior-driven-development
catalog_garden_order: 42
catalogue_one_liner: >-
  Convert a plain-English behavior scaffold into a locked-down test skeleton — describe/it structure with empty bodies — before a line of logic is written.
description: >-
  Turn an agreed behavior hierarchy into an executable test skeleton — describe/it structure with empty markers and no logic. Use when the behavior hierarchy is agreed and you want to lock test structure before writing any logic.
context-perspective: spec
context-fidelity:
  - level: engineering
    mode: bdd-signature
---
# abd-bdd-specification

## Grill prompts

Read `common/reference/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these traps:

- **Scaffold completeness** — is the scaffold fully approved, or are there describe blocks with open questions? Generating signatures from an unapproved scaffold bakes in the gaps.
- **Framework choice** — is the target framework confirmed? Jest and Mamba have different nesting syntax; choosing the wrong one means the signatures are wrong from the first line.
- **Hierarchy fidelity** — does every level of the scaffold have a code equivalent? Any level collapsed or skipped here will be hard to recover in the test phase without restructuring the file.
- **File target** — does a test file already exist? If yes, signatures go into it (don't create a duplicate); if no, confirm the file name before writing.

---

## Purpose

Convert a plain-English BDD scaffold into an **executable test skeleton** — the describe/it code structure with empty bodies and `// BDD: SIGNATURE` markers. No test logic, no assertions, no mocks. Just the structure.

This gives the team a reviewable code hierarchy before any test logic is committed. Stakeholders confirm the structure still matches the intended behaviors. Developers confirm the nesting matches what the framework needs. The marker makes it easy to scan for unsigned tests later.

---

## When to use

- You have an approved BDD scaffold (`*-behavior.md`) and want to turn it into code structure.
- You are in Phase 1 of a BDD workflow and want to lock hierarchy before adding assertions.
- You want to review that every scaffold behavior maps to a real test slot before writing logic.

**Not this skill when:**
- No scaffold exists yet → use `abd-bdd-behavior` first.
- You want to add test assertions → use `abd-bdd-development`.
- You are writing tests directly from acceptance criteria without a BDD workflow → use `abd-story-acceptance-test`.

---

## Output file

**Deliverables folder:** alongside the feature's `*-behavior.md` file, or in `test/` / `src/` following the project convention.

**File name:** `{domain-name}.test.ts` (Jest/TypeScript) or `{domain-name}_spec.py` (Mamba/Python).

**Resolution:**
1. User names the file explicitly → use that.
2. A `{stem}-behavior.md` exists → derive `{stem}.test.ts` or `{stem}_spec.py` in the same directory.
3. A test file already exists → add signatures to it; do not create a duplicate.

---

## Agent Instructions

Read every file in `rules/` and `reference/` before generating or validating.

### 1. Read context

- **`../../../reference/bdd-concepts.md`** — shared BDD theory: what the hierarchy is, observable behavior, domain practice alignment.
- **`reference/concepts.md`** — signature-phase specifics: what a signature file is, the BDD: SIGNATURE marker, hierarchy preservation, framework syntax.
- **`reference/examples.md`** — worked signature examples in both Jest and Mamba.
- Behavior hierarchy file: look for `{stem}-behavior.md` in the same directory as the target test file.
- Confirm: **Is a test file already there?** If yes, add to it; if no, create it.

### 2. Generate

**Before writing any code:**

1. **Confirm framework** — ask if not stated. Default: Jest/TypeScript. Mamba/Python for Python projects.
2. **Confirm scaffold** — read and confirm the scaffold file path.
3. **Declare the hierarchy** — state the full describe/it nesting structure in chat before writing the file, so the user can confirm it matches the scaffold.

**Build rules:**

- Convert every scaffold line to its framework equivalent:
  - Describe-level line → `describe()` block (Jest) or `with description()` / `with context()` block (Mamba)
  - Behavior line ("should …") → `it()` block (Jest) or `with it()` block (Mamba)
- Preserve **all nesting levels** from the scaffold exactly — do not flatten.
- Every test body contains **only** the signature marker comment:
  - Jest: `// BDD: SIGNATURE`
  - Mamba: `# BDD: SIGNATURE`
- **No mocks, no stubs, no helpers, no assertions** in this phase.
- Process in batches of ~18 describe blocks when the scaffold is large.
- Update the test file directly; do not create a second file alongside it.

**Framework syntax:**

| Construct | Jest (TypeScript) | Mamba (Python) |
|---|---|---|
| Top-level concept | `describe('Concept', () => {` | `with description('Concept'):` |
| Nested state/context | `describe('that has been created', () => {` | `with context('that has been created'):` |
| Behavior | `it('should have initial stats', () => {` | `with it('should have initial stats'):` |
| Signature marker | `// BDD: SIGNATURE` | `# BDD: SIGNATURE` |
| Body close | `});` | *(indentation only)* |

### 3. Validate

Read every file in `rules/` and emit per-rule verdicts:

```
Rule: hierarchy-preservation    ->  PASS
Rule: signature-markers         ->  PASS
Rule: no-implementation         ->  PASS
Rule: framework-syntax          ->  PASS
```

---

## Principles

### 1. Hierarchy Preservation

The signature file is a 1:1 translation of the scaffold. Every describe and every behavior in the scaffold appears in the signature file at the matching nesting depth.

**DO:**
- Translate every line of the scaffold to a code equivalent.
- Keep nesting depth identical between scaffold and signature.
- When the scaffold has 4 levels of nesting, the signature has 4 levels of nesting.

**DON'T:**
- Collapse multiple scaffold levels into one describe block.
- Skip scaffold entries because they seem redundant.
- Add describe blocks not present in the scaffold.

### 2. Signature Markers

Every `it` body contains exactly one comment: `// BDD: SIGNATURE` (Jest) or `# BDD: SIGNATURE` (Mamba). Nothing else. The marker makes unsigned tests scannable and prevents partial implementations slipping through unnoticed.

**DO:**
```typescript
it('should have initial stats assigned', () => {
  // BDD: SIGNATURE
});
```

**DON'T:**
```typescript
// Missing marker — unsigned, invisible to scanners
it('should have initial stats assigned', () => {
});

// Has implementation — wrong phase
it('should have initial stats assigned', () => {
  const character = new Character();
  expect(character.stats).not.toBeNull();
});
```

### 3. No Implementation

The signature phase is about structure, not logic. No assertions, no mocks, no helper calls, no imports of production code.

**DO:**
- Import only the test framework itself if needed (e.g., `describe`, `it` from vitest/jest — only if the project requires explicit imports).

**DON'T:**
- Call production code.
- Import domain classes or utility functions.
- Write `expect()` assertions.
- Set up `beforeEach()` or factory functions.

### 4. Framework Syntax

Use the correct framework syntax for the project throughout. Do not mix Jest and Mamba syntax in the same file.

**Jest/TypeScript:**
```typescript
describe('Character', () => {
  describe('that has been created', () => {
    it('should have initial stats assigned', () => {
      // BDD: SIGNATURE
    });
    it('should have zero starting wounds', () => {
      // BDD: SIGNATURE
    });
  });
});
```

**Mamba/Python:**
```python
with description('Character'):
    with context('that has been created'):
        with it('should have initial stats assigned'):
            # BDD: SIGNATURE
        with it('should have zero starting wounds'):
            # BDD: SIGNATURE
```

---

## Validate

**Goal:** Inspect the generated signature file as a reviewer.

- **Hierarchy preserved** — every scaffold describe and every scaffold behavior maps to a code equivalent at the same nesting depth; nothing added, nothing removed.
- **Signature markers present** — every `it` body contains exactly `// BDD: SIGNATURE` (or `# BDD: SIGNATURE`) and nothing else.
- **No implementation** — no assertions, no mocks, no production-code imports, no helper calls.
- **Framework syntax correct** — consistent use of the confirmed framework throughout; no mixed syntax.
- **Single file** — no duplicate test files created; signatures merged into the existing test file when one already exists.
- **Per-rule verdict** — enumerate every rule in `rules/` and emit `Rule: <name> -> PASS` or `Rule: <name> -> FAIL <reason>`.
