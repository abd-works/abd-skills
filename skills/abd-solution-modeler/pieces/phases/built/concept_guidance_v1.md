# Critical Quality Steps

**These steps MUST be followed for every AI phase. No exceptions.**

---

## Step 0 — Deep Scan of Evidence and Conceptual Guidance (REQUIRED FIRST)

Before generating any output, you MUST:

1. **Do a deep scan of the evidence** — Read all files in `evidence/` (terms.json, actions.json, decisions.json, states.json, relationships.json, modifiers.json, evidence_graph.json). Understand every concept, every action, every decision, every state.
2. **Do a deep examination of the conceptual guidance** — Read `concept_guidance.md` and `concept_guidance.json`. Examine ALL concepts. Understand the nuance at a very detailed level.
3. **Verify understanding** — Before writing, confirm you can articulate: What are the key mechanisms? What are the subtypes and their distinct data/behavior? What variations exist? What constraints apply?

Do not proceed to generation until you have done this deep scan. Shallow or partial understanding produces shallow, broken models.

---

## Three-Stage Process (MUST follow for every AI step)

Each AI phase uses three validation layers. All three are required.

**Layer 1 — Generate with rules.** Phase spec + accumulated rules are included in the generation instructions. Follow DO/DO NOT guidance while producing output. Rules are guidance — produce natural output that complies.

**Layer 2 — Scan.** After generation, run `pipeline.py scan <phase>`. Scanners check structural violations mechanically (naming, child counts, concept sync, property types). Fix reported violations before proceeding.

**Layer 3 — Validate.** After scanners, run `pipeline.py validate <phase>`. This prints all applicable rules. AI re-reads generated output against the rules AND the completeness checklists. For each rule: does the output comply with the spirit, not just the letter? Report violations with rule name, location, proposed fix. Fix all violations. Re-validate until clean.

**This layer is critical.** Be adversarial. Take a contrarian stance. A scanner says "all clear" but the AI reviewing the rules sees that 3 operations on a concept all make decisions that belong to other concepts.

---

## AI Behavior Per Layer

| Layer           | Behavior                                                                            |
| --------------- | ----------------------------------------------------------------------------------- |
| Step 0          | Deep scan evidence + concept_guidance; verify understanding before generating       |
| Generation      | Pay strict attention to rules naturally while producing output                      |
| Scanner fixes   | Fix reported violations mechanically; re-run until clean                            |
| Validation pass | Adversarial checklist review — each rule is a checklist item; report ALL violations |

---

## Corrections Format

When recording corrections:

- **DO** or **DO NOT** rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be


---

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
   - **subtype vs enum checklist** — for each subtype in concept_hierarchy, verify: does the evidence show different properties, operations, or resolution mechanics? If not, model as enum on parent (e.g. `EffectType type {attack, control, defense, general}`), not as subtypes.
   - **do not derive subtypes from ToC** — table of contents and section headers list names; they do not prove distinct mechanics. Read the actual rule text for each variant before creating a subtype.
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
   - **high-complexity areas are epic candidates** — when the source describes many named variants, each with its own rules, that area is likely an epic. Do not collapse into one variation axis or one concept. Model as an epic with sub-epics and stories per variant type.

6. **Variation Axes** (in Extraction Guidance)
   - **variation axis = dimension of mechanical difference** — switching from one value to another changes the *rules* that apply (triggers, resolution, state transitions). If it only changes which value a variable has (same rules, different input), it is NOT a variation axis.
   - **variable values are not axes** — e.g. "payment method (credit card, bank transfer)", "order status (pending, shipped)", "customer tier (gold, silver)" are just different values of a variable. Same mechanism, different input. Do not list as variation axes.
   - **derive from rule text, not ToC or headers** — for each axis, you must have read the actual rules. ToC and headers name things; they do not prove distinct mechanics.
   - **do not collapse many mechanical variants into one axis** — when the source has many named variants, each with distinct rules, either list the mechanically distinct variants or treat as an epic.
   - **checklist** — before adding each axis: (a) Which chunks did I read? (b) What distinct mechanics does each variant have? (c) Is this a variable's values or a real mechanical dimension?

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


---

# Domain Model Format

# Domain Model Format

## Module

Heading: `## Module: <name>`

```
## Module: <name>
- concepts — **ConceptA**, **ConceptB**, **ConceptC**
- examples: at end of module, after all concepts; one table per concept; shared scenario links the module
```

## Domain Concept

Heading: `### **ConceptName** : <BaseConcept if any>`
One-liner description of the purpose of the concept

```
**ConceptName** : <BaseConcept if any>
- <type> property
      <collaborating concepts if any>
      Invariant: <constraint on this property>
- <type> operation(<param>, ...) → <return>
      <collaborating concepts if any>
      Invariant: <constraint enforced by this operation>
- Interactions: interaction nodes this concept is used by
```

## Examples

**## Examples** (at end of module, after all concepts — one table per concept, shared scenario links all):
```
ConceptName (qualifier):
| scenario | property1 | property2 |
|----------|-----------|-----------|
| module-scenario.phase | val1 | val2 |
===
AnotherConcept (qualifier):
| scenario | property1 |
|----------|-----------|
| module-scenario.phase | val1 |
```

- One scenario prefix for the module (e.g. `monthly-operations`); sub-phases allowed (e.g. `monthly-operations.after-payroll`)
- Qualifier in parentheses after concept name
- Scenario column required; kebab-case
- Columns match concept property names
- `===` separator between tables

### Invariants

Place invariants under the specific property or operation they apply to — not as a separate section. Format: `Invariant: <constraint>`.

```
- Number balance
      Invariant: balance >= 0
- debit(amount) → Boolean
      Invariant: amount <= balance
```

## Guidelines

- Prefer **composition** over inheritance
- Use `Dictionary<K,V>` when items are keyed
- Use `List<T>` only when ordering matters
- Avoid central "service/manager" concepts
- Use `EnumType name {value1, value2}` for constrained options — not `String` with parenthetical options

## Example — Connected Concepts with Tables

Account holds funds; transactions record deposits and withdrawals. The balance is what’s available.

```
## Module: Accounts
- concepts — **Account**, **Transaction**

### **Account**

Holds funds. You deposit (credit) or withdraw (debit). Balance is what you have available.

- String name
- List<**Transaction**> transactions
      **Transaction** — history of deposits and withdrawals
- balance() → Number
      current available funds
- debit(amount) → Boolean
      withdraws funds; fails if insufficient
      **Transaction** — adds a withdrawal record
- credit(amount) → void
      deposits funds
      **Transaction** — adds a deposit record

- Interactions: Debit Account, Credit Account

### **Transaction**

A deposit or withdrawal. Belongs to an account.

- **Account** account
      **Account** — which account this affects
- Number amount
- String type {debit, credit}

- Interactions:  Debit Account, Credit Account

### examples

Account (selected):
| scenario                             | name            | balance  |
|--------------------------------------|-----------------|----------|
| monthly-operations.main-checking     | Main Checking   | 3247.50  |
| monthly-operations.main-checking-od  | Main Checking   | 42.00    |
| monthly-operations.savings           | Savings         | 500.00   |
===
Transaction (recorded):
| scenario                             | account         | amount   | type   |
|--------------------------------------|-----------------|----------|--------|
| monthly-operations.main-checking     | Main Checking   | 2400.00  | credit |
| monthly-operations.main-checking     | Main Checking   | 1000.00  | credit |
| monthly-operations.main-checking     | Main Checking   | 142.50   | debit  |
| monthly-operations.main-checking     | Main Checking   | 10.00    | debit  |
| monthly-operations.main-checking-od  | Main Checking   | 500.00   | credit |
| monthly-operations.main-checking-od  | Main Checking   | 458.00   | debit  |
| monthly-operations.savings           | Savings         | 500.00   | credit |
```

One scenario per account. Balance = sum of transactions (credits − debits) for that account in that scenario. Main Checking: 3247.50 = 2400 + 1000 − 142.50 − 10. Overdraft: 42 = 500 − 458. Savings: 500 = 500.

## Validation Checklist

- [ ] Format: `**Concept** : <Base Concept if any>`
- [ ] Module has examples: one table per concept, shared scenario, `===` separator
- [ ] Properties, operations, collaborating concepts listed
- [ ] Each concept referenced via `**Concept**` in interaction tree must exist here
- [ ] Invariants under specific property/operation they apply to
- [ ] No implementation details (APIs, services, databases, UI components, code)
- [ ] No speculation beyond the provided material
- [ ] Everything at logical/domain level


---

# Interaction Tree Format

# Interaction Tree Format

## Hierarchy

Epic → Sub-Epic → Story → Scenario → Step

| Node | Meaning | Heading |
| ----- | ----- | ----- |
| Epic | Large domain capability — a major area of the system | `# Epic: <name> (<statement>)` |
| Sub-Epic | Logical grouping of related stories — a feature area, not a behavior itself | `## Epic: <name> (<statement>)` |
| Story | Smallest independently valuable behavior — has a triggering actor, a responding actor, and produces observable state change. If it has no actor and no state change, it is not a story. | `### Story: <name> (<statement>)` |
| Scenario | A condition-specific grouping of steps within a story (e.g. success path, failure path) | `#### Scenario: <name>` |
| Step | A single atomic interaction — one action by one actor | `- Step N: <name> (When/Then <statement>)` |

## Per Interaction

- **Trigger** — Triggering-Actor, Behavior
- **Response** — Responding-Actor, Behavior
- **Pre-Condition** — label only (Given/And)
- **Failure-Modes** — bullet list, max 3; rule/state based only (no infrastructure failures)
- **Domain Concepts** - Domain Concepts related to Interaction, must exist in the domain model
- **Examples** — tables per concept


### Commonly Generated Fields Per Node

| Node | Commonly Generated | Case-by-Case |
|------|--------------------|--------------|
| Epic | Triggering-Actor, Responding-Actor, Name, Pre-Condition | Constraints |
| Story | Trigger, Response, Name, Examples, Pre-Condition, Failure-Modes | Constraints |
| Scenario | Trigger, Response, Pre-Condition, Examples | |
| Step | Trigger, Response, Examples | Constraints (when step-specific) |

## Domain Grounding

Use `**Concept**` in labels. Every concept must exist in Domain Model.

## Inheritance

Parent → child; use `[brackets]` for inherited values (e.g. `Triggering-Actor: [User]`).

## Example Tables

Tables live on the interaction. One per concept referenced in labels, should be identical to examples in the domain model

```
ConceptName (qualifier):
| scenario | field1 | field2 |
|----------|--------|--------|
| success  | val1   | val2   |

AnotherConcept (qualifier):
| scenario | field1 |
|----------|--------|
| success  | val1   |
```

- Qualifier in parentheses after concept name
- Scenario column required; use kebab-case (e.g. `success`, `invalid-details`)
- `===` separator between tables
- Inherited examples: `Examples: [Table Name 1, Table Name 2]`

## Validation Checklist

**Epic**
- [ ] Heading: `# Epic: <name using **Domain Concepts**> (<statement>)`
- [ ] Triggering-Actor, Responding-Actor, Pre-Condition, Examples present (or inherited)
- [ ] Pre-Condition on parent only when shared; children list only new or specialized state

**Story**
- [ ] Heading: `### Story: <name using **Domain Concepts**> (<statement>)`
- [ ] Pre-Condition, Failure-Modes (max 3), Trigger, Response present
- [ ] Trigger: sub-bullets Triggering-Actor, Behavior
- [ ] Response: sub-bullets Responding-Actor, Behavior

**Step**
- [ ] `- Step N: <name using **Domain Concepts**> (When/Then <statement>)`
- [ ] Trigger and Response with [inherited] when from parent

**Example tables**
- [ ] Qualifier in parentheses: `ConceptName (qualifier):`
- [ ] Scenario column required; kebab-case
- [ ] Each table: label, header row, separator row, data rows

**Hierarchy**
- [ ] Epic → Epic/Story → Scenario → Step
- [ ] Each node touches at least one domain concept via `**Concept**`


---

## Domain Model Rules (4)

Apply these rules when producing the domain model output for this phase.

---
title: Speculation and assumptions
impact: HIGH
---

## Speculation and assumptions

**DO** state an assumption when something is unclear.
- Example (right): "Assumption: Shipping Address is provided before checkout"; "Assumption: Loyalty points not in scope".

**DO NOT** speculate beyond the provided material or invent mechanics when unclear.
- Example (wrong): Story "Apply loyalty points at checkout" when context never mentions loyalty. Right: Omit, or state "Assumption: Loyalty points not in scope."


---

---
title: Derive from context
impact: HIGH
---

## Derive from context

**DO** derive concepts from the interactions you find in the context; focus on *who* exchanges *what* and *what must be true before and after*.
- Example (right): Context says "Customer adds to cart" → interaction: Add to Cart; concepts: Shopping Cart, LineItem. Context says "User selects country for payment" → interaction: Select Country; concepts: Country, PaymentType.

**DO NOT** invent workflows or mechanics not present in the context.
- Example (wrong): Story "Express checkout" or concept "LoyaltyPoints" when context never mentions them. Right: Omit; if needed, state assumption.


---

---
title: Mechanics from evidence, not table of contents
impact: HIGH
---

## Mechanics from evidence, not table of contents

**DO** read evidence chunks for mechanical depth. For each candidate subtype, scan actions.json and terms.json for that name. Derive properties, operations, and collaborators from what the evidence says that variant does. A subtype is justified when the evidence describes different rules, formulas, state transitions, or interaction patterns.

**DO** verify each subtype has its own trigger, conditions, or resolution path in the source. Different mechanics = subtype. Same mechanics with different label = enum.

**DO NOT** infer subtypes from chapter titles, section headers, or bullet lists without reading the actual rule text. A table of contents that lists "Volume Discount, Loyalty Reward, Bundle Offer" under Promotions does not make them subtypes — only the rules for each do.

**DO NOT** create subtypes from variation axes or category lists when each item shares the same resolution logic. "Transaction types: Purchase, Return, Exchange" in a summary is a categorization; read the rules to see if each resolves differently.

- Example (wrong): Source has section "Transaction Types" with Purchase, Return, Exchange. You list those as subtypes. But the ToC categories are wrong — the mechanics show different resolution types (e.g. forward payment vs reversal vs disputed reversal). Right: Read the rules. Derive subtypes from resolution mechanics, not from ToC labels.
- Example (wrong): Source lists "Payment Methods: Credit Card, Bank Transfer, Invoice" and you model each as a subtype because they use different rails. But the mechanics are identical — same flow, different input. Right: PaymentMethod with `method_type {credit_card, bank_transfer, invoice}` — data field, not subtypes. Same mechanics with different input = variable, not subtype.


---

---
title: Subtypes vs enum — distinct mechanics required
impact: HIGH
---

## Subtypes vs enum — distinct mechanics required

**DO** use subtype when the evidence shows different properties, operations, or resolution mechanics for each variant. A subtype is a concept when it has its own rules — different validation, different settlement, different formulas, different state transitions.

**DO** use enum (or type property) when variants share the same logic and differ only by label. Same behavior, different data = enum. Format: `EnumType property_name {value1, value2, value3}`.

**DO NOT** derive subtypes from table of contents or section headers alone. Verify each subtype has distinct mechanics in the evidence (actions.json, terms.json, context chunks). If the source only lists names under a category without different rules per name, it's an enum.

**DO NOT** create both a parent "Type" or "Category" enum and subtypes that mirror it. Example (wrong): Transaction has `TransactionType type {purchase, refund, chargeback}` AND subtypes Purchase, Refund, Chargeback. Use one representation: either enum or subtypes with genuinely different mechanics.

- Example (right — subtype): Transaction subtypes Purchase, Refund, Chargeback — each has different validation, settlement, and reversal rules. Purchase: forward payment, creates obligation. Refund: reversal, requires original. Chargeback: disputed reversal, involves issuer. Each gets its own concept.
- Example (right — enum): Order has `OrderStatus status {pending, shipped, delivered}` — same state machine, different state. Or: LineItem has `ItemType type {product, service, subscription}` — same line-item logic, different label.
- Example (wrong): Transaction types Purchase, Return, Exchange as Transaction subtypes when the rules treat them the same way and only categorize by label. Right: `TransactionType type {purchase, return, exchange}` on Transaction.
- Example (wrong): Subtypes inferred from a bullet list "Promotions: Volume Discount, Loyalty Reward, Bundle Offer..." without reading whether each has different mechanics. Right: Read the actual rule text; if Volume Discount has tier-based calc, Loyalty Reward has points logic, Bundle has bundle rules, they're subtypes. If they're just names under a category, enum.


---



## Interaction Tree Rules (4)

Apply these rules when producing the interaction tree output for this phase.

---
title: Verb-noun format
impact: HIGH
order: 1
---

## Verb-noun format

Use verb-noun format for epic/story/step names and steps. Actor documented separately. Use active voice, base verb forms, and business language for all interaction text. Use behavioral language — describe what happens, not how it's implemented. Use domain concepts in steps (Given/When/Then) — not UI labels. Applies to all nodes (epic, story, step, scenario), including steps in or out of scenarios.
**DO** use Actor → verb noun [qualifiers]. Actor is documented separately, NOT in the name.
- Names: "Places Order" (actor: Customer); "Validates Payment" (actor: System); "Process Order Payment".
- **Step format** — strategy may specify When/Then (strict) or vanilla (verb-noun). Show both:
  - **When/Then:** `When **User** browses countries; Then **System** displays list of **Country** options`.
  - **Vanilla:** `User submits form`, `System validates payment`, `Select item from list`.
- Use base verb forms (infinitive/imperative): "Select Tokens", "Group Minions", "Process Payment".
- Use behavioral terms: "When user enters name; Then system saves character information" (not "system writes to JSON").
- Use domain concepts in steps: "User selects **Country**", "User enters **PaymentDetails**" (not "User clicks dropdown", "User fills form field").

**DO NOT** include actor in name, use noun-only, gerunds, or third-person singular.
**DO NOT** use technical implementation terms (config, json, api, sql, class, method). Use behavioral language instead.
- Wrong: "Customer Places Order" (actor in name). Right: "Places Order" (actor: Customer).
- Wrong: "Order submission", "Payment processing", "Form validation" (noun-only). Right: "Submit order", "Process payment", "Validate form".
- Wrong: "Submitting order", "Selects item", "Displays confirmation" (gerund/third-person). Right: "Submit order", "Select item", "Display confirmation".
- Wrong: "Then system saves to JSON file", "Then system parses XML", "Then system executes SQL query" (technical). Right: "Then system saves configuration data", "Then system processes data", "Then system retrieves data".
- Wrong: "User clicks dropdown", "User fills form field", "User submits button" (UI). Right: "User selects **Country**", "User enters **PaymentDetails**", "User submits payment".


---

---
title: Outcome-oriented language
impact: HIGH
order: 2
---

## Outcome-oriented language

Use outcome-oriented language over mechanism-oriented language. Focus on what is created or achieved, not how it's shown or communicated.

**DO** use verbs that describe artifacts and outcomes — name concepts by what they ARE or CREATE.
- Example (right): "System → displays power activation animation" (not "Visualizing Power Activation"); "System → provides combat outcome feedback" (not "Showing Combat Results"); "System → displays hit indicators" (not "Displaying Hit Information").

**DO NOT** use generic communication or mechanism verbs.
- Example (wrong): "Visualizing Power Activation", "Showing Combat Results", "Displaying Hit Information", "Presenting Configuration Options".
- Wrong: "Showing results", "Displaying information", "Visualizing data", "Presenting options", "Providing settings", "Enabling features", "Allowing access".


---

---
title: Story granularity
impact: MEDIUM-HIGH
order: 4
---

## Story granularity

**DO** break down by distinct requirements areas, distinct concept structure, or workflow steps; sufficient stories to capture rule detail.
- Example (right): Story "View Product Details", Story "Make Payment" (each has distinct logic). Story "Drive Bike", Story "Drive Car" (concept structure differs).

**DO NOT** collapse large rule sections into one story.
- Example (wrong): Story "All combat effects" or "All attack types" when the context has dozens of distinct rules. Right: Story "Apply damage effect", Story "Apply condition effect", Story "Resolve melee attack", etc.


---

---
title: Small and testable
impact: HIGH
order: 5
---

## Small and testable

Stories must be testable as complete interactions and deliverable independently. Story = testable outcome; Step = implementation detail.

**DO** create stories that can be tested and delivered independently.
- Example (right): "Customer → places order" (testable: order created, payment processed).
- Story = User/system outcome (testable independently with clear acceptance criteria).
- Step = Implementation detail (not testable alone, verified as part of parent story test).

**DO NOT** create stories too small to test meaningfully or make implementation steps into stories.
- Example (wrong): "Add order button" (can't test without full order flow); "Display error message" (can't test without validation context).
- Wrong: "Convert Diagram to StoryGraph Format", "Serialize Components to JSON", "Calculate Component Positions" (implementation steps, not testable alone).


---

