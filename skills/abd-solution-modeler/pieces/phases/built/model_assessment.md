# Phase 11 — Scenario Walkthrough

**Actor:** AI + Human |

## Purpose

Validate design by walking through scenarios at two levels. A model that looks elegant but fails in message flow is not good OOAD.

## Trigger

scenario walkthrough, walk through scenarios, validate design

## Inputs

`generated/interaction_model/interaction_tree.md`, `generated/domain/refined_domain_model.md`

## Outputs

`generated/domain/model_assessment.md`

---

## Walkthrough Selection

**Rule 1 — Cross-cutting coverage:** Pick the top 3–5 stories by concept count (count `**Concept**` entries in the `Concepts:` line). These are highest risk for ownership errors across module boundaries.

**Rule 2 — Epic coverage:** Add 1 story from each epic not already covered by the cross-cutting picks. Pick the highest-concept-count story in that epic.

Do **not** pick walkthroughs from background knowledge — select from the interaction tree by concept count.

---

## Walkthrough Paths

For each selected story, walk **all applicable paths:**

- **Happy path** — normal success
- **Error path** — invalid input or precondition failure
- **Edge case** — boundary values (rank = 0, DC exactly met, max trade-off)
- **Exception path** — rule override, immunity, special condition
- **Stateful repetition** — what happens when the same action repeats (Grab maintained, Condition stacked again)
- **Alternate variation mode** — different subtype (Affliction vs Damage, Grab vs Disarm)
- **Recovery / retry / cancellation** — HeroPoint reroll, escaping Grab, recovering from Condition

---

## Two-Level Validation

For each walkthrough path:

**1. Scenario flow** — What happens in the domain? Is the sequence correct?

**2. Message flow** — Which object sends what message to whom? Does the receiver know enough to act? Is the sender delegating a decision or making it centrally?

Message flow exposes:
- Missing objects
- Misplaced behavior
- Centralization (one object making all decisions)
- Fake relationships (connected but no message flows)
- State with no owner
- Rules with no owner

---

## Anemia / Centralization Critique

After walkthroughs, explicitly attack the model before accepting it.

**Look for:**
- Centralized handlers, resolvers, or managers — who is doing too much?
- Anemic entities — objects with no decisions, just data
- Data bags — objects that hold state but delegate all behavior
- Config-holder pseudo-objects
- Orphan concepts — referenced in interactions but not in the model
- State with no owner — who holds it? who changes it?
- Rules with no owner — which object enforces this rule?
- Fake inheritance — shared fields only, no shared semantics
- Type/mode/effect switches that should be polymorphism
- Orchestration making domain decisions (should be delegating)
- Relationships with no behavioral significance

For each issue found: propose a concrete correction.

---

## Inheritance Test

Test every class that uses inheritance or that has subtypes:

1. **Shared identity or shared algorithm?** If only shared algorithm, consider strategy, policy, or composition instead.
2. **Stable substitutability?** Can every subtype stand in for the base without breaking behavior?
3. **Shared invariants?** Do subtypes inherit meaningful behavior and rules — not just fields?
4. **Variation in behavior or just configuration?** If difference is data or config, do not use inheritance — use objects or examples instead.

Good inheritance appears when:
- The domain itself has a stable is-a structure
- The base has real semantics that subtypes preserve
- Subtypes share meaningful invariants and protocol

---

## Output Format

```
## Walkthrough N — [Story Name] ([concept count] concepts)

**Paths walked:** happy | error | edge | exception | stateful | variation | recovery

**Scenario flow:**
[prose: what happens]

**Message flow:**
[object.method() → receiver.method() chain with rationale]

**Issues found:**
- [issue type]: [description] → [proposed fix]

**Critique notes:**
- [anemia | centralization | orphan | fake inheritance | etc.]
```

After all walkthroughs:

```
## Anemia / Centralization Critique Summary
[table of issues and fixes]

## Inheritance Validation
[table: class | subtype justified? | fix if not]

## Proposed Corrections
[numbered list]
```


---

## Domain Model Rules (2)

Apply these rules when producing the domain model output for this phase.

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
title: Scenario / Message Walkthrough Validation
impact: HIGH
---

## Scenario / Message Walkthrough

Make sure the model can actually behave. A model that looks elegant but fails in message flow is not good OOAD.

**Run walkthroughs for:**
- Happy path
- Error path
- Edge case
- Exception path
- Stateful repetition
- Alternate variation mode
- Recovery, retry, or cancellation where relevant

**Validate at two levels:**

**Scenario flow:** What happens in the domain?

**Message flow:** Which object sends what message to whom? Does the receiver know enough to act? Is the sender delegating a decision or making it centrally?

**This step exposes:** missing objects, misplaced behavior, centralization, fake relationships, state with no owner.

**DO NOT** truncate. Full Model Assessment requires multiple scenario walkthroughs with message flow (happy path, error path, edge case, stateful repetition, alternate variation, recovery where relevant). Persist the full assessment in run-N-ooad.md. A one-line note is insufficient.


---



## Interaction Tree Rules (6)

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

---
title: Example tables match Domain Model
impact: HIGH
---

## Example tables must align with Domain Model

**DO** ensure every example table corresponds to a domain concept in the Domain Model. Table columns must match the concept's properties. Table relationships must match the Domain Model's concept relationships (composition, aggregation). Every `**Concept**` referenced in Pre-Condition, Trigger, or Response labels must have a corresponding example table (or inherit one). Every example table must be referenced via `**Concept**` in labels — no orphaned tables.
- Example (right): Domain Model has `Country` with properties `country_code`, `country_name`. Example table: `Selected Country: | scenario | country_code | country_name |`. Domain Model has `User` → `Session` (composition). Tables appear in order: `Logged In User`, then `Active User Session` — relationship expressed through table ordering.

**DO** use source entity data in tables, not aggregated or calculated values. Show the actual records that produce the outcome. If a scenario computes a result, the table shows the inputs, not the output count.
- Example (right): `UpdateReport (renames): | original_name | new_name | parent |` — shows actual renamed entities.
- Example (wrong): `UpdateReport: | renames_count | new_count | | 1 | 2 |` — counts defer real work; where do these numbers come from?

**DO** express table relationships through table ordering and qualifier names — not through ID columns. IDs are implementation concerns. Domain Model says `Epic` contains `SubEpic`; tables appear in that order: `Epic` first, then `SubEpic (child of Epic)`.
- Example (right): `User: | user_name | user_role |` then `Session: | user_name | session_id | expires_at |` — connected by domain attribute, not by `user_id` foreign key.

**DO NOT** have `**Concept**` in labels without a matching example table. Do not have example tables that no label references. Do not invent column names not in the Domain Model — use the concept's actual property names.
- Example (wrong): Steps reference `**PaymentType**` but no PaymentType example table exists. Or: `Entitlement` table exists but no step mentions `**Entitlement**`.
- Example (wrong): Domain has `recipient_name` but table uses `payee` or `beneficiary_label`.

**DO NOT** flatten related concepts into one table or use lookup-style tables with ID columns for joining. Each concept gets its own table; relationships are expressed through ordering and qualifiers.
- Example (wrong): `| enterprise_id | recipient_id | account_id |` — flat table loses relationship structure. Right: separate tables for Enterprise, Recipient, Account in domain relationship order.


---

---
title: Scaffold pattern not enumeration
impact: HIGH
---

## Scaffold pattern not enumeration

The first cut of `interaction-tree.md` and `domain-model.md` establishes the pattern for each epic. Later phases expand and refine. If the first cut enumerates everything, later phases have nothing to do.

**DO** detail 2-3 representative stories per epic/sub-epic with full fields (Trigger, Response, Pre-Condition, domain concepts). List remaining stories by name only with "N more stories following this pattern based on [specific items]."
- Example (right): Two stories under a sub-epic shown in full with Trigger/Response and domain concepts; then "4 more stories following this pattern: [Story A], [Story B], [Story C], [Story D]."

**DO** have the session scaffold reference the output files and list every story by name with exact counts. Mark which stories have full trigger/response detail *(detailed)* and which are listed by name only. Use "N detailed + N more = total" counts per sub-epic that sum to the epic total.
- Example (right): Session scaffold says "See `interaction-tree.md` for full trigger/response detail on stories marked *(detailed)*." then lists: "Configure **Abilities** (2 stories): Set **AbilityRank** *(detailed)*, Validate **AbilityRank** *(detailed)*". Epic total: "16 sub-epics, 66 stories".
- Example (right): "Configure **Damage** Powers [MG1] (1 detailed + 4 more = 5 stories): Configure **Damage** *(detailed)*, 4 more following this pattern: Configure **Blast**, Configure **MentalBlast**, Configure **EnergyAura**, Configure **Strike**"
- Example (wrong): "Configure **Damage** Powers | 5 | DamageEffect, ResistanceCheck" — a table row with a count and concept names but no story names, no *(detailed)* markers, no reference to where the full content lives.
- Example (wrong): "~55 stories" when the actual count is 66 — approximate counts lose trust and make it impossible to verify completeness.

**DO NOT** enumerate every story with full detail in the first cut. The first cut is not the finished map — it is the pattern that runs expand.
- Example (wrong): All 6 stories in a sub-epic shown with full Trigger, Response, Pre-Condition, and domain concepts in the first-cut interaction-tree.md. Runs then have nothing to add for that sub-epic.


---

