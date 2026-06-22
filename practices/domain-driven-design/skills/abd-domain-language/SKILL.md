---
name: abd-domain-language
catalog_garden_tier: practice
catalog_garden_order: 2
catalogue_one_liner: >-
  Define each domain term precisely — name, meaning, boundaries, relationships — so models, stories, and code share one vocabulary.
description: >-
  Get domain experts and builders to agree on what each term means — terms, Key Abstractions, and concept sketches that downstream artifacts rely on. Use when source material exists but no agreed domain vocabulary yet.
context-perspective: domain
context-fidelity:
  - level: discovery
    mode: language
---
# abd-domain-language

## Purpose

Define each domain term precisely — name, meaning, boundaries, and relationships — so domain models, stories, and code use the same words with the same meaning.

---

## Output file

**Deliverables folder:** `<active_skill_workspace>/domain/`

**File name:** `domain-language.md`. Add a `<name>-` prefix only when disambiguation is needed. For multi-module engagements: `<deliverables-folder>/modules/<module-name>-domain-language.md`. When the scope spans more than one module in a single file, organize with `# Module: [ModuleName]` sections.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these common input traps:

- **Vocabulary collisions** — which term means different things to different people in the room — and where is the team smoothing over a real boundary by using one word for two concepts?
- **Missing behavior** — which concepts are described as things that exist but not things that do anything — where is the behavior hiding behind nouns?
- **Premature hierarchy** — are we organizing concepts into parent-child relationships because the domain actually has that structure, or because it feels tidy?
- **Implicit concepts** — what ideas does the team use in every conversation but hasn't named — the concept that everyone assumes but nobody has articulated?
- **Business vs. implementation language** — which descriptions capture what the concept does in the business versus how it might be implemented — and where has technical thinking leaked into the domain vocabulary?

---

## Agent Instructions

### 1. Read context

Read these files:
- **`reference/concepts.md`** — Domain Language, terms, KAs, concepts, two tests, three outcomes, modeling decisions (concept vs subtype vs property vs instance), italicized-term resolution, decisions/references per KA, three passes, and the consistent file shape.
- **`../../reference/oo-concepts.md`** — OO fundamentals (what is a class, inheritance and subtypes). Read the **`### Inheritance and subtypes`** section before classifying terms. **Do not** read or apply `### Decomposing responsibilities` — that applies at domain model stage and beyond.

### 2. Generate

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/domain-language-template.md` | The Domain Language file with Terms list, KA intros, concept blocks, decisions, and references. |
| `templates/domain.json` | Domain JSON with concept names, attributes, and inheritance. |

**Quality bar:** Every KA intro opens with "*KAName* is …". Every concept has verb-led behavior bullets. Every `*italicized*` term resolves to a heading, stub, or parenthetical primitive. One `#### Decisions made` and one `#### References` per KA, after all concept blocks.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Each KA anchors at least 3–5 terms** — subordinate concepts, subtypes, and properties included. A KA with fewer than three terms is not a KA; merge it under an existing KA or downgrade it to a subordinate concept.
- **Terms list in header** — a single hierarchical `**Terms**` list.
- **Every KA has an intro paragraph** — opens with "*KAName* is …".
- **Every KA's own concept appears first** — the first `### concept` under each `## KA` matches the KA name.
- **Every concept has verb-led behavior bullets** — active voice; the concept is the subject.
- **Domain terms italicized** — every domain term in bullets, invariants, and KA intro paragraphs.
- **Italicized terms resolve** — every `*italicized*` term resolves to a heading, stub, or parenthetical primitive.
- **No bold on headings** — `## KAName`, `### concept`, and subtype headings carry no bold.
- **One `#### Decisions made` per KA** — after all concept blocks.
- **One `#### References` per KA** — after `#### Decisions made`.
- **Boundary entries have a single named owner** — `Owned by: ModuleName`.
- **Properties with independent behavior visible** — properties that have their own invariants, behavior, or interactions get a `###` stub; properties that are only "a property of X" are mentioned in the parent concept's bullets only.
- **No premature design commitments** — no UML stereotypes, typed properties, method signatures, or cardinality notation.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
