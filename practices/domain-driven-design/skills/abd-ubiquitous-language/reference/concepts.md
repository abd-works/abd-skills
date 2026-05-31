# Ubiquitous Language — Concepts

## Ubiquitous language

The **ubiquitous language** is the single set of names, definitions, and rules a team uses everywhere — conversations, requirements, tests, code, and diagrams. It is not a glossary collected from many places; it is one curated vocabulary the team commits to and updates together. Each named concept carries its own purpose, its own behavior, and its own invariants, so anyone reading the file can challenge what is true and anyone writing downstream artifacts can re-use the same words without paraphrase.

## Terms

A **term** is any named concept in the source that has behavior, rules, interactions, or distinct identity. The first pass of the skill extracts every term and assigns it a short plain-English definition and a placement decision: keep under a KA, move to boundary, or move out entirely. Terms appear as a flat list in the output file header — one bullet per term, definition only, no source references. A term's placement decision is recorded there with a parenthetical note and fleshed out later in `### Decisions made`.

## Key Abstraction (KA)

For the base definition of a Key Abstraction, the five aspects of a concept, and the candidate-term tests and outcomes, read [`../../../reference/key-abstractions.md`](../../../reference/key-abstractions.md). This skill adds the following ubiquitous-language–specific guidance:

KAs act as **centers of gravity** — the named ideas domain experts reach for first when explaining the domain. Because of that, their intro paragraphs carry the richest treatment of all five aspects: role, boundary, relationships, responsibilities, and rules/invariants. Relationships to other KAs get particular weight, because that is how domain experts discuss them — "*Check* depends on *Trait* for its modifier; *Trait* knows nothing about *Check*."

**A KA must anchor at least 3–5 terms.** A KA with only its own name is not a KA — it is a single concept. If a candidate KA has fewer than three terms including its subordinates, merge it under an existing KA or downgrade it to a subordinate concept.

## Concept

A **concept** is a named domain idea the team treats as a candidate object: something the business talks about that has its own purpose, its own behavior, and relationships with other concepts. A concept is not a class — it is the plain-English precursor to one. Every concept — KA or subordinate — can be described across the **five aspects** (Role, Boundary, Relationships, Responsibilities, Rules / invariants) defined in [`../../../reference/key-abstractions.md`](../../../reference/key-abstractions.md).

These five aspects are not independent sections in the output — they are woven into the concept's story as verb-led behavior bullets. Same format for every concept. The KA's own concept block doubles as the term definition for the KA itself. How much any concept has to say is driven by the complexity of what the source actually says about it. Domain terms in bullets are *italicized* so the language stays visually precise.

The first `### concept` listed under each `## KA` heading **must be the KA's own concept** — the one whose name matches the KA. Other concepts grouped under the KA are subordinate.

## Two tests and three outcomes for every term

The independence test, the fit test, and the three outcomes (keep under a KA / move to boundary / move out) are defined in [`../../../reference/key-abstractions.md`](../../../reference/key-abstractions.md). This skill applies them at **scope** level — the second test is the **scope-fit test** (does this concept connect to the core purpose of the scope being modeled, or only touch it tangentially?).

One ubiquitous-language–specific refinement on the **move to boundary** outcome: if a boundary term is relevant to more than one KA, each KA records its own view — only the behaviors that KA actually depends on — as a concept stub inside that KA's block. The `# Boundary Domain` entry is the canonical record; the per-KA stubs are scoped views, not duplicates.

## Modeling each term: concept, subtype, property, instance, or invariant

Not every domain term deserves its own concept block. Before classifying, **read the source material for that term** and do proper object-oriented analysis on what the source actually says.

A term becomes a **concept** when it has **distinct identity**, **state**, **behavior**, **structure**, or **interactions**. A term that is a **specialized version** of another concept and adds **different behavior** is a **subtype**. A term that differs from its siblings only by **data values** is an **instance** or **type property** on the parent. A term that is a **value, slot, or attribute** another concept carries is a **property**. A term that describes a **rule that must always hold** is an **invariant** on the concept it constrains.

For typing decisions, see **`### Inheritance and subtypes`** in `../../../reference/oo-concepts.md`. Read it before classifying any term as a concept, subtype, property, or instance. **Do not read or apply `### Decomposing responsibilities`** — that section applies at CRC stage and beyond.

Property and instance terms still get a stub heading with a one-line classification note — no term is silently dropped.

## Subtypes

A subtype is one concept **being a type of** another. Write the heading in plain English (`### International Shipment *is a type of* Shipment`), not in code notation. Keep **shared** behavior on the **base**; the subtype block adds only **delta** behavior — what the subtype does differently or additionally.

## Roles and actors

A role (gamemaster, administrator, operator, reviewer) **is** a domain concept if it has distinct identity, state, or behavior from the system's perspective. A role that only performs tasks outside the system or the UI is a contextual label — note it in `### Decisions made`, do not model it as a concept.

## Properties

A pure property — one with no independent behavior, invariants, or cross-concept interactions — is mentioned only as a bullet on its parent concept. It does **not** get its own `### heading`. A property earns a `### heading` only when it has at least one of: its own invariant, its own behavior, or its own cross-concept interaction. Record the typing call in `#### Decisions made` so nothing is silently dropped.

## Italicized terms are the file's connectors

Every `*italicized*` term in a behavior bullet, invariant, KA intro paragraph, or boundary stub must resolve to one of:

- a `### concept_name` block (in any KA, Core or Boundary, including the KA's own concept),
- a `### Subtype *is a type of* Base` heading,
- a property / instance / type-property stub heading (e.g. `### rank` with first bullet `is a property of *trait*`),
- a `### boundary_term *(boundary)*` scoped stub under the KA, OR
- a parenthetical primitive description in plain text (e.g. `(integer)`, `(true or false)`, `(0–40)`) — the parenthetical itself is **not** italicized.

This is what makes a Ubiquitous Language **diagram-ready as a second pass** for [drawio-domain-sync](../drawio-domain-sync/SKILL.md). Once every italicized term resolves to a heading, a renderer can treat each `### concept` as a card, each behavior bullet as a row, each subtype heading as an inheritance edge, and each unique cross-concept italicized reference as one association edge.

To keep relationship types readable without labels, use stable verb families in bullets:

- `has`, `owns`, `is composed of`, `consists of` → composition / aggregation,
- `uses`, `references`, `supplies … to`, `depends on`, `is made against` → association,
- `produces`, `creates`, `yields` → dependency / creates,
- `is a type of` → inheritance (heading-level only),
- `is a property of`, `is an instance of` → property/instance stub heading.

## Decisions made and References — per KA

Every KA carries one `#### Decisions made` list and one `#### References` section, placed **after all of its concept blocks**. This keeps the reasoning and evidence co-located with the KA they support. `#### Decisions made` records independence test results, scope-fit test results, typing calls, and any open questions for any concept in the KA. `#### References` lists every source passage that supports any concept in the KA. Do not bundle decisions or references per concept.

## Three passes, one file

1. **Terms** — flat list of every named concept with a short plain-English definition and a placement decision (keep / boundary / moved out). No source references in the Terms list.
2. **Key Abstractions** — terms grouped under named KAs; each KA gets an intro paragraph that is its term definition.
3. **Concept blocks** — each KA's concept blocks (KA's own first, then subordinates, subtypes, property stubs), with verb-led behavior; **one** `### Decisions made` and **one** `### References` per KA, after all its concept blocks.

---

## Consistent shape

```
# Module: [ScopeName]           ← omit if single-scope; include per-module for multi-module

**Terms**:
- **KAName**
  - **ka_term** — short plain-English definition
  - **subordinate_term** — short plain-English definition
- **AnotherKAName**
  - **another_term** — short plain-English definition

---

{{Analytical overview paragraph(s) — end-to-end domain mechanic with *italicized domain terms*.}}

---

# Core Domain

## KAName                                       ← h2, no bold

KAName is [definition as term — role, boundary, responsibilities,
relationships, invariants woven naturally. This paragraph IS the
term definition for the KA.]

### ka_name_as_a_concept                        ← MUST appear first; matches the KA
- verb-led behavior with *italicized domain terms*
- **Invariant:** rule that must always hold

### another_concept
- verb-led behavior with *italicized domain terms*

### SubtypeName *is a type of* BaseName
- delta behavior — only what the subtype adds

### property_term
- is a property of *parent_concept* — brief classification note

### Decisions made                              ← ONE per KA, after ALL concept blocks
- independence test result, scope-fit test result, typing call, or open question

### References                                  ← ONE per KA, after Decisions made
**Ref — title**
Source: ...
Locator: ...
Extract: whole

---                                             ← separator between KAs

# Boundary Domain

## boundary_concept

Owned by: ModuleName

- verb-led behavior with *italicized domain terms*

### Decisions made
- boundary placement reasoning

### References
**Ref — title**
Source: ...

---
```
