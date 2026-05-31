# Domain Terms — Concepts

## Key Abstraction (KA)

For the definition of a Key Abstraction and the five aspects of a concept (Role, Boundary, Relationships, Responsibilities, Rules / invariants), read [`../../../reference/key-abstractions.md`](../../../reference/key-abstractions.md). The KA's intro paragraph weaves those five aspects into a single definition.

Specific to this skill: there is no separate `### ka_name_as_a_term` entry. The KA intro paragraph is the term definition. Subordinate terms follow as `### term` blocks beneath it.

## Domain term

A named concept from the module's domain. For each term, the skill captures *what it does* — behavior, interactions, rules, and flows — as short prose statements grounded in source material. Every claim traces back to the source it came from.

## Two tests and three outcomes for every candidate term

The independence test, the fit test, and the three outcomes (keep under a KA / move to boundary / move out) are defined in [`../../../reference/key-abstractions.md`](../../../reference/key-abstractions.md). This skill applies them at **module** scope:

- The fit test is the **module-fit test** — does this concept fundamentally connect to the core purpose of *this module*? If only one of its many uses relates to this module, it doesn't belong here.
- **Keep under a KA** — passes both tests. Group under the right KA.
- **Move to boundary** — this module depends on it without owning it. Add to `# Boundary Domain` with `*(owned by: Module)*`.
- **Move to another module** — this module does not depend on it at all. Record in `**Moved to other modules**`.

## Boundary terms

A concept this module depends on but does not own. Another module is the single source of truth for it. Appears under `# Boundary Domain` as `### term *(owned by: Module)*`.

---

## Consistent shape

```
## KAName

KAName is [definition as term — role, boundary, responsibilities, relationships,
invariants woven naturally. This paragraph IS the term definition for the KA.]

### subordinate_term
- behavioral line with *italicized domain terms*

### Decisions made
- independence-test result, module-fit result, grouping call

### References
**Ref — title**
Source: ...
Locator: ...
Extract: whole

```source
verbatim
```

---

### another_term
- behavioral line with *italicized domain terms*

### References
**Ref — title**
Source: ...

---
```
