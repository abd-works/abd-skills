# Type vs Subtype Investigation — Rules, Scanners, and Gaps

## Problem Statement

The modeler currently:
1. **Treats enums as subtypes** — Same behavior, slightly different data (e.g. Effect Type: Attack, Control, Defense, General) modeled as inheritance hierarchy instead of `EffectType type {attack, control, defense, general}`.
2. **Creates shallow subtypes from ToC** — Subtypes inferred from table of contents or section headers without evidence of distinct mechanics in the source.
3. **Lacks early discrimination** — The decompose-vs-consolidate rule exists in variation_model (phase 9) but the hierarchy is baked in by concept_guidance (phases 2, 5) and concept_model (phase 6).

---

## Current Rules That Help

### 1. concept_guidance_v1 (Phase 2) — Buried instruction

**Location:** `pieces/phases/built/concept_guidance_v1.md` line 105

> **enumerate subtypes with distinct mechanics** — when the context describes multiple variants of a concept (e.g. "payment methods: CreditCard, BankTransfer, DigitalWallet, BuyNowPayLater...") and each variant has its own rules (different validation, settlement, fee structure, reversal process), list EACH variant as a separate concept, not as an enum on the parent. **A subtype is a concept when it has its own mechanics; it's an enum value when it's just a label.**

**Problem:** One bullet among many; no explicit DO NOT for the inverse; no validation rule; no scanner.

### 2. variation_model (Phase 9) — Decompose vs consolidate

**Location:** `pieces/phases/built/variation_model.md`; rule `domain/variation-decompose-variants.md`

> **DO** when subtypes have fundamentally different properties, operations, or resolution mechanics, decompose into an inheritance hierarchy with invariant examples per subtype. **Conversely, when operations differ only by a type discriminator with the same logic, consolidate into a single parameterized operation with a type property.**

**Problem:** Applies at phase 9. By then, concept_hierarchy from v1/v2/v5 and concept_model from v6 have already created subtypes. Too late.

### 3. concept-model-subtypes-first-class

**Location:** `rules/domain/concept-model-subtypes-first-class.md`

> **DO** give each subtype its own section... Subtypes inherit from parent but have **distinct mechanics** — model those mechanics explicitly.

**Problem:** Assumes subtypes are correct. Does not say: "DO NOT create subtypes when it's really an enum." Does not say: "Verify each subtype has distinct mechanics before creating it."

### 4. concept-model-property-types

**Location:** `rules/domain/concept-model-property-types.md`

> Use `EnumType name {value1, value2}` for constrained options — not `String` with parenthetical options.

**Problem:** Tells you to use enums for properties. Does not tell you when a "subtype" should be an enum instead.

---

## Current Scanners — None Check Type vs Subtype

| Scanner | Rule | What it checks |
|---------|------|----------------|
| `hierarchy_sizing` | interaction-approximately-4-to-9-children | Child count per epic/story |
| `sync_concepts` | domain-synchronize-concepts | Concept names in interactions vs domain model |
| `domain_model_parser` | (domain model structure) | Parses concept_model.md |
| `refined_concept_roles` | (refined phase) | Concept roles |
| `behavior_*` | (behavior phase) | Behavior rules |

**No scanner** checks:
- Subtype names mirroring a type/category enum (e.g. Effect Type + Attack Effect, Control Effect, etc.)
- Subtypes with no evidence of distinct mechanics in actions.json/terms.json

---

## Current Phase Instructions — Gaps

### concept_guidance_v1
- Has the subtype-vs-enum rule but buried.
- Does not say: "DO NOT derive subtypes from table of contents or section headers alone."
- Does not say: "For each subtype candidate, verify: different properties, operations, or resolution mechanics in the evidence."

### concept_guidance_v2
- Says "refine concept hierarchy" and "split overloaded variation axes" (promote to concept when distinct mechanics).
- Does not say the converse: "Reclassify subtypes as enum when they have no distinct mechanics."
- Does not say: "Flag subtypes that mirror a type/category enum — use one or the other, not both."

### concept_model
- Says "use concept_hierarchy as starting point" — bad hierarchy propagates.
- Says "each subtype must have its own first-class section" — assumes subtypes are correct.
- Does not say: "Before creating a subtype, verify evidence shows different mechanics."

---

## Domain Description Content — Story Synchronizer

**Story synchronizer** — Within this skill ecosystem, the story synchronizer syncs the story map structure (epics, sub-epics, stories) between DrawIO diagrams and the story representation — not domain concepts from a JSON file. It handles layout, hierarchy, and structural changes.

**Domain description** — The content that describes what each concept does (short statements, properties, mechanics) lives in:
- **This skill:** `concept_guidance.md`, `concept_model.md`, `context/context_chunks.json` — the evidence and guidance that feeds type vs subtype decisions
- **Story synchronizer:** If the story synchronizer carries or displays domain concept descriptions as part of its sync (e.g. concept names, responsibilities attached to story nodes), that content could provide type-vs-subtype signals — but the synchronizer's primary role is structural (epic/sub-epic/story hierarchy), not domain modeling

**Conclusion:** The fix for type vs subtype discrimination belongs in the solution modeler skill — in rules, phase instructions, and evidence-based verification. Domain description content that could help: the concept statements and evidence in concept_guidance, the mechanics described in context chunks, and the properties/operations in concept_model. The story synchronizer's domain-related content (if any) would need to be identified in its actual implementation.

---

## Proposed Fixes

### 1. New rule: `domain-subtypes-vs-enum.md`

Apply at all phases (no phase prefix — cross-phase rule).

**Content:**
- **DO** use subtype when: different properties, operations, or resolution mechanics in the evidence.
- **DO** use enum (or type property) when: same logic, different label; same behavior, different data.
- **DO NOT** derive subtypes from table of contents or section headers alone — verify each has distinct mechanics in the evidence.
- **DO NOT** create both a parent "Type" enum and subtypes that mirror it (e.g. Effect Type: Attack, Control, Defense, General AND Effect subtypes: Attack Effect, Control Effect, etc.) — use one or the other.
- **Examples:** (right) Defense subtypes Dodge, Parry, Toughness — each resists different attack types, different base ability. (wrong) Effect subtypes Attack Effect, Control Effect, Defense Effect, General Effect when Effect Type already categorizes Attack, Control, Defense, General — use enum.

### 2. New rule: `domain-mechanics-not-toc.md`

Apply at all phases (no phase prefix — cross-phase rule).

**Content:**
- **DO** read evidence chunks for mechanical depth — each subtype must have different rules, formulas, state transitions, or interaction patterns in the source.
- **DO NOT** infer subtypes from chapter titles, section headers, or bullet lists without reading the actual rule text for each variant.

### 3. Phase instruction updates

**concept_guidance_v1.md:**
- Add explicit checklist: "For each subtype in concept_hierarchy: does it have different properties, operations, or resolution mechanics in the evidence? If not, model as enum."

**concept_guidance_v2.md:**
- Add: "Reclassify subtypes as enum when evidence shows same logic, different label. Check for parent + type enum + subtypes that mirror the enum — use one representation."

**concept_model.md:**
- Add: "Before creating a subtype section, verify actions.json and terms.json show different mechanics for that subtype. If not, use EnumType on parent."

### 4. Optional scanner: `domain-subtypes-vs-enum.py`

**Heuristic checks (regex-only, nerfed):**
- If concept has `Subtypes:` list and also has a property like `EffectType type {attack, control, defense, general}` — flag: "Parent has both type enum and subtypes; verify subtype names don't mirror enum values."
- If concept has subtypes A, B, C and parent name is X — flag when A, B, C look like X category values (e.g. "Attack Effect", "Control Effect" under "Effect" when "Effect Type" exists).

**Limitation:** Full mechanics check requires semantic analysis of evidence. Scanner can only flag structural patterns.

---

## Summary

| Gap | Fix |
|-----|-----|
| Enum-as-subtype | New rule: `domain-subtypes-vs-enum.md` (all phases) |
| ToC-as-subtype | New rule: `domain-mechanics-not-toc.md` (all phases) |
| Rule too late (variation phase) | Move subtype-vs-enum guidance to concept_guidance and concept_model phases |
| No scanner | Optional scanner for structural pattern (type enum + mirroring subtypes) |
| Buried instruction | Promote to dedicated rule + phase instructions |
