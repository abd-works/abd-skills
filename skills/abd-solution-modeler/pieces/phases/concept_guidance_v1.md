# Phase 2 — Concept Guidance v1

**Actor:** AI | 
## Purpose

Create the **initial domain hypothesis** that will guide extraction.

This phase should identify the domain's likely:
- **Concepts**
- **Modules**
- **Mechanisms**
- **Actors**
- **Epics**

**Interaction detail:** Story Map Skeleton: Epics, Sub-Epics, some stories where possible.

## Trigger

concept scan, first-cut domain, epic skeleton, domain hypothesis

## Domain detail
Only include:
- concept names
- short interaction-oriented concept statements

Do **not** include:
- properties
- operations
- collaborators
- invariants
- final inheritance
- service/manager/resolver concepts unless explicitly present in the source domain

## Interaction detail
Produce:
- **Story Map Skeleton** — Epics, Sub-Epics, some stories where possible
- Epic names and short statements
- Sub-epics under epics where evident
- Stories where evident from context

Add stories where evident from context; defer Trigger, Response, scenarios, steps to later phases.

## Inputs
- `context/context_chunks.json`

## Instructions

Identify:

1. **Candidate Concepts**
   - include concepts that participate in interactions or state changes
   - avoid example-only roles unless they are real domain concepts
   - **enumerate subtypes with distinct mechanics** — when the context describes multiple variants of a concept (e.g. "payment methods: CreditCard, BankTransfer, DigitalWallet, BuyNowPayLater...") and each variant has its own rules (different validation, settlement, fee structure, reversal process), list EACH variant as a separate concept, not as an enum on the parent. A subtype is a concept when it has its own mechanics; it's an enum value when it's just a label.
   - **check for category hierarchies** — when the context groups things into categories (e.g. "retail promotions: volume discounts, loyalty rewards, bundle offers, clearance markdowns") with different rules per category (different eligibility, stacking, expiry), model each category as a concept
   - **read chunks for mechanical depth, not just chapter summaries** — scan the actual chunk text for every distinct rule, formula, or state transition. A mechanic that has its own trigger, its own conditions, its own state transitions, or its own interaction rules is a concept, not a property.
   - **organize concepts into type / subtype / related** — for every concept that has subtypes with distinct mechanics, list the subtypes indented under the parent in the markdown output and in `concept_hierarchy` in the JSON output. Use `-> related:` to link associated concepts that collaborate but are not subtypes. This initial hierarchy map feeds directly into later phases — getting it right here avoids rediscovery.

2. **Candidate Modules**
   - group concepts around likely mechanisms
   - modules should be broad and provisional
   - **a variation axis with its own rules, interactions, and state is a strong candidate for a module**

3. **Likely Mechanisms**
   - name mechanisms that appear to organize multiple rules
   - do not convert mechanisms into classes yet

4. **Likely Actors**
   - identify human/system/domain actors only where relevant to interactions

5. **Likely Epics**
   - broad domain interaction areas only
   - epic names should be verb-noun and domain-grounded
   - **scan `context/context_chunks.json` for verb clusters** — groups of action verbs (grab, restrain, redirect, etc.) that don't fit an existing epic suggest a missing epic; do not rely on background knowledge alone to identify epics

## Noise Filter Instructions

Populate `noise_filters` in the JSON output with strings that identify low-value chunks from this specific source material. Always include generic defaults, then add domain-specific terms you observe in the chunks.

**Always include these defaults:**
- `"table of contents"`, `"appendix"`, `"index"`, `"license"`

**Add domain-specific terms** — scan chunks for repeated noise: archetype random-table row labels, second-person tutorial prose, license text, roll-table instructions. 

**CRITICAL:** Only include strings that appear **exclusively** in worthless chunks. Do NOT include strings like chapter headers or book titles that also appear in good rule content — they appear in headers of every chunk and will cause the entire corpus to be filtered out.

## Output quality rules
- prefer breadth AND depth over brevity — missing a concept is worse than listing a marginal one
- do not include formulas or exact rule math
- if uncertain, mark as **candidate**, not final
- every concept should have a short interaction-oriented statement
- every epic should be grounded in **Concept** language
- every concept named in the interaction skeleton must exist in the guidance output
- **concept count drives extraction quality** — the extraction script (Phase 3) can only find evidence for concepts you name here. If you list "Transaction" as one concept, all transaction subtypes get lumped together. If you list "Purchase", "Refund", "Chargeback" separately, extraction separates them. Err on the side of MORE concepts.

## Alias quality rules
- **no short aliases (2-3 characters)** — aliases like "TX", "CC", "PO", "SL" will false-match common letter pairs in English text and poison the evidence. Use full phrases ("transaction", "credit card", "purchase order", "service level").
- **no ambiguous common words** — aliases like "order", "item", "status", "type", "level", "plan", "rate" will match too broadly. Use compound phrases that are unambiguous in context (e.g. "service plan" not "plan"; "line item" not "item").
- **test each alias mentally** — would this string appear in text that has NOTHING to do with this concept? If yes, don't use it.

## Outputs

1. `generated/domain/concept_guidance.md`
2. `generated/domain/concept_guidance.json`
3. `generated/interaction_model/interaction_tree.md` (Story Map Skeleton: Epics, Sub-Epics, some stories)

## Markdown output shape

```text
# Domain Concept Guidance

## Modules

### Module: <name>
- concepts — **ConceptA**, **ConceptB**, **ConceptC**

## Concepts (candidate)

**Transaction** — exchange of value between parties
  **Purchase** : Transaction — forward payment, creates obligation
  **Refund** : Transaction — reversal, requires original purchase
  **Chargeback** : Transaction — disputed reversal, involves issuer
  -> related: **PaymentMethod**, **Receipt**

**PaymentMethod** — instrument used to settle a **Transaction**
  **CreditCard** : PaymentMethod — delayed settlement, supports chargeback
  **BankTransfer** : PaymentMethod — immediate settlement, no reversal
  **DigitalWallet** : PaymentMethod — tokenized, delegates to underlying method
  -> related: **Transaction**, **Fee**

**Receipt** — proof of completed **Transaction**

## Mechanisms (likely)

- **MechanismA** — short description
- **MechanismB** — short description

## Actors (likely)

- **ActorA** — short description

## Extraction Guidance

### Priority Concepts
- **Transaction**
- **PaymentMethod**

### Priority Mechanisms
- **MechanismA**
- **MechanismB**

### Variation Axes
- axis a
- axis b

### Synonym Hints
- **Transaction**: transaction
- **Purchase**: purchase, buy
- **Refund**: refund, return payment
```

**Hierarchy notation in markdown:**
- Indent subtypes under parent with `**Subtype** : Parent` notation
- `-> related:` line lists associated concepts (not subtypes)
- Top-level concepts with no parent stay unindented
- Leaf concepts with no children get a single line

## Required JSON shape (concept_guidance_v1.json)

```json
{
  "priority_concepts": ["Transaction", "Purchase", "Refund", "Chargeback", "PaymentMethod", "CreditCard", "BankTransfer"],
  "concept_aliases": {
    "Transaction": ["transaction"],
    "Purchase": ["purchase", "buy"],
    "Refund": ["refund", "return payment"],
    "PaymentMethod": ["payment method"]
  },
  "concept_hierarchy": {
    "Transaction": {
      "subtypes": ["Purchase", "Refund", "Chargeback"],
      "related": ["PaymentMethod", "Receipt"]
    },
    "PaymentMethod": {
      "subtypes": ["CreditCard", "BankTransfer", "DigitalWallet"],
      "related": ["Transaction", "Fee"]
    }
  },
  "priority_mechanisms": ["MechanismA", "MechanismB"],
  "priority_actors": ["ActorA", "ActorB"],
  "variation_axes": ["axis a", "axis b"],
  "noise_filters": [
    "table of contents", "appendix", "index", "license",
    "chapter header repeated", "title page",
    "<domain-specific noise terms you identified from chunks>"
  ],
  "focus_sections": ["section a", "section b"]
}
```

**`concept_hierarchy` rules:**
- All subtypes MUST also appear in `priority_concepts` (so extraction finds them individually)
- `subtypes` = "is-a" — subtype has its own distinct mechanics, inherits from parent
- `related` = "works-with" — collaborates but is not a subtype
- Only list parents that have subtypes or notable related concepts; leaf concepts with no children can be omitted from hierarchy

## Checkpoint 1

Human verifies domain framing before proceeding.
