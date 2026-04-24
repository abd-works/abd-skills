---
name: nouns-verbs-rules-and-states
description: >-
  Mandatory vocabulary inventory: when a source map and/or corpus exist, a
  complete module-by-module pass in domain-noun-verb.md; candidate nouns,
  verbs, rules, and states grounded in the real text—not a registry-led stub.
  Feeds refined downstream OOAD; not a design or notation pass.
---
# nouns-verbs-rules-and-states

## Purpose

This skill is an **inventory exercise** on the **real source text**. Under each `## [Name]` (anchor name only—**not** `## [Name module]`; see **Section titles** in **Core concepts**), you capture **Candidate** nouns, verbs, rules, and states, plus class sketches only where the text already supports them. The goal is a **grounded, complete** first-cut vocabulary by anchor for **refined downstream OOAD**, not a final class diagram. It **tests anchor boundaries** without locking final lists (later skills do that).

## Complete pass (mandatory when the engagement has a map and/or source)

If the workspace has **any** of: a **source map** (typically `domain-scan-results.md` or the team’s equivalent), **direct access to the source corpus** (book, spec, rules shards, monolithic markdown, etc.), or both—**you do not** ship a **thin** noun–verb file built only from `term-registry.md` and `domain-model-skeleton.md`. That would skip the work.

**You must:**

1. **Use the map** to fix **reading order** and **which modules** (chapters, services, subsystems) matter. The map names **where** the vocabulary lives; it is not a substitute for reading.
2. **Read the source module by module** in that order (or anchor by anchor if the map is organized that way). **Each** mapped module (or each anchor section you align to the map) gets a **full** pass: large **Candidate** lists mined from the **text** of that module—not a one-line restatement of the skeleton.
3. **Treat the deliverable as complete only when** every module the map says is in scope (or every anchor the engagement uses) has been **read and inventoried** in this pass, unless the user has explicitly **scoped down** a smaller region (then say so in the file).

**In short:** a **source map** and/or **source text** in hand means a **complete** inventory pass **module by module** (or **anchor by anchor** in lockstep with the map). Partial or registry-only work is **out of spec** for this skill.

## When to use this skill

**Use it** when the team is running—or explicitly requesting—this **vocabulary inventory**: read the book/spec **in map order**, fill **Candidate** blocks from the text under each anchor, and promote new terms to `term-registry.md` as first capture when appropriate.

**Triggers:** user asks for **nouns and verbs**, **rules and states**, or **extraction by anchor**; and the work is a **serious** pass with **source** available—**not** a three-line summary.

## When not to use this skill

- The **source is not available** to read, so a **grounded** inventory is impossible. (A map without corpus still fails this skill if you cannot open the text.)
- The work is **only** to edit the registry, nudge the sketch, or clean evidence, **and** the user is **not** asking for a noun–verb inventory—**do that work under other skills.**
- The work is **past** this layer: final types, services, or detailed design. Use the skills aimed at that layer.
- A **vocabulary pass at the current model level is already done** and there is no new source or new request—repeating is churn.

**Note:** “We only have time for a quick pass” is **not** a valid excuse if **map + source** exist. Either **narrow scope in writing** (which chapters or anchors) and complete **that** region module-by-module, or **do not** claim a noun–verb pass under this skill.

---

## Agent Instructions

Outputs are **domain content** in the noun–verb deliverable and updates to the **term list** the engagement uses (see **Core concepts** for usual filenames in this repo).

### 1. Templates

The skill ships `templates/domain-noun-verb-template.md`. The deliverable lives in the project **OOAD area** (e.g. a folder like `abd-ooad`).

**Per anchor (or per module, mapped to anchors):** a level-two heading with **only the name** in brackets, a `### Note` for what that section owns in the source, then **Candidate** subsections (nouns, verbs, rules / invariants, states), then class-style boxes when the text supports them. Optional `## Cross-anchor notes`. **Do not** put skill paths, template filenames, or repo layout into the **body** of the deliverable—**domain content only**. Use **every** file in the skill’s `templates/` folder unless the user explicitly asks for a single format.

### 2. Work order (mandatory shape)

1. Open **`domain-scan-results.md`** (or equivalent **source map**). If there is no map, derive an explicit list of **modules** to read and record it in the deliverable or engagement notes.
2. For **each** module in map order, open the **source** (primary text, not only `term-registry.md`).
3. For **each** anchor you attach that module to, **append** or **fill** **Candidate** lists from that reading. **Inventory** is the point: the lists should be **large** where the text is dense (e.g. skills chapter, power effects, advantages lists).
4. For **new** domain terms **first** captured in this pass, add **`term-registry.md`** rows with **Skill** = `nouns-verbs-rules-and-states` and **Evidence** pointing at the right slice.
5. Use **`terms.md`** (same headings as the noun–verb file) for **long verbatim** quotes so the main file stays structured.

### 3. Review

- After drafting, act as a *peer reviewer*: `## [Name]` headings (no `module` in the `##` line); **each** in-scope **module** from the map has been **read** and reflected in **Candidate** depth (not skeleton-only); content matches `domain-model-skeleton.md` and **term-registry** where they apply; the registry has a row per **new** term, with **Notes** labels from the **term-registry** skill and **`[p1]`** (or the project’s tag) where the model template uses it.
- **Who is checking:** a **modeler** and someone who will run **later OOAD** skills (they need **evidence of a full pass**, not a thin stub).

### 4. Bundled rules

This skill has **no** separate `rules/*.md` folder. `SKILL.md` is maintained by hand.

---

## Prerequisites

| Artifact | Role |
| --- | --- |
| `domain-scan-results.md` (or equivalent) | **Source map**—defines modules and **reading order**; **mandatory** for a complete pass when the engagement uses one. |
| `term-registry.md` | Vocabulary and evidence—**extend** with every **new** term; **Notes** from the **term-registry** skill. |
| `domain-model-skeleton.md` (optional) | **Anchor** names; **align** `## [Name]` sections unless the text **forces** a change (then **update the registry** and say why). The skeleton is **not** a substitute for reading the book. |

**Pipeline:** **domain-scan** (orients) → seed registry/skeleton as needed → **this skill** is the **full** source-grounded **inventory** in `domain-noun-verb.md`.

---

## Core concepts

### Deliverable — `domain-noun-verb.md` (normative)

**Primary file:** `domain-noun-verb.md` in the **OOAD folder** (e.g. `…/abd-ooad/`). If you need long **verbatim** quotes, use `terms.md` in the same place, with the same `## [Name]` headings.

| Item | Rule |
| --- | --- |
| **Path** | e.g. `<active_skill_workspace>/abd-ooad/domain-noun-verb.md`, or your team’s OOAD path. |
| **H1** | Short label for the corpus or book. |
| **Structure** | Per anchor: `## [Name]`, `### Note`, **Candidate** lists (all four kinds where relevant), class lines, gaps. Optional `## Cross-anchor notes`. |
| **Body** | **Domain content only**—no skill paths, template filenames, or process meta. |
| **Completeness** | If a **source map** exists, the file must show **module-by-module** (or **anchor-by-anchor**) coverage of **all** in-scope map entries, unless a **smaller** scope is **explicitly** stated in the deliverable. |

### Section titles (same as **domain-model-skeleton**)

Use `## [Series]`, `## [Check]`, not `## [Series module]`. The heading is **only** the anchor name; *module* is spoken language, not the `##` line.

### Traceability

| Artifact | Role |
| --- | --- |
| `term-registry.md` | **Skill**, **Target**, **Value**, **Notes** for promoted terms. |
| `terms.md` | Long quotes—not a wall of prose inside `domain-noun-verb.md`. |
| `domain-noun-verb.md` | **What the source said** under each anchor; **large** **Candidate** lists from reading. |

Every **new term** **first** captured here gets a registry row. Use **Notes** labels from the **term-registry** skill: **Anchor Boundary**, **Sibling Candidate**, **Tension**, **High Confidence Anchor**, **Follow-up**. Tag with **`[p1]`** where the project’s model table applies.

### Anchor boundaries under test

**Anchors meet the full vocabulary** you read, **module by module**. Watch for support, challenge, and split for boundaries; record in **term-registry** with **Anchor Boundary**; update **domain-model-skeleton** when the source **forces** a change.

### Focus

**Delta for this skill:** pre-notation richness—nouns, verbs, rules, states, tensions. Do not invent full APIs here.

---

## Example (shape)

Under `## [Check]`, after reading Ch.1 **Core Mechanic** in the book, **Candidate nouns** might include d20, DC, effort, circumstances, **Candidate verbs** roll / add / compare, **rules** the meet-or-beat line and variation bullet—**all** from the paragraph you read, not from the skeleton alone.

---

## Build

**Goal:** author or **complete** `domain-noun-verb.md` and update `term-registry.md`.

- **Outputs:** `domain-noun-verb.md`; optional `terms.md`; updated `term-registry.md`.
- **Format:** `templates/domain-noun-verb-template.md`.
- **While writing:** align `## [Name]` with the registry and skeleton; evidence IDs in the registry, not raw paths, in the deliverable body.
- **Persistence:** engagement root from the parent agent **workspace** config.

---

## Validate

**Goal:** confirm a **full** pass, not a stub.

- **Who is checking:** someone who will use **downstream** skills and a **term-registry** reviewer.

Check that:

- The engagement had **map and/or source** → **`domain-noun-verb.md`** shows **per-module (or per-anchor) inventory** for **all** in-scope map rows (or the **explicit** subset named in the file), with **source-derived** **Candidate** lists—**not** only restating `term-registry.md` or `domain-model-skeleton.md`.
- **Nouns, verbs, rules, and states** are represented for each covered module (no **silent** skip of a whole mapped region).
- **New terms** are in `term-registry.md` with **Skill** = `nouns-verbs-rules-and-states` when first captured here, **Notes** pointing at the right `## [Name]`.
- **Cross-anchor** tensions and **Anchor Boundary** where the source strains the model.
- **No** process boilerplate in the artifact body.

If coverage is missing, **read the missing module** in the source and extend the file—**not** a “targeted” patch that leaves the pass incomplete for in-scope work.

---
