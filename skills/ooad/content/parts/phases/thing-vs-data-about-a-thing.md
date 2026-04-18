# Thing vs data about a thing

**Skill:** abd-ooad — **Phase-id:** `thing-vs-data-about-a-thing` (Stage 1 — Scaffold, p3).

**Upstream:** `raw-candidates` (p3) — every noun has a `<< kind? >>` provisional stub and a `Provisionally Classified` note in `term-registry.md`.

**What this phase does:** For each provisional stub, apply the four identity questions to confirm the kind or demote it. Drop the `?` when confirmed; replace the stereotype when demoted. Record every decision as a `Classified` note in `term-registry.md`. All candidates leave this phase with a firm kind — no `?` carries into Structure.

---

## The four identity questions

For each `<< kind? >>` stub, ask:

- Does it exist **independently** (not just as data hanging off something else)?
- Can two instances be distinguished by **identity** (not just by value)?
- Does it **own behavior** — invariants, lifecycle, rules?
- Can it **change independently** of another object?

**If no to most → demote.** Replace `<< Entity? >>` with `<< ValueObject >>`, `<< Enum >>`, or drop to a property on another class. If the term doesn't warrant its own model element, mark `Rejected` in the registry.

---

## What you produce

For each stub in `domain-model.md`:

- **Confirmed:** rename `Name << Kind? >>` → `Name << Kind >>` (drop `?`). Add `[p4] Classified — Kind; {{reason}}` note.
- **Demoted:** replace stereotype with correct kind, or remove stub and note where the term lands (property on which class). Add `[p4] Classified — demoted to {{target}}; {{reason}}` note.
- **Renamed:** if two terms resolve to one aggregate, consolidate stubs and add `[p4] Renamed — {{old}} → {{new}} {{reason}}` note.

Update `term-registry.md` Target column and Notes for every term touched.

---

## term-registry.md

Tag model notes with `[p4]` — see `templates/domain model template.md` for the full tag table.

Common Notes labels added at this phase:

- `Classified - {{kind}} {{reason}}` — confirmed or demoted; kind is `Entity`, `ValueObject`, `Enum`, `Policy`, `Role`, `Event`, `Process`, `Property`
- `Renamed - {{old_name}} → {{new_name}} {{reason}}` — when two candidates resolve to one class
- `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}` — boundary still unclear; must be named before moving to Structure
- `Follow-up - {{question_or_action}}` — deferred only if genuinely blocked; must not carry unresolved `?` into Structure

---

## Action Checklist

- [ ] Every `<< kind? >>` stub from p3 has been visited.
- [ ] Confirmed stubs have `?` removed; `[p4] Classified` note added.
- [ ] Demoted terms have stereotype replaced or stub removed; note records where term lands.
- [ ] No `?` stereotype remains in `domain-model.md` after this phase.
- [ ] `term-registry.md` Target column updated for every term touched.
- [ ] All unresolved tensions named as `Tension` notes — none silently carried forward.

---

## Prompt

> For each `<< kind? >>` stub: apply the four questions, confirm or demote, drop the `?`, record the decision. A term with no clear answer gets a `Tension` note and a provisional decision — not silence.
