# Key Abstractions

Shared reference for the domain-discovery skills (`abd-domain-terms`, `abd-ubiquitous-language`). This file owns the definition of a Key Abstraction and the candidate-term decision tests. Each skill owns its own notation, format, and any fidelity-specific elaboration.

## Key Abstraction (KA)

A **Key Abstraction** is a named domain building block that anchors a **group** of related terms — subordinate concepts, subtypes, and properties that only make sense in relation to the KA. KAs are the **centers of gravity** of the domain: the named ideas domain experts reach for first when explaining how the domain works. The KA owns the core responsibility and enforces the rules that keep the abstraction coherent.

The KA name is itself the **primary term**. The KA's intro paragraph opens with "*KAName* is …" and **is** the term definition — there is no separate subordinate entry that re-states it.

A typical module has **three to eight** Key Abstractions. More usually means subordinate terms have been promoted prematurely.

## The five aspects of a concept

Every concept — a KA or a subordinate term — can be described across five aspects:

- **Role** — the unique purpose this concept serves that no other does.
- **Boundary** — what it owns (single source of truth), what is external, how it collaborates.
- **Relationships** — explicit connections to other concepts and KAs.
- **Responsibilities** — the specific behaviors it performs and services it provides.
- **Rules / invariants** — non-negotiable truths that must always hold.

## Two tests for every candidate term

**1. Independence test.** Can this concept be defined and reasoned about on its own, without the parent it came from? If it has no meaning outside another concept, it stays as a subordinate term, not a KA of its own.

**2. Fit test.** Does this concept fundamentally connect to the core purpose of the scope being modeled, or does it only touch it tangentially? If it belongs more squarely in an adjacent area, place it at the boundary or move it out. *(Some skills name this the "scope-fit test"; the module-scoped skills name it the "module-fit test" — same test, scoped to the artifact.)*

## Three outcomes for each candidate term

- **Keep under a KA** — passes both tests; group under the right KA in the Core Domain.
- **Move to boundary** — independent, but this scope depends on it without owning it; record under the Boundary Domain with a single named owning module.
- **Move out** — independent and unrelated to this scope's purpose; note it and remove it from the model. *(Module-scoped skills phrase this as "move to another module".)*
