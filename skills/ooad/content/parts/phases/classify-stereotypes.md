# Classify stereotypes

**Skill:** abd-ooad — **Phase-id:** `classify-stereotypes` (Stage 3 — DDD patterns, p7).

**Upstream:** `inherit-interface-or-compose` (p6) — every class has typed properties, operations, relationships, and a structural mechanism (inherit / interface / compose).

**What this phase does:** Assign a single DDD stereotype to each class. Stereotypes are classification labels — they describe *what role the class plays in the domain*, not how it is implemented. They feed **`design-bounded-contexts`** (p8) and invariant scope in **Behaviour** (p9 onward).

---

## Stereotype reference

| Stereotype | What it means |
|-----------|--------------|
| `Entity` | Has identity (an ID); changes over time; tracked across operations |
| `ValueObject` | Defined by its value; immutable; no identity beyond its content |
| `Aggregate` | Root Entity that owns a consistency boundary; external access only via root |
| `DomainService` | Stateless operation that coordinates multiple entities; belongs in domain, not application |
| `Policy` | Captures a rule or decision criterion; often a predicate or strategy |
| `DomainEvent` | Something that happened in the domain; immutable record of a fact |
| `Role` | A contextual identity an Entity plays; extracted when one class is doing two jobs |
| `Process` | Orchestrates a multi-step workflow; may be stateful (saga) or stateless |
| `Factory` | Creates complex aggregates or entities; separates construction from use |

---

## How to classify

Work class by class. For each class:

1. Ask: does it have identity that persists across operations? → Entity or Aggregate candidate
2. Ask: is it defined entirely by its value, no lifecycle, no ID needed? → ValueObject
3. Ask: does it represent something that *happened*, immutable, timestamped? → DomainEvent
4. Ask: is it a stateless operation that does not naturally belong on any entity? → DomainService
5. Ask: does it capture a rule, decision, or policy that changes independently? → Policy
6. Ask: is it orchestrating a process across multiple steps/entities? → Process or Saga
7. Ask: is this class doing two jobs — one entity playing a role in a context? → split into Entity + Role

Apply one stereotype per class. If more than one fits, the class probably has hidden responsibilities — record a `Tension` note and consider splitting.

---

## Aggregate boundaries

If you classify a class as Aggregate, immediately mark:
- Which classes are inside the aggregate boundary (child entities and VOs)
- Which classes reference the aggregate root by ID only (external associations)

Aggregate boundaries are confirmed in `design-bounded-contexts` (p8). Do not finalise them here — but do flag aggregate candidates.

---

## Updates to the model

- Add the stereotype to each class in `domain-model.md`: `ClassName : << Entity >>`, `ClassName : << ValueObject >>`, etc.
- Replace any remaining `<< Kind? >>` provisional stubs with the confirmed stereotype
- If a `Role` is extracted from an Entity, add the new Role class and update its collaborators

---

## term-registry.md

Tag all model notes with `[p7]` — see `templates/domain model template.md` for the full tag table.

Common Notes labels added at this phase:

- `Classified - {{Stereotype}} {{reason}}` — final stereotype assigned; replaces any `Provisionally Classified` note from earlier phases
- `Promoted - {{from_target}} → Role {{reason}}` — hidden role extracted as its own class
- `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}` — class resists a single stereotype; may need to be split
- `Follow-up - {{question_or_action}}` — deferred; to be resolved at p8 aggregate boundaries

---

## Action Checklist

- [ ] Every class has exactly one stereotype in `domain-model.md`.
- [ ] No remaining `<< Kind? >>` provisional stubs.
- [ ] Aggregate candidates are flagged with an initial boundary sketch.
- [ ] Hidden roles extracted as separate classes where found.
- [ ] ValueObjects confirmed as immutable with no ID.
- [ ] `term-registry.md` updated — `Provisionally Classified` notes promoted to `Classified - {{Stereotype}}`.
- [ ] Tensions recorded for any class that resisted classification.

---

## Prompt

> Work class by class. Assign one stereotype — the one that best describes what role this class plays in the domain. If a class resists classification, that is a signal: it has two responsibilities. Name the tension, consider splitting, and move on. Do not invent roles; stereotypes come from domain behaviour already captured in the model.
