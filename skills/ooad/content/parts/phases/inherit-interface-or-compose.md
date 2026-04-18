# Inherit, interface or compose

**Skill:** abd-ooad — **Phase-id:** `inherit-interface-or-compose` (Stage 2 — Model, p6).

**Upstream:** `properties-methods-and-relationships` (p5) — every class has typed properties, operations, and explicit relationships.

**What this phase does:** For every relationship defined in p5, decide the structural mechanism. Three lenses — evaluated simultaneously for each relationship, not sequentially:

| Question | Answer → | Mechanism |
|----------|----------|-----------|
| Is A substitutable for B? Callers use them interchangeably? | yes | **Inherit** (is-a) |
| Do A and B share a contract (same interface) but are not substitutable? | yes | **Interface** |
| Does A hold or use B but is not B? | yes | **Compose** (has-a / uses-a) |

All three questions apply to every relationship at once. A composition can also satisfy an interface. Inheritance without substitutability is wrong — change it to composition or interface.

---

## Rules

**Inherit only when:**
- The subtype is substitutable for the parent in every caller context (Liskov)
- Callers actually use the parent type — otherwise the hierarchy is notional, not structural
- The behavioral difference is domain-driven, not infrastructure-driven (PSP brand differences belong in adapters, not domain subtypes)

**Interface when:**
- Two classes share a contract (method names and semantics) but are not subtypes of each other
- A port to an external system should be defined as a domain interface with infrastructure implementations
- Callers depend on the abstraction, not the concrete class

**Compose when:**
- A has B as a part — B has its own identity or lifecycle that is just used by A
- Behavior varies by swapping the composed part (strategy pattern)
- The relationship would require inheritance just to share one method — that is composition

---

## Decisions to record in the model

For each relationship from p5:

1. Write the mechanism next to the relationship in `domain-model.md`: `inherits`, `implements`, or `composes`
2. If inherit: add the subtype hierarchy to the model (`### Subtype : ParentClass`)
3. If interface: define the interface (`### InterfaceName : << Interface >>`) with the contracted methods
4. If compose: confirm the composition/association type already recorded in p5; no further model change needed unless the composition is a strategy (then make the type explicit)

---

## term-registry.md

Tag all model notes with `[p6]` — see `templates/domain model template.md` for the full tag table.

Common Notes labels added at this phase:

- `Classified - Inherit {{reason}}` — subtype confirmed; callers use polymorphism
- `Classified - Interface {{reason}}` — shared contract defined; implementations injected
- `Classified - Compose {{reason}}` — confirmed has-a; composition or strategy
- `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}` — unclear whether relationship warrants inheritance vs composition
- `Follow-up - {{question_or_action}}` — deferred hierarchy decisions

---

## Action Checklist

- [ ] Every relationship from p5 has an explicit mechanism: inherit, interface, or compose.
- [ ] Every inheritance decision passes the substitutability test — callers actually use the parent type.
- [ ] No inheritance for infrastructure variation (adapters, PSP brands) — these are compose.
- [ ] Every interface is defined with its contracted methods in `domain-model.md`.
- [ ] `term-registry.md` updated with `Classified` (Inherit / Interface / Compose) notes.
- [ ] Tensions recorded where mechanism is contested or unclear.

---

## Prompt

> For each relationship: ask all three questions simultaneously — is-a? shared contract? has-a? Pick the mechanism the model actually needs, not the one that feels familiar. If inheritance requires callers to use a type that no caller actually uses, it is wrong. Record the decision and the reason.
