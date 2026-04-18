# State and lifecycle

**Skill:** abd-ooad — **Phase-id:** `state-and-lifecycle` (Stage 4 — Behaviour, p10).

**Upstream:** `invariants` (p9) — invariants are attached; guards are defined on operations.

**What this phase does:** For every stateful entity and aggregate, define the complete lifecycle: all valid states, all allowed transitions, all illegal transitions, and the guard on each transition (which should already be an invariant from p9). The lifecycle makes the invariants structural — illegal transitions become unreachable or explicitly rejected.

---

## How to define a lifecycle

For each stateful entity:

1. **List all states** — every named state the entity can be in; use SCREAMING_SNAKE_CASE
2. **List allowed transitions** — for each state, which transitions are valid? → draw the forward edges
3. **List illegal transitions** — which transitions must be explicitly rejected? → these have guard clauses from p9
4. **Map domain events to transitions** — which state changes emit a domain event?
5. **Mark terminal states** — states with no outgoing transitions; the lifecycle ends here

---

## Notation

Write the state transition summary in `domain-model.md` as a `State:` block under the entity:

```
State: INITIATED → METHOD_SELECTED → AUTHORIZED → CAPTURED → SETTLED
Branches: FAILED (terminal), CANCELLED (if policy allows)
Illegal: SETTLED → AUTHORIZED (rejected; no reverse)
Events: PaymentSettled on SETTLED
```

---

## Domain events

Domain events are emitted when a state transition represents a fact that other BCs care about. Every domain event:

- Is named in the past tense: `PaymentSettled`, `RefundRequested`
- Is immutable
- Carries the minimum data needed by subscribers
- Is emitted by the aggregate operation that causes the transition

---

## Cross-BC lifecycle dependencies

If BC-B must not act until BC-A reaches a state (e.g., "warehouse must not pick before payment is settled"), this is a cross-BC ordering constraint. Record it as a `Follow-up` for integration test scope — it is not enforced in the domain model, it is enforced at the boundary via events and subscriptions.

---

## term-registry.md

Tag all model notes with `[p10]` — see `templates/domain model template.md` for the full tag table.

Common Notes labels added at this phase:

- `State Candidate - states: {{list}} illegal transitions: {{list}}` — full state set and which transitions are rejected
- `Invariant - {{rule_that_must_always_hold}}` — transition guard confirmed (cross-reference to p9 if already recorded)
- `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}` — ambiguous states, conflicting spec transitions, configurable TTLs
- `Follow-up - {{question_or_action}}` — cross-BC ordering constraints; deferred lifecycle decisions

---

## Action Checklist

- [ ] Every stateful entity has a complete state list in `domain-model.md`.
- [ ] Every allowed and illegal transition is documented.
- [ ] Every transition guard maps to an invariant from p9.
- [ ] Domain events identified and named for all significant state transitions.
- [ ] Cross-BC lifecycle dependencies recorded as `Follow-up` notes.
- [ ] `term-registry.md` updated with `State Candidate`, `Invariant` (cross-reference), and `Tension` notes.

---

## Prompt

> For each stateful entity: list every state, every allowed transition, every illegal one. Map each guard to an invariant. Name the events that fire on significant transitions. If a transition requires a cross-BC ordering constraint, record it as a follow-up — it belongs in integration tests, not in the domain model.
