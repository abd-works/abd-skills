# Domain scan

**Outcome:** You have a source map, 3–7 high-confidence **central modules** (each with a named core class), and a list of suspected tensions — enough orientation to begin extraction as a targeted pass rather than a mechanical word sweep.

For **which files the scan creates** (`domain-scan-results.md`, `strategy.md`, models, registry) and how they evolve after the scan — see **`strategy-led-generation`** in this library.

**Live checkboxes** for pipeline position and per-phase steps live under **`<skill_workspace>/abd-ooad/progress/`** — see **`library/strategy-execution-and-checklists.md`**. Do not use `strategy.md` for tick lists.

For canonical **module** terminology, the three-part stability test, and what to do when a cluster has no clear core class — see **`anchors`** in this library (detailed module framing is merged in when this phase is assembled).

---

A domain scan is not extraction. It is orientation. Before reading line by line for nouns and verbs, you do a rapid pass to answer three questions:

- What kind of source is this, and what technique fits it?
- Which concepts are clearly central and stable?
- Where is the complexity or ambiguity concentrated?

The scan calibrates how you will approach extraction. Without it, you risk either over-extracting noise from low-signal sections or missing the most loaded concepts entirely.

---

## Work order (Phase 1)

Do **analysis in domain markdown only**; **then** render Draw.io.

| Order | Artifact | Role |
|-------|----------|------|
| 1 | `domain-scan-results.md` | Findings: source map, anchors, tensions. |
| 2 | `domain-scan-model.md` | Integrated class-line listing per module — the **same** content the diagram will show. |
| 3 | `strategy.md`, `term-registry.md` | Plan and term rows (see **strategy-led-generation**, **term-registry**). |
| 4 | `domain-scan-model.drawio` | **After** 1–2 match: visual twin of the model — **using-diagram-cli**, not a separate analysis pass. |

Do **not** duplicate the same anchor inventory as both a giant table in results **and** a full repeat in the model file. Split by purpose (map vs class lines), or keep one integrated file if the project prefers.

---

## Techniques by source type

### Specification or structured document

For each **major section** (chapter, top-level heading):
- Read the section title and note it in the source map
- Read the first 1–2 paragraphs to understand what the section is about
- Sample 3–4 paragraphs from within the section at random to test your initial read
- Read the last 1–2 paragraphs to confirm scope

For **small subsections** (a page or less): read the first 2–3 sentences only — enough to confirm whether it introduces a new concept.

Also note: bold terms, defined terms, "shall/must/cannot/always/never" language (invariants), and any section that is visibly larger than its neighbours.

### Codebase

For each **top-level module or package**:
- Read the module/package name and any top-level docstring or README (first paragraph)
- List class names within; do not open method bodies yet
- Sample 2–3 classes that look most central or most large

Flag: "Manager", "Handler", "Service", "Factory", "Util" — these are often overloaded. Identify the 3 largest files by line count; they are usually the most coupled.

### Meeting notes or conversation transcript

- Count how many times each noun appears; frequency signals domain weight
- Read the opening and closing of the transcript in full (first and last 10%)
- Sample 3–4 passages from the middle at random
- Note moments of disagreement or hedging ("depends", "it depends", "sometimes") — boundary ambiguity
- Capture proper nouns: product names, role names, system names

### Domain expert session

- Read the opening in full — experts define their core vocabulary immediately
- Sample 3–4 exchanges from across the session
- Note any vocabulary the expert corrects; corrections are boundary markers
- Flag anything called "different" or "special"; these are often variant subtypes or exceptional states
- Record exact phrasing; expert language often maps directly to domain class names

---

## Output

After the scan, record:

| Output | Description |
|--------|-------------|
| **Source map** | What sections, modules, or files exist, and which look heaviest |
| **High-confidence central modules** | 3–7 modules that are clearly central and stable enough to start modeling from. Each is a **module**: a named thing with a clear core class you can identify by name. If you cannot name the core class, you have not found the module yet — see **`anchors`** in this library. |
| **Suspected tensions** | 1–3 places where the material seems inconsistent, ambiguous, or overloaded |
| **Strategy (in `strategy.md`)** | **Modeling scope**; **§1 source slices** (Goal, **Source**, Coverage, Importance); **§2 slice plan** (goal restated + phases per slice); **coverage across steps**; **cross-slice integration**; **anchor and subdomain elaboration**; **execution plan (normative)** — phase slugs with **slice IDs**; plus **approach** and **dated pivots** — see `strategy-led-generation` and `strategy-execution-and-checklists` in this library |
| **Progress (under `abd-ooad/progress/`)** | **Ticks only:** `strategy-run-checklist.md` (your planned phases + scope), `process-checklist.md` (full pipeline map), `<phase>-checklist.md` (phase steps) — generated by `generate.py` when missing; see `library/strategy-execution-and-checklists.md` |

---

## Term Registry

The registry is maintained in its own file — see `term-registry` in this library for column definitions, step short-name reference, and update protocol.

**At this step:** Add your 3–7 central modules using **Classification** (model role: `anchor (class + module)` vs `class`, etc.) and **Status** (OOAD scale: e.g. **Active**, **Tension**, **Candidate**) plus step codes from **`term-registry`** and **`anchors`**. Flag boundary conflicts with **Status = Tension** (not by overloading Classification). Do not bulk-add extraction terms yet — that happens at NOUNS/CANDS.

---

## Action Checklist

Before completing this step, verify all of these:

- [ ] Have you identified which source type you are working with?
- [ ] Do you have at least three central modules you are confident about?
- [ ] Have you flagged at least one suspected tension or ambiguous boundary?
- [ ] Have you recorded **`strategy.md`** with **§1 source slices**, **§2 slice plan**, **coverage across steps**, **cross-slice integration**, **anchor and subdomain elaboration** (every anchor’s attached types tied to **nouns-verbs / raw-candidate / responsibilities** — not only “Character”), and **execution plan (normative)**? See `strategy-led-generation` and `strategy-execution-and-checklists` in this library.
- [ ] With `active_skill_workspace` set, have you run `python scripts/base/generate.py --phase domain-scan` so `abd-ooad/progress/process-checklist.md`, `abd-ooad/progress/domain-scan-checklist.md`, and (when seeded from template) `abd-ooad/progress/strategy-run-checklist.md` exist? Align `strategy-run-checklist.md` with your execution plan. (See `library/strategy-execution-and-checklists.md`.)
- [ ] `domain-scan-results.md` is present and complete
- [ ] `strategy.md` is present
- [ ] `domain-scan-model.md` is present
- [ ] `domain-scan-model.drawio` is present
- [ ] `term-registry.md` exists, contains at least the scan's primary modules and terms, and every Term has a confidence level

If any of these are missing, extend the scan before proceeding.

---

## Required Output Files

**Five deliverables** under `<workspace>/abd-ooad/`:

| File | Template | Content |
|------|----------|---------|
| `domain-scan-results.md` | `templates/domain-scan-results.md` | Source map, central modules, and tensions (scan findings; not the long extraction plan) |
| `strategy.md` | `templates/strategy.md` | **§1 source slices**, **§2 slice plan**, **coverage**, **cross-slice integration**, **anchor and subdomain elaboration**, **execution plan**, **approach**, **dated pivots** — see `strategy-led-generation` in library |
| `domain-scan-model.md` | `templates/domain model template.md` | Class notation listing for each central module — name, fields with cardinality notation, supporting classes |
| `domain-scan-model.drawio` | built via `scripts/drawio_cli.py` | Modules as frames, core class + supporting classes inside each frame, intra-module and cross-module relationships |
| `term-registry.md` | see `term-registry` in library | Seeded with primary modules and visible tensions from the scan |

### Notation in `domain-scan-model.md` (class lines)

**Skill only — not part of the workspace file:** These rules belong in **`phases/domain-scan`** (here) and in **`anchors`**. The **`domain-scan-model.md` artifact** should be **model content only** (title, optional phase line, module sections, class lines). Do **not** paste methodology boilerplate (e.g. a “class-line convention” paragraph) into the project’s `domain-scan-model.md`.

At scan fidelity, each **class line** is either:

1. **Anchor (core class of a module)** — the class that passes the **anchor test** in **`anchors`**. Mark it with the UML stereotype **`<<Anchor>>`** (e.g. `Character : <<Anchor>>`, `Check : <<Anchor>>`). One primary anchor line per module section.

2. **Other classes in the module** — types, value objects, or structures that belong **inside** an anchor’s module (their attributes, associations, and invariants are scoped to that module). **Do not** put `<<Anchor>>`, `<<scan>>`, or any other stereotype on them. List them under the same `## [Module name]` section as the anchor; **do not** add redundant tags like `[supporting class — … module]` on each line — the section groups them.

Do **not** label every class with the same stereotype. Later phases may promote or refactor them; the scan only needs to distinguish **module cores** (`<<Anchor>>`) from **scoped types** (plain class names under the section).

**Live workflow checklists** (see **`library/strategy-execution-and-checklists.md`**), under `<workspace>/abd-ooad/progress/` when `active_skill_workspace` is set. Created on first `python scripts/base/generate.py --phase domain-scan` if missing:

| File | Role |
|------|------|
| `progress/process-checklist.md` | Pipeline position — one checkbox per phase in `skill-config` |
| `progress/domain-scan-checklist.md` | Steps copied from **## Action Checklist** above — **tick completion here** |

> Walkthrough diagrams are not produced at scan fidelity. The scan does not yet have the resolution needed for a meaningful sequence scenario. Walkthroughs begin at the nouns-verbs phase.

For module framing (core class, dashed frame, fields vs supporting classes), diagram CLI commands, templates, and layout rules — see **`anchors`** and **`using-diagram-cli`** in this library.
