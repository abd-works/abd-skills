---

## name: term-registry
description: >-
  Build or extend the shared term-registry.md from domain-scan orientation
  (domain-scan-results.md and your scan notes). Use after domain scan has
  produced a section map, or when the user asks to "seed the term registry",
  "capture terms", or formalize vocabulary before modeling.

# term-registry

## Purpose

Turn scan orientation into a **single shared vocabulary table**: `term-registry.md` — anchors, siblings, tensions, and notes.

## When to use this skill

Load this skill when **any** of the following apply:

- `**domain-scan`** has produced `**domain-scan-results.md**` and you need to **seed or extend** the term table.
- The user asks to **capture terms**, **seed the term registry**, or **formalize vocabulary** before modeling.
- You are about to run `**domain-model-skeleton`** and `term-registry.md` is missing or stale.
- You need **targeted** vocabulary fixes (not a second full corpus scan).

---

## Agent Instructions

1. **Templates**

Generate content using **every** template file in this skill’s `templates/` folder.
**Do not** emit only Markdown or only plain text unless the user **explicitly** asks for a single format.


| Template                      | What to produce                                                                                                                                                                                                                                                     |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `templates/terms-template.md` | `term-registry.md` under `<active_skill_workspace>/abd-ooad/`: one row per term; columns per template; Notes carry anchor labels, tensions, and reasoning. Do not paste long maintainer comment blocks into the engagement file unless the team wants them in-repo. |


**Consistency:** Column meanings and Notes labels must match the **Term capture** section below (this same file).



1. **Rules**

- Follow the **Term capture** section below for columns, labels, capture workflow, and evidence pointers.
- This skill has **no** bundled `rules/*.md`. After editing, act as a *peer reviewer*: check that anchors, siblings, and tensions are reflected in **Notes**, and that the table is usable for `**domain-model-skeleton`**.
- **Who is checking:** A **modeler** (rows support class lines and UML notes), and anyone tracing terms back to **Evidence** / source.

1. **Assembling this Skill**

This `**SKILL.md`** is maintained by hand. Use `**bundle_rules_into_skill_md.py**` only if a `rules/` folder is added later.

---

## What is a term registry?

The **term registry** is the project’s **shared vocabulary table**: one row per term, with **Skill** (which skill first captured the term), target, value, evidence links, and **Notes** that carry anchor reasoning and tensions. It is the bridge between **section map** and **model skeleton**.

**No full rescan.** Work from `domain-scan-results.md`, the prior scan, and `**term-registry.md`** as you edit it. **Targeted re-read** only when something is unclear (confirm an anchor, resolve a tension, quote evidence).

---

## Core concepts

### Workspace

Output: `<active_skill_workspace>/abd-ooad/term-registry.md` (engagement root from the parent agent’s `**workspace`** skill).

### Prerequisites

After `**domain-scan**` has produced `**domain-scan-results.md**` (and you have scan notes or memory of the source). `**domain-model-skeleton**` assumes `term-registry.md` exists and stays authoritative when it builds `domain-model-skeleton.md`.

### Seed with (domain-scan fidelity)

- **Core modules** — 3–7 top-level concepts that appear to own the most behaviour
- **Anchor class candidates** — primary class inside a module; mark `<<Anchor>>` if confident, leave stereotype blank if uncertain
- **Sibling class candidates** — terms alongside an anchor (subtypes, closely related entities in the same module)
- **Visible tensions** — terms straddling modules or unclear boundaries

Notes column labels commonly used at this fidelity:

- `High Confidence Anchor - {{why_this_module_or_class_is_central}}`
- `Sibling Candidate - {{anchor_term}} {{why_related}}`
- `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}`

---

## Term capture

The full loop for identifying, recording, and refining terms as you work through **skills** — registry format, evidence extraction, and update protocol.

### What a term is

A **Term** is any concept identified from the source material that may become part of the domain model. At identification time it is not committed to a model role — it might become a class, a property, a value type, an association, or nothing. The registry tracks terms as **later skills** determine what each one actually is.

**File:** `<workspace>/abd-ooad/term-registry.md`

### When to capture

Capture term information whenever you:

- Encounter a new concept in source material
- Refine an existing term (rename, reclassify, change Target or Value)
- Promote a term (candidate → Class, Module, Property, etc.)
- Split a term into two or reject one entirely

### Extraction steps

1. **Find the source passage** — the paragraph(s) that caused you to identify or change the term.
2. **Create an evidence block** — new file `<workspace>/abd-ooad/evidence/EVD-NNN.md` using `templates/evidence-block-template.md`.
  - Assign the next sequential ID (check `evidence/` for the highest current number).
  - Set `Terms:` to every term this passage supports — one passage often yields multiple terms.
  - Paste source text **verbatim** into the `evidence` code block.
  - Record locator precisely:
    - document: file, chapter, section, page
    - code: code file, class, method, line range.
3. **Update `term-registry.md`** — add or update the row; set `Evidence` column to the EVD ID(s).
  - Multiple blocks for one term: `EVD-001, EVD-003`
  - One block for multiple terms: same ID in each row

### Refinement triggers


| Trigger                       | Action                                                                              |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| First mention in source       | New EVD block + new registry row                                                    |
| Passage refines understanding | New EVD block + update existing row                                                 |
| Term promoted to modelled     | New EVD block when promoted, specify target; note the skill in **Notes** if helpful |
| Term split into two           | New EVD block for each                                                              |
| Term rejected                 | Keep EVD block; note rejection in it — never delete IDs                             |


### Registry columns

Use `templates/terms-template.md` for the file format.


| Column       | Role                                                                                                                                                                                                                                                                                                                                                |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Term**     | Concept name from source — exact word or phrase as found; rename in `refine-names` if needed.                                                                                                                                                                                                                                                       |
| **Skill**    | **Skill name** (kebab-case) for the skill that **first** captured the term — same string as the skill folder (e.g. `domain-scan`, `term-registry`).                                                                                                                                                                                                 |
| **Target**   | One or more of: `Module` | `Class` | `Property` | `Operation` | `Example` — always in that order. Use `<br>` to stack multiple. Blank = not yet modelled.                                                                                                                                                                                           |
| **Value**    | Dot notation per target in same order as Target, stacked with `<br>`: `Module` for Module, `Module.Class << Stereotype >>` for Class, `Module.Class.property` for Property, `Module.Class.operation` for Operation, `Module.Class.example` for Example. Stereotype inline after Class value with spaces: `<< Anchor >>`. Blank if not yet modelled. |
| **Evidence** | EVD ID(s) pointing to `evidence/EVD-NNN.md`. Use `<br>` to stack multiple.                                                                                                                                                                                                                                                                          |
| **Notes**    | Labelled analysis entries. Use standard labels (see Notes labels below) so any skill can find and filter term analysis. When the raw quote lives in an evidence block, write: *"see EVD-NNN"* and keep your analysis here.                                                                                                                          |


### Notes labels

**Every piece of data that can be associated with a term goes in the term registry — not in a separate document.** Use labels in the Notes column to make entries filterable and consistent across skills.


| Label                      | Format                                                                                                                                                            | Typical skill(s)                                                                           |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `Tension`                  | `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}`                                                                                              | domain-scan, any                                                                           |
| `High Confidence Anchor`   | `High Confidence Anchor - {{why_this_module_or_class_is_central}}`                                                                                                | domain-scan, any                                                                           |
| `Sibling Candidate`        | `Sibling Candidate - {{anchor_term}} {{why_related}}`                                                                                                             | domain-scan, nouns-verbs-rules-and-states                                                  |
| `Provisionally Classified` | `Provisionally Classified - {{kind}}? {{reason}}` — kind is one of `Entity`, `ValueObject`, `Enum`, `Policy`, `Role`, `Event`, `Process`, `Property`, `Operation` | raw-candidates                                                                             |
| `Classified`               | `Classified - {{kind}} {{reason}}` — kind is one of `Entity`, `ValueObject`, `Enum`, `Policy`, `Role`, `Event`, `Process`, `Property`, `Operation`                | thing-vs-data-about-a-thing, responsibilities-and-collaborators, properties-and-operations |
| `Anchor Boundary`          | `Anchor Boundary - {{challenge_or_support}} {{evidence_summary}}`                                                                                                 | nouns-verbs-rules-and-states                                                               |
| `Responsibility`           | `Responsibility - {{one_sentence_what_this_class_is_responsible_for}}`                                                                                            | responsibilities-and-collaborators                                                         |
| `Collaborator`             | `Collaborator - {{comma_separated_class_names_this_class_depends_on}}`                                                                                            | responsibilities-and-collaborators                                                         |
| `Invariant`                | `Invariant - {{rule_that_must_always_hold}}`                                                                                                                      | invariants-in-the-model, model-state-transitions, any                                      |
| `State Candidate`          | `State Candidate - states: {{list}} illegal transitions: {{list}}`                                                                                                | model-state-transitions                                                                    |
| `Bloat Signal`             | `Bloat Signal - {{what_clusters_are_mixed}} suggest: {{extract}}`                                                                                                 | watch-for-bloated-classes                                                                  |
| `Role Separation`          | `Role Separation - {{merged_role}} splits into: {{role_a}}, {{role_b}}`                                                                                           | smashed-abstractions-and-hidden-roles                                                      |
| `Cohesion Group`           | `Cohesion Group - {{group_name}} changes with: {{related_terms}}`                                                                                                 | design-bounded-contexts                                                                    |
| `Scenario Gap`             | `Scenario Gap - {{scenario}} exposes: {{missing_responsibility_or_operation}}`                                                                                    | validate-with-scenarios                                                                    |
| `Promoted`                 | `Promoted - {{from_target}} → {{to_target}} {{reason}}` — e.g. Property → Class when a property warrants its own type                                             | properties-and-operations, refine-names, any                                               |
| `Rejected`                 | `Rejected - {{why_not_modelled}}`                                                                                                                                 | any                                                                                        |
| `Renamed`                  | `Renamed - {{old_name}} → {{new_name}} {{reason}}`                                                                                                                | refine-names                                                                               |
| `Split`                    | `Split - into {{term_a}}, {{term_b}} {{reason}}`                                                                                                                  | any                                                                                        |
| `Merged`                   | `Merged - with {{other_term}} {{reason}}`                                                                                                                         | any                                                                                        |
| `Follow-up`                | `Follow-up - {{question_or_action}}`                                                                                                                              | any                                                                                        |


Labels are free-text after the colon — use plain sentences. Multiple labels in one Notes cell are separated by `<br>`. Later work in other skills **must** use this same convention when adding to existing rows.

### Targets

A single term may be modelled in many ways, captured as modelling "targets" in terms registry. Each term may also have more than one evidence passage that supports it. A single term can be both a Module and a Class; it will often be a class and property in another class. It can be grounded in multiple separate source passages. See `templates/terms-template.md` for format and worked examples.

### Skill names

Put the **skill name** in the **Skill** column: the kebab-case folder name of the skill where the term was first captured (e.g. `domain-scan`, `term-registry`, `domain-model-skeleton`). That is the stable identifier—**not** “Phase 1 / Phase 2” or other ordinals, which drift. If you use other OOAD-related skills in your workspace, their folder names are valid values too (same kebab-case rule). **There is no separate `phase_id` or `skill-config.json` lookup in this flow**—the column is literally the skill you were running.

### Evidence file naming

```
evidence/
  EVD-001.md
  EVD-002.md
  ...
```

Pad to three digits. Never reuse or delete an ID — rejected terms keep their evidence as audit trail.

Template: `templates/evidence-block-template.md`

### Template files (term capture)

- `templates/terms-template.md` — registry file format
- `templates/evidence-block-template.md` — evidence block format

---

## Example

A single row illustrates the shape (values illustrative):


| Term    | Skill       | Target       | Value              | Evidence | Notes                                                            |
| ------- | ----------- | ------------ | ------------------ | -------- | ---------------------------------------------------------------- |
| Payment | domain-scan | Module Class | Payment Payment <> | EVD-001  | High Confidence Anchor — every flow routes settlement through it |


## The shape of a good `term-registry.md`

```markdown
# Term Registry — {{project_name}}

| Term | Skill | Target | Value | Evidence | Notes |
|------|-------|--------|-------|----------|-------|
| {{Term}} | {{skill-name}} | {{Module<br>Class}} | {{Module<br>Module.Class << Stereotype >>}} | {{EVD-NNN}} | {{reasoning / tensions / follow-ups}} |
```

Expand with real rows only; keep **Notes** rich enough that **`domain-model-skeleton`** can write one-sentence UML `note:` lines per term.

---

## Build

**Goal:** Author or extend `term-registry.md` from the section map and scan memory.

- **Outputs:** `term-registry.md` under `<active_skill_workspace>/abd-ooad/`. Align with `templates/terms-template.md`.
- **Per format:** Markdown table; optional evidence files under `evidence/` per **Term capture** above.
- **While writing:** Keep **Notes** labels consistent; link **Evidence** where you quote or paraphrase source.
- **Persistence:** Engagement root from parent agent `workspace`; table lives in `abd-ooad/term-registry.md`.

---

## Validate

**Goal:** Review the registry like a peer before **`domain-model-skeleton`** (or a modeling handoff) — **not** a second full corpus scan. Use **spot checks** and **cross-walks** between artifacts; fix gaps with **targeted** re-reads of the source or `domain-scan-results.md` only where something fails a check.

### Who is checking

- **You (author):** Before closing the registry pass, work through the checklist below.
- **Consumer of `domain-model-skeleton`:** They need every modeled term to be **defensible** from evidence, **typed** in **Target** / **Value**, and **legible in Notes** (anchor, sibling, tension) so `note:` lines and class rows do not require guesswork. If a row cannot support a one-sentence UML `note:`, it is not done.

### Evidence

- **Files exist:** Every **`EVD-NNN`** cited in the **Evidence** column has a file `abd-ooad/evidence/EVD-NNN.md` (padding matches how you name files).
- **Round-trip:** In each EVD file, `Terms:` includes every term row that lists that EVD; every term in `Terms:` has a row that cites that EVD (or document why a term was dropped in that EVD’s body).
- **Auditability:** Locators in EVDs are **specific** (file, section, page, or code range — per **Term capture**). Rejected or superseded terms do **not** delete old EVD IDs; **Notes** or the EVD explains the change.
- **Quotes vs Notes:** If analysis leans on a passage, either the passage is in the EVD or **Notes** say *see EVD-NNN* and the EVD holds the quote.

### Rows (structure and labels)

- **Skill:** Every row has a **Skill** value (the skill that first captured the term).
- **Target / Value:** Stacking order is consistent (**Target** order matches **Value** lines). **Value** uses dot notation and stereotypes as in **Term capture**; no impossible paths (e.g. property without a class in the path) unless **Notes** flag it as a tension or follow-up.
- **Notes:** Terms that are **anchors**, **siblings**, or **tensions** use the standard **Notes labels** (see **Notes labels** above), not only free text. Gaps in coverage vs `domain-scan-results.md` are **on purpose** and called out, not silent.

### Match to the model sketch

Do this when **`domain-model-skeleton.md` already exists** or is **about to** be built from the registry. Cross-skill convention: section headings in **`domain-model-skeleton.md`**, **`domain-noun-verb.md`**, and **`terms.md`** use **`## [Name]`** (anchor name only) — **not** `## [Name module]`.

- **Same names, same locus:** For each class or module in the sketch that is supposed to represent a term, a registry row’s **Value** points at the same **module** / **Module.Class** path (or the row explains a deliberate name skew in **Notes**).
- **Targets match role:** If the sketch shows a term as a **class**, **Target** includes **Class** and **Value** has a class line; if unmodelled in the sketch, **Target** / **Value** are blank and **Notes** say why (tension, deferred, or rejected).
- **Anchor test:** **High-confidence anchors** in **Notes** have a **home** in the scan model (module + core class, or a recorded tension with `domain-model-skeleton` in mind). No anchor that the sketch depends on is missing from the registry.
- **Dry run for `note:`:** For each row you expect to show up in the model, mentally write **one sentence** for a UML `note:` from **Notes** alone. If you cannot, strengthen **Notes** or the evidence link.

### Light alignment with the section map

- **domain-scan-results.md** major areas and tensions have **enough** registry rows that nothing critical is unrepresented; if you skipped an area, **Notes** or the scan map say so (briefly).

If the registry is thin or wrong, **improve in place** with targeted evidence or map passes — not a wholesale rescan unless the source or goals changed.

---

<!-- execute_rules:bundle_rules:begin -->
<!-- No rules/*.md for this skill yet. If rules are added, bundle with:
     python skills/execute_using_rules/scripts/bundle_rules_into_skill_md.py --skill-root <this-skill-dir>
-->
<!-- execute_rules:bundle_rules:end -->

