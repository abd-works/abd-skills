---
name: abd-bdd-behavior
catalog_garden_tier: practice
catalog_garden_family: behavior-driven-development
catalog_garden_order: 41
catalogue_one_liner: >-
  Translate domain practice artifacts into a plain-English behavior hierarchy mapped to sub-epics, so stakeholders can read it and agents can test against it.
description: >-
  Discover and name the behaviors a system should exhibit, producing a plain-English hierarchy anchored to sub-epics that stakeholders can review. Use when you want to agree on what the system should do before writing any test code.
context-perspective: exploration
context-fidelity:
  - level: engineering
    mode: bdd-scaffold
---
# abd-bdd-behavior

## Purpose

Translate domain practice artifacts into a **plain-English behavior hierarchy** — the first artifact in a BDD workflow. The scaffold names every domain concept, state, and behavior in natural language before any code is written, anchored to the sub-epics in the story map. This gives stakeholders a readable picture of what the system will do and gives the team a validated starting point for test structure.

The hierarchy is not code. It is not Gherkin. It is an indented outline where each sub-epic becomes a top-level `describe` heading, domain concepts from the domain language and domain model nest beneath it, and every leaf is a `should` statement.

---

## Output file

**Deliverables folder:** `docs/bdd/` — see [`common/folder-conventions.md`](../../../../common/folder-conventions.md). If this project uses non-standard paths, check `cdd-context-index.md` at the workspace root first.

**File name:** `<feature>-behavior.md`. Use the feature or sub-epic name as the stem.

---

## When to use

- Starting a new feature with non-trivial domain behavior
- Domain language, domain model, or acceptance criteria exist and you want to derive test structure from them, not invent it
- Stakeholders need to review what the system will do before code is written
- You want a validated behavior list before writing signatures or tests

**Not this skill when:**
- The behavior is simple and obvious (no discovery needed)
- A hierarchy already exists and is still valid
- You are running BDD on a well-understood refactor with existing tests

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these traps:

- **Missing sub-epic anchor** — which sub-epics from the story map are in scope? Without a named sub-epic, the top-level describe blocks have no anchor and the hierarchy floats free of the delivery structure.
- **Domain vocabulary gap** — are the concept names from the domain language and domain model, or are they being invented here? Names invented in the behavior file that don't exist in domain artifacts will mismatch the production code and every downstream test.
- **Observable vs. implementation** — do the leaf `should` lines describe what the system does from a user's point of view, or what implementation method gets called? "should call calculateDiscount" is an implementation detail; "should apply a percentage discount to eligible items" is observable behavior.
- **Bundle risk** — does a single `should` line actually describe multiple distinct behaviors? Each leaf must imply one verifiable outcome; if it implies two or more, it needs splitting.

---

## Agent Instructions

Read every file in `rules/` and `reference/` before generating or validating.

### 1. Read context

- **`../../../reference/bdd-concepts.md`** — shared BDD theory: what the hierarchy is, observable behavior, domain practice alignment.
- **`reference/concepts.md`** — behavior-phase specifics: the scaffold format, how to read domain artifacts, naming rules.
- **`reference/examples.md`** — worked example of a correct and incorrect behavior hierarchy.

### 2. Generate

**Before writing any hierarchy:**

1. **Confirm sub-epics in scope** — list the sub-epics from the story map that this hierarchy will cover.
2. **Read domain artifacts** — extract concepts, states, and transitions from `domain-language.md` and `domain-model.md`; extract observable behaviors from `acceptance-criteria.md`.
3. **Declare the structure** — state the top-level describe blocks and their nesting in chat before writing the file so the user can confirm it matches the story map and domain language.

**Build rules:**

| Step | What to do |
|------|-----------|
| **Name top-level describes** | One per sub-epic in scope. Use the sub-epic's exact name from the story map — no abbreviations. |
| **Name nested describes** | Domain concepts, states, or operation groups from the domain language and domain model that belong to this sub-epic. Use names verbatim. |
| **Write behavior lines** | Each leaf starts with `should`. Describes one observable behavior. Draws from acceptance criteria and domain model behaviors. No code syntax. |
| **Validate with a stakeholder** | Walk the hierarchy with a domain expert before handing off. Each `should` line must make sense to a non-technical reader. |
| **Save** | Markdown file, indented with 2 spaces per level. No code. No test syntax. |

### 3. Validate

Read every file in `rules/` and emit per-rule verdicts:

```
Rule: domain-practice-alignment    ->  PASS
Rule: plain-english-only           ->  PASS
Rule: business-readable-language   ->  PASS
Rule: every-describe-has-behavior  ->  PASS
```

---

## Principles

**Domain practice alignment** — Every describe block corresponds to a sub-epic or a named concept from the domain language or domain model. Do not invent names. If a concept is missing from those artifacts, surface it there first.

**Plain English only** — No code syntax in the scaffold. No `()`, `=>`, `{}`, `[]`. No method names. No type annotations. If you catch yourself writing a function signature, stop — that belongs in abd-bdd-specification.

**Business-readable language** — Every leaf `should` line must be readable by a business stakeholder who has never seen the code. Use the domain's ubiquitous language.

**Every describe has behavior** — No describe block should be a dead end. Every grouping must have at least one `should` leaf beneath it. Empty groupings signal the domain concept is unclear or misplaced.

**Behaviors, not test cases** — The hierarchy describes what the system *does*, not test scenarios. A single `should` line may imply multiple test cases — that detail belongs in abd-bdd-specification.

**Story traceability** — Every top-level describe block traces to a sub-epic. Every behavior leaf traces to a story or acceptance criterion in that sub-epic.

---

## Validate

Before handing off to the next phase, verify:

- [ ] Every top-level describe block corresponds to a sub-epic in the story map
- [ ] Every nested describe block corresponds to a concept in the domain language or domain model
- [ ] Every leaf line starts with `should`
- [ ] No code syntax appears anywhere in the file
- [ ] A business stakeholder can read every line without asking what it means
- [ ] Every describe block has at least one `should` leaf
- [ ] Every behavior traces to a story or acceptance criterion in scope
- [ ] Per-rule verdict emitted for every rule in `rules/`
