---
name: module-partition
catalog_garden_order: 1
description: >-
  After domain scan, partition the source corpus into modules by allocating
  source file references to per-module index files. No classes, no anchors â€”
  only module boundaries and file references to the source that belongs to
  each. Supports an Unallocated bucket for pending decisions and a Rejected
  bucket for out-of-scope context. Modules are flat by default and nested only
  when the source itself supports a sub-module. Use when the user asks to
  "partition the source", "allocate context to modules", "draw module
  boundaries", or needs a defensible scope cut before any class-level modeling.
---
# module-partition

## Purpose

Produce a **root index** (`module-partition.md`) plus **per-module files** under `abd-domain-driven-design/modules/` â€” each containing scope, core terms, and **source file references** (not verbatim copies). No classes, no anchors, no UML, no stereotypes. Just boundaries and pointers to the source text that lives inside them.

This is the *scope cut* before any class identification. It answers a single question for every chunk of source: **which module does this text belong to** â€” or is it **unallocated** (pending) or **rejected** (out of scope)?

### Why references, not verbatim copies

When the source is already structured as individually addressable files (corpus chunks, markdown files, scanned documents), copying their full content into the partition document is pure duplication. The partition's real value is the **allocation decision** â€” which files belong to which module. Downstream agents read the module file to get the file list, then read the actual source files as needed. This keeps module files small, avoids duplication, and supports parallel agents working one module at a time.

## When to use this skill

Load this skill when **any** of the following apply:

- `**domain-scan-results.md**` exists and you need to commit to **module boundaries** before extracting terms or sketching classes.
- The user asks to **partition the source**, **allocate context to modules**, **draw module boundaries**, **cut scope**, or **decide what's in/out** of the model.
- A scan tension calls for **physically splitting** the source by module so a later pass (term-registry, nouns-verbs, domain-model-skeleton) operates on a **bounded slice**, not the whole corpus.
- You need a **defensible "what's out of scope"** record that survives later phases (catalogs, settings, adventure scripts, marketing prose).

This skill **does not** define classes, anchors, properties, operations, responsibilities, or stereotypes. Those belong to `**term-registry`**, `**nouns-verbs-rules-and-states`**, `**domain-model-skeleton**`, and later OOAD skills.

---

## Agent Instructions

1. **Templates**

Generate content using **every** template file in this skill's `templates/` folder. **Do not** emit only Markdown or only plain text unless the user **explicitly** asks for a single format.

| Template | What to produce |
| -------- | --------------- |
| `templates/module-partition-template.md` | Root index `module-partition.md` under `<active_skill_workspace>/abd-domain-driven-design/` â€” lists all modules with scope, core terms, chunk ranges, and links to per-module files. |
| `templates/module-file-template.md` | One file per module under `<active_skill_workspace>/abd-domain-driven-design/modules/` â€” scope, core terms, and **source file references** (file path + locator per source file, no verbatim content). Also produce `modules/rejected.md` and optionally `modules/unallocated.md`. |

2. **Rules**

- **Source files on disk are the only allowed input.** Every `Source:` reference must point to a file the reviewer can open and verify (corpus chunk, scanned document, user-supplied context file). If no source files exist, **stop and tell the user** â€” do not generate, reconstruct, or summarize content from training data or domain knowledge as a substitute.
- Follow the **Allocation rules** and **Reference format** sections below for what counts as a module, when to nest, and how to label references.
- Source file references must be accurate: the file must exist, the locator must be correct. No invented file paths or fabricated locators.
- After drafting, act as a *peer reviewer*: every reference has a locator and lives under exactly one module file (or `unallocated` / `rejected`); no module exists without references; no nesting exists without source-supported justification.

3. **Who is checking**

A **boundary reviewer** â€” someone who needs to defend the scope cut to the team. They read the file front-to-back and ask: *can I trust that every paragraph in the source ended up exactly one place, and that the place is justified by the source itself?*

---

## What is module partitioning?

A **module** is a named region of the domain â€” a slice of the source the modeler intends to treat as one bounded scope in later passes. At this fidelity, a module is **only** a name + a body of source extracts; it carries **no classes, no anchors, no behavior**.

A **partition** is the assignment of every meaningful chunk of source to exactly one of:

1. A **named module** (top-level or â€” only when the source supports it â€” a sub-module of one),
2. **`Unallocated`** â€” text that clearly matters but whose home is undecided,
3. **`Rejected`** â€” text that is intentionally **out of scope** (front matter, marketing prose, settings/adventures, license, etc.).

**Partitioning is a commitment.** Each piece of source has one home. If you find yourself wanting to put the same passage in two modules, that is a **tension** â€” record it under the module you chose and note the alternative, or move it to `Unallocated` until a later pass resolves it.

**Prerequisites:** `domain-scan-results.md` from `**domain-scan`**, plus access to the source memory chunks. Do **not** rescan the corpus; work from the scan map and **targeted** re-reads.

### Hard prerequisite â€” source files must exist

**STOP** if there are no readable source files (corpus chunks, scanned documents, or user-supplied context files) on disk. This skill copies verbatim text from source files into module sections. If the source files do not exist, there is nothing to copy and the skill **cannot run**.

- **Do not** generate, reconstruct, or summarize domain knowledge from the agent's training data as a substitute for source files. That is not partitioning â€” it is authoring, and it belongs to a different skill.
- **Do not** write "domain-knowledge" extracts, paraphrased descriptions, or memory-based rule summaries into the `\`\`\`source` blocks. Every byte inside a source block must be traceable to a file the reviewer can open and verify.
- If the user asks to partition but the corpus is empty, **tell the user** that source material must be loaded first and offer to help populate the source directory. Do not silently proceed with generated content.

---

## What is â€” and is not â€” a module (DDD-grounded)

> "MODULES are a communications mechanism. The meaning of the objects being partitioned needs to drive the choice of MODULES. When you place some classes together in a MODULE, you are telling the next developer who looks at your design to **think about them together**." â€” Eric Evans, *Domain-Driven Design*, Ch. 5
>
> "**High cohesion** of objects with related responsibilities allows modeling and design work to concentrate within a single MODULE â€” a scale of complexity a human mind can easily handle." â€” Evans

A module in this skill is the same **MODULE** Evans describes in DDD: a named, **high-cohesion / low-coupling** region of the domain. It is **not** a heading, a feature, a single concept, or a section title in the source.

### The independence test (the only test that matters)

For any candidate boundary, ask:

> **Can a reader, modeler, or downstream pass reason about *this* slice with meaningful independence from the *other* slices â€” without needing to constantly cross-reference them?**

- If two clusters of source **must** be reasoned about together (one constantly references rules, terms, or invariants of the other), they belong in **one** module. Forcing a boundary between them creates a coupling magnet you'll have to untangle later.
- If a cluster can be **discussed, modified, taught, or modeled** with only an arm's-length reference to its neighbours, it earns its own boundary.

A useful sanity check: if you can describe what changes inside Module A without saying anything substantive about Module B, the boundary is real. If your first sentence about A is a definition that references B, they're one module.

#### Standalone-mechanic test (sharper form for procedural domains)

For each *pair of mechanics* inside a candidate module, ask:

> **Can mechanic A run completely without mechanic B?**

- If yes â€” if you could write down mechanic A in full and a reader could use it without ever knowing mechanic B exists â€” then A and B do **not** belong in the same module. They may *reference* each other in play, but each is its own bounded mechanism and earns its own scope.
- If no â€” if you cannot describe mechanic A without invoking the rules or vocabulary of mechanic B (e.g. "a wire transfer is a funds transfer with same-day settlement and a regulatory message" â€” you cannot say "wire transfer" without "funds transfer") â€” they are the **same** mechanism in different applications, and they belong together.

This is the sharper form of the independence test for **procedural / rules-style** domains, where the unit of analysis is a *mechanic* rather than a concept. Use it in addition to (not in place of) the kind-test:

- The **kind-test** catches modules that mix unrelated *kinds* (resolution + state vocabulary + meta-currency stuffed into one bag).
- The **standalone-mechanic test** catches modules that mix unrelated *mechanisms within the same kind* â€” for example, two distinct resource-economies under one resource-economy umbrella, or two unrelated state vocabularies forced under one state-module heading.

Two short illustrations from a payments / banking domain:

- *Wire Transfer* and *ACH Transfer* are both forms of *Funds Transfer*. You cannot describe either without invoking the underlying transfer mechanism (debit a source account, credit a destination account, reconcile). **Same mechanism, different applications â†’ same module** (a `[Funds Transfer]` module).
- *Refund* (merchant-initiated reversal of a captured payment) and *Chargeback* (customer-initiated dispute that reverses a captured payment) reference each other in their rules â€” an issued refund pre-empts a chargeback; a successful chargeback often blocks a follow-up refund â€” but each runs on its own with its own triggers, actors, and SLA. The user can defensibly keep them together (because they are the *same kind* â€” payment-reversal mechanics â€” and the cross-references are dense) or split them (because each is a self-contained mechanism). The test surfaces the choice rather than dictating it. The deciding factor is usually whether splitting forces the reader to bounce between modules to follow a single mechanic; if so, merge.

### Cohesion and coupling, in practice

- **Cohesion (inside the boundary):** Every extract in the module shares a single overarching subject. The terms, rules, and invariants reinforce each other; removing any one would leave the module noticeably less complete.
- **Coupling (across the boundary):** Modules will reference each other â€” that's fine and expected â€” but the references are *named pointers*, not a shared web of intermingled rules. If Module A's text only makes sense when Module B's text is at hand, they are coupled, not bounded.

### Modules are not the source's headings

This is the most common mistake. A book's chapter, section, or subsection structure is **organizational scaffolding for readers**, not a domain partition. In particular:

- A single source heading often belongs *inside* a module â€” it is a **content-level heading inside one bounded scope**, not a module of its own.
- A single module often spans **multiple** source headings, sometimes across multiple chapters.
- "I see a `####` in the source" is **not** a reason to create a module. Promote a heading to a module only if it survives the independence test.

### Watch for *kind-mixing* â€” when one source heading hides multiple modules

When a source's organizational heading (a TOC chapter, an all-caps section break, a named cluster like `OPERATIONS`, `RULES`, or `WORKFLOW`) shelves content of **multiple kinds** under one umbrella, the heading is **editorial shelving**, not a domain partition. Forcing the heading to become a module creates a coupling magnet that fails the independence test on inspection.

After drafting modules, ask of each one: ***what kind of thing is this module about?*** If the answer is "more than one kind", split.

Common kinds in rules-style and procedural domains (rough catalog, not exhaustive â€” examples are deliberately **not** drawn from the corpus you are partitioning):

- **Resolution** â€” how outcomes of uncertain operations are determined (validation rules, eligibility checks, authorization steps).
- **Scaling / Measure** â€” how trait or quantity values translate to real-world values (rate cards, conversion tables, unit-of-measure mappings).
- **Actor** â€” entities that take action (customers, merchants, accounts, claims, agents).
- **Temporal structure** â€” billing cycle, turn, phase, sequence; the time grid of the process.
- **State vocabulary** â€” statuses, modes, lifecycle stages an entity can be in (Pending, Authorized, Captured, Refunded, Disputed, Settled).
- **Resource economies / meta-currency** â€” internal currencies that gate behavior (account balance, credit limit, loyalty points, refund credits).
- **Behavior catalogs** â€” explicit lists of capabilities, products, or features (product catalog, fee schedule, promotion list).
- **Constraint systems** â€” limits, thresholds, regulatory rules (KYC tier, transaction caps, eligibility constraints).

A module that draws extracts from more than one of these kinds is almost always two-modules-disguised-as-one, even when a single source heading puts them together. Two warning signs:

1. The **Core terms** list visibly clusters into separate vocabularies (one cluster of process verbs, one cluster of unrelated state nouns, one cluster of currency terms).
2. The module name keeps wanting to be a compound or generic noun (`[Operations]`, `[Foundations]`, `[Basics]`, `[Core]`) because no single kind fits.

When you see those signs, split until each module has **one kind**.

### Modules are not (necessarily) single concepts â€” but they ARE single-kind

A module is a **collection** of related domain content of a single kind. Two clarifications follow:

- A small, *single-kind* bounded scope **is** a legitimate module, even if its vocabulary is short. In a payments domain, `[Loyalty Points]` (an internal currency with a small set of earn-and-spend rules) is a legitimate module â€” it is one kind (resource economy) with its own bounded vocabulary. `[Order Status]` (a state vocabulary of named statuses with transition rules) is a legitimate module of a different kind (state vocabulary). They are not "single concepts" â€” each is a small bounded scope.
- A single *concept* â€” one rule, one term, one feature â€” that does not carry its own vocabulary or invariants is an **anchor or class inside another module**, not a module itself. A single status name like `Authorized` would be an anchor inside `[Order Status]`; it does not earn its own scope.

The distinction is **kind + bounded vocabulary**, not size. Some legitimate modules are large; some are small; the test is the same.

If you have produced more than ~10 top-level modules from a corpus, or every section in the TOC has become a module, you have **over-partitioned**. Collapse aggressively to bounded scopes that pass the independence test, then revisit.

### Heuristics for naming a real module

A module name should answer **"what bounded scope is this?"** in one short, source-grounded noun phrase that names the **kind**.

**Single-noun rule.** If you can pick a single noun (or tight noun phrase) the source itself uses for the kind, that is the right name. If you keep reaching for compounds or generic glue (`[Operations]`, `[Authorization & Capture]`, `[Foundations]`, `[Core]`, `[Basics]`), you are almost certainly trying to name a multi-kind bag â€” split until each module accepts a single-noun name.

(Examples below are drawn from a payments / banking domain â€” illustrative, not the corpus you are partitioning.)

| Name | Verdict | Reason |
|------|---------|--------|
| `[Funds Transfer]`, `[Authorization]`, `[Settlement]`, `[Order Status]`, `[Loyalty Points]`, `[Billing Cycle]`, `[Catalog]`, `[Customer]` | âœ… | Single kind, source-grounded, short noun. |
| `[Operations]`, `[Foundations]`, `[Basics]`, `[Core]`, `[Mechanics]`, `[Workflow]` | âš ï¸ | Generic / multi-kind. Often a TOC heading rather than a kind. Split or rename. |
| `[Refund & Chargeback]`, `[Authorization & Capture]` | âš ï¸ | Compound names usually signal two kinds (or two mechanisms) glued together. Split unless the conjunction is genuinely indivisible. |
| `[Chapter 1]`, `[Section 3.2]`, `[Part II]` | âŒ | Source-structure naming, not domain naming. |
| `[Misc]`, `[Other]`, `[Foundation]` (without source grounding) | âŒ | Generic placeholders that hide ambiguity. |

### Module decisions coevolve with the model

Module boundaries are **not** final on first pass â€” but they are deliberately costlier to change than later artifacts. Evans:

> "Refactoring MODULES is more work and more disruptive than refactoring classes, and probably can't be as frequent. [â€¦] Letting the MODULES reflect changing understanding of the domain will also allow more freedom for the objects within them to evolve."

Choose conservative, well-justified boundaries now; expect them to refine as `term-registry`, `nouns-verbs-rules-and-states`, and `domain-model-skeleton` reveal deeper structure.

---

## Core concepts

### Workspace

Output directory: `<active_skill_workspace>/abd-domain-driven-design/` (engagement root from the parent agent's `**workspace`** skill).

Files produced:
- `abd-domain-driven-design/module-partition.md` â€” root index listing all modules
- `abd-domain-driven-design/modules/<module-name>.md` â€” one per module, with source file references
- `abd-domain-driven-design/modules/rejected.md` â€” rejected files with reasons
- `abd-domain-driven-design/modules/unallocated.md` â€” (optional) pending allocation decisions

### Modules â€” flat by default, hierarchical only when the source earns it

- **Default shape is flat.** Most corpora produce **4â€“10 top-level modules for the entire corpus** (not per chapter, not per section). A single chapter often produces zero, one, or two modules â€” never one per heading. If you find yourself producing more than ~10 modules total, re-apply the **independence test** above and collapse aggressively.
- **Nest only when the source itself supports a real sub-module** â€” a self-contained slice that has its own bounded behavior, terminology, and extract set, *and* whose existence is independently visible in the source (a dedicated chapter, a named subsystem, a clearly separated rule cluster).
- **Do not nest just to organize.** A nested heading without its own non-trivial extract set is wrong â€” collapse it back into the parent or promote it to a top-level module.
- **Do not nest by section/paragraph proximity.** Source structure (chapter â†’ section â†’ subsection) is **not** the same as module structure. A single chapter often produces multiple top-level modules; a module often draws extracts from many chapters.
- **Stay at module level.** Even when nested, every level is still a module â€” no sub-module decomposes into classes, properties, or operations here.

If you cannot point at the source and say "this sub-module has its own extracts and its own boundary", do not nest.

### Section titles

- Each module is introduced by `## Module: [Name]` at top level. Sub-modules use `### [Name]` (the `Module:` prefix is implicit at deeper levels because they sit under a `## Module: â€¦` parent). The `Module:` prefix on top-level headings makes it unambiguous to a reviewer that the heading is a partition module â€” not a content-level heading copied or paraphrased from the source.
- Brackets around the name; **no** ` module` suffix in the heading (`## Module: [Combat]`, not `## Module: [Combat module]`).
- Reserved names â€” used **exactly** once each: `## Module: [Unallocated]`, `## Module: [Rejected]`. They are top-level only and never nested under another module.
- Names are short, source-grounded, and stable. Prefer the noun the source itself uses; fall back to a one-word descriptive name only if no source noun fits.

### Allocation rules

For every source file you decide to allocate:

1. **Pick the module** whose scope best matches the file's *primary* subject. If two modules match equally, the file is a tension â€” pick one and note the alternative in the reference header, or move to `Unallocated`.
2. **Decide whole vs partial.** Whole references allocate the entire file. Partial references allocate a contiguous slice; non-contiguous selection is two references, not one.
3. **Reference the source file on disk.** Every `Source:` line must point to a real file the reviewer can open. No paraphrase, no reconstruction, no agent-generated content. If you cannot point to a file path, the reference does not belong in this artifact.
4. **Label.** Every reference gets a header block (see **Reference format**) with locator, whole/partial, and â€” if partial â€” a clause naming exactly which part is allocated.
5. **Stop when the file has a home.** Do not add a paraphrase or summary alongside the reference. The source file is the content.

### When to use Unallocated

A chunk goes to `## [Unallocated]` when **all** of these are true:

- It clearly matters for the domain model (it carries terms, rules, or invariants you do not want to lose).
- You cannot defensibly assign it to exactly one existing module.
- Creating a new module *just* for it would be premature (you have not seen enough related material yet).

Each `Unallocated` extract carries a `Reason:` line in its header explaining the ambiguity (e.g. *spans Authorization and Settlement*, *might warrant its own module after a later pass over the corpus*).

### When to use Rejected

A chunk goes to `## [Rejected]` when it is **intentionally out of scope** for the domain model. Typical rejections:

- Front matter â€” cover, credits, table of contents, license, index.
- Setting / lore / flavor prose â€” proper nouns, history, geography, character bios â€” when the model is for *rules*, not *content*.
- Worked examples and adventure scripts that illustrate but do not define rules.
- Marketing copy, designer notes, "under the hood" sidebars when they do not change behavior.

Each `Rejected` extract carries a `Reason:` line stating *why* it is out of scope. **Never delete a rejection silently** â€” the rejection record is the audit trail.

### Core terms â€” a lightweight read-out of what each module *contains*

Module partitioning is a scope cut, **not** a term registry. The full term-capture loop (Targets, Values, Evidence files, Notes labels, anchor stereotypes) belongs to `**term-registry**` â€” **do not** do that work here.

But each module section does carry a short, source-grounded **Core terms** list directly under the module heading and scope statement, *before* the verbatim extracts. The point is purely diagnostic: at a glance, a reviewer (and you) can see whether the module is the bounded scope you claim it is, or whether the terms inside it actually pull in two directions and the module needs to split.

**What goes in the list**

- **Source-grounded noun phrases** the source itself uses inside the module's extracts (e.g. *funds transfer*, *billing cycle*, *authorization hold*, *settled status*).
- Listed **flat**, in source order (or grouped lightly by sub-area when the list is long).
- Use the source's casing and exact phrase. No renaming, no normalization. That is `**refine-names**`'s job.

**What does NOT go in the list**

- No targets, values, or stereotypes (`<<Anchor>>`, `Module.Class`, etc.) â€” that is `**term-registry**`.
- No `EVD-NNN` evidence IDs, no evidence files. The verbatim extracts in the same module section *are* the evidence at this fidelity.
- No `Notes:` labels (`High Confidence Anchor`, `Sibling Candidate`, `Tension`, etc.) â€” that is `**term-registry**`.
- No tables. A simple bullet list.
- No invented terms, no synonyms the source does not use.

**How to use the list to test the boundary (back to the independence test)**

Once each module has its Core terms list, ask:

1. **Does the list read as one bounded vocabulary?** If the terms feel like *two* coherent vocabularies stuck together (e.g. one cluster of process verbs + one cluster of unrelated geometry nouns), the module probably needs to split.
2. **Does the list lean heavily on terms defined in another module?** If most entries are forward references to another module's anchors, your scope cut is probably misplaced â€” the content belongs in that other module, or this module is really a sub-scope of it.
3. **Is the list trivially short (one or two terms)?** Then the "module" is almost certainly a single concept and should fold into a larger one.
4. **Is the list overwhelming and uneven (50+ terms with no center of gravity)?** Then the module is probably too coarse and may genuinely contain two bounded scopes the source treats together.

The Core terms list is the cheapest possible way to make the cohesion-and-coupling argument visible *inside the partition file itself*, without crossing into term-registry territory.

### Tensions inside an allocation

If an extract is allocated to a module but also has meaningful pull toward another, add an `Also relates to:` line in its header. This is **not** a second allocation â€” the extract still lives in exactly one section. It is a flag for downstream skills (especially `term-registry`) that the boundary is contested.

### What you do not do here

- Do **not** identify classes, anchors, properties, operations, or responsibilities.
- Do **not** rename source terms or normalize vocabulary â€” that is `**refine-names**`.
- Do **not** invent modules for concepts the source does not name as a coherent scope.
- Do **not** add `note:` lines, `[dms]` tags, or any UML notation. The artifact is a partitioned reading list, not a model.

---

## Reference format

Every source file reference sits inside a **per-module file** under a **reference header** so a reviewer can verify allocation without re-opening the source.

### Reference header (required for every source file)

```
**Ref â€” {{short title}}**
Source: {{relative_path_to_source_file}}
Locator: {{chapter / page / lines / topic â€” whatever is precise for this source type}}
Extract: {{whole | partial}}
{{Part: {{which slice is relevant â€” required when Extract: partial}}}}
{{Also relates to: [{{other module name}}] â€” {{one-line why}}}}
{{Reason: {{why this lives in Unallocated or Rejected â€” required in those sections}}}}
```

- The `Extract:` line is `whole` when the entire file is allocated to this module, `partial` when only a slice is relevant.
- When `Extract: partial`, the `Part:` line is **mandatory** and names the slice in source-grounded terms (e.g. *paragraphs 1â€“2 of "Refund Eligibility" subsection*, *lines 14â€“22*).
- `Also relates to:` is optional, used to flag tensions on an otherwise clean allocation.
- `Reason:` is required in `rejected.md` and `unallocated.md`; omit in module files.

### No verbatim copy â€” reference only

The reference header points to the source file; the file itself is the authoritative content. Downstream agents read the module file to learn which source files belong to the module, then read those files directly. This avoids duplication and keeps module files small.

### One reference = one allocation

If a single source file has two unrelated parts that belong in two different modules, that is **two references** â€” one in each module file, each with `Extract: partial` + `Part:` line. Never split across modules without splitting the reference.

---

## The shape of good output

The output is a **root index** plus **per-module files**. The root index is thin; the detail lives in the module files.

### Root index: `module-partition.md`

Lists every module with its scope, file reference, and chunk range. No verbatim content.

```markdown
# Module Partitioning â€” {{project_name}}

Source: {{source directory or scan map reference}}
Modules: {{N}}  Unallocated: {{count}}  Rejected: {{count}}

---

## Module: [{{ModuleName}}]
File: modules/{{module-name}}.md
Chunks: {{range}} ({{count}} files)
Scope: {{one or two source-grounded sentences}}.

## Module: [{{AnotherModule}}]
File: modules/{{another-module}}.md
Chunks: {{range}} ({{count}} files)
Scope: {{one or two source-grounded sentences}}.

---

## [Unallocated]
File: modules/unallocated.md
{{or: "No unallocated source files."}}

## [Rejected]
File: modules/rejected.md
Chunks: {{range}} ({{count}} files)
```

### Per-module file: `modules/{{module-name}}.md`

Each module file has scope, core terms, and source file references â€” no verbatim content.

```markdown
## Module: [{{ModuleName}}]

Scope: {{one or two source-grounded sentences}}.

**Core terms**:
- {{noun phrase the source uses}}
- {{noun phrase the source uses}}
- â€¦

---

**Ref â€” {{short title}}**
Source: {{relative/path/to/source/file.md}}
Locator: {{lines, chapter, page â€” precise}}
Extract: whole

**Ref â€” {{short title}}**
Source: {{relative/path/to/source/file.md}}
Locator: {{lines, chapter, page}}
Extract: partial
Part: {{which slice}}
Also relates to: [{{OtherModule}}] â€” {{why}}
```

### Rejected/Unallocated files

Same format as module files but with `Reason:` lines on each reference.

Modules are listed in the order they earn their boundary in the source (or in scan-map order). `[Unallocated]` and `[Rejected]` are always last, in that order.

---

## Example

A small worked example showing the root index and a per-module file with references. **Drawn from a payments / banking domain â€” illustrative, not the corpus you are partitioning.** Adapt to your own corpus.

### Root index (`module-partition.md`)

```markdown
# Module Partitioning â€” Payments Platform

Source: context/rulebook/
Modules: 2  Unallocated: 0  Rejected: 1

---

## Module: [Funds Transfer]
File: modules/funds-transfer.md
Chunks: section_03â€“section_05 (3 files)
Scope: how an instruction to move funds is validated, executed, and reconciled.

## Module: [Customer]
File: modules/customer.md
Chunks: section_01â€“section_02 (2 files)
Scope: customer identity, KYC tiers, onboarding.

---

## [Rejected]
File: modules/rejected.md
Chunks: section_00 (1 file)
```

### Per-module file (`modules/funds-transfer.md`)

```markdown
## Module: [Funds Transfer]

Scope: how an instruction to move funds from one account to another is validated, executed, and reconciled. Covers the underlying transfer mechanism shared by every named transfer product (Wire, ACH, Internal Book Transfer).

**Core terms**:
- funds transfer
- source account / destination account
- debit / credit
- reconciliation
- Wire Transfer
- ACH Transfer
- Internal Book Transfer

---

**Ref â€” Funds Transfer (overview)**
Source: context/rulebook/PaymentsRulebook__section_03.md
Locator: Ch.3 Â§Funds Transfer
Extract: whole

**Ref â€” Wire Transfer limits**
Source: context/rulebook/PaymentsRulebook__section_05_02.md
Locator: Ch.5 Â§Wire Transfer â€” bullet list of limits
Extract: partial
Part: the three-bullet list under "The following limits apply to outbound wire transfers:"
Also relates to: [Customer] â€” the per-customer caps reference the customer's KYC tier set during onboarding.
```

### Rejected file (`modules/rejected.md`)

```markdown
## [Rejected]

**Ref â€” Cover / Disclosures / ToC**
Source: context/rulebook/PaymentsRulebook__section_00.md
Locator: Front matter
Extract: whole
Reason: Front matter â€” regulatory disclosures and table of contents; no domain rules; out of scope.
```

---

## Build

**Goal:** Author `module-partition.md` (root index) and `modules/*.md` (per-module files) from `domain-scan-results.md` and the source files.

1. **Verify source files exist.** List the source directory (corpus chunks, context files, or scan results). If it is empty or missing, **stop and tell the user** â€” do not proceed with agent-generated content as a substitute.
2. **Draft the module list first** â€” from the scan map's high-signal rows, propose 4â€“10 top-level module names (no nesting yet). Names must be source-grounded.
3. **Walk the corpus once, in source order**, and assign each meaningful source file to exactly one module, `Unallocated`, or `Rejected`. Record the file path and locator â€” do not copy file content.
4. **Write per-module files** under `abd-domain-driven-design/modules/`. Each file contains scope, core terms, and source file references. One file per module, plus `rejected.md` and optionally `unallocated.md`.
5. **Write the root index** at `abd-domain-driven-design/module-partition.md` listing all modules with scope, chunk ranges, and links to per-module files.
6. **Apply the kind-test before declaring the partition done.** For each module, name its kind in one word (Resolution, Measure, Actor, Temporal structure, State vocabulary, Resource economy, Behavior catalog, Constraint systemâ€¦). If a module's Core terms list visibly clusters into more than one kind, **split it**. Symptoms: the module name keeps wanting to be a compound or generic glue word; the Core terms list reads as two coherent vocabularies stuck together; you cannot describe what changes inside the module without referencing a different kind. If you find yourself naming a module after the source's TOC heading rather than the kind, suspect kind-mixing.
7. **Apply the standalone-mechanic test for procedural domains.** For each pair of named mechanics inside a candidate module, ask: *can mechanic A run completely without mechanic B?* If yes for several internal pairs, the module is a bag of co-located mechanisms â€” split. Conversely, if mechanic A's text constantly invokes mechanic B's vocabulary, they are one mechanism in different applications and belong together. Use this on top of the kind-test: kind-test catches *kind* mixing; standalone-mechanic test catches *mechanism* mixing within the same kind.
8. **Re-read your `Unallocated` pile** after the first pass. Most entries either find a home (move them) or reveal a missing module (promote a new top-level section). A small residual Unallocated set is healthy and expected.
9. **Re-read your `Rejected` pile** to confirm each rejection is *intentional* and audit-grade â€” not an accidental drop.
10. **Consider nesting only at the end.** For each top-level module, ask: does this module contain two or more *bounded* sub-scopes that the source itself separates? If yes, introduce `### [SubModule]` headings and re-allocate the relevant references. If not, leave flat.
11. **Persistence:** engagement root from parent agent `workspace`; files live at `abd-domain-driven-design/module-partition.md` and `abd-domain-driven-design/modules/*.md`.

**While writing:**

- One reference = one allocation. Split into partial references if a single source file straddles modules.
- References only â€” no verbatim content. Headers and labels are yours; the source files are the content.
- `Also relates to:` flags do not move the reference â€” they only annotate it.
- **Parallel-agent friendly:** each module file is independent, so separate agents can work on separate modules concurrently.

---

## Validate

**Goal:** Read the partition as a boundary reviewer â€” coverage and traceability, not a second scan.

### Coverage

- Every module file has at least one source reference. **Empty modules are deleted** or moved to a follow-up note.
- `rejected.md` exists; `unallocated.md` exists if any files are unallocated. If either is empty, a one-line note states *why* (e.g. "no front matter in this corpus", "every section landed cleanly on first pass").
- The scan map's **High** and **Medium** signal rows in `domain-scan-results.md` each show up in **at least one** reference somewhere â€” module, unallocated, or rejected. Low-signal rows are typically rejected; that is fine, but they should appear.

### Allocation discipline

- No source file appears in two modules (unless split with `Extract: partial` + different `Part:` slices).
- Every `Extract: partial` line is paired with a `Part:` line that names the slice in source-grounded terms â€” not "the relevant bit" or "the important paragraph".
- Every reference in `unallocated.md` and `rejected.md` has a `Reason:` line.
- Reference discipline: pick three random references, verify the source file exists on disk and the locator is correct. If any reference points to a non-existent file or uses a generated-content marker (e.g. `Source: domain-knowledge`), **remove it** â€” only real files on disk are valid references.

### Boundary discipline

- Module names are source-grounded. No generic placeholders ("Misc", "Core", "Foundation") â€” replace or merge them.
- Nesting (`###` and deeper) is justified by the source. For each nested heading, the parent module's body is **not** what the sub-module covers â€” the sub-module has its own bounded extract set. If you cannot say what the sub-module covers in one source-grounded sentence, collapse the nesting.
- `Also relates to:` flags are present where the boundary is genuinely contested. Spot-check a few to make sure the flagged tension is real.

### Core terms list (per module)

- Every module section has a **Core terms** bullet list directly under the heading and scope statement, before the extracts.
- Terms are **source-grounded noun phrases** the source itself uses inside the module's extracts â€” not invented, not normalized, not classified.
- The list contains **no** Targets, Values, evidence IDs, stereotypes, or Notes labels â€” those belong to `**term-registry**`. If you find yourself writing `<<Anchor>>` or `EVD-NNN` here, stop and move that to the term registry pass.
- Sanity-check the list against the **independence test**: does it read as one bounded vocabulary? Does it lean heavily on terms defined elsewhere? Is it trivially short, or unevenly enormous? Any "yes" is a flag to revisit the boundary, not to enrich the list.

### Kind-test (per module)

- For each module, write the module's **kind** in one word: *Resolution, Measure, Actor, Temporal structure, State vocabulary, Resource economy, Behavior catalog, Constraint system,* etc. If you cannot pick one, the module is mixed.
- Read the module's **Core terms** with that kind in mind. Every term should belong to that kind; if a sub-cluster of terms belongs to a different kind, split that cluster into its own module.
- Check the module's **name** against the kind. Generic glue or compound names (`[Operations]`, `[Foundations]`, `[Basics]`, `[Core]`, `[Authorization & Capture]`) are red flags â€” they usually indicate the module is two kinds glued together.
- Cross-check against the corpus's source-organization (TOC headings, all-caps section breaks, named clusters): if a single source heading produced more than one of your modules, that is **good** â€” it confirms the source heading was editorial shelving and the kind-test caught a real boundary the source did not draw.

### Standalone-mechanic test (per pair of mechanics inside a module)

- For each pair of named mechanics inside a candidate module, ask: *can mechanic A run completely without mechanic B?* If yes for several internal pairs, the module is a bag of co-located mechanisms rather than one mechanic â€” split.
- The reverse also holds: if a candidate split would force the reader to bounce between modules to understand a single mechanic's full text (e.g. you cannot describe Wire Transfer without describing Funds Transfer, or 3-D Secure Step-Up without describing Authorization), the split is wrong â€” collapse them.
- For tightly cross-referenced same-kind mechanics (e.g. two payment-reversal mechanics â€” Refund and Chargeback â€” that gate or pre-empt each other), prefer to **merge** rather than split: dense cross-references inside one kind are a signal that the two mechanics are one bounded scope from the modeler's point of view.

### Hand-off readiness

A reviewer (or downstream agent) running `**term-registry**` next should be able to:

- Read a single module file, get the list of source files for that scope, and read those files to seed terms â€” the module file is the authoritative index for that bounded scope.
- Trust that source files **not referenced** in any module file are intentionally outside (in `rejected.md`) or pending (in `unallocated.md`) â€” not silently dropped.

If the partition is thin, vague, or leaks across boundaries, **improve in place** with targeted re-reads â€” not a wholesale rescan unless the source or the project goals changed.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Full source coverage — every source file must appear in the partition

**Scanner:** `scanners/full-source-coverage-scanner.py` — **`FullSourceCoverageScanner`**

Every file in the workspace's source directories must be referenced by at least one `Source:` line across all module files (`abd-domain-driven-design/modules/*.md`) — allocated to a module, placed in `unallocated.md`, or explicitly placed in `rejected.md`. No source file may be silently dropped.

#### DO

- Walk every file in the source directories (context/, corpus/, source/, data/) and confirm it appears in at least one `Source:` line across the module files.
- Place files that don't fit any module into `unallocated.md` with a `Reason:` line explaining the ambiguity.
- Place out-of-scope files into `rejected.md` with a `Reason:` line explaining why they are excluded.
- After the first pass, re-read the source directory listing and confirm full coverage.

#### DON'T

- Silently skip source files because they "don't seem important" — every file gets an explicit allocation decision.
- Leave source files unreferenced on the assumption they'll be handled in a later pass — the partition is the single authoritative record of what's in, what's out, and what's pending.
- Assume a source file is covered because a nearby file from the same directory was included — each file must appear individually.

### Rule: Source references only — no generated, reconstructed, or summarized content

**Scanner:** `scanners/verbatim-source-only-scanner.py` — **`VerbatimSourceOnlyScanner`**

Every `Source:` line in module files must reference a file that exists on disk. The agent must never substitute its own domain knowledge, training data, or memory-based descriptions for actual source file references.

#### DO

- Reference source files that exist on disk (corpus chunks, scanned documents, user-supplied context files).
- Use the exact relative file path in every `Source:` line so a reviewer can open the file and verify it exists.
- **Stop and tell the user** when the source directory is empty or source files do not exist — the skill cannot run without readable source files.

#### DON'T

- Use telltale source markers like `Source: domain-knowledge`, `Source: application-requirements`, `Source: user requirements`, or any other non-file reference in `Source:` lines.
- Reference files that do not exist on disk.
- Proceed with partitioning when no source files exist on disk — the correct action is to halt and inform the user.

#### Examples

**Wrong — agent-generated reference:**

```
**Ref — Abilities overview**
Source: domain-knowledge — "Abilities"
Locator: MM3E Hero's Handbook, Ch. 1 Abilities
Extract: whole
```

The `Source: domain-knowledge` marker proves this was generated by the agent, not referencing a file.

**Right — reference to a file on disk:**

```
**Ref — Abilities overview**
Source: context/rules/ch01-abilities.md
Locator: lines 1–14
Extract: whole
```

The reviewer can open `context/rules/ch01-abilities.md` and confirm it exists.
<!-- execute_rules:bundle_rules:end -->
