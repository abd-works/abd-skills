---
name: module-partitioning
description: >-
  After domain scan, partition the source corpus into modules by allocating
  verbatim source context to module sections. No classes, no anchors — only
  module boundaries and the source text that belongs to each. Supports an
  Unallocated bucket for pending decisions and a Rejected bucket for
  out-of-scope context. Modules are flat by default and nested only when the
  source itself supports a sub-module. Use when the user asks to "partition
  the source", "allocate context to modules", "draw module boundaries", or
  needs a defensible scope cut before any class-level modeling.
---

# module-partitioning

## Purpose

Produce **`module-partitioning.md`** — a hierarchy of **module sections** whose bodies are **verbatim source extracts** allocated to each module. No classes, no anchors, no UML, no stereotypes. Just boundaries and the text that lives inside them.

This is the *scope cut* before any class identification. It answers a single question for every chunk of source: **which module does this text belong to** — or is it **unallocated** (pending) or **rejected** (out of scope)?

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
| `templates/module-partitioning-template.md` | `module-partitioning.md` under `<active_skill_workspace>/abd-ooad/`: module sections (`##` top-level, `###`+ only when the source supports a real sub-module), each containing **verbatim** source extracts under labelled extract headers. Reserved sections **`## [Unallocated]`** and **`## [Rejected]`** are mandatory and may be empty (with a one-line note explaining why). |

2. **Rules**

- Follow the **Allocation rules** and **Extract format** sections below for what counts as a module, when to nest, when to copy whole vs partial, and how to label.
- Source text inside extracts is **never** paraphrased, summarized, edited, or reformatted. Copy bytes; quote characters as-is. The only allowed editorial mark is an ellipsis `[…]` for an explicit gap inside a partial extract — and that gap must be labelled.
- After drafting, act as a *peer reviewer*: every extract has a locator, a whole-or-partial label, and lives under exactly one module section (or `Unallocated` / `Rejected`); no module exists without source extracts; no nesting exists without source-supported justification.

3. **Who is checking**

A **boundary reviewer** — someone who needs to defend the scope cut to the team. They read the file front-to-back and ask: *can I trust that every paragraph in the source ended up exactly one place, and that the place is justified by the source itself?*

---

## What is module partitioning?

A **module** is a named region of the domain — a slice of the source the modeler intends to treat as one bounded scope in later passes. At this fidelity, a module is **only** a name + a body of source extracts; it carries **no classes, no anchors, no behavior**.

A **partition** is the assignment of every meaningful chunk of source to exactly one of:

1. A **named module** (top-level or — only when the source supports it — a sub-module of one),
2. **`Unallocated`** — text that clearly matters but whose home is undecided,
3. **`Rejected`** — text that is intentionally **out of scope** (front matter, marketing prose, settings/adventures, license, etc.).

**Partitioning is a commitment.** Each piece of source has one home. If you find yourself wanting to put the same passage in two modules, that is a **tension** — record it under the module you chose and note the alternative, or move it to `Unallocated` until a later pass resolves it.

**Prerequisites:** `domain-scan-results.md` from `**domain-scan`**, plus access to the source memory chunks. Do **not** rescan the corpus; work from the scan map and **targeted** re-reads.

---

## What is — and is not — a module (DDD-grounded)

> "MODULES are a communications mechanism. The meaning of the objects being partitioned needs to drive the choice of MODULES. When you place some classes together in a MODULE, you are telling the next developer who looks at your design to **think about them together**." — Eric Evans, *Domain-Driven Design*, Ch. 5
>
> "**High cohesion** of objects with related responsibilities allows modeling and design work to concentrate within a single MODULE — a scale of complexity a human mind can easily handle." — Evans

A module in this skill is the same **MODULE** Evans describes in DDD: a named, **high-cohesion / low-coupling** region of the domain. It is **not** a heading, a feature, a single concept, or a section title in the source.

### The independence test (the only test that matters)

For any candidate boundary, ask:

> **Can a reader, modeler, or downstream pass reason about *this* slice with meaningful independence from the *other* slices — without needing to constantly cross-reference them?**

- If two clusters of source **must** be reasoned about together (one constantly references rules, terms, or invariants of the other), they belong in **one** module. Forcing a boundary between them creates a coupling magnet you'll have to untangle later.
- If a cluster can be **discussed, modified, taught, or modeled** with only an arm's-length reference to its neighbours, it earns its own boundary.

A useful sanity check: if you can describe what changes inside Module A without saying anything substantive about Module B, the boundary is real. If your first sentence about A is a definition that references B, they're one module.

#### Standalone-mechanic test (sharper form for procedural domains)

For each *pair of mechanics* inside a candidate module, ask:

> **Can mechanic A run completely without mechanic B?**

- If yes — if you could write down mechanic A in full and a reader could use it without ever knowing mechanic B exists — then A and B do **not** belong in the same module. They may *reference* each other in play, but each is its own bounded mechanism and earns its own scope.
- If no — if you cannot describe mechanic A without invoking the rules or vocabulary of mechanic B (e.g. "a wire transfer is a funds transfer with same-day settlement and a regulatory message" — you cannot say "wire transfer" without "funds transfer") — they are the **same** mechanism in different applications, and they belong together.

This is the sharper form of the independence test for **procedural / rules-style** domains, where the unit of analysis is a *mechanic* rather than a concept. Use it in addition to (not in place of) the kind-test:

- The **kind-test** catches modules that mix unrelated *kinds* (resolution + state vocabulary + meta-currency stuffed into one bag).
- The **standalone-mechanic test** catches modules that mix unrelated *mechanisms within the same kind* — for example, two distinct resource-economies under one resource-economy umbrella, or two unrelated state vocabularies forced under one state-module heading.

Two short illustrations from a payments / banking domain:

- *Wire Transfer* and *ACH Transfer* are both forms of *Funds Transfer*. You cannot describe either without invoking the underlying transfer mechanism (debit a source account, credit a destination account, reconcile). **Same mechanism, different applications → same module** (a `[Funds Transfer]` module).
- *Refund* (merchant-initiated reversal of a captured payment) and *Chargeback* (customer-initiated dispute that reverses a captured payment) reference each other in their rules — an issued refund pre-empts a chargeback; a successful chargeback often blocks a follow-up refund — but each runs on its own with its own triggers, actors, and SLA. The user can defensibly keep them together (because they are the *same kind* — payment-reversal mechanics — and the cross-references are dense) or split them (because each is a self-contained mechanism). The test surfaces the choice rather than dictating it. The deciding factor is usually whether splitting forces the reader to bounce between modules to follow a single mechanic; if so, merge.

### Cohesion and coupling, in practice

- **Cohesion (inside the boundary):** Every extract in the module shares a single overarching subject. The terms, rules, and invariants reinforce each other; removing any one would leave the module noticeably less complete.
- **Coupling (across the boundary):** Modules will reference each other — that's fine and expected — but the references are *named pointers*, not a shared web of intermingled rules. If Module A's text only makes sense when Module B's text is at hand, they are coupled, not bounded.

### Modules are not the source's headings

This is the most common mistake. A book's chapter, section, or subsection structure is **organizational scaffolding for readers**, not a domain partition. In particular:

- A single source heading often belongs *inside* a module — it is a **content-level heading inside one bounded scope**, not a module of its own.
- A single module often spans **multiple** source headings, sometimes across multiple chapters.
- "I see a `####` in the source" is **not** a reason to create a module. Promote a heading to a module only if it survives the independence test.

### Watch for *kind-mixing* — when one source heading hides multiple modules

When a source's organizational heading (a TOC chapter, an all-caps section break, a named cluster like `OPERATIONS`, `RULES`, or `WORKFLOW`) shelves content of **multiple kinds** under one umbrella, the heading is **editorial shelving**, not a domain partition. Forcing the heading to become a module creates a coupling magnet that fails the independence test on inspection.

After drafting modules, ask of each one: ***what kind of thing is this module about?*** If the answer is "more than one kind", split.

Common kinds in rules-style and procedural domains (rough catalog, not exhaustive — examples are deliberately **not** drawn from the corpus you are partitioning):

- **Resolution** — how outcomes of uncertain operations are determined (validation rules, eligibility checks, authorization steps).
- **Scaling / Measure** — how trait or quantity values translate to real-world values (rate cards, conversion tables, unit-of-measure mappings).
- **Actor** — entities that take action (customers, merchants, accounts, claims, agents).
- **Temporal structure** — billing cycle, turn, phase, sequence; the time grid of the process.
- **State vocabulary** — statuses, modes, lifecycle stages an entity can be in (Pending, Authorized, Captured, Refunded, Disputed, Settled).
- **Resource economies / meta-currency** — internal currencies that gate behavior (account balance, credit limit, loyalty points, refund credits).
- **Behavior catalogs** — explicit lists of capabilities, products, or features (product catalog, fee schedule, promotion list).
- **Constraint systems** — limits, thresholds, regulatory rules (KYC tier, transaction caps, eligibility constraints).

A module that draws extracts from more than one of these kinds is almost always two-modules-disguised-as-one, even when a single source heading puts them together. Two warning signs:

1. The **Core terms** list visibly clusters into separate vocabularies (one cluster of process verbs, one cluster of unrelated state nouns, one cluster of currency terms).
2. The module name keeps wanting to be a compound or generic noun (`[Operations]`, `[Foundations]`, `[Basics]`, `[Core]`) because no single kind fits.

When you see those signs, split until each module has **one kind**.

### Modules are not (necessarily) single concepts — but they ARE single-kind

A module is a **collection** of related domain content of a single kind. Two clarifications follow:

- A small, *single-kind* bounded scope **is** a legitimate module, even if its vocabulary is short. In a payments domain, `[Loyalty Points]` (an internal currency with a small set of earn-and-spend rules) is a legitimate module — it is one kind (resource economy) with its own bounded vocabulary. `[Order Status]` (a state vocabulary of named statuses with transition rules) is a legitimate module of a different kind (state vocabulary). They are not "single concepts" — each is a small bounded scope.
- A single *concept* — one rule, one term, one feature — that does not carry its own vocabulary or invariants is an **anchor or class inside another module**, not a module itself. A single status name like `Authorized` would be an anchor inside `[Order Status]`; it does not earn its own scope.

The distinction is **kind + bounded vocabulary**, not size. Some legitimate modules are large; some are small; the test is the same.

If you have produced more than ~10 top-level modules from a corpus, or every section in the TOC has become a module, you have **over-partitioned**. Collapse aggressively to bounded scopes that pass the independence test, then revisit.

### Heuristics for naming a real module

A module name should answer **"what bounded scope is this?"** in one short, source-grounded noun phrase that names the **kind**.

**Single-noun rule.** If you can pick a single noun (or tight noun phrase) the source itself uses for the kind, that is the right name. If you keep reaching for compounds or generic glue (`[Operations]`, `[Authorization & Capture]`, `[Foundations]`, `[Core]`, `[Basics]`), you are almost certainly trying to name a multi-kind bag — split until each module accepts a single-noun name.

(Examples below are drawn from a payments / banking domain — illustrative, not the corpus you are partitioning.)

| Name | Verdict | Reason |
|------|---------|--------|
| `[Funds Transfer]`, `[Authorization]`, `[Settlement]`, `[Order Status]`, `[Loyalty Points]`, `[Billing Cycle]`, `[Catalog]`, `[Customer]` | ✅ | Single kind, source-grounded, short noun. |
| `[Operations]`, `[Foundations]`, `[Basics]`, `[Core]`, `[Mechanics]`, `[Workflow]` | ⚠️ | Generic / multi-kind. Often a TOC heading rather than a kind. Split or rename. |
| `[Refund & Chargeback]`, `[Authorization & Capture]` | ⚠️ | Compound names usually signal two kinds (or two mechanisms) glued together. Split unless the conjunction is genuinely indivisible. |
| `[Chapter 1]`, `[Section 3.2]`, `[Part II]` | ❌ | Source-structure naming, not domain naming. |
| `[Misc]`, `[Other]`, `[Foundation]` (without source grounding) | ❌ | Generic placeholders that hide ambiguity. |

### Module decisions coevolve with the model

Module boundaries are **not** final on first pass — but they are deliberately costlier to change than later artifacts. Evans:

> "Refactoring MODULES is more work and more disruptive than refactoring classes, and probably can't be as frequent. […] Letting the MODULES reflect changing understanding of the domain will also allow more freedom for the objects within them to evolve."

Choose conservative, well-justified boundaries now; expect them to refine as `term-registry`, `nouns-verbs-rules-and-states`, and `domain-model-skeleton` reveal deeper structure.

---

## Core concepts

### Workspace

Output: `<active_skill_workspace>/abd-ooad/module-partitioning.md` (engagement root from the parent agent's `**workspace`** skill).

### Modules — flat by default, hierarchical only when the source earns it

- **Default shape is flat.** Most corpora produce **4–10 top-level modules for the entire corpus** (not per chapter, not per section). A single chapter often produces zero, one, or two modules — never one per heading. If you find yourself producing more than ~10 modules total, re-apply the **independence test** above and collapse aggressively.
- **Nest only when the source itself supports a real sub-module** — a self-contained slice that has its own bounded behavior, terminology, and extract set, *and* whose existence is independently visible in the source (a dedicated chapter, a named subsystem, a clearly separated rule cluster).
- **Do not nest just to organize.** A nested heading without its own non-trivial extract set is wrong — collapse it back into the parent or promote it to a top-level module.
- **Do not nest by section/paragraph proximity.** Source structure (chapter → section → subsection) is **not** the same as module structure. A single chapter often produces multiple top-level modules; a module often draws extracts from many chapters.
- **Stay at module level.** Even when nested, every level is still a module — no sub-module decomposes into classes, properties, or operations here.

If you cannot point at the source and say "this sub-module has its own extracts and its own boundary", do not nest.

### Section titles

- Each module is introduced by `## Module: [Name]` at top level. Sub-modules use `### [Name]` (the `Module:` prefix is implicit at deeper levels because they sit under a `## Module: …` parent). The `Module:` prefix on top-level headings makes it unambiguous to a reviewer that the heading is a partition module — not a content-level heading copied or paraphrased from the source.
- Brackets around the name; **no** ` module` suffix in the heading (`## Module: [Combat]`, not `## Module: [Combat module]`).
- Reserved names — used **exactly** once each: `## Module: [Unallocated]`, `## Module: [Rejected]`. They are top-level only and never nested under another module.
- Names are short, source-grounded, and stable. Prefer the noun the source itself uses; fall back to a one-word descriptive name only if no source noun fits.

### Allocation rules

For every chunk of source you decide to bring into the file:

1. **Pick the module** whose scope best matches the chunk's *primary* subject. If two modules match equally, the chunk is a tension — pick one and note the alternative in the extract header, or move to `Unallocated`.
2. **Decide whole vs partial.** Whole extracts copy the chunk top-to-bottom. Partial extracts copy a contiguous slice; non-contiguous selection is two extracts, not one.
3. **Copy verbatim.** No paraphrase, no rewording, no reformatting beyond preserving the source's own line breaks and bullets. Do not "clean up" OCR artifacts, page numbers, or running headers — those are part of the locator's audit trail.
4. **Label.** Every extract gets a header block (see **Extract format**) with locator, whole/partial, and — if partial — a clause naming exactly which part was taken.
5. **Stop when the chunk has a home.** Do not also add a paraphrase or summary alongside the verbatim block. The verbatim text is the artifact.

### When to use Unallocated

A chunk goes to `## [Unallocated]` when **all** of these are true:

- It clearly matters for the domain model (it carries terms, rules, or invariants you do not want to lose).
- You cannot defensibly assign it to exactly one existing module.
- Creating a new module *just* for it would be premature (you have not seen enough related material yet).

Each `Unallocated` extract carries a `Reason:` line in its header explaining the ambiguity (e.g. *spans Authorization and Settlement*, *might warrant its own module after a later pass over the corpus*).

### When to use Rejected

A chunk goes to `## [Rejected]` when it is **intentionally out of scope** for the domain model. Typical rejections:

- Front matter — cover, credits, table of contents, license, index.
- Setting / lore / flavor prose — proper nouns, history, geography, character bios — when the model is for *rules*, not *content*.
- Worked examples and adventure scripts that illustrate but do not define rules.
- Marketing copy, designer notes, "under the hood" sidebars when they do not change behavior.

Each `Rejected` extract carries a `Reason:` line stating *why* it is out of scope. **Never delete a rejection silently** — the rejection record is the audit trail.

### Core terms — a lightweight read-out of what each module *contains*

Module partitioning is a scope cut, **not** a term registry. The full term-capture loop (Targets, Values, Evidence files, Notes labels, anchor stereotypes) belongs to `**term-registry**` — **do not** do that work here.

But each module section does carry a short, source-grounded **Core terms** list directly under the module heading and scope statement, *before* the verbatim extracts. The point is purely diagnostic: at a glance, a reviewer (and you) can see whether the module is the bounded scope you claim it is, or whether the terms inside it actually pull in two directions and the module needs to split.

**What goes in the list**

- **Source-grounded noun phrases** the source itself uses inside the module's extracts (e.g. *funds transfer*, *billing cycle*, *authorization hold*, *settled status*).
- Listed **flat**, in source order (or grouped lightly by sub-area when the list is long).
- Use the source's casing and exact phrase. No renaming, no normalization. That is `**refine-names**`'s job.

**What does NOT go in the list**

- No targets, values, or stereotypes (`<<Anchor>>`, `Module.Class`, etc.) — that is `**term-registry**`.
- No `EVD-NNN` evidence IDs, no evidence files. The verbatim extracts in the same module section *are* the evidence at this fidelity.
- No `Notes:` labels (`High Confidence Anchor`, `Sibling Candidate`, `Tension`, etc.) — that is `**term-registry**`.
- No tables. A simple bullet list.
- No invented terms, no synonyms the source does not use.

**How to use the list to test the boundary (back to the independence test)**

Once each module has its Core terms list, ask:

1. **Does the list read as one bounded vocabulary?** If the terms feel like *two* coherent vocabularies stuck together (e.g. one cluster of process verbs + one cluster of unrelated geometry nouns), the module probably needs to split.
2. **Does the list lean heavily on terms defined in another module?** If most entries are forward references to another module's anchors, your scope cut is probably misplaced — the content belongs in that other module, or this module is really a sub-scope of it.
3. **Is the list trivially short (one or two terms)?** Then the "module" is almost certainly a single concept and should fold into a larger one.
4. **Is the list overwhelming and uneven (50+ terms with no center of gravity)?** Then the module is probably too coarse and may genuinely contain two bounded scopes the source treats together.

The Core terms list is the cheapest possible way to make the cohesion-and-coupling argument visible *inside the partition file itself*, without crossing into term-registry territory.

### Tensions inside an allocation

If an extract is allocated to a module but also has meaningful pull toward another, add an `Also relates to:` line in its header. This is **not** a second allocation — the extract still lives in exactly one section. It is a flag for downstream skills (especially `term-registry`) that the boundary is contested.

### What you do not do here

- Do **not** identify classes, anchors, properties, operations, or responsibilities.
- Do **not** rename source terms or normalize vocabulary — that is `**refine-names**`.
- Do **not** invent modules for concepts the source does not name as a coherent scope.
- Do **not** add `note:` lines, `[dms]` tags, or any UML notation. The artifact is a partitioned reading list, not a model.

---

## Extract format

Every verbatim extract sits inside a **module section** under an **extract header** so a reviewer can verify allocation without re-opening the source.

### Extract header (required for every extract)

```
**Extract — {{short title}}**
Source: {{chunk_id_or_file}} — "{{section_path}}"
Locator: {{chapter / page / lines / code range — whatever is precise for this source type}}
Extract: {{whole | partial}}
{{Part: {{which slice of the source was copied — required when Extract: partial}}}}
{{Also relates to: {{other module name}} — {{one-line why}}}}
{{Reason: {{why this lives in Unallocated or Rejected — required in those sections}}}}
```

- The `Extract:` line is `whole` when the chunk is copied top-to-bottom, `partial` otherwise.
- When `Extract: partial`, the `Part:` line is **mandatory** and names the slice in source-grounded terms (e.g. *paragraphs 1–2 of "Refund Eligibility" subsection*, *the bullet list under "The following limits apply to authorization holds"*, *the formula line plus its caption*, *lines 14–22 of the chunk*).
- `Also relates to:` is optional, used to flag tensions on an otherwise clean allocation.
- `Reason:` is required in `## [Unallocated]` and `## [Rejected]` sections; omit elsewhere.

### Extract body (required)

Place the verbatim text inside a **fenced block** so reviewers can see exactly what was copied (whitespace, bullets, OCR artifacts, page numbers — all preserved):

```
```source
{{copied verbatim from the source — no edits, no paraphrase}}
```
```

If the partial extract has an internal gap, mark the gap with `[…]` on its own line **inside** the fenced block, and describe the gap in the `Part:` header line:

```
```source
First half of the passage, copied verbatim.
[…]
Second half of the passage, copied verbatim.
```
```

### One extract = one allocation

If a single source chunk has two unrelated parts that belong in two different modules, that is **two extracts**, each with its own header and `Extract: partial` + `Part:` line — one in each module. Never split across modules without splitting the extract.

---

## The shape of a good `module-partitioning.md`

**Front matter is thin by contract.** It carries only the source pointer and the module/Unallocated/Rejected counts. **Do not** put per-module descriptions, scope statements, term lists, "module list" prose, or rationale in the front matter. Every piece of information about a particular module lives **inside that module's section**, under its own heading. If you find yourself describing what a specific module covers in the front matter, stop and move that prose under the module's heading instead.

Each module section follows the same shape, in this order:

1. `## Module: [{{Name}}]` — the heading.
2. `Scope: …` — one or two source-grounded sentences naming the bounded scope (and, if useful, what it does **not** cover).
3. `**Core terms**` — bullet list of source-grounded noun phrases that appear inside this module's extracts.
4. `**Extract — …**` blocks — verbatim source.

```markdown
# Module Partitioning — {{project_name}}

Source: {{corpus or scan map reference}}
Top-level modules: {{N}}     Unallocated: {{count}}     Rejected: {{count}}

---

## Module: [{{ModuleName}}]

Scope: {{one or two source-grounded sentences — what bounded scope this module covers}}.

**Core terms** (source-grounded noun phrases that appear inside this module's extracts):

- {{noun phrase the source uses}}
- {{noun phrase the source uses}}
- {{noun phrase the source uses}}
- …

**Extract — {{short title}}**
Source: {{chunk}} — "{{section path}}"
Locator: {{precise locator}}
Extract: whole

```source
{{verbatim text}}
```

**Extract — {{short title}}**
Source: {{chunk}} — "{{section path}}"
Locator: {{precise locator}}
Extract: partial
Part: {{which slice}}
Also relates to: [{{OtherModule}}] — {{why}}

```source
{{verbatim slice}}
```

---

## Module: [{{NestedParent}}]

Scope: {{source-grounded one-liner for the parent}}.

**Core terms** (parent's own extracts):
- …

### [{{NestedChild}}]

Scope: {{source-grounded one-liner for the sub-module}}.

**Core terms** (sub-module's own extracts):
- …

**Extract — …**
…

---

## Module: [Unallocated]

**Core terms**: *n/a — Unallocated extracts are pending an allocation decision; their terms will be captured under whichever module receives them.*

**Extract — …**
…
Reason: {{why no module fits yet}}

---

## Module: [Rejected]

**Core terms**: *n/a — Rejected extracts are intentionally out of scope.*

**Extract — …**
…
Reason: {{why out of scope}}
```

Modules are listed in the order they earn their boundary in the source (or in scan-map order). `## Module: [Unallocated]` and `## Module: [Rejected]` are always last, in that order.

---

## Example

A small worked example showing a top-level module with one whole and one partial extract, plus an `Also relates to:` flag and a single rejected chunk. **Drawn from a payments / banking domain — illustrative, not the corpus you are partitioning.** Adapt to your own corpus.

```markdown
## Module: [Funds Transfer]

Scope: how an instruction to move funds from one account to another is validated, executed, and reconciled. Covers the underlying transfer mechanism shared by every named transfer product (Wire, ACH, Internal Book Transfer).

**Core terms** (source-grounded noun phrases that appear inside this module's extracts):

- funds transfer
- source account / destination account
- debit / credit
- reconciliation
- Wire Transfer
- ACH Transfer
- Internal Book Transfer

**Extract — Funds Transfer (overview)**
Source: PaymentsRulebook__section_03 — "Funds Transfer"
Locator: Ch.3 §Funds Transfer
Extract: whole

```source
A funds transfer moves a specified amount from a source account to a destination account in a single atomic operation. Every transfer:
- Debits the source account by the transfer amount.
- Credits the destination account by the transfer amount.
- Records a matched debit/credit pair on the ledger for reconciliation.
…
A transfer that cannot be matched within the reconciliation window is escalated to the exceptions desk.
```

**Extract — Wire Transfer limits**
Source: PaymentsRulebook__section_05_02 — "Wire Transfer Limits"
Locator: Ch.5 §Wire Transfer — bullet list of limits
Extract: partial
Part: the three-bullet list under "The following limits apply to outbound wire transfers:" (per-transaction cap, daily cap, beneficiary-jurisdiction cap); excludes the surrounding prose and the FX-rate reference table.
Also relates to: [Customer] — the per-customer caps reference the customer's KYC tier set during onboarding.

```source
- Per-transaction cap: A single outbound wire cannot exceed the customer's per-transaction limit for the assigned KYC tier. …
- Daily cap: The total outbound wire amount on a single business day cannot exceed twice the per-transaction cap. …
- Beneficiary-jurisdiction cap: Wires destined for jurisdictions on the enhanced-due-diligence list cannot exceed the EDD cap regardless of KYC tier.
```

---

## Module: [Rejected]

**Extract — Cover / Disclosures / ToC**
Source: PaymentsRulebook__section_00 — "Cover / Regulatory Disclosures / Table of Contents"
Locator: Front matter
Extract: whole
Reason: Front matter — regulatory disclosures and table of contents; no domain rules, no terms; out of scope for a rules-domain partition.

```source
…front-matter text copied verbatim…
```
```

---

## Build

**Goal:** Author `module-partitioning.md` from `domain-scan-results.md` and the source memory chunks.

1. **Draft the module list first** — from the scan map's high-signal rows, propose 4–10 top-level module names (no nesting yet). Names must be source-grounded.
2. **Walk the corpus once, in source order**, and place each meaningful chunk into exactly one section: a module, `Unallocated`, or `Rejected`. Copy verbatim; label whole vs partial.
3. **Fill in each module's Scope and Core terms** as you go — one or two source-grounded sentences for the bounded scope, plus a bullet list of the noun phrases the source itself uses inside the module's extracts.
4. **Apply the kind-test before declaring the partition done.** For each module, name its kind in one word (Resolution, Measure, Actor, Temporal structure, State vocabulary, Resource economy, Behavior catalog, Constraint system…). If a module's Core terms list visibly clusters into more than one kind, **split it**. Symptoms: the module name keeps wanting to be a compound or generic glue word; the Core terms list reads as two coherent vocabularies stuck together; you cannot describe what changes inside the module without referencing a different kind. If you find yourself naming a module after the source's TOC heading rather than the kind, suspect kind-mixing.
5. **Apply the standalone-mechanic test for procedural domains.** For each pair of named mechanics inside a candidate module, ask: *can mechanic A run completely without mechanic B?* If yes for several internal pairs, the module is a bag of co-located mechanisms — split. Conversely, if mechanic A's text constantly invokes mechanic B's vocabulary, they are one mechanism in different applications and belong together. Use this on top of the kind-test: kind-test catches *kind* mixing; standalone-mechanic test catches *mechanism* mixing within the same kind.
6. **Re-read your `Unallocated` pile** after the first pass. Most entries either find a home (move them) or reveal a missing module (promote a new top-level section). A small residual Unallocated set is healthy and expected.
7. **Re-read your `Rejected` pile** to confirm each rejection is *intentional* and audit-grade — not an accidental drop.
8. **Consider nesting only at the end.** For each top-level module, ask: does this module contain two or more *bounded* sub-scopes that the source itself separates? If yes, introduce `### [SubModule]` headings and re-allocate the relevant extracts. If not, leave flat.
9. **Persistence:** engagement root from parent agent `workspace`; file lives at `abd-ooad/module-partitioning.md`.

**While writing:**

- One extract = one allocation. Split the extract if a single chunk straddles modules.
- Verbatim only. Headers and labels are yours; bodies are the source's.
- `Also relates to:` flags do not move the extract — they only annotate it.

---

## Validate

**Goal:** Read the partition as a boundary reviewer — coverage and traceability, not a second scan.

### Coverage

- Every module section has at least one extract. **Empty modules are deleted** or moved to a follow-up note.
- `## [Unallocated]` and `## [Rejected]` exist; if either is empty, a one-line note states *why* (e.g. "no front matter in this corpus", "every section landed cleanly on first pass").
- The scan map's **High** and **Medium** signal rows in `domain-scan-results.md` each show up in **at least one** extract somewhere — module, unallocated, or rejected. Low-signal rows are typically rejected; that is fine, but they should appear.

### Allocation discipline

- No source passage appears in two modules. If two modules quote the same passage, one of them is wrong (or it should have been split into two extracts with different `Part:` slices).
- Every `Extract: partial` line is paired with a `Part:` line that names the slice in source-grounded terms — not "the relevant bit" or "the important paragraph".
- Every `## [Unallocated]` and `## [Rejected]` extract has a `Reason:` line.
- Verbatim discipline: pick three random extracts, open the source chunk, and confirm character-level identity. If any has been "lightly cleaned", restore the original text.

### Boundary discipline

- Module names are source-grounded. No generic placeholders ("Misc", "Core", "Foundation") — replace or merge them.
- Nesting (`###` and deeper) is justified by the source. For each nested heading, the parent module's body is **not** what the sub-module covers — the sub-module has its own bounded extract set. If you cannot say what the sub-module covers in one source-grounded sentence, collapse the nesting.
- `Also relates to:` flags are present where the boundary is genuinely contested. Spot-check a few to make sure the flagged tension is real.

### Core terms list (per module)

- Every module section has a **Core terms** bullet list directly under the heading and scope statement, before the extracts.
- Terms are **source-grounded noun phrases** the source itself uses inside the module's extracts — not invented, not normalized, not classified.
- The list contains **no** Targets, Values, evidence IDs, stereotypes, or Notes labels — those belong to `**term-registry**`. If you find yourself writing `<<Anchor>>` or `EVD-NNN` here, stop and move that to the term registry pass.
- Sanity-check the list against the **independence test**: does it read as one bounded vocabulary? Does it lean heavily on terms defined elsewhere? Is it trivially short, or unevenly enormous? Any "yes" is a flag to revisit the boundary, not to enrich the list.

### Kind-test (per module)

- For each module, write the module's **kind** in one word: *Resolution, Measure, Actor, Temporal structure, State vocabulary, Resource economy, Behavior catalog, Constraint system,* etc. If you cannot pick one, the module is mixed.
- Read the module's **Core terms** with that kind in mind. Every term should belong to that kind; if a sub-cluster of terms belongs to a different kind, split that cluster into its own module.
- Check the module's **name** against the kind. Generic glue or compound names (`[Operations]`, `[Foundations]`, `[Basics]`, `[Core]`, `[Authorization & Capture]`) are red flags — they usually indicate the module is two kinds glued together.
- Cross-check against the corpus's source-organization (TOC headings, all-caps section breaks, named clusters): if a single source heading produced more than one of your modules, that is **good** — it confirms the source heading was editorial shelving and the kind-test caught a real boundary the source did not draw.

### Standalone-mechanic test (per pair of mechanics inside a module)

- For each pair of named mechanics inside a candidate module, ask: *can mechanic A run completely without mechanic B?* If yes for several internal pairs, the module is a bag of co-located mechanisms rather than one mechanic — split.
- The reverse also holds: if a candidate split would force the reader to bounce between modules to understand a single mechanic's full text (e.g. you cannot describe Wire Transfer without describing Funds Transfer, or 3-D Secure Step-Up without describing Authorization), the split is wrong — collapse them.
- For tightly cross-referenced same-kind mechanics (e.g. two payment-reversal mechanics — Refund and Chargeback — that gate or pre-empt each other), prefer to **merge** rather than split: dense cross-references inside one kind are a signal that the two mechanics are one bounded scope from the modeler's point of view.

### Hand-off readiness

A reviewer running `**term-registry**` next should be able to:

- Read a single module section and have **all** the source they need to seed terms for that scope — no need to re-open the corpus for that module.
- Trust that text **outside** the file is intentionally outside (rejected) or pending (unallocated) — not silently dropped.

If the partition is thin, vague, or leaks across boundaries, **improve in place** with targeted re-reads — not a wholesale rescan unless the source or the project goals changed.

---

<!-- execute_rules:bundle_rules:begin -->
<!-- No rules/*.md for this skill yet. If rules are added, bundle with:
     python skills/execute_using_rules/scripts/bundle_rules_into_skill_md.py --skill-root <this-skill-dir>
-->
<!-- execute_rules:bundle_rules:end -->
