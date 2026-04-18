# Check — hidden roles

**Skill:** abd-ooad — **Validator-id:** `check-hidden-roles`.

**When to run:** After `classify-stereotypes` (p7). Can also be applied when a generic noun (User, Actor, Person, Account) appears in the model.

**What this validator does:** Ask whether a single noun is covering multiple distinct roles in different contexts. A smashed abstraction is one class carrying two distinct identities — the check surfaces it so the roles can be separated.

---

## The test

For each generic or high-traffic class:

> *In context A, what does this class do and what does it know?*
> *In context B, what does this class do and what does it know?*

If contexts A and B have different properties, different operations, and different collaborators — the noun covers two roles and needs to be split.

---

## Common smash signals

- A single `User` class used for: payer identity, merchant config, admin action, and audit actor — these are four distinct roles
- A class that has `isAdmin`, `isMerchant`, `isCustomer` flags — each flag is a hidden role
- Operations that check `if type == X / else type == Y` on the same object — the branches are roles
- A class that collaborates with completely different BCs depending on context
- Generic names: `Account`, `Party`, `Actor`, `Person` — always check these

---

## Outcome

For each hidden role found:

- Name the distinct roles explicitly
- Decide: is the original class still needed as a base, or does it become an `Entity` holding references?
- Add the new role class(es) to `domain-model.md`
- Record `Role Separation` note in `term-registry.md`
- Update collaborator lists for affected classes

References to external BCs (e.g., `payerRef`, `merchantRef`) are **references**, not modeled roles inside this BC — record them as `Follow-up` if the referenced entity belongs elsewhere.

---

## term-registry.md notes at this validator

- `Role Separation - {{merged_role}} splits into: {{role_a}}, {{role_b}}` — hidden role extracted from a smashed abstraction
- `Classified - Role {{reason}}` — role confirmed and added to the model
- `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}` — role ownership is contested between BCs or organisational boundaries
- `Follow-up - {{question_or_action}}` — deferred role boundary; cross-BC identity question

---

## Checklist

- [ ] All generic nouns checked for hidden roles.
- [ ] Role smashes named and `Role Separation` notes recorded in `term-registry.md`.
- [ ] New role classes added to `domain-model.md`.
- [ ] Collaborator lists updated for affected classes.
- [ ] Cross-BC references confirmed as references (not rich classes inside this BC).
- [ ] Deferred role boundaries recorded as `Follow-up` with reason.
