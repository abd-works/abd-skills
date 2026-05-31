# Build Architecture Skill — Concepts

## What is an "architecture implementation skill"?

An **architecture implementation skill** is a packaged practice — same shape as every other `abd-*` skill — that takes a project's domain requirements (a story, an entity, a sub-epic) and **emits code that already obeys a specific architecture**. It is the inverse of a reference document: the reference tells you what the architecture is; the implementation skill turns that knowledge into runnable folders, files, and tests. The generated skill **owns its own copy** of the reference so it is self-contained.

---

## Reference → skill: one-to-one mapping

| Reference document part | Generated skill part |
|---|---|
| **Overview** (principles list) | `SKILL.md` **Purpose** + **What is …** sections |
| **Architecture Layers** | `SKILL.md` **Core concepts → Layers** table + `templates/` folder structure |
| **Mechanism: File Structure** | `templates/<mechanism>.template.txt` folder tree |
| **Mechanism: Participants** | `templates/` named files/classes; `SKILL.md` **The shape of a good module** |
| **Mechanism: Flow** | `SKILL.md` **Build steps** numbered list |
| **Mechanism: Walkthrough Example** | `SKILL.md` **Example** section (one full filled example) |
| **Mechanism: Principles & Patterns** | One `rules/<principle-slug>.md` per principle |
| **Mechanism: Testing the mechanism** | `rules/test-structure.md` + `Validate` checklist |

---

## Mechanism slice vs. domain slice

The generated skill can be invoked in two modes:

- **Domain slice** — generate a full domain module covering every mechanism for one capability.
- **Mechanism slice** — generate only the code for one mechanism without re-emitting the whole module.

---

## Scanners are optional but expected

If the architecture has machine-checkable invariants, the generated skill should ship `scanners/<lang>/<scanner>.py`. This skill does **not** invent scanners that do not exist; missing scanners are recorded as `# TODO` in rule bodies.

---

## The generated skill is a regular practice skill

The output has `SKILL.md`, `inputs/architecture-reference.md`, `templates/`, `rules/`, `ide-files/`, and `scanners/`. It can be deployed and validated with the same tools as any other skill.
