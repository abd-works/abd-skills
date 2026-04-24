---
name: domain-model-skeleton
description: >-
  After domain scan and term registry, produce domain-model-skeleton.md: module
  sections, anchor and supporting classes, and UML notes tied to
  term-registry rows. Use when the user asks for a "domain model skeleton",
  "scan-level class sketch", or initial markdown model from anchors.
---
# domain-model-skeleton

## Purpose

Produce the first structural draft of the domain in `**domain-model-skeleton.md**`: module sections, one `**<<Anchor>>**` on each module’s **core** class, **plain** supporting class names (no `**<<Entity>>` / `**<<Aggregate>>` / other stereotypes), and `**note:**` lines tied to `**term-registry.md**` rows — scan fidelity only, no deep model or sequence diagrams.

## When to use this skill

Load this skill when **any** of the following apply:

- `**term-registry.md`** and `**domain-scan-results.md**` exist and you need the **markdown class sketch** for the engagement.
- The user asks for a **domain model skeleton**, **scan-level model**, or **initial class lines** from anchors.
- You are past vocabulary seeding and need `**domain-model-skeleton.md`** before later OOAD phases (nouns-verbs, etc.).
- You will **not** invent structure beyond what the scan and registry support (use **targeted** re-reads only to resolve gaps).

---

## Agent Instructions

1. **Templates**

Generate content using **every** template file in this skill’s `templates/` folder.
**Do not** emit only Markdown or only plain text unless the user **explicitly** asks for a single format.


| Template                             | What to produce                                                                                                                                                                                                                                            |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `templates/domain-model-skeleton-template.md` | `domain-model-skeleton.md` under `<active_skill_workspace>/abd-ooad/`: `##` module sections, **one `<<Anchor>>` per module** (core class only), supporting classes **without** UML/DDD stereotypes, optional properties/operations only where the scan supports them, and `**note:`** lines per **Core concepts** / **Stereotypes** / **Anchors** below. |

1. **Validate** The contract is `references/` (if present), **Core concepts**, and the embedded **Anchors** guidance below.
2. After drafting, act as a *peer reviewer*: verify **anchor test**, **`## [Name]`** section titles (no ` module` suffix), `**<<Anchor>>`** only on each core class (no other `**<<…>>` stereotypes), and `**note:**` coverage for registry rows.
3. **Who is checking:** A **modeler** (structure matches sketch fidelity) and a **reader of `term-registry.md`** (every modeled line traceable to a row).

---

## What is a domain model skeleton (scan fidelity)?

It is a **first-pass** grouping of classes under module headings, with one `**<<Anchor>>`** core class per module when the anchor test passes. It makes **boundaries visible** without committing to full properties, relationships, or walkthrough diagrams.

**Prerequisites:** `domain-scan-results.md` from `**domain-scan`**, and `**term-registry.md**` from `**term-registry**`. Work from those plus **targeted** source re-reads only when something is unclear — **no full rescan**.

---

## Core concepts

### Build procedure

Translate anchor + sibling candidates **from `term-registry.md`** into a module/class skeleton.

Add one module block per anchor with an anchor class and any sibling of the anchor class. For each class add only properties/operations already evident from the scan — **do not invent structure**.

**Note tag — `[dms]`:** Prefix scan-fidelity / skeleton `note:` lines in **`domain-model-skeleton.md`** with **`[dms]`** — **d**omain-**m**odel-**s**keleton (this skill). The older full-OOAD table used **`[p0]`** for a “domain-scan” phase index; in **abd-ooad**, use **`[dms]`** so the tag names the **skill** that owns the file. Labels after the tag still mirror **term-registry** (e.g. `High Confidence Anchor`, `Sibling Candidate`, `Tension`).

**UML notes:** attach a `note:` line immediately after each class/module for every term that has a row in `term-registry.md`. One sentence — term name + why it exists. Tag **`[dms]`** where appropriate. Deeper reasoning stays in `term-registry.md`.

**Anchors, `<<Anchor>>`, and module sections:** use the **Anchors** subsections below.

### Stereotypes in `domain-model-skeleton.md` (skeleton only)

- **Only** **`<<Anchor>>`** may appear in guillemets on a class line. Use it **once per module**, on the **core class** (same name as the module) when it passes the anchor test.
- **Do not** write **`<<Entity>>`**, **`<<Aggregate>>`**, **`<<Value Object>>`**, **`<<Role>>`**, **`<<State>>`**, **`<<Resource>>`**, **`<<Abstract>>`**, or any other stereotype in this file. Those are **later** (candidate typing, DDD, roles, state modeling, and similar skills). Carrying `<<Abstract>>` or value-object hints from **term-registry** `Value` into the skeleton is **out of scope** here — the skeleton lists **names and notes**, not type commitments.
- **Supporting** classes under a `##` section: **plain** class lines (name only, or `Name` with a `note:`) — no `<<…>>` after the name.

**Review:** if you see any guillemets in `domain-model-skeleton.md` other than `<<Anchor>>` on a module core class, remove them or move that typing to a later artifact.

### Section titles — do not use the word `module` in the `##` heading

Each **module** (grouping) is introduced by a **level-2 heading that is only the anchor name**, in brackets — no ` module` suffix.

| Use | Do not use |
| --- | --- |
| `## [Series]` | `## [Series module]` |
| `## [Check]` | `## [Check module]` |
| `## [Payment]` | `## [Payment module]` |

**Why:** “Module” describes the **role** of the section in prose (an anchor slice of the model), not part of the **title**. Repeating `module` in the heading is noisy and reads wrong for names like **Series** (“Series module” is redundant). The **core class** name still matches the bracket title (e.g. `Series : <<Anchor>>` under `## [Series]`).

### Anchors — what an anchor is

An **anchor** is a module. It is the most stable, central thing you have found in the domain - the concepts you are confident will survive the entire modeling process without being renamed or restructured away.

An anchor is three things at once:

1. **A module section** — in `domain-model-skeleton.md`, a `## [Name]` heading (anchor name only — **not** `## [Name module]`) that groups related classes
2. **A core class** with the same name as that heading — the primary class in that section, marked `<<Anchor>>`
3. **A scope boundary** — every class listed under that heading belongs to this module; other modules relate to it via that core class

The **section title** (`[Name]`) and **core class** name must match. If they don't, the anchor is not yet correctly identified.

### Anchors — the anchor test

Before calling something an anchor, it must pass all three of these:

**1. Can you name a core class that matches the module?**
The core class must be identifiable by name in the source. You should be able to point to a section, definition, or keyword in the material that defines this concept by that name. A generic name like "Foundation," "Basics," or "Mechanics" with no corresponding defined concept is a signal you are grouping by proximity rather than identity — not a real anchor.

**2. Do other anchors reference it independently?**
If another module needs to point to this concept, does it reference this class by name — or does it go through some other class to get to it? If the only path to it goes through another anchor, it is likely a supporting class inside that anchor's module, not its own anchor.

> Example: HeroPoint has its own lifecycle and lifecycle rules, but nothing in the resolution system references HeroPoint directly — it is always accessed through the Character who holds it. HeroPoint belongs inside the Character module.
>
> Contrast: Check IS referenced directly — the entire game resolves outcomes through Check. No other anchor is needed to mediate access to it.

**3. Does it have structural stability?**
An anchor is a concept you expect to be present in the model from scan through final refinement. If you think it might disappear, merge with something else, or be renamed significantly, it is a candidate — not an anchor.

### Anchors — what an anchor is NOT

- **A chapter in the source** — a chapter is an organization of the source, not a domain concept. Multiple real anchors can come from one chapter; one chapter alone does not make an anchor.
- **A concept with a dedicated section** — many things have dedicated sections. The anchor test is structural (other anchors reference it independently), not documentary.
- **A grouping of related concepts** — if you find 3–4 concepts that are related but none of them clearly dominates, keep exploring. The anchor will be the one that the others depend on. If none dominates, record the cluster as a tension.

### Anchors — what it looks like in outputs


| Output                   | What anchor produces                                                                                                                                                                                                                                                                                             |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `domain-scan-results.md` | **Source map** for the corpus (`**domain-scan`**). It is **not** the anchor roster — that lives in `**term-registry.md`** (Notes: `High Confidence Anchor`, `Sibling Candidate`, `Tension`, …) and in `**domain-model-skeleton.md**` (module sections and `<<Anchor>>` on the core class).                           |
| `domain-model-skeleton.md`   | `## [Name]` (no ` module` in the title) + **one** `<<Anchor>>` on the core class only. Other classes: **no** `<<…>>` stereotypes. Cross-module ties only where the scan supports them. |
| `term-registry.md`       | Core class of a module → Classification `**anchor (class + module)`**; supporting classes → `**class**` with owning module in **Notes** (e.g. `Supporting class — Character module`). Use **Status** for lifecycle (e.g. **Tension**, **Candidate**) — not a duplicate of Classification.                        |


### Anchors in later phases

Anchor status is not permanent. Anchors are your highest-confidence starting point, but subsequent phases will test and revise them:

- **nouns-verbs-rules-and-states (NOUNS):** All bolded and defined terms in the source are extracted. Anchors can be re-evaluated here; new candidates emerge and will challenge or subdivide existing anchor boundaries.
- **candidate-list (CANDS):** Candidates are sorted and scored. At this stage, watch for candidates that score high enough on the anchor test to be promoted — or anchors whose core class fails the independence test and should be demoted.
- **thing-vs-data-about-a-thing (THINGS):** Supporting classes inside anchor modules are evaluated here — each gets a class/property decision. If a supporting class earns class status, it may eventually warrant its own module section in later phases.
- **All subsequent phases:** Anchors drive the backbone of the model. Relationship decisions, responsibility assignments, and inheritance structures are all organized relative to anchor modules. Changes to anchor boundaries affect the whole model — flag them explicitly in the term registry before proceeding.

### Incomplete anchor signal

The absence of a matching core class is the clearest signal that you have not yet found the anchor. When you encounter this situation:

1. Do not force a name — generic names produce models that are hard to reason about
2. Read the relevant chapter(s) more carefully — the anchor often has its own defined term or dedicated section
3. Ask: if another module needed to reference this cluster, what single class would it name?
4. If no single class emerges after exploration, record the cluster as a **tension** in `**term-registry.md`** (and reference it from the scan map in `**domain-scan-results.md**` if useful) and defer

### Anchor as module (scan fidelity)

An **anchor** is a module. At this fidelity every anchor is both:

1. **A module section** in `domain-model-skeleton.md` — a `##` heading that groups the anchor's core class and its close subordinates
2. **A core class** with the same name as the module, listed first as the `<<Anchor>>` line for that section

This is not optional. The module name and the core class name must match. If they don't, you have a section title without a real anchor.

#### The core class requirement

The core class is the most important single concept in the module. It is:

- Named exactly what the module is named (e.g., module `Character` → core class `Character`)
- The thing other modules reference when they need to talk about this concept
- Identifiable by name from the source material — you should be able to point to a section that defines it

**If you cannot find a natural core class name for a cluster of related concepts, you have not found the anchor yet.** This is a signal to explore further, not to invent a placeholder name. A generic name like "Foundation", "Basics", or "Mechanics" with no matching class is an anti-pattern — it means you are grouping by chapter proximity rather than by conceptual identity.

#### What to do when you find a cluster but no core class

When the scan surfaces 3–4 closely related concepts from the same chapter but none of them clearly dominates:

1. **Ask:** which concept would other modules reference by name? That one is probably the anchor.
2. **Ask:** if another module needed to point to this cluster, what would it say? The answer is the core class name.
3. **Explore the relevant chapter(s) more carefully** — do a targeted read of the section titles, defined terms, and opening paragraphs. The anchor often has its own dedicated section.
4. **You will typically get 1–2 real anchors**, not one grouped one. Separating them is usually correct.
5. If after exploration you still cannot find a core class, record the cluster as a **tension** and leave it unresolved for now — do not force an anchor.

#### What an anchor module looks like in the outputs

- `**domain-model-skeleton.md`:** under `## [anchor name]` (title = name only, see **Section titles** above), the core class (same name) with `<<Anchor>>`, then any supporting classes you are confident belong in this module at scan fidelity — with fields/ops only where the scan already supports them
- **Term registry:** the core class row has Classification = `anchor (class + module)`; supporting classes in that module have Classification = `class` with a note naming the module they belong to (**Status** tracks Ambiguous / Tension / Candidate / etc.)

#### Initial model sketch

Before writing `domain-model-skeleton.md`:

- **Name each anchor module:** one-line responsibility statement from the source — do not invent
- **Identify the core class:** confirm it has a name you can point to in the source
- **Identify supporting classes:** 0–3 classes that clearly belong in the same module section at this fidelity level
- **Do not add detail:** if you only know a class name and broad responsibility from the scan, the sketch only contains that — do not fill in properties, methods, or relationships you haven't confirmed

**CRITICAL CONSTRAINT:** `domain-model-skeleton.md` must match the sketch fidelity exactly. If the sketch has four anchor modules with only their core classes, the file has four `##` sections each with one `<<Anchor>>` line and nothing invented beyond that.

#### Anchor module rule

Every anchor gets:

- A core class with the same name (the most important concept in the module)
- A module section listing that core class and any supporting classes that clearly belong at this fidelity level
- Fields on the core class for concepts you found but have not yet decided are classes vs. properties

> The core class anchors the section. Supporting classes that are confident enough are listed under the same `##` heading. Everything else is a field on the core class — evaluated in `thing-vs-data-about-a-thing`.

Example: `Character` module has a `Character` core class with `abilities: AbilitySet` as a field. If `Ability` is clearly its own class at this fidelity, it appears under the Character section as a supporting class. If uncertain, it stays as a field.

---

## Example

Under `**## [Payment]`**, a minimal anchor line and note:

```markdown
## [Payment]

note: [dms] Payment -- owns settlement lifecycle for a transaction

Payment : <<Anchor>>
note: [dms] High Confidence Anchor -- every flow routes through settlement here
```

## The shape of a good `domain-model-skeleton.md`

Follow `templates/domain-model-skeleton-template.md`: module headings, class lines, optional properties/operations with phase tags in parentheses, and `**note:`** lines with **`[dms]`** that trace to `**term-registry.md**`. Do not paste the template’s full instruction tables into the engagement file unless your process requires it.

---

## Build

**Goal:** Author `domain-model-skeleton.md` from `**term-registry.md`** and scan orientation.

- **Outputs:** `domain-model-skeleton.md` under `<active_skill_workspace>/abd-ooad/`.
- **Per format:** Markdown class-line document; match module and anchor rules in **Core concepts**.
- **While writing:** One `**<<Anchor>>`** per module (core class only); no other `<<…>>` stereotypes; `**note:**` per registry-backed term.
- **Persistence:** Engagement root from parent agent `workspace`.

---

## Validate

**Goal:** Read the skeleton as a reviewer — structure and traceability, not a second full model pass.

- **Who is checking:** A **modeler** (sketch fidelity, anchor test) and someone spot-checking `**term-registry.md`** links.
- **Cross-artifact parity:** *N/A* unless you add a second paired template later.

Check that:

- `domain-model-skeleton.md` exists; every module and class has a `**note:`** linking back to its term-registry row with a one-sentence rationale.
- **Section titles** follow **Section titles — do not use the word `module` in the `##` heading** (e.g. `## [Series]`, not `## [Series module]`).
- The only guillemets in the file are `<<Anchor>>` on each module’s core class — not `<<Entity>>`, `<<Aggregate>>`, `<<Value Object>>`, or any other stereotype.
- No invented modules/classes beyond scan-supported material; sketch fidelity matches **Initial model sketch** above.

If the skeleton is thin or wrong, improve with **targeted** passes over the source, `domain-scan-results.md`, and `term-registry.md` — not a full corpus rescan unless the source or goals changed.

---





