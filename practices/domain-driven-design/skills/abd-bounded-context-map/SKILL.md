---
name: bounded-context-map
catalog_garden_tier: practice
catalog_garden_order: 8
catalogue_one_liner: >-
  Bounded context inventory with dependency arcs across three dimensions.
description: >-
  Map bounded contexts and their relationships so integration strategy, team
  collaboration, and domain translation are explicit before they are discovered
  in production. Use when module or service boundaries exist and the team needs
  to declare how they relate and integrate, when multiple teams own different
  parts of the domain, or when an architecture review requires a global view
  of model contexts and their points of contact.
---
# abd-bounded-context-map

## Purpose

Teams working across multiple models, services, or subsystems need a single shared picture of how those pieces relate — which concepts cross boundaries, how the systems talk to each other, and how the teams will collaborate. Without that picture, integration strategy is discovered in production, translation is ad hoc, and team dependencies are invisible until they block someone. This skill produces a **Bounded Context Map**: a named inventory of every bounded context with every dependency declared across three explicit dimensions — domain mapping, integration mechanism, and team engagement model — so the architecture is honest and the team structure matches.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `bounded-context-map.md`. Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — bounded contexts, context maps, the three dimensions per dependency, relationship patterns (Shared Kernel, Customer/Supplier, Conformist, ACL, Open Host/Published Language, Separate Ways), and boundary heuristics.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/bounded-context-map-template.md` | A single `bounded-context-map.md` — inventory of bounded contexts, dependency arcs with three dimensions each, decisions and tensions. |

**Quality bar:** Every bounded context has an owning team and scope description. Every dependency arc fills all three dimensions — domain mapping, integration mechanism, and team engagement model. Every relationship uses a named pattern from the DDD/ABD catalogue. Direction is explicit on every arc. No orphan contexts.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-bounded-context-map \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect the completed bounded context map as a reviewer.

- **Completeness** — every bounded context in the system appears in the inventory with owning team and scope.
- **Three dimensions** — every dependency arc has all three dimensions filled. No blanks, no "TBD" without a follow-up action.
- **Named patterns** — every team engagement model uses a recognized pattern (Shared Kernel, Customer/Supplier, Conformist, ACL, Open Host/Published Language, Separate Ways) or named collaboration model (Travelling Team Members, Service Provider, Enabler).
- **Direction** — every dependency states direction explicitly: upstream/downstream, mutual, or standalone.
- **No orphans** — every bounded context participates in at least one dependency or is explicitly declared standalone with a rationale.
- **Decisions and tensions** — open questions, contested boundaries, and deferred integrations are recorded, not hidden.
- **Consistency with domain language** — bounded context names appear in the project's ubiquitous language.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
