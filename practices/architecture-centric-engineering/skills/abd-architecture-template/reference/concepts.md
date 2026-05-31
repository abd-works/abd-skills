# Architecture Template (Reference Document) — Concepts

## What is an architecture reference?

An **architecture reference** details one or more cross-cutting mechanisms the system needs and defines how that mechanism is realized across the architecture's layers. "Mechanism" is the verbed concern — *how the architecture handles errors*, *how it caches*, *how it persists*, *how it authorizes*, *how it observes*. A reference is the design and working implementation of one or more mechanisms, saying which layers participate and what each one does.

A finished reference lets a reviewer answer three questions in one read:

- **What is the principle?** — the one-line rule that, if you violated it, your code would no longer be "in this architecture".
- **What is the pattern?** — the named, repeatable shape that implements the principle.
- **How does it actually run?** — the participants, the file layout, the call sequence, and the test approach.

---

## Mechanism

**Architecture mechanism** is a family-level concept — see [`reference/architecture-mechanism.md`](../../../reference/architecture-mechanism.md) for the definition and the canonical categories. The reference document devotes one section (or file) to each mechanism the project has actually decided, and is the deepest-fidelity treatment: it gives each mechanism the full five-part shape below.

**Document once, assign later.** After discovery (or the first run that creates a mechanism), later exploration, specification, and engineering **assign** the existing section. Only **create** when the scope needs a mechanism that has no complete section yet.

---

## Assign vs create

Each mechanism is documented **once**. Before writing anything, **discover** what already exists under `docs/architecture/` — `architecture-reference.md` and scoped companions (e.g. `increment-*-reference.md`).

**Workflow:**

1. **List mechanisms in scope** — from the ticket (story, sprint, increment) and upstream artifacts (AC, blueprint, UL). One line of intent per mechanism.
2. For each mechanism:
   - **Assign** — a section titled `## Mechanism: <Name>` (or equivalent combined section) already has Principles & Patterns, File Structure, Participants, Flow, Walkthrough, and Testing → record path and heading; do not rewrite.
   - **Create** — section missing or incomplete → append to the canonical reference or add a scoped companion when many new mechanisms would bloat the main doc.
3. **Emit an assignment table** — every mechanism in scope gets a row: name, `assign` | `create`, path, section anchor.

| Situation | Action |
| --- | --- |
| `## Mechanism: <Name>` exists with full five-part shape | **Assign** — cite path and heading; do not rewrite |
| Section missing or incomplete for a mechanism in scope | **Create** — add or finish that section only |
| Scoped increment adds many new mechanisms | **Create** in a companion file; link from main reference TOC |

**Avoid:** regenerating a full `architecture-reference.md` when only new mechanisms are needed; duplicating a mechanism under a different heading when an equivalent section exists.

**Example:** Increment 8 needs Customer Review and Marketing Email Dispatch. Error Handling and Communication already exist → assign those sections; create only the two new mechanism sections; assignment table shows two assign and two create.

---

## Principle vs. pattern

A **principle** is a one-liner stance the architecture takes — a constraint the team is not allowed to break. It is technology-agnostic, fits in a sentence, and survives in a corridor conversation.

A **pattern** is the full description of how the team has chosen to satisfy that principle in this project: the named shape, its structural options, its benefits, and its trade-offs.

---

## Layered description vs. mechanism reference

The **layered description** answers *what are the layers and what tech sits in each*. **This skill** answers *for each mechanism, which of those layers participate and in what order*.

---

## The five-part shape

Every mechanism section has the same five-part shape:

1. **Principles & Patterns** — one-liner principle(s) followed by a named pattern description per principle.
2. **File Structure** — where the mechanism's code lives (a fenced tree).
3. **Participants** — the classes/modules involved, as a class diagram or table.
4. **Flow** — a sequence diagram of one representative scenario.
5. **Walkthrough Example** — a step-by-step narration of the same scenario with example code and test snippet.

A short **Testing the mechanism** subsection explains which test tier owns the verification.

---

## Section organization

The reference is **always one file**: `architecture-reference.md`.

- **Combined section** — when there are only **2–3 mechanisms** and they are tightly related, use one `## Mechanisms` section that weaves the five-part shape across all of them.
- **One section per mechanism** — the default for **4+ mechanisms**, and always allowed. Each mechanism gets its own `## Mechanism: <Name>` section.

---

## Code and test standards

Code in walkthroughs follows the project's coding standard (defaulting to `abd-clean-code` when in scope). Test snippets follow the project's testing standard (defaulting to `abd-acceptance-test-driven-development` when in scope).
