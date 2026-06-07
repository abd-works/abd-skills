# Architecture Reference (Implementation) — Concepts

## Assign before create

Implementation work **starts from what already exists**. Assign existing reference sections and code; create only gaps.

**Workflow:**

1. **Resolve the reference document** — read `docs/architecture/architecture-reference.md` and scoped companions from the ticket or exploration handoff.
2. **List mechanisms in scope** — same list as the template pass (or derive from domain model, spec-by-example, stories).
3. For each mechanism:
   - **Assign reference** — section is complete (five-part shape from `abd-architecture-specification`) → record path and heading; use as specification; do not re-author.
   - **Create reference** — section missing → run `abd-architecture-specification` for that mechanism only, then continue.
   - **Assign code** — production and test files in the reference File Structure already exist and match the walkthrough → record paths; skip generation.
   - **Create code** — reference exists but files missing → generate only missing files; extend existing modules rather than replace working code.
4. **Emit an assignment table** — mechanism | reference (assign/create) | code (assign/create/n/a) | paths.

**Avoid:** hello-world mode when a project reference exists; duplicating mechanism sections or package folders that already implement the walkthrough.

**Example:** Sprint 1 needs Customer Review — reference missing → create via template, then generate `packages/marketing/` files. Sprint 2 needs Persistence — section and repository code exist → assign reference § Persistence and existing repository path; no new files.

---

## Kanban ticket run (quick pass vs long pass)

When pulled from a kanban board, **always run this skill** — kanban does not auto-skip.

1. **List mechanisms in scope** from the ticket's architecture blueprint (`architecture-blueprint.md` or increment companion).
2. **Check** existing reference sections on disk and `docs/planning/delivery-war-room/mechanism-registry.json`.
3. **Quick pass** — every mechanism has a complete reference section and assignable code paths → write **`architecture-reference-assignment.md`** only (all rows **assign**); mark skill done.
4. **Long pass** — missing reference and/or code → create only gaps; update the registry for new mechanisms; write the assignment table.

The assignment document is the mapping artifact for downstream work and for later tickets that reuse the same mechanisms.

---

## Reference document as specification

Assigned or newly created reference sections are the contract: File Structure is the file list, Participants is the type graph, Flow is the call sequence, Walkthrough is the acceptance scenario.

---

## Project mode vs hello-world

| Mode | When |
| --- | --- |
| **Project** | Reference exists (assigned or just created) — implement from File Structure and Walkthrough |
| **Hello-world** | No project reference and no in-scope ticket — calibration only |

Do not use hello-world when `docs/architecture/architecture-reference.md` already exists for the engagement.
