---
name: mern-technical-architecture
catalog_garden_tier: practice
catalog_garden_family: architecture-centric-engineering
catalog_garden_order: 70
catalogue_one_liner: >-
  Domain-first MERN web applications: domain modules, shared logic, Clean Architecture layers, story-driven tests, scanner-verified compliance.
description: >-
  Generate production MERN (MongoDB, Express, React, Node.js) web applications
  using a domain-first architecture. Code is organized by business capability
  (domain module) with shared domain logic, Clean Architecture layer separation,
  and story-driven testing across three tiers. Use when scaffolding a new MERN
  project, adding a domain module, reviewing architecture compliance, or
  transforming a technically-organized codebase into domain-first structure.
---
# mern-technical-architecture

## Purpose

Generate production MERN web applications using a **domain-first architecture** — organizing by business capability, sharing domain logic across tiers, enforcing Clean Architecture layer purity, and testing with story-driven scenarios.

This skill produces real, runnable TypeScript domain modules — each with a `shared/` domain core, `server/` Express backend, and `client/` React frontend. The output follows the architecture defined in `inputs/mern-architecture.md`: domain entities with business logic, Zod validation schemas shared across tiers, and story-driven tests mirroring Gherkin scenarios.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** A complete domain module under `packages/<domain>/` with `shared/`, `server/`, `client/`, and `tests/` subdirectories.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — domain-first architecture principles, five layers, file structure, shared logic strategy, story-driven testing, and module shape.
- **`inputs/mern-architecture.md`** — the authoritative architecture reference with full mechanism details, participants, flows, and walkthroughs.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/domain-module.ts` | Complete domain module with shared/, server/, and client/ packages |

**Consistency:** All three tiers must reference the same domain entities, use the same Zod schemas, and maintain identical naming conventions. When creating or rewriting a domain module, deliver all three tier packages as a complete unit.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/mern-technical-architecture \
  --workspace <path-to-output>
```

Then verify compilation:

```bash
npm install
npx tsc --noEmit
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Domain structure complete** — shared/, server/, client/ all present with required files.
- **Layer purity** — no forbidden imports (shared imports nothing from server/client; server never imports client).
- **Naming conventions** — PascalCase entities, camelCase methods, kebab-case files per tier conventions.
- **Test structure** — all 3 tiers present (server, client, E2E).
- **Test data isolation** — no blanket resets or `deleteMany({})`.
- **Compilation passes** — `npx tsc --noEmit` reports zero errors.
- **Shared logic used** — domain entities and Zod schemas imported from shared/ in both server/ and client/.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
