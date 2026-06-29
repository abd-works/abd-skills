---
name: bounded-context-map
catalog_garden_order: 8
catalogue_one_liner: >-
  Bounded context inventory with dependency arcs across three dimensions.
description: >-
  Map bounded contexts and their relationships so integration, collaboration, and translation are explicit. Use when module or service boundaries exist and the team needs to declare how they relate.
---
# abd-bounded-context-map

## Purpose

Make integration, ownership, and translation between contexts explicit — so teams know who owns what and how they communicate across boundaries.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these:

- **Hidden coupling** — Which contexts do people treat as independent but actually share data, vocabulary, or lifecycle?
- **Ownership ambiguity** — Where does one team's responsibility end and another's begin — and does everyone agree?
- **Translation cost** — Which boundary crossings silently corrupt meaning because the same word means different things on each side?
- **Missing context** — Is there a bounded context the team hasn't named yet because it lives inside someone's head or a spreadsheet?
- **Relationship direction** — For each dependency, which side sets the rules — and what happens when the downstream context disagrees?

---

## Output file

**Deliverables folder:** see `../common/skill-workflow.md` — Output file resolution.

**File name:** `bounded-context-map.md`. Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

Follow `../common/skill-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — bounded contexts, context maps, the three dimensions per dependency, relationship patterns (Shared Kernel, Customer/Supplier, Conformist, ACL, Open Host/Published Language, Separate Ways), and boundary heuristics.

### 2. Generate

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/bounded-context-map-template.md` | A single `bounded-context-map.md` — inventory of bounded contexts, dependency arcs with three dimensions each, decisions and tensions. |

**Quality bar:** Every bounded context has an owning team and scope description. Every dependency arc fills all three dimensions — domain mapping, integration mechanism, and team engagement model. Every relationship uses a named pattern from the DDD/ABD catalogue. Direction is explicit on every arc. No orphan contexts.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect the completed bounded context map as a reviewer.

- **Completeness** — every bounded context in the system appears in the inventory with owning team and scope.
- **Three dimensions** — every dependency arc has all three dimensions filled. No blanks, no "TBD" without a follow-up action.
- **Named patterns** — every team engagement model uses a recognized pattern (Shared Kernel, Customer/Supplier, Conformist, ACL, Open Host/Published Language, Separate Ways) or named collaboration model (Travelling Team Members, Service Provider, Enabler).
- **Direction** — every dependency states direction explicitly: upstream/downstream, mutual, or standalone.
- **No orphans** — every bounded context participates in at least one dependency or is explicitly declared standalone with a rationale.
- **Decisions and tensions** — open questions, contested boundaries, and deferred integrations are recorded, not hidden.
- **Consistency with domain language** — bounded context names appear in the project's Domain Language.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
