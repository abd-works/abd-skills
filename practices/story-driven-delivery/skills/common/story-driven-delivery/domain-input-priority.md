# Story-Driven Delivery — Domain Input Priority

Read domain artifacts **before** writing acceptance criteria, specification scenarios, or acceptance tests. Use exact concept names from these sources — do not paraphrase, abbreviate, or rename.

---

## Priority order

1. **Class Model** (`domain-specification.md`) — typed classes with invariants and typed relationships. Use first when present.
2. **Domain model** (`domain-model.md`) — concepts with responsibilities and collaborators. **Default source** when no Class Model exists.
3. **Domain language** (`domain-language.md`) — defined terms and key abstractions. Use for term verification and when no model file exists.

Check for `domain.json` in the workspace. If it does not exist and a domain model markdown file is present, produce `domain.json` before running scanners (specification skill).

---

## Per skill

| Skill | Domain use |
| --- | --- |
| `abd-story-acceptance-criteria` | **Domain terms** section per story — every term must exist in a domain source (Domain Language, domain sketch, domain model, Class Model, or team-designated vocabulary file). If a term is missing, **stop — list every missing term and ask the user how to proceed**. **Never create `domain-terms.md` when domain sources already exist.** Only create `domain-terms.md` as a bootstrap when the engagement has no domain sources at all. |
| `abd-story-specification` | Structural spine for scenarios — concept names in bold, relationships in step language, invariants exercised by scenarios. |
| `abd-story-acceptance-test` | Class names, helper names, and fixtures trace to domain vocabulary and spec Examples tables. |

---

## New vs existing system

Mode detection and evidence sources: [`../../reference/new-vs-existing-system.md`](../../reference/new-vs-existing-system.md).
