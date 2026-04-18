# Domain scan

## Outcome:
You have a list of initial terms, 3–7 high-confidence **central modules** (each with a named core class), and a list of suspected tensions — enough orientation to begin extraction as a targeted pass rather than a mechanical word sweep.

A domain scan answers three questions - each maps to an artifact:

- *What kind of source material, and how do we parse it?* → `term-registry.md`
- *Which concepts are clearly central?* → `term-registry.md` (Notes: `High Confidence Anchor`) and `domain-scan-model.md`
- *Where is there complexity, ambiguity, or tension?* → `term-registry.md` (Notes: `Tension`) and `strategy.md`

Without scan calibrates you risk either over-extracting noise from low-signal sections or missing the most loaded concepts entirely.

---

## Step 1: Scan
Scan source material considering the best approach based on the nature of te source material.

### Specification or structured documents

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

## Step 2: Seed Terms 
Seed key term from source into `term-registry.md` — the project's shared vocabulary file. At scan time, seed it with:
   - **Core modules** — the 3–7 top-level concepts that appear to own the most behaviour
   - **Anchor class candidates** — terms that look like the primary Class inside a module; mark with `<< Anchor >>` if confident, leave stereotype blank if uncertain
   - **Sibling class candidates** — terms that appear alongside an anchor (subtypes, closely related entities within the same module)
   - **Visible tensions** — terms that seem to belong to more than one module, or whose boundary is unclear

   Use Notes column labels for each entry (see **`library/term-capture`** for the full label list). At scan time the most common are:
   - `High Confidence Anchor - {{why_this_module_or_class_is_central}}`
   - `Sibling Candidate - {{anchor_term}} {{why_related}}`
   - `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}`

   See below section on **Term Capture** below for details on term registry format and approach.

   template: `templates/terms-template.md`

## Step 2 - Map Source Sections - create a map that organizes and summarizes source material into cohesive sections based on topic categorization. Create `domain-scan-results.md`.

template: `templates/domain-scan-results.md`

## Step 3. `domain-scan-model.md` - initial model skeleton; class-line listing per module — exactly what the diagram will show.

template: `templates/domain model template.md`

Translate anchor and sibling candidates from `term-registry.md` into a module/class skeleton. This is not a deep model yet — it is a first-pass structural draft so anchor boundaries are visible.

Add one module block with its anchor class and any sibling class candidates already identified. For each class add only properties and operations that are already evident from the scan — do not invent structure.

**UML notes:** attach a `note:` line immediately after each class or module declaration for every term that has a row in `term-registry.md`. One sentence — term name, then why it exists. Tag with `[s1-p0]`. Deeper reasoning stays in the `term-registry.md` Notes column. See `templates/domain model template.md` for the full tag table and example.

## Step 4
4. `domain-scan-model.drawio` - visual twin of the model; render **after** 1-3 are complete using **using-diagram-cli**.
template: `templates/domain model template.drawio`

5. `strategy.md` - modeling scope, source slices, slice plan, execution plan (see **strategy-led-generation**). Progress ticks go in `abd-ooad/progress/` - not here.
template: `templates/strategy.md`

---

## Action Checklist

Before completing this step, verify all of these:

- [ ] `term-registry.md` — source type identified; core modules and anchor candidates present; tensions and high-confidence anchors labelled in Notes column.
- [ ] `domain-scan-results.md` — source map and section anchors recorded; file present.
- [ ] `domain-scan-model.md` — present; every module and class has a UML note linking back to its term-registry row with a one-sentence rationale.
- [ ] `domain-scan-model.drawio` — present.
- [ ] `strategy.md` — recorded with source slices, slice plan, coverage, cross-slice integration, anchor elaboration, and strategy-run-checklist plan and strategy-run-checklist exist and are aligned with your execution plan.

If any of these are missing, extend the scan before proceeding.

---

### Notation in `domain-scan-model.md` (class lines)

**Skill only — not part of the workspace file:** These rules belong in **`phases/domain-scan`** (here) and in **`anchors`**. The **`domain-scan-model.md` artifact** should be **model content only** (title, optional phase line, module sections, class lines). Do **not** paste methodology boilerplate (e.g. a “class-line convention” paragraph) into the project’s `domain-scan-model.md`.

At scan fidelity, each **class line** is either:

1. **Anchor (core class of a module)** — the class that passes the **anchor test** in **`anchors`**. Mark it with the UML stereotype **`<<Anchor>>`** (e.g. `Character : <<Anchor>>`, `Check : <<Anchor>>`). One primary anchor line per module section.

2. **Other classes in the module** — types, value objects, or structures that belong **inside** an anchor’s module (their attributes, associations, and invariants are scoped to that module). **Do not** put `<<Anchor>>`, `<<scan>>`, or any other stereotype on them. List them under the same `## [Module name]` section as the anchor; **do not** add redundant tags like `[supporting class — … module]` on each line — the section groups them.

Do **not** label every class with the same stereotype. Later phases may promote or refactor them; the scan only needs to distinguish **module cores** (`<<Anchor>>`) from **scoped types** (plain class names under the section).

**Live workflow checklists** (see **`library/strategy-execution-and-checklists.md`**), under `<workspace>/abd-ooad/progress/` when `active_skill_workspace` is set. Created on first **`python scripts/base/generate.py --phase domain-scan --slice <slice-id>`** (default **`main`**) if missing:

| File | Role |
|------|------|
| `progress/slices/<slice-id>/domain-scan-checklist.md` | Steps copied from **## Action Checklist** above — **tick completion here** |

**Strategy (which phases next):** `strategy.md` + `progress/strategy-run-checklist.md` — see **`library/strategy-execution-and-checklists.md`**.

> Walkthrough diagrams are not produced at scan fidelity. The scan does not yet have the resolution needed for a meaningful sequence scenario. Walkthroughs begin at the nouns-verbs phase.

For module framing (core class, dashed frame, fields vs supporting classes), diagram CLI commands, templates, and layout rules — see **`anchors`** and **`using-diagram-cli`** in this library.
