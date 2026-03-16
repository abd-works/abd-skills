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
   - include only concepts that appear central to the domain
   - prefer concepts that participate in interactions or state changes
   - avoid example-only roles unless they are real domain concepts

2. **Candidate Modules**
   - group concepts around likely mechanisms
   - modules should be broad and provisional

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
- stay shallow
- prefer fewer, stronger concepts over long noun lists
- do not include formulas or exact rule math
- if uncertain, mark as **candidate**, not final
- every concept should have a short interaction-oriented statement
- every epic should be grounded in **Concept** language
- every concept named in the interaction skeleton must exist in the guidance output

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

**ConceptA** — interacts with **ConceptB**
**ConceptB** — modifies **ConceptC**
**ConceptC** — results from **ConceptA**

## Mechanisms (likely)

- **MechanismA** — short description
- **MechanismB** — short description

## Actors (likely)

- **ActorA** — short description

## Extraction Guidance

### Priority Concepts
- **ConceptA**
- **ConceptB**

### Priority Mechanisms
- **MechanismA**
- **MechanismB**

### Variation Axes
- axis a
- axis b

### Synonym Hints
- **ConceptA**: alias 1, alias 2
- **ConceptB**: alias 3, alias 4
```

## Required JSON shape (concept_guidance_v1.json)

```json
{
  "priority_concepts": ["ConceptA", "ConceptB"],
  "concept_aliases": {
    "ConceptA": ["alias 1", "alias 2"],
    "ConceptB": ["alias 3", "alias 4"]
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

## Checkpoint 1

Human verifies domain framing before proceeding.


---

## Domain Model Rules (2)

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

