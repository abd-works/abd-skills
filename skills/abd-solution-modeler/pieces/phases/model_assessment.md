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
