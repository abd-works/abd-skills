---
rule_id: verb-noun-module-epic-story
phases: [step1]
order: 8
impact: HIGH
---

## Verb/noun alignment for modules, epics, and scaffold stories

Naming must match the story-map conventions in `parts/story-map.md` and stay consistent with `parts/domain.md` (modules = bounded contexts; epics = journey; confirming stories = observable outcomes).

**Non-negotiable:** Domain object words in **`epic.statement`** and **`confirming_stories[]`** must use **the exact same strings** as **`concepts[].name`** in that module (**100% match**). See **`scaffold-concept-story-name-alignment`** — not separate from this rule.

**Modules (nouns)**

- **Module names** are **noun phrases** — a bounded context or subsystem (e.g. `Order Fulfillment`, `Policy Engine`).
- Avoid verb-led module titles unless the domain truly names the area that way; prefer the thing being coordinated.

**Epics (verb + noun)**

- **Epic titles** follow **Verb Noun** (or **Verb the Noun**): the user or system **does** something meaningful (e.g. `Place Order`, `Resolve Coverage Conflict`).
- **`epic.statement`** should read as a goal or outcome in the same voice, not a module dump.

**Confirming stories (verb + noun)**

- Each **`confirming_stories[]`** entry is **Verb Noun** — one observable outcome that **confirms** the epic (see `epic-requires-confirming-stories.md`).
- The **object noun** (the domain thing acted on) must be **identical** to a **`concepts[].name`** in that module — **100% string match**, not paraphrase.
- Stories are **not** module names and **not** generic placeholders (`Do work`, `Handle requests`).

**DO**

- Cross-check epic and story titles against `parts/story-map.md` § Epics and § Stories.
- If an epic is noun-only, rewrite to verb+noun or document the exception in `open_questions`.

**DON'T**

- Use the same string for module name, epic title, and story title without a deliberate reason (that usually hides missing decomposition).
