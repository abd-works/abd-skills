# Research: Subtype vs Type-Field Discrimination

## Problem

The system conflates **real subtypes** (inheritance — extra data and behavior, need separate modeling) with **type fields** (e.g. red vs blue — same flow, different value; just data). This is a core weakness. The deprecated modifiers bucket did not address it.

## Research Summary

### 1. Feature modeling / product configurators

**What it offers:** Feature models capture variation via mandatory/optional features, alternative features, or-features, and feature groups. Product configurators assemble variants from a shared superset of assets.

**Key insight:** Variation is about *which elements exist* vs *which values they take*. Mandatory vs optional vs alternative is about *existence and composition*, not inheritance.

**Limitation for our use:** This is software/product config — selecting features to build a variant. It does not tell us how to extract "subtype vs type field" from *rule text*.

**Takeaway:** The distinction "same flow, different input" vs "different rules apply" is analogous to "same asset, different config" vs "different assets exist." We could use a *mechanical difference test*: does switching from A to B change the *rules* that apply? If yes → subtype; if no → type field.

---

### 2. Ontology learning

**What it offers:**

- **Taxonomic relations** (hypernym/hyponym, "is-a"): hierarchical, categorical. X is a kind of Y.

- **Attribute relations** (data-properties): non-taxonomic. Color, price, etc. — descriptive properties that characterize concepts.

- **Meronymic relations** (part-whole): has-part, component-of.

**Key insight:** Ontology learning explicitly separates *inheritance* (is-a, subsumption) from *attributes* (has-attribute, data-properties). Inheritance = vertical hierarchy; attributes = horizontal descriptive properties.

**Extraction patterns:**

- **Hypernym patterns:** "is a", "such as", "including", "kinds of", "types of", "for example" — indicate subsumption.

- **Attribute patterns:** "has", "with", "of color" — indicate descriptive properties.

**Limitation:** Ontology learning focuses on *structure* (taxonomy vs attributes). It does not directly address *rule-mechanics variation* — i.e. whether a variant changes *how things work*.

**Takeaway:** Lexico-syntactic patterns can distinguish "X is a kind of Y" (subtype) from "X has property P" (type field). We could add pattern-based detection: "Effect such as Damage, Healing" → subtype candidates; "attack of type [melee, ranged]" → type field if rules are identical.

---

### 3. Linguistic modification (adjectives/adverbs)

**What it offers:** FrameNet models adjective-noun relations via semantic frames and frame elements. Adjectives express degree, quality, etc. within a frame.

**Key insight:** Adjective modification is *syntactic* — it modifies a noun's meaning. "Heavy rain" vs "light rain" — same concept (rain), different degree. "Red car" vs "blue car" — same concept (car), different attribute.

**Limitation:** This is syntactic/semantic, not rule-mechanics. It does not tell us whether "Impervious" (as modifier) changes *how rules resolve* vs just being a parameter.

**Takeaway:** Adjectives alone are weak signals. "Impervious modifier" could mean (a) a type field that changes a numeric value, or (b) a subtype that changes penetration rules. We need *behavioral* evidence: do different rules apply?

---

### 4. Domain-driven design / software engineering heuristics

**When to use enums (type fields):**

- Fixed set of values, unlikely to change
- Simple state representation, no behavior differences
- No additional properties per value
- Data-driven conditions (switch on value)

**When to use inheritance (subtypes):**

- Different behaviors or additional properties per type
- Extendable types — new types may be added
- Shared functionality — common base, specialized overrides
- Rich object model — complex interactions

**Key heuristic:** *Behavior differences* → subtype. *Same flow, different value* → type field.

**Takeaway:** The "behavior difference" vs "data difference" criterion is the primary discriminator. We need to detect from rule text: does each variant have *distinct rules, triggers, or resolution*? Or do they share the same flow and differ only by a value?

---

### 5. Discriminator vs subtype polymorphism

**Discriminator (type field):** Closed set of types, value semantics, no RTTI. Used when all variants are known upfront and behavior is the same (switch on type).

**Subtype polymorphism:** Open set of types, reference semantics. Used when types have distinct behaviors or when extensibility is needed.

**Takeaway:** Closed vs open set is a secondary signal. If the rule text explicitly lists a fixed set of values with no behavioral difference, that's a type field. If it describes variants with "each has its own rules," that's subtype.

---

## Actionable Heuristics for Rule Text

| Signal | Subtype | Type field |
|--------|---------|------------|
| **Behavior** | Different rules, triggers, resolution per variant | Same flow; variant only changes input/value |
| **Lexical pattern** | "X such as A, B, C" + each has distinct rules | "X of type [A, B, C]" with same rules |
| **Attribute vs inheritance** | "X is a kind of Y" + adds data/behavior | "X has property P" or "X is P" (adjective) |
| **Mechanical difference test** | Switching variant changes which rules apply | Switching variant does not change rules |
| **Extensibility** | Open set — new variants may emerge | Closed set — fixed enum |

---

## Proposed Extraction Strategy

1. **Pattern-based pre-filter:** Use Hearst-style patterns ("such as", "is a", "kinds of") to find candidate subtype relations. Use attribute patterns ("has", "of type", "with value") to find candidate type fields.

2. **Mechanical difference test:** For each candidate, scan rule text for *distinct rules* per variant. If variant A and B both go through the same resolution steps with different parameters → type field. If A and B have different triggers, conditions, or outcomes → subtype.

3. **Behavioral evidence:** Actions and decisions already extracted. For a candidate subtype pair (A, B), check: do A and B have different `actions` or `decisions` in the evidence? If yes → subtype. If they share the same actions/decisions with different parameters → type field.

4. **Human-in-the-loop:** When signals conflict, flag for human review. "Effect: Damage vs Healing" — both have "applies to target" but different outcomes (damage vs healing). That's subtype. "Attack: melee vs ranged" — if rules are identical except range, that's type field.

---

## Design Doc Alignment

The concept-anchored pipeline design (`design-concept-anchored-pipeline.md`) now encodes this distinction:

- **Concept guidance (Phase 2):** Hierarchy shows Attack → AreaEffectAttack (standard inheritance). No extra structural notes.
- **Phase 8 variations:** Only real subtypes (e.g. AreaEffectAttack) appear in `variations`. Type fields (melee, ranged) appear as `parameterized_examples` in steps.

---

## References

- Feature modeling: Software Product Line Engineering; feature models (mandatory, optional, alternative)
- Ontology learning: Taxonomic vs meronymic relations; hypernym extraction (Hearst patterns, WebIsA); attribute learning
- FrameNet: Adjective-noun semantic frames; frame elements for modification
- DDD: "When to use enums vs. inheritance" (DEV Community); composition vs inheritance
- Polymorphism: Discriminator vs subtype polymorphism; closed vs open type sets
