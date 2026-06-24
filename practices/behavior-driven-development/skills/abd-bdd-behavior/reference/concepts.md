# Concepts — abd-bdd-behavior

For shared BDD theory (what BDD is, the three phases, observable behavior, domain practice alignment) see `../../../reference/bdd-concepts.md`.

This file covers concepts specific to the behavior-discovery phase.

---

## The behavior hierarchy

The behavior hierarchy is a plain-English indented outline. It has three levels:

1. **Sub-epic** (top-level describe) — one block per sub-epic in scope from the story map. The name is taken verbatim from the story map.
2. **Domain concept or state** (nested describe) — concepts from the domain language or states from the domain model that belong to this sub-epic. One nesting level per concept or state grouping.
3. **Observable behavior** (leaf) — a `should` statement describing one thing the system does. Every leaf traces to a story or acceptance criterion.

```
Redeem Voucher                    ← sub-epic (from story-map.md)
  Voucher                         ← concept (from domain-language.md)
    Redemption                    ← state grouping (from domain-model.md)
      should apply a percentage discount to eligible items
      should reject a voucher past its expiry date
    Eligibility
      should only allow redemption by the customer it was issued to
  Order
    Display
      should show the saving amount on the order summary
```

Depth is not fixed at three levels. Follow the structure the domain gives you. If a concept has sub-groupings, add a level. If the domain is flat, the hierarchy is flat.

---

## Reading domain artifacts

The behavior hierarchy is derived, not invented. For each domain artifact, here is what to extract:

| Artifact | What to extract |
|---|---|
| `story-map.md` | Sub-epic names — these become top-level describe blocks |
| `domain-language.md` | Concept names — these become nested describe blocks |
| `domain-model.md` | States, transitions, operation groups — these become inner describe groupings |
| `acceptance-criteria.md` | Observable behaviors per story — these become `should` leaf statements |

If a concept is referenced in acceptance criteria but not present in domain-language or domain-model, flag it — do not add it silently to the hierarchy.

---

## Naming rules

- **Sub-epic names:** copied verbatim from the story map. No paraphrasing.
- **Domain concept names:** copied verbatim from the domain language. No synonyms, no abbreviations.
- **Should statements:** start with `should`. Written in the domain's ubiquitous language. No method names, class names, or implementation vocabulary.

**Pass:** `should apply a percentage discount to eligible items`
**Fail:** `should call applyDiscount() on VoucherService`

---

## What this phase does not produce

- No code syntax of any kind
- No Gherkin (`Given / When / Then`)
- No test file structure (`describe()`, `it()`, `beforeEach()`)
- No assertions
- No mocks

Those belong in abd-bdd-specification (structure) and abd-bdd-development (implementation).
