---
name: domain-scan
description: >-
  OOAD orientation pass: read the source by type and produce domain-scan-results.md
  (section map). Use when the user asks to "domain scan", "map the source", or
  start orienting a new corpus — not for term tables (see term-registry)
  or the markdown model sketch (see domain-model-skeleton).
---
# domain-scan

## Purpose

**Domain structure** is **not always obvious** — not from a table of contents, informal briefing, or a quick skim alone. Headings and backstory can mislead; real **clustering**, **ownership**, and **tension** often surface only when you read **with a sampling discipline**. A **scan** builds a grounded picture of *where* the material clusters, *how* it is organized (chapters, **sections**, **subsections**, modules, conversation arcs), and *what* reads as load-bearing versus peripheral — including early signals of **tension** or **ambiguity** (hedged language, overlapping ownership, hot spots).

That picture is captured in a **section map** (`domain-scan-results.md`). The point is **calibration**: you decide how to read next (depth, sampling, where not to waste effort) instead of treating the corpus as a flat word bag. Without that pass, modeling work tends to **over-extract noise** or **miss the concepts that actually carry the domain** — because you never oriented the structure before committing to names and boundaries.

## When to use this skill

Load this skill when **any** of the following apply:

- The source is **new, large, or uneven** — specs, code, transcripts, workshops — and nobody has a **shared, written picture** of how it is organized and what parts look “hot.”
- You keep **opening random sections** or files because there is no **reliable map** of topics, modules, or conversation arcs; a scan is how you **stop thrashing** and read with intent.
- The user (or you) explicitly asks to **domain scan**, **map the source**, **orient the corpus**, or **summarize structure** before deeper work.
- **Disagreement or fog** about “where the domain lives” in the material — a section map forces an **evidence-backed** first pass (signal + notes) instead of arguing from memory.

---

## Agent Instructions

1. **Templates**

Generate content using **every** template file in this skill’s `templates/` folder.


| Template                           | What to produce                                                                                                                                                                                                                               |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `templates/domain-scan-results.md` | `domain-scan-results.md` under `<active_skill_workspace>/abd-ooad/`: source map table (sections, signal, notes), organized by topic. Do not paste the template’s instructional comments into the engagement file if they are maintainer-only. |


2. **Review**

- After drafting, act as a *peer reviewer*: check coverage (**chapters plus load-bearing subsections** — not chapter-only rollups; major modules or packages in code; transcript bands), signal quality (high/medium/low), and whether central concepts and tensions are called out for downstream skills.
- **Who is checking:** A **modeler** (enough structure to seed registry and skeleton), and **future-you** reading the map cold — it should be navigable without re-opening every file.

---

## What is a domain scan?

A **domain scan** is the first **structured** pass over the source: sampled reading by material type, with explicit attention to organization, salience, and friction. Its output is **orientation** in one place — the section map — not a finished model or vocabulary.

Without that pass, you lack a shared, evidence-backed answer to “what is this corpus *made of*?” and modeling turns into guesswork or a mechanical sweep.

---

## Core concepts

### Scan by source type

Adapt depth to the material.

**Specification / structured documents**

The **Source Map** must reflect the document’s **own hierarchy**, not jsut a chapter-only rollup. Where the source has meaningful **sections and subsections** (e.g. `##` / `###`, numbered clauses, volume/part/chapter/section), add **rows at that granularity** when a subsection carries distinct domain weight — same as you would not model only at “Part I” if the real behavior lives in §4.2.

For each **major section** (chapter, top-level heading, or equivalent):

- Read the title and note it in the source map (you may also add a parent row for the chapter, then **child rows** for heavy subsections)
- Read the first 1–2 paragraphs to fix what the section is about
- Sample 3–4 paragraphs from the middle to test that read
- Read the last 1–2 paragraphs to confirm scope

For **subsections** that are **large or load-bearing** (longer than a page, dense rules, or visibly heavier than siblings): apply the same sampling pattern — they deserve their own **Section / Module** row, not a vague note under the chapter.

For **small subsections** (about a page or less): read the first 2–3 sentences only; still **list them** if they introduce a **new concept** or **invariant block** so the map is navigable below chapter level.

Also flag: bold terms, defined terms, "shall/must/cannot/always/never" language (invariants), any section visibly larger than its neighbours.

**Codebase**

For each **top-level module or package**:

- Read the module name and top-level docstring/README (first paragraph)
- List class names; do not open method bodies yet
- Sample 2–3 classes that look most central or largest

Flag `Manager`, `Handler`, `Service`, `Factory`, `Util` — often overloaded. Identify the three largest files by line count; they are usually the most coupled.

**Meeting notes / transcript**

- Count noun frequency; frequency signals domain weight
- Read the opening and closing in full (first and last 10%)
- Sample 3–4 passages from the middle
- Note "depends", "sometimes", hedging — boundary ambiguity
- Capture proper nouns: products, roles, systems

**Domain expert session**

- Read the opening in full — experts define core vocabulary immediately
- Sample 3–4 exchanges from across the session
- Any vocabulary the expert **corrects** is a boundary marker
- Flag anything called "different" or "special" — likely variant subtype or exceptional state
- Record exact phrasing; expert language often maps straight to class names

### Section map

**Step 2** in practice: fill `domain-scan-results.md` from `templates/domain-scan-results.md` — **rows follow the real outline** (chapter → section → subsection as the source warrants), with **Signal** and **Notes** per row. A thin map that only lists chapters is **not enough** when the spec or book is actually organized into titled subsections that split the domain.


---

## Example

**Source Map** rows should go as **deep** as the source structure and salience require — not only “Chapter 4.” Below, one row could be the chapter for orientation; the next is a **subsection** where the real rules live:


| Section / Module | Sig | Notes |
|---|:---:|---|
| Ch. 4 — Settlement | M | Chapter frames payment lifecycle; scan subsections for where states are defined. |
| Ch. 4 §4.2 — Payment states and transitions | H | Defines named states, transition rules; heavy "shall" / invariant language; subsection is the load-bearing unit here. |


## The shape of a good `domain-scan-results.md`

```markdown
# Domain Scan Results — {{project_name}}

## Source Map

**Signal:** H = High · M = Medium · L = Low.

| Section / Module | Sig | Notes |
|---|:---:|---|
| {{section_or_subsection}} | H / M / L | {{what_looks_heavy_or_relevant}} |
```

Use **`{{section_or_subsection}}`** labels that match how a reader would **open the source** (e.g. chapter + §, heading path, or clause id) — **deeper than chapter-only** when the outline warrants it.

The engagement file should make it obvious **where to read next** and **what is noisy vs central**, without duplicating a full term registry.

---

## Build

**Goal:** Author `domain-scan-results.md` from a real pass over the source.

- **Outputs:** `domain-scan-results.md` under `<active_skill_workspace>/abd-ooad/`. One artifact aligned with `templates/domain-scan-results.md`.
- **Per format:** Markdown with at least a **Source Map** table; extend with extra headings only if they help navigation and stay consistent with the template’s intent.
- **Column widths are content-driven, not CSS-driven.** Cursor preview, GitHub, and most renderers auto-size table columns to the longest cell and ignore `style` / `width` attributes (HTML or pipe-markdown). To keep the middle column narrow and let Notes fill the rest of the row: (a) abbreviate the Signal column to a single character — `H` / `M` / `L` (header `Sig`, not `Signal`); (b) keep Section labels short — move long parenthetical examples (`(Affliction, Damage, …)`) into Notes; (c) use a normal pipe-markdown table — no HTML wrapper.
- **While writing:** Tie rows to how you actually sampled (**sections and subsections** in prose specs, not only chapter titles; packages and files in code; transcript bands in dialogue). Flag tensions and heavy areas for **`term-registry`**.
- **Persistence:** Engagement root comes from the parent agent `workspace` config; paths use `abd-ooad/` under that root.

---

## Validate

**Goal:** Read the section map as a reviewer — not a second full scan unless gaps are obvious.

- **Who is checking:** Someone who will run **`term-registry`** next (needs enough signal to seed anchors and tensions).
- **Cross-artifact parity:** *N/A* — single primary template output.

Check that:

- The map goes **below chapter level** where the source does: **subsections** (or equivalent) that matter appear as their own rows, not only parent chapters.
- Major corpus regions (chapters **and** nested sections, packages, transcript arcs) appear with plausible **Signal** and **Notes**.
- Central vs peripheral **units** are distinguishable; obvious tensions or ambiguities are called out.
- The file is present and named `domain-scan-results.md` in the engagement `abd-ooad/` folder.

If the map is thin or wrong, extend with **targeted** passes — not a full redo unless the source or goals changed.

---





