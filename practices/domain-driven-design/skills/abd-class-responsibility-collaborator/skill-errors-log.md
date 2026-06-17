# Skill Errors Log — abd-class-responsibility-collaborator

---

### Receiver given responsibility to call the thing that changes it

- **Context:** CRC for Check Resolution — `remove by source` / `remove by applied effect` on Imposed Conditions
- **DO NOT:** Give the object being changed a responsibility that references back to the thing doing the changing. The changed object is passive — it gets told, it doesn't call out.
- **DO:** Put the removal responsibility on the actor that drives it. The actor knows what it created and tells the collection to remove.
- **Example (wrong):** `remove by applied effect | Applied Effect, Imposed Condition` on Imposed Conditions — the collection calling back to the thing that modifies it.
- **Example (correct):** Removal logic lives on `Applied Effect`; when it ends, it removes the imposed conditions it created. Imposed Conditions just receives the removal.
- **Likely source:** `prompt gap` — overlaps with existing `receiver-not-responsible-for-receiving` rule but was not applied to collection removal patterns.
- **Status:** confirmed

---

### Responsibility placed on base class pointing to its own subtype

- **Context:** CRC for Check Resolution — `team assistance | Team Check` on Check
- **DO NOT:** Put a responsibility on a base class whose only collaborator is one of its own subtypes. The subtype knows what it does; the base class doesn't reference its children.
- **DO:** Let the subtype own its own behavior. If there's nothing to say on the base, say nothing.
- **Example (wrong):** `team assistance | Team Check` on Check — a base class pointing at its own subtype as a collaborator.
- **Example (correct):** Remove entirely. Team Check owns `perform check` with its helper logic; Check doesn't know Team Check exists.
- **Likely source:** `instruction not read` — base classes must not reference their subtypes as collaborators.
- **Status:** confirmed

---

### Object traversal described as an invariant instead of listed as collaborators

- **Context:** CRC for Check Resolution — Trait `penalty` / `modifier`
- **DO NOT:** Use an invariant to describe how to navigate to a value through other objects. Navigation is collaborators.
- **DO:** List every object in the traversal chain as a collaborator. Invariants are for rules and constraints, not for describing how you walk the object graph.
- **Example (wrong):** `penalty | Character` with invariant `retrieved from character's imposed conditions applicable to this trait`
- **Example (correct):** `modifier | Character, Imposed Conditions, Condition, Game Modifier` — the full traversal chain is visible in the collaborator column.
- **Likely source:** `prompt gap` — no rule stated that object traversal paths belong in collaborators, not invariants.
- **Status:** confirmed

---

### Responsibility name repeats the class name it belongs to

- **Context:** CRC for Check Resolution — `trait penalty` on Imposed Conditions
- **DO NOT:** Include the owning class name in a responsibility name. The class context is implied.
- **DO:** Name the responsibility after the concept alone.
- **Example (wrong):** `trait penalty | Trait` on Imposed Conditions — "trait" is redundant; you're already on Imposed Conditions asking for a penalty.
- **Example (correct):** `penalty | Trait`
- **Likely source:** `prompt gap` — no rule stated that responsibility names must not echo the class they belong to or the collaborator they reference.
- **Status:** confirmed

---

### Responsibility named as a process description instead of plain English domain action

- **Context:** CRC for Check Resolution — Effect `handle resistance check outcome`
- **DO NOT:** Name a responsibility as a process step or handler description. These are implementation framing, not domain language.
- **DO:** Name it as the domain action in plain English — what the class actually does from the outside.
- **Example (wrong):** `handle resistance check outcome | Graded Check Result, Imposed Conditions`
- **Example (correct):** `resist | Character, Trait, Graded Check Result` — the Effect can be resisted by a Character using a Trait; result is a Graded Check Result.
- **Likely source:** `prompt gap` — no rule stated that responsibility names must be plain-English domain actions, not process-handler phrases.
- **Status:** confirmed

---

### Collaborator included that belongs to a different module's scope

- **Context:** CRC for Check Resolution — Effect `resist` responsibility
- **DO NOT:** Include a collaborator that handles consequences outside this module's scope.
- **DO:** Stop at the boundary. What happens after a failure (Imposed Conditions on Character) is the Character Construction / Condition module's concern, not Check Resolution's.
- **Example (wrong):** `resist | Graded Check Result, Imposed Conditions` — Imposed Conditions is what the Character does with the result, not what Effect does during resistance.
- **Example (correct):** `resist | Character, Trait, Graded Check Result` — Effect drives the check; what Character does with the Graded Check Result is out of scope.
- **Likely source:** `prompt gap` — no rule stated that collaborators must stop at module boundaries.
- **Status:** confirmed

---

### Responsibility name includes SET or GET

- **Context:** CRC for Check Resolution — Effect `imposed condition set`
- **DO NOT:** Append `set`, `get`, `list`, `collection`, or similar accessor/container words to a responsibility name. These are implementation noise, not domain language.
- **DO:** Name the responsibility after the concept itself.
- **Example (wrong):** `imposed condition set | Condition`
- **Example (correct):** `imposed conditions | Condition`
- **Likely source:** `prompt gap` — no rule stated that SET/GET/LIST suffixes are forbidden in responsibility names.
- **Status:** confirmed

---

### One-time computation hidden behind a property responsibility

- **Context:** CRC for Check Resolution — Team Check helper rolls / circumstance modifier
- **DO NOT:** Model a one-time computation as a property responsibility. A property implies it can be read at any time; hiding a computation behind it suggests it re-executes on every read.
- **DO:** Place one-time computations inside the operation where they actually happen. If something is computed once and then applied, it belongs as an invariant on the operation that drives it, not as a standalone property responsibility.
- **Example (wrong):** `circumstance modifier | Check, Difficulty Class, Check Result` on Team Check — implies helper rolls could be re-triggered whenever the modifier is read.
- **Example (correct):** `perform check | Check, Difficulty Class, Check Result` with invariant that helpers run once, modifier is computed once, leader's check runs once.
- **Likely source:** `prompt gap` — no rule stated that consistency of execution (once vs. many) must be reflected in whether something is modeled as a property or an operation.
- **Status:** confirmed

---

### Responsibility name embeds its value conditions instead of naming the concept

- **Context:** CRC rendering for Check Resolution — Check Result `status`
- **DO NOT:** Put the possible values or conditions in the responsibility name. The name is the concept; the invariant holds the conditions.
- **DO:** Name the responsibility after the concept alone. Put success/failure conditions in the invariant.
- **Example (wrong):** `success or failure status | (success or failure)` — conditions appear in both the name and the collaborator column.
- **Example (correct):** `status | (success or failure)` — name is the concept; invariant says when each value applies.
- **Likely source:** `prompt gap` — no rule stated that responsibility names must not embed their own value space.
- **Status:** confirmed

---

### Constraint expressed only as invariant when it deserves a named operation

- **Context:** CRC for Check Resolution — Rank's rank arithmetic rule; learned from user's `Add` edit
- **DO NOT:** Bury a constraint this fundamental as an invariant on another responsibility. If the operation exists and is callable, name it.
- **DO:** Give it a responsibility name (`Add`) that makes the constraint a first-class operation with explicit collaborators.
- **Example (wrong):** Rank arithmetic rule buried as an invariant on `real-world value` — callers cannot see it as an operation.
- **Example (correct):** `Add | Rank, Measurement, MEASUREMENT_TYPE` — the operation is named and its collaborators are explicit.
- **Likely source:** `prompt gap` — no rule stated that inviolable operations should be named responsibilities, not just invariants.
- **Status:** confirmed

---

### Responsibility placed on the wrong class — not where the caller goes

- **Context:** CRC for Check Resolution — `perform check`; learned from user's Trait edit
- **DO NOT:** Place a responsibility only on the class that does the work internally if callers go to a different class first.
- **DO:** Put the responsibility on the class the caller actually talks to.
- **Example (wrong):** `perform check` missing from Trait — callers ask a Trait to perform a check, not Check directly.
- **Example (correct):** `perform check | Check, Rank, Check Result` on Trait — the caller goes to Trait; Trait collaborates with Check.
- **Likely source:** `prompt gap` — no rule stated that responsibilities should be placed at the caller's entry point, not just at the implementer.
- **Status:** confirmed

---

### Enum class defined without its constant values

- **Context:** CRC for Check Resolution — Measurement Type / MEASUREMENT_TYPE; learned from user's enum edit
- **DO NOT:** Define an enum concept with only a name and invariant listing values as prose.
- **DO:** List the constants with their values directly in the CRC block.
- **Example (wrong):** `### **Measurement Type**` with `invariant: one of mass, time, distance, or volume` — values are prose, not named constants.
- **Example (correct):** `### **MEASUREMENT_TYPE**` with `MASS=1 / TIME=2 / DISTANCE=3 / VOLUME=4` — constants are named and valued.
- **Likely source:** `prompt gap` — no rule stated that enum CRC blocks must define their constants explicitly.
- **Status:** confirmed

---

### Stale collaborator reference after class deletion

- **Context:** CRC rendering for Check Resolution — Effect boundary class
- **DO NOT:** Leave a collaborator reference pointing to a class that was removed during review.
- **DO:** Update collaborator columns immediately when a class is deleted; find which class now plays that role.
- **Example (wrong):** `handle resistance check outcome | Resistance Check, Imposed Conditions` after Resistance Check was removed.
- **Example (correct):** `handle resistance check outcome | Graded Check Result, Imposed Conditions`.
- **Likely source:** `automation gap` — no cross-reference check exists between collaborator columns and the class list.
- **Status:** confirmed

---

### Inherited responsibility repeated in subtype with no distinguishing invariant

- **Context:** CRC rendering for Check Resolution — Routine Check (and general subtype pattern)
- **DO NOT:** Repeat a parent responsibility in a subtype block when the subtype adds no invariant or collaborator that changes how that responsibility works. It is noise.
- **DO:** Only include a responsibility in a subtype if it carries a new invariant, a different collaborator, or both. Pure clones of the parent row are omitted.
- **Example (wrong):** `using trait | Trait` on Routine Check — identical to Check; no distinguishing invariant.
- **Example (correct):** Omit the row entirely. If the eligibility nuance exists, fold it into the responsibility that IS different (`roll total`).
- **Likely source:** `prompt gap` — no rule stated that subtype CRC blocks must only contain rows that differ from the parent.
- **Status:** confirmed

---

### Usage pattern modeled as a class instead of an instance

- **Context:** CRC rendering for Check Resolution — Resistance Check
- **DO NOT:** Create a class for what is just a particular configuration of an existing class — a specific trait choice and DC source do not make a new type.
- **DO:** Recognize that if a "class" only carries invariants on inherited responsibilities with no structural difference, it is an instance/usage pattern, not a class.
- **Example (wrong):** `Resistance Check : Check` as a named class — it is just a `Check` run with a defense trait against an Effect DC.
- **Example (correct):** No `Resistance Check` class; the usage pattern is documented as an invariant on the mechanism that triggers it (e.g., on Effect's `handle resistance check outcome`).
- **Likely source:** `prompt gap` — no rule stated that subtypes must have structural differences, not just named parameter choices.
- **Status:** confirmed

---

### Subtype added new responsibility names for inherited responsibilities with different parameters

- **Context:** CRC rendering for Check Resolution — Resistance Check
- **DO NOT:** Add new responsibility names in a subtype for things that are just inherited responsibilities with specific invariants — the trait used, the source of the DC, the type of result produced.
- **DO:** Use the same inherited responsibility names (`using trait`, `difficulty class`, `resolve`); express what is specific about the subtype as invariants on those responsibilities.
- **Example (wrong):** `defense bonus modifier | Trait`, `effect difficulty class | Effect`, `produces graded result | Graded Check Result` as new responsibilities on Resistance Check.
- **Example (wrong):** `routine fixed value | (integer 10)`, `routine eligibility | Trait`, `fallback to standard roll | Check` as new responsibilities on Routine Check.
- **Example (correct):** `using trait | Trait` with invariant naming the defense trait; `difficulty class | Effect` with invariant DC = 10 + effect rank; `resolve | Graded Check Result` with invariant it always produces a Graded Check Result. Same pattern for Routine Check: `roll total`, `using trait`, `resolve` with mode invariants.
- **Likely source:** `prompt gap` — same root as subtype renaming; no rule stated inherited responsibilities must keep their names even when their parameters or outcomes specialise.
- **Status:** confirmed

---

### Relationship obscured behind a "mapping" property instead of traced explicitly

- **Context:** CRC rendering for Check Resolution — Graded Check Result, Resistance Check
- **DO NOT:** Name a property `X mapping` when the class simply holds a resulting value. "Mapping" hides which classes are actually involved and where the mapping logic lives.
- **DO:** Name the property after what the class holds (`resulting condition`); put the mapping logic on the class that owns it (`Effect`); do not duplicate the mapping as a responsibility on classes that only consume the result.
- **Example (wrong):** `resistance failure condition mapping | Condition` on Graded Check Result; `degree of failure condition mapping | Graded Check Result, Condition` on Resistance Check.
- **Example (correct):** `resulting condition | Condition` on Graded Check Result with invariant `the condition is determined by the degree and the effect's condition set`; no mapping row on Resistance Check — that belongs to Effect.
- **Likely source:** `prompt gap` — no rule stated that mapping relationships must be traced to their owner class, not duplicated as vague properties on consumers.
- **Status:** confirmed

---

### Subtype responsibility renamed instead of inheriting with new invariants

- **Context:** CRC rendering for Check Resolution — Opposed Check
- **DO NOT:** Rename an inherited responsibility in a subtype just because it works differently. Do not add a new responsibility row for a rule variation.
- **DO:** Keep the same responsibility name as the parent; express the variation as additional invariants or collaborators on that responsibility.
- **Example (wrong):** `opposing roll total as difficulty class | Check Result` as a new responsibility on Opposed Check.
- **Example (wrong):** `passive opposition difficulty class | Trait` as a second separate responsibility — it is still `difficulty class`, just with a different mode invariant.
- **Example (wrong):** `comparison rank resolution | Rank` — it is still `resolve`, just with a mode invariant that skips the d20.
- **Example (correct):** `difficulty class | Trait, Check Result` — same responsibility name as Check; active and passive mode rules both expressed as invariants on that one responsibility. Same pattern for `resolve`: mode variations are invariants, not new responsibility names.
- **Likely source:** `prompt gap` — no rule stated that subtype responsibilities must preserve the parent's responsibility name.
- **Status:** confirmed

---

### Variant rule written as separate responsibility instead of invariant on existing one

- **Context:** CRC rendering for Check Resolution — Opposed Check, tie-break by bonus
- **DO NOT:** Add a new responsibility row for a rule that applies under a specific condition of an existing responsibility.
- **DO:** Add it as an additional invariant on the existing responsibility it constrains.
- **Example (wrong):** `tie-break by bonus | (trait bonus comparison)` as a separate responsibility on Opposed Check.
- **Example (correct):** Second invariant on `difficulty class`: `on tied roll totals, the higher trait bonus wins; if bonuses also tie, a tie-break d20 decides`.
- **Likely source:** `prompt gap` — no rule stated that conditional sub-rules belong as invariants, not new responsibility rows.
- **Status:** confirmed

---

### Success/failure direction duplicated as two properties instead of one

- **Context:** CRC rendering for Check Resolution — Graded Check Result
- **DO NOT:** Create two properties (`degree of success`, `degree of failure`) when they are the same value read through an inherited status property.
- **DO:** Use one property (`degree`) and let the inherited `success or failure status` carry the direction.
- **Example (wrong):** `degree of success | (1–4)` and `degree of failure | (1–4)` as two separate properties on Graded Check Result.
- **Example (correct):** `degree | (1–4)` — combined with inherited `success or failure status`, callers know the direction without duplication.
- **Likely source:** `prompt gap` — no rule stated that inherited state must not be re-expressed as duplicated property names in subtypes.
- **Status:** confirmed

---

### Responsibility label used instead of concept name

- **Context:** CRC rendering for Check Resolution — Rank class
- **DO NOT:** Use the CRC responsibility label as a property name when the label describes a structural rule, not a state the class holds.
- **DO:** Name the property after what the class actually carries; put the structural rule in an invariant.
- **Example (wrong):** `doubling scale step | Measurement` rendered as property `doubling scale step` in the diagram — "doubling scale step" is not a thing Rank holds, it's describing how the scale works.
- **Example (correct):** `real-world value | Measurement` as the responsibility; the halving rule lives as an invariant.
- **Likely source:** `prompt gap` — no rule existed stating responsibility labels must name state, not describe mechanics.
- **Status:** confirmed

---

### Domain enumeration written as parenthetical instead of named class

- **Context:** CRC rendering for Check Resolution — Measurement class
- **DO NOT:** Write a domain-named enumeration (a constrained set of named values with domain meaning) as a parenthetical in the collaborator column.
- **DO:** Model it as a named concept class with the values listed as an invariant; reference it by name as the collaborator.
- **Example (wrong):** `dimension type | (mass, time, distance, or volume)`
- **Example (correct):** `dimension type | Measurement Type` where `### **Measurement Type**` carries `invariant: one of mass, time, distance, or volume`.
- **Likely source:** `prompt gap` — the `collaborators-from-sketch` rule explicitly permitted parentheticals for enums; rule has been updated to restrict parentheticals to true primitives only.
- **Status:** confirmed

---

### Responsibility named after implementation detail, not public API

- **Context:** CRC rendering for Check Resolution — Check Result class
- **DO NOT:** Name a responsibility after the internal mechanism that sets it (`natural 20 degree upgrade`, `natural 20 indicator`).
- **DO:** Name it after what a caller would ask for — the observable state from the outside.
- **Example (wrong):** `natural 20 degree upgrade | (natural 20 indicator)`
- **Example (correct):** `is critical | (true or false)`
- **Likely source:** `prompt gap` — no rule existed requiring responsibility names to reflect the public-facing query, not the internal trigger.
- **Status:** confirmed

---

### Invariant placed on wrong class — references concept that class does not have

- **Context:** CRC rendering for Check Resolution — Check Result vs Graded Check Result
- **DO NOT:** Place an invariant on a class that references a concept (degree) the class does not own.
- **DO:** Move the invariant to the class that owns the referenced concept.
- **Example (wrong):** Invariant `a natural 20 always increases the degree of success by one` on `Check Result`, which has no degree.
- **Example (correct):** Invariant `if is critical, increase degree of success by one after normal calculation` on `Graded Check Result`, under `degree of success`.
- **Likely source:** `prompt gap` — no rule existed requiring invariant placement to be validated against the responsibilities of the class it sits on.
- **Status:** confirmed
