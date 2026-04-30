---
name: key-abstraction-identification
description: >-
  Identify the Key Abstractions of a domain — the named domain units the source
  text orbits, before any class-level decision — then settle the list in a final
  pass (merges, splits, promotions/demotions, tension closure). Each Key
  Abstraction carries a source-grounded name, intent, Core terms, Shape hint,
  verbatim extracts, and optional residual Tension only. Per module, a
  ### Resolutions block logs every structural change and every closed tension.
  Output: key-abstractions.md. module-partitioning.md is optional. No kinds,
  properties, operations, or cross-context relationships. Use when the user asks
  to identify and settle key abstractions before noun-verb or class-level work.
---
# key-abstraction-identification

## Purpose

This skill lives in folder **`key-abstraction-identification`** (Cursor skill name: `key-abstraction-identification`). It produces **`key-abstractions.md`** — a **settled** list of named **Key Abstractions** (the named domain units the source text orbits), with a **final pass** that closes or defers every tension. Each Key Abstraction has an intent, Core terms, a free-form Shape hint, **optional residual `Tension:` only** (omit when closed in **Resolutions**), and verbatim source extracts.

This is the rung *before* any class-level modeling. It answers: **what does this source talk about as if each one were a thing?** — without committing to classes, values, services, events, or anything else.

**Naming.** The term comes from Grady Booch's *Object-Oriented Analysis and Design*: the "key abstractions and mechanisms" that a team elevates to first-class status in the model and language. Evans reinforces the same move — "identify the most important concepts of the domain and elevate them in the model and the language". This skill is that elevation move **plus** consolidation of overlaps inside each module (see **Settle tensions** below).

### Two phases (one artifact)

1. **Identification** — Name clusters, attach Core terms and verbatim extracts, draft optional `Tension:` lines where merge/split/promotion/demotion is plausible.
2. **Settle (final pass, same engagement)** — Inside each module, apply **only** merges, splits, promotions, and demotions (see **Settle tensions** below). Add **`### Resolutions`** under each `## Module:` (and a single **`### Resolutions`** / **`### Deferred tensions`** at the top if the file is flat with no modules). Remove or rewrite `Tension:` lines that you close; list anything that cannot close on module-internal evidence under **`### Deferred tensions`**.

### Module partitioning (optional)

**If `module-partitioning.md` exists:** mirror it — one `## Module: [Name]` per partition module, in partition order, with `### Key Abstraction: Name` inside each. Sub-allocate verbatim extracts from the partition (split multi-subject extracts into partials; see Sub-allocation).

**If it does not:** read the corpus (or the chunks the user gave you). You may use **no** outer modules and go straight to `## Key Abstraction: Name` under the H1, *or* add a few `## Module:` headings if loose grouping makes the file easier to read — do not treat that choice as a formal gate or a reason to block work. Same split-first rule for multi-subject passages. `## [Unallocated]` stays rare: only for a slice you truly cannot place after cutting, not a junk drawer.

Do **not** invent a second, parallel "mode" vocabulary. One file, one pass: partition when you have it, light modules when you don't and it helps, flat abstractions when that is enough.

## When to use this skill

Load this skill when **any** of the following apply:

- The user asks to **identify key abstractions**, **find the concepts in this domain**, **name what this source talks about**, **extract the concepts**, or **refine the source into named units**.
- A `module-partitioning.md` exists and you want Key Abstractions aligned to that scope cut — or it does not exist and you still need named units from raw source.
- A downstream vocabulary or class pass needs a **settled** `key-abstractions.md` — named, source-grounded domain units, not a raw Core-terms bag.
- You need a **defensible list of "what the modeled things are"** that is auditable back to verbatim source, *before* any class-level commitment is made.

This skill **does not** define classes, stereotypes, kinds, properties, operations, responsibilities, cross-context relationships, or super/sub hierarchies. Those belong to later class-level skills (after this file’s settle pass is complete).

---

## Agent Instructions

1. **Templates**

Generate content using **every** template file in this skill's `templates/` folder. **Do not** emit only a partial shape unless the user **explicitly** asks for a single format.

| Template | What to produce |
| -------- | --------------- |
| `templates/key-abstraction-identification-template.md` | `key-abstractions.md` under `<active_skill_workspace>/abd-ooad/`. With a partition: `## Module: [Name]` per partition module (order preserved), `### Key Abstraction: Name` under each, verbatim extracts from the partition. Without a partition: `## Key Abstraction: Name` under the H1 and/or optional lightweight `## Module:` — your judgment. **Multi-subject extracts are split into partials** (`Extract: partial` + `Part:`); each piece lives under **one** Key Abstraction; the same `Source:` on every partial from the same upstream extract is how reviewers reassemble coverage — no separate index section. `## [Unallocated]` at file end, rare, with `Reason:` when used. |

2. **Rules**

- Follow the **Identification rules**, **Sub-allocation rules**, and **Extract format** sections below for what counts as a Key Abstraction, how Core terms get divided, and how source extracts get sub-allocated.
- Source text inside extracts is **never** paraphrased, summarized, edited, or reformatted. Copy bytes from the real source — partition extracts when you have them, otherwise the corpus chunk — as-is. The only allowed editorial mark is an ellipsis `[…]` for an explicit gap inside a partial extract, and that gap must be labelled in the `Part:` header line.
- No kinds, no stereotypes, no UML notation. No `<<Entity>>`, `<<ValueObject>>`, `?`, typed properties, method signatures, or relationship arrows. Shape hints are **free-form prose**, not labels.
- When the file uses `## Module:`, a Key Abstraction lives in exactly one module; the same name under two modules is a scope tension — record under one and flag overlap in `Tension:`, do not duplicate. With no modules, keep abstractions distinct from each other.
- After drafting, act as a *peer reviewer*: every Key Abstraction has Intent + Core terms + Shape hint + at least one source extract; Core-terms phrases are attached sensibly (or `[Unallocated]` with `Reason:` — rare); no source passage silently dropped; multi-subject passages are **sliced into partials**, not parked whole under the wrong abstraction.

3. **Who is checking**

A **modeler** about to move from settled key abstractions toward a class-level model. They read the file front-to-back and ask: *can I trust that every phrase in the Core terms ended up attached to exactly one named Key Abstraction — and that the attachment is supported by verbatim source I can see inline?*

---

## What is — and is not — a Key Abstraction

A **Key Abstraction** is a named, source-grounded domain unit that the **source in scope** (a module's text, or the whole passage you are working on) orbits. At this fidelity, a Key Abstraction is **only** a name + intent + Core-terms absorption + Shape hint + source extracts; it carries **no kind, no fields, no methods, no relationships, no super/sub decisions**.

### The text-orbits test (the only test that matters)

For any candidate Key Abstraction, ask:

> **Does the source speak about *this* as a named unit — with its own slice of the Core terms and its own sentences — or is it just vocabulary that hangs off another unit?**

- If yes — the source treats this as a named unit with its own vocabulary cluster — it is a Key Abstraction.
- If no — if removing the candidate and folding its terms into another abstraction would not lose any meaning the source is actually carrying — fold it in.

A useful sanity check: if you can write the Intent line for a candidate in one source-grounded sentence *without referring to another Key Abstraction's Core terms*, the abstraction stands. If the Intent keeps wanting to borrow another abstraction's vocabulary to make sense, it is not yet its own abstraction.

### Commitment-deferred on every axis except name and intent

A Key Abstraction is deliberately *uncommitted* on every modeling decision a later skill will make. This is the entire reason the rung exists:

| Decision | Deferred to |
| -------- | ----------- |
| Is this one class, two classes, or a hierarchy? | Settle pass (this skill) / class-level skills |
| Does it have identity (Entity) or is it a value (Value Object)? | Class-level skill — stereotypes come later |
| What fields / properties does it have? | Later still |
| What operations / methods does it have? | Later still |
| How does it relate to Key Abstractions in **other** modules? | Cross-module relationship skill, later |
| Is it a Service, Event, Policy, Process, Role? | Tactical DDD skill, much later |
| Is its "Not responsible for" line… | Never asked here — responsibility is a later rung |

A Key Abstraction **may** hold a taxonomy (one base + several variants, all inside one abstraction). It **may** hold multiple responsibilities that will later split. It **may** be both noun-shaped and verb-shaped at once. It **may** later turn out to be a property of another abstraction (demoted in the settle pass). None of those are defects *at the identification draft*.

### Shape hint — a free-form modeler note, never a tag

Every Key Abstraction carries a one-line **Shape hint**: a free-form prose note about what the source seems to be treating it as. Common shapes you will observe (but never stop at):

- *Single-thing* — one named domain unit with its own vocabulary cluster.
- *Taxonomy* — one base with several named variants in the source.
- *Value-like* — defined entirely by content, no identity cues.
- *Procedure-like* — verb-shaped; a named mechanic with a trigger and an outcome.
- *State-vocabulary-like* — a list of named statuses, each with transition rules.
- *Rule-attached* — a rule the source frames as belonging to another abstraction rather than a unit of its own.
- *Both-shaped* — noun-shaped and verb-shaped at once; a thing-with-state *and* a named procedure.

These are **notes for the modeler**, not stereotypes. They are written as free-form prose sentences, never as `<<Tag>>` labels. The settle pass may confirm or contradict any of them.

### How to name a Key Abstraction

- Pick the noun phrase the **source itself** uses for the unit. If the source has stable names, use them. Capitalize once (`Funds Transfer`, `Settlement Window`, `Loyalty Point`) so the name is distinguishable from ordinary prose.
- Keep it short and singular where possible (`Funds Transfer`, not `Funds Transfers and Their Reconciliation`).
- Do not invent names to generalize. If the source has one noun phrase for it, use that. If the source uses two or three phrases for the same unit, pick one and absorb the others into the Core terms list.
- No compound glue words (`[Funds Transfer and Settlement]`, `[Loyalty Point System]`, `[Foundations]`, `[Core]`). A compound name is almost always a signal that you are naming a *module* inside a Key Abstraction, or two abstractions glued together.
- No source-structure names (`[Section 3.2]`, `[Ch. 1 subsection 4]`).

---

## Core concepts

### Workspace

Output: `<active_skill_workspace>/abd-ooad/key-abstractions.md` (engagement root from the parent agent's `workspace` skill).

### Inputs
`module-partitioning.md` 
When present: module names, per-module Core terms, verbatim partition extracts — use them and mirror module headings. When absent: skip; read the corpus instead

**Do not** treat missing partition as a blocker. If the corpus is huge and unpartitioned, you may still produce a useful `key-abstractions.md` with light modules or a flat list; optionally suggest running 
`module-partitioning` later if the team wants a stricter scope cut.


### Structure

**With `module-partitioning.md`:** Each `## Module: [Name]` matches a partition module one-for-one, in partition order. Under each module, only:

- `### Key Abstraction: {{Name}}` — in source order. **All** verbatim material for that abstraction lives here, including every **partial** slice cut from a longer extract. Multi-concept upstream extracts become **several partials** under **different** headings here; reviewers reassemble by matching `Source:` + `Part:` across those headings.

**Without a partition (or you chose not to mirror it):**

- Prefer `## Key Abstraction: {{Name}}` directly under the H1 when the scope is small or a flat list is clearer.
- Optionally add `## Module:` groupings if it helps navigation — loose and practical, not a second formal partition pass.
- `## [Unallocated]` at end of file — **rare**; same rules as above.


### Identification rules

Repeat the identification loop **per module** when the file has modules; **once over the whole scope** when it does not.

1. **Read the Core terms** for that scope. From the partition list when you have it; otherwise derive a phrase list from the source — repeated, source-grounded noun phrases.
2. **Group the phrases** that cluster around the same named unit in the source.
3. **Name each cluster** with the source's noun phrase. Prefer a single short name.
4. **Write Intent** as one source-grounded sentence: what role the abstraction plays in the source.
5. **List Core terms absorbed** — each phrase that the abstraction's extracts speak about.
6. **Write Shape hint** as a one-line free-form prose observation — never a tag.
7. **Write Tension** only if there is one. Common tensions: overlap with another abstraction; possible taxonomy under the abstraction; possible absorption into another.
8. **Sub-allocate verbatim extracts** (see next section).

Key Abstractions are listed in **source order** — the order the source introduces them.

### Sub-allocation rules (verbatim source)

**Default: break the extract into pieces and park each piece under the right concept.** A passage that mentions **more than one** Key Abstraction is **not** one extract under whichever abstraction you like best. **Cut** it at natural boundaries (paragraph, bullet, numbered step, sentence only when you must). For **each** slice:

1. Put a separate `**Extract — …**` block under the **single** Key Abstraction (the named concept) that slice **primarily** supports — that is where the verbatim body lives.
2. Set `Extract: partial` and a precise `Part:` line (which sentences, bullets, or paragraph range).
3. Repeat the **same** `Source:` line on every partial that came from that one upstream extract (partition pointer or corpus locator), so a reviewer can reassemble by `Source:` + `Part:`.

There is **no** shared holding area for “this belongs in the module but not under one abstraction.” Multi-concept prose is always **multiple partials**, each under its concept.

Every byte of the input extract must appear in **exactly one** partial body across the module or across the flat file. No overlap between partials unless the source itself repeats text; no dropped sentences between slices.

**Where things land:**

1. **Under a `### Key Abstraction:`** — whole extracts (`Extract: whole`) when the entire source passage is about one abstraction only, or **partial extracts** when you sliced it. Sibling partials from the same upstream extract share the same `Source:` line and different `Part:` lines — that is the whole audit trail.
2. **`## [Unallocated]`** — only when a slice cannot be placed after a genuine attempt to cut and name abstractions; document `Reason:`. Prefer adding or refining a Key Abstraction over growing Unallocated.

Common rules:

- **Verbatim copy** — extract bodies are copied byte-for-byte from the input. Do not paraphrase; do not "clean up" OCR artifacts, running headers, or page numbers — those are part of the audit trail.
- **Non-contiguous slices** of the same input extract are **separate** `**Extract — …**` blocks (each with its own `Part:`), not one block with a gap unless you use `[…]` and describe the gap in `Part:`.
- **Back-reference traceability.** When using the partition, `Source:` points at `module-partitioning.md` (module + extract title). Otherwise `Source:` points at the corpus (file / chunk / page / section). One hop back, not none.

### When to use `[Unallocated]`

**Try partial splits first.** If a passage spans several concepts, slice it and place each slice under its Key Abstraction before considering `[Unallocated]`.

An extract goes to `## [Unallocated]` only when **all** of these are true **after** that attempt:

- The passage clearly carries domain content (it names terms, describes rules, or establishes shape).
- A **single remaining fragment** still cannot be placed under one Key Abstraction (genuinely ambiguous, missing context, or would force a bad name).
- Splitting further would **not** improve attribution (not merely “awkward” — use partials when it is merely awkward).

Each `[Unallocated]` extract carries a `Reason:` line. Empty `[Unallocated]` is healthy — it means every passage attributed cleanly on first pass.

### Tensions inside a Key Abstraction (draft phase)

During **identification**, if an abstraction has a meaningful pull toward merging with another, splitting, or containing a taxonomy the source hints at, add a `Tension:` line. This is **not** a second allocation — extracts stay put until the **settle** pass.

During **settle**, every draft `Tension:` is either **closed** (logged under **`### Resolutions`** with evidence) or moved to **`### Deferred tensions`** with a one-line reason. **Omit** the `Tension:` field on a Key Abstraction when nothing remains after settlement (do not leave stale open tensions next to a closure in Resolutions).

---

## Settle tensions (final pass — same skill, same file)

**When:** Immediately after identification in the same engagement, before calling the file done.

**Evidence:** Module-internal only — the extracts and Core terms already in `key-abstractions.md`, plus spot-checks against the same corpus scope. **No** typed fields, methods, associations, stereotypes, Entity/VO/Service labels, or cross-module “same concept” merges (note name collision as residual scope tension only).

**Only four structural moves** (nothing else changes the concept set):

### Merge

Two or more Key Abstractions are **one** named unit in the source (synonymy, redundant naming, or one is clearly a subset with no separate vocabulary).

- **Output:** One surviving `### Key Abstraction: Name` (prefer the **source-dominant** phrase).
- **Core terms:** Union of absorbed phrases; dedupe; **disjoint** across the module.
- **Extracts:** All extracts from merged abstractions under the survivor (same ```source bodies).
- **Log in `### Resolutions`:** `Merge: A + B -> C` with rationale and **Evidence:** (extract title or quote).

### Split

One abstraction carries a **clear taxonomy** or **distinct named mechanisms** the text treats as separate kinds.

- **Output:** Sibling abstractions **named from the source**.
- **Core terms:** Partition phrases; no phrase under two abstractions.
- **Extracts:** Re-home whole or partial extracts; shared `Source:` on partials from one upstream extract.
- **Log:** `Split: A -> B, C` with rationale and evidence.

### Promotion / Demotion

- **Promotion:** A cluster under a parent **earns** its own Key Abstraction (enough distinct sentences, rules, and vocabulary **in this module**).
- **Demotion:** A named unit is **not** first-class here — fold Core terms and extracts **under** the parent; remove the extra `### Key Abstraction:` heading.
- **Log:** `Promoted: …` or `Demoted: …` with evidence.

### Per-module `### Resolutions`

Under each `## Module:` (after optional scope one-liner), **before** the first `### Key Abstraction:`:

1. Bullets for every **Merge / Split / Promotion / Demotion** (or state explicitly that none occurred).
2. Bullets that **close** each draft `Tension:` from identification (**Evidence:** extract or quote).
3. **`### Deferred tensions`** — only if something cannot close on module-internal evidence; omit the heading if empty.

**Flat files (no `## Module:`):** Put one **`### Resolutions`** and optional **`### Deferred tensions`** block immediately under the H1 / front matter, before the first `### Key Abstraction:`.

**Front matter:** After settlement, the file is the single hand-off artifact — pointer to `module-partitioning.md` and/or corpus as today; **module count** and **settled Key Abstraction count** (rename the count label to **Settled Key Abstractions: K** if you applied merges/splits, or keep **Key Abstractions: K** if unchanged).

### What you do not do here

- Do **not** leave a multi-concept extract **whole** under one Key Abstraction — **break it up**; one partial per concept, each under that concept’s heading.
- Do **not** identify classes, stereotypes, kinds, properties, operations, or responsibilities.
- Do **not** invent a Key Abstraction that the source text does not orbit.
- Do **not** promote a rule or a property to its own Key Abstraction unless the source treats it as a named unit with its own vocabulary. When in doubt, absorb it into the abstraction it hangs off — and record a Tension if you are unsure.
- Do **not** decide super/sub, Entity/VO, or kind tags — those belong to later skills.
- Do **not** draw relationships between abstractions. `Tension:` may mention overlap with another **named** unit; structured relationships come later.

---

## Extract format

Every verbatim extract sits under a **single** `### Key Abstraction:` or under `## [Unallocated]`, with an extract header. Sliced upstream passages appear as **multiple** partials in **different** Key Abstraction sections, tied together by the same `Source:` line — no extra index section.

### Extract header (required for every extract)

```
**Extract — {{short title}}**
Source: {{from partition: "module-partitioning.md — Module: [{{ModuleName}}] — \"{{partition extract title}}\"" — else: "{{corpus file or chunk id}} — \"{{section path or anchor}}\""}}
Locator: {{precise locator — chapter / page / lines / section heading / etc.}}
Extract: {{whole | partial}}
{{Part: {{which slice — required when Extract: partial}}}}
{{Reason: {{required only on [Unallocated] extracts}}}}
```

- The `Extract:` line is `whole` when the full source passage is copied under exactly one Key Abstraction; `partial` otherwise.
- When `Extract: partial`, the `Part:` line is **mandatory** and names the slice in source-grounded terms (e.g. *the second paragraph of "Reconciliation Window"*, *the three-bullet list under "Outbound Wire Limits"*).
- `Reason:` is required on `## [Unallocated]` extracts only; omit elsewhere.
- The `Source:` line points back to the input one hop (partition or corpus).

### Extract body (required)

Place the verbatim text inside a fenced `source` block so reviewers see exactly what was copied (whitespace, bullets, OCR artifacts, page numbers — all preserved):

```
```source
{{verbatim text — copied byte for byte from the input}}
```
```

If a partial extract has an internal gap, mark the gap with `[…]` on its own line inside the fenced block, and describe the gap in the `Part:` header line.

---

## The shape of a good `key-abstractions.md`

**Front matter is thin by contract.** Source pointer(s) + counts (modules if any, key abstractions total). **Do not** put per-module or per-abstraction descriptions, intent statements, term lists, or rationale in the front matter. Every piece of information about a particular abstraction lives under that abstraction's heading.

When the file uses modules, each module section follows this shape:

1. `## Module: [{{Name}}]` — from the partition when you have it, or your lightweight grouping.
2. *(Optional one-liner)* — tight scope note.
3. **`### Resolutions`** — merges/splits/promotions/demotions (or explicit “none”) and closure of every draft tension (**Evidence:**); optional **`### Deferred tensions`**.
4. A `### Key Abstraction: {{Name}}` sub-section per settled abstraction, in source order. Each carries Intent, Core terms, Shape hint, optional residual `Tension:` only, and one or more verbatim extracts (whole or partial). Partials from the same upstream extract use the **same** `Source:` in each section where they appear.

```markdown
# Key Abstractions — {{project_name}}

Source: {{module-partitioning.md at path, and/or corpus roots}}
Modules: {{N or 0}}     Key Abstractions: {{K}}

---

## Module: [{{ModuleName}}]

### Resolutions

- **Merge / Split / Promotion / Demotion:** {{none or logged moves with Evidence:}}
- {{Closed tensions with Evidence:}}

### Key Abstraction: {{Name}}

Intent: {{one source-grounded sentence}}.

Core terms (absorbed from this module's Core terms list):

- {{noun phrase from the module's Core terms}}
- {{noun phrase}}
- …

Shape hint: {{free-form prose observation — never a tag}}.

Tension: {{optional residual only after settle; omit when closed in Resolutions}}.

**Extract — {{short title}}**
Source: module-partitioning.md — Module: [{{ModuleName}}] — "{{partition extract title}}"
Locator: {{partition locator}}
Extract: whole

```source
{{verbatim text copied from module-partitioning.md}}
```

### Key Abstraction: {{AnotherName}}

Intent: …
Core terms:
- …
Shape hint: …

**Extract — … (partial from same partition extract as above)**
Source: (same Source line as sibling partial)
Extract: partial
Part: {{which slice}}

```source
{{verbatim slice}}
```
```

Key Abstractions are listed in source order within each module. Coverage for a sliced upstream extract: find all partials with the same `Source:` and check `Part:` lines reassemble the original.

---

## Example

A small worked example: one module, two Key Abstractions, **sliced** module opener (two partials under two concepts — same `Source:`). **Payments / banking — illustrative only.**

```markdown
## Module: [Funds Transfer]

### Resolutions

- **Merge / Split / Promotion / Demotion:** None (example module).
- **Wire Transfer vs Funds Transfer:** Closed for this example — both KAs retained; cap rules stay under Wire Transfer. Evidence: Wire Transfer limits extract.

### Key Abstraction: Funds Transfer

Intent: The atomic operation that moves a specified amount from one account to another and records a matched debit/credit pair for reconciliation.

Core terms (absorbed from this module's Core terms list):

- funds transfer
- source account / destination account
- debit / credit
- reconciliation window
- exceptions desk

Shape hint: Both noun-shaped and verb-shaped — a thing-with-state (pending / matched / escalated) and a named procedure (debit → credit → record → reconcile).

**Extract — Funds Transfer (overview)**
Source: module-partitioning.md — Module: [Funds Transfer] — "Funds Transfer (overview)"
Locator: Ch.3 §Funds Transfer
Extract: whole

```source
A funds transfer moves a specified amount from a source account to a
destination account in a single atomic operation. Every transfer:
- Debits the source account by the transfer amount.
- Credits the destination account by the transfer amount.
- Records a matched debit/credit pair on the ledger for reconciliation.
…
A transfer that cannot be matched within the reconciliation window is
escalated to the exceptions desk.
```

**Extract — Module opener (partial — generic transfer framing)**
Source: module-partitioning.md — Module: [Funds Transfer] — "Funds Transfer module opener"
Locator: Ch.3 opening sentences
Extract: partial
Part: Sentences that define the generic transfer mechanism and reconciliation — before the wire / KYC paragraph.

```source
…first sentences of module opener, verbatim…
```

### Key Abstraction: Wire Transfer

Intent: A named Funds Transfer variant whose per-transaction, daily, and beneficiary-jurisdiction caps are gated by the customer's KYC tier.

Core terms:

- Wire Transfer
- per-transaction cap
- daily cap
- beneficiary-jurisdiction cap
- KYC tier
- EDD cap

Shape hint: Taxonomy under Funds Transfer — the module treats it as a specialization with its own cap vocabulary; may settle as a sub-type or a kind-tag on Funds Transfer.

**Extract — Module opener (partial — wire and KYC)**
Source: module-partitioning.md — Module: [Funds Transfer] — "Funds Transfer module opener"
Locator: Ch.3 opening sentences
Extract: partial
Part: Sentences on outbound wires, KYC tiers, and product-specific caps.

```source
…remaining sentences of module opener, verbatim…
```

**Extract — Wire Transfer limits**
Source: module-partitioning.md — Module: [Funds Transfer] — "Wire Transfer limits"
Locator: Ch.5 §Wire Transfer — bullet list of limits
Extract: whole

```source
- Per-transaction cap: A single outbound wire cannot exceed the customer's
  per-transaction limit for the assigned KYC tier. …
- Daily cap: The total outbound wire amount on a single business day cannot
  exceed twice the per-transaction cap. …
- Beneficiary-jurisdiction cap: Wires destined for jurisdictions on the
  enhanced-due-diligence list cannot exceed the EDD cap regardless of
  KYC tier.
```
```

---

## Build

**Goal:** Author `key-abstractions.md`, using a partition when you have one and the corpus when you do not.

1. **Scope the file** — If `module-partitioning.md` exists, list its `## Module: [Name]` headings in order. If not, decide whether to use flat `## Key Abstraction:` only or a few optional `## Module:` groupings; do not stall on this.
2. **Per scope chunk (module or whole file), propose Key Abstraction names** — from the Core terms list (partition) or from reading the source. Group phrases that cluster around one named unit. Commonly 2–6 abstractions per chunk, sometimes 1, rarely more than ~8.
3. **Apply the text-orbits test** to each candidate — fold weak candidates in.
4. **Attach every Core-terms phrase** to exactly one Key Abstraction when you have a partition list; otherwise keep terms consistent with your extracts. No phrase silently dropped.
5. **Write Intent, Shape hint, and optional Tension** for each Key Abstraction.
6. **Sub-allocate verbatim extracts** — whole under one abstraction when the passage is single-subject; otherwise **slice** into partials, each block under its concept, shared `Source:` + distinct `Part:` on every partial from the same upstream extract.
7. **Re-read sliced extracts** — partials reassemble to the full source; no gaps, no duplicate sentences.
8. **Settle (final pass)** — Per **Settle tensions**: list every tension and overlapping intent; apply only merge/split/promotion/demotion; add **`### Resolutions`** (and **`### Deferred tensions`** if needed) per module or once for flat files; re-home extracts and Core terms; remove closed `Tension:` lines.
9. **Validate settlement** — Every draft `Tension:` is closed in **Resolutions** or **Deferred tensions**; Core terms are disjoint per module; extract coverage unchanged except for documented merges/splits.
10. **Persistence:** engagement root from the parent agent `workspace`; file lives at `abd-ooad/key-abstractions.md`.

**While writing:**

- Multi-abstraction passages become multiple partials, not one mis-tagged whole extract.
- Verbatim only — bodies from the partition or corpus; headers and labels are yours.
- During identification, `Tension:` lines annotate only — the settle pass resolves them.

---

## Validate

**Goal:** Read the Key Abstractions file as a modeler after settlement, ready for vocabulary or class-level work — not as a second partition.

### Coverage

- If the engagement used `module-partitioning.md`, every `## Module: [Name]` from it appears here, in partition order, one-for-one.
- Every module (if any) has at least one `### Key Abstraction:` — zero abstractions under a non-empty module is a signal to reread.
- Every Core-terms phrase from each partition module (when present) appears under exactly one Key Abstraction in that module, or is explained via a rare `[Unallocated]` slice with `Reason:`.
- Every verbatim extract you took from the partition (when present) appears inline here — reassembled from whole + partials — nothing silently dropped. Without a partition, spot-check against the corpus the same way.

### Identification discipline

- Every Key Abstraction has all four required fields: **Intent** (one source-grounded sentence), **Core terms** (bullet list), **Shape hint** (free-form one-liner), and **at least one source extract**. Any missing field is a gap; fix or demote.
- Intent does not borrow vocabulary from another Key Abstraction's Core terms to make sense. If it does, the abstraction is not yet its own unit — fold it in or split the borrowed term into its own abstraction.
- Names are source-grounded — the source uses these noun phrases. No invented generic names, no compounds, no source-structure names.
- When modules exist: no Key Abstraction should appear under two modules as duplicate work; same name in two modules is a scope tension — record it, do not duplicate bodies.

### Sub-allocation discipline

- No source passage appears under two Key Abstractions except as **partials** — each with `Extract: partial`, its own `Part:`, and the **same** `Source:` as its sibling partials from that upstream extract.
- Every `Extract: partial` has a `Part:` line naming the slice in source-grounded terms — not "the relevant bit".
- Every `## [Unallocated]` extract has a `Reason:` line.
- Verbatim discipline: pick three random extracts and spot-check against the partition or corpus — character-level identity, not light cleanup.

### No-commitment discipline (the point of this rung)

- No `<<Entity>>`, `<<ValueObject>>`, `<<Service>>`, `<<Event>>` or any other stereotype tag.
- No typed properties, no method signatures, no cardinality arrows.
- No super/sub commitments — a Key Abstraction may hold a taxonomy in one chunk; that is correct.
- No cross-module relationships — Tension lines only note in-module pulls.
- If the file carries any of the above, the rung has leaked into later skills; strip them and record the decisions as Tensions to resolve in the settle pass.

### Settlement discipline

- Every `## Module:` (or the flat file) has **`### Resolutions`** before the first `### Key Abstraction:`.
- Every identification `Tension:` is **closed** in **Resolutions** (with evidence) or listed under **Deferred tensions** — no silent drops.
- Remaining `Tension:` lines on Key Abstractions are **rare residuals** only (omit the field when nothing remains).

### Hand-off readiness

A reviewer after settlement in this same file should be able to:

- Read a single `### Key Abstraction:` sub-section and have **all** the source they need for the next rung — no need to re-open the partition or the corpus for that abstraction.
- Trust that multi-subject text was **sliced**, not hidden: partials with matching `Source:` reassemble; `[Unallocated]` is rare and explained; nothing silently duplicated.

If the file is thin, vague, or leaks into class-level commitments, **improve in place** with targeted re-reads of the partition or corpus — not a wholesale rework unless the scope was wrong.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Core terms disjoint within module

Within a single module (or the whole flat file), every Core-terms phrase must be attached to exactly one Key Abstraction. No phrase should appear under two different abstractions in the same scope. Passing means every bullet in every Core terms list is unique within its module. Failing means a phrase is duplicated across two or more Key Abstractions.

#### DO

- Attach each Core-terms phrase to the single Key Abstraction whose extracts primarily speak about that concept.

  **Example (pass):** `reconciliation window` appears only under `Funds Transfer`, not also under `Wire Transfer`.

- When two abstractions share vocabulary, assign the phrase to the one with stronger source grounding and note the overlap in a `Tension:` line on the other.

  **Example (pass):** `Tension: "KYC tier" also appears in Funds Transfer context — assigned here because cap rules use it more directly.`

#### DON'T

- List the same phrase under two Key Abstractions in the same module.

  **Example (fail):**
  ```
  ### Key Abstraction: Funds Transfer
  Core terms:
  - reconciliation window

  ### Key Abstraction: Settlement
  Core terms:
  - reconciliation window    ← duplicate
  ```

- Use slightly different wording of the same concept to bypass disjointness (e.g., "reconciliation window" vs "recon window" for the same thing).

  **Example (fail):** Two entries that are clearly the same phrase with cosmetic variation, placed under different abstractions.

### Rule: Extract format compliance

Every `**Extract — …**` block must carry the required header fields: `Source:`, `Locator:`, `Extract: whole|partial`, and `Part:` when the extract is partial. Passing means every extract block has a complete, well-formed header. Failing means a header field is missing or `Extract: partial` appears without a `Part:` line.

#### DO

- Include `Source:` on every extract pointing back one hop (partition file or corpus locator).

  **Example (pass):**
  ```
  **Extract — Funds Transfer (overview)**
  Source: module-partitioning.md — Module: [Funds Transfer] — "Funds Transfer (overview)"
  Locator: Ch.3 §Funds Transfer
  Extract: whole
  ```

- Include `Locator:` with a precise locator (chapter, page, lines, section heading).

  **Example (pass):** `Locator: Ch.5 §Wire Transfer — bullet list of limits`

- Set `Extract:` to exactly `whole` or `partial` (no other values).

  **Example (pass):** `Extract: partial`

- When `Extract: partial`, always include a `Part:` line naming the slice in source-grounded terms.

  **Example (pass):** `Part: Sentences that define the generic transfer mechanism — before the wire/KYC paragraph.`

#### DON'T

- Omit the `Source:` line from an extract header.

  **Example (fail):** An extract block with title, Locator, and Extract type but no Source line.

- Use vague `Part:` descriptions like "the relevant bit" or "see above".

  **Example (fail):** `Part: the relevant section` — not source-grounded.

- Set `Extract:` to a value other than `whole` or `partial`.

  **Example (fail):** `Extract: summary` or `Extract: paraphrased`.

- Omit `Part:` when `Extract: partial` is set.

  **Example (fail):** `Extract: partial` with no `Part:` line following it.

### Rule: Front matter is thin

The front matter (everything before the first `## Module:` or `### Key Abstraction:` heading) must contain only source pointer(s) and counts (modules, key abstractions). No per-module descriptions, no per-abstraction summaries, no intent statements, and no term lists belong in the front matter. Passing means the front matter is a few metadata lines. Failing means it contains teaching content that belongs under abstraction headings.

#### DO

- Keep front matter to: H1 title, `Source:` line(s), and counts (`Modules: N`, `Key Abstractions: K`).

  **Example (pass):**
  ```
  # Key Abstractions — Payments Domain

  Source: module-partitioning.md at abd-ooad/module-partitioning.md
  Modules: 3     Key Abstractions: 8

  ---
  ```

- Place all abstraction-specific information (intent, terms, extracts) under the appropriate `### Key Abstraction:` heading.

  **Example (pass):** Front matter is 5 lines; first module starts at line 7.

#### DON'T

- Put per-abstraction summaries, intent statements, or term listings in the front matter.

  **Example (fail):**
  ```
  # Key Abstractions — Payments Domain

  Source: ...
  Modules: 3     Key Abstractions: 8

  Key abstractions identified:
  - Funds Transfer: moves money between accounts
  - Wire Transfer: variant with caps
  - Settlement: end-of-day reconciliation
  ```
  (The summary list belongs under module/abstraction headings, not here.)

- Include module-level scope notes or descriptions above the first `## Module:` heading.

  **Example (fail):** Two paragraphs explaining the domain before the first module heading — that belongs in the module's optional one-liner or in an external document.

### Rule: No class-level commitments

Key Abstractions are deliberately uncommitted on every modeling axis except name and intent. The file must contain no stereotypes, typed properties, method signatures, cardinality arrows, or other class-level notation. Passing means the file stays at the identification rung. Failing means class-level decisions have leaked into the file.

#### DO

- Use only free-form prose in the Shape hint line — observations like "taxonomy under Funds Transfer" or "value-like — defined entirely by content".

  **Example (pass):** `Shape hint: Taxonomy under Funds Transfer — the module treats it as a specialization with its own cap vocabulary.`

- Record modeling uncertainty as a `Tension:` line, not as a class decision.

  **Example (pass):** `Tension: May settle as a sub-type or a kind-tag on Funds Transfer.`

- Keep Core terms as plain noun phrases — no types, no annotations.

  **Example (pass):**
  ```
  - per-transaction cap
  - daily cap
  - beneficiary-jurisdiction cap
  ```

#### DON'T

- Use UML stereotype tags like `<<Entity>>`, `<<ValueObject>>`, `<<Service>>`, `<<Event>>`, `<<Aggregate>>`.

  **Example (fail):** `Shape hint: <<Entity>> with lifecycle states.`

- Add typed properties like `amount: Decimal`, `status: String`, or `transferId: UUID`.

  **Example (fail):** Core terms list includes `transferId: UUID` or `amount: Money`.

- Include method signatures like `execute(from, to, amount) -> Result`.

  **Example (fail):** `Operations: validate(amount) -> bool, execute() -> TransferResult`

- Use cardinality notation like `1..*`, `0..1`, or relationship arrows.

  **Example (fail):** `Funds Transfer 1..* --> Account` in any section of the file.

- Commit to super/sub hierarchies (Entity vs Value Object, parent/child splits).

  **Example (fail):** `Wire Transfer <<extends>> Funds Transfer` — this belongs to a later skill.

### Rule: Partial extracts have Part line

Every extract marked `Extract: partial` must have a corresponding `Part:` line that names the slice in source-grounded terms. Conversely, `Extract: whole` must not have a `Part:` line. This ensures reviewers can reassemble sliced upstream extracts. Passing means the pairing is correct on every extract. Failing means a partial without `Part:` or a whole with an unnecessary `Part:`.

#### DO

- When `Extract: partial`, include `Part:` naming the specific slice (paragraph range, bullet list, sentence group).

  **Example (pass):**
  ```
  Extract: partial
  Part: Sentences that define the generic transfer mechanism — before the wire/KYC paragraph.
  ```

- Name the slice in source-grounded terms a reviewer can locate in the upstream extract.

  **Example (pass):** `Part: The three-bullet list under "Outbound Wire Limits".`

- Omit `Part:` when `Extract: whole` (the entire passage lives here).

  **Example (pass):**
  ```
  Extract: whole
  ```
  (No `Part:` line.)

#### DON'T

- Set `Extract: partial` without a `Part:` line.

  **Example (fail):**
  ```
  Extract: partial
  ```
  (Missing `Part:` — reviewer cannot identify which slice this is.)

- Add a `Part:` line to a `Extract: whole` block (contradicts the "whole" claim).

  **Example (fail):**
  ```
  Extract: whole
  Part: First two paragraphs only.
  ```
  (If it is only part of the passage, it should be `Extract: partial`.)

### Rule: Required fields per abstraction

Every `### Key Abstraction:` section must carry all four required fields — **Intent**, **Core terms** (bullet list), **Shape hint**, and at least one verbatim extract — so the next skill in the pipeline has a complete, self-contained unit to work from. Passing means every abstraction has all four present and non-empty. Failing means any abstraction is missing a field or has a placeholder-only stub.

#### DO

- Include an `Intent:` line with a complete, source-grounded sentence for every Key Abstraction.

  **Example (pass):** `Intent: The atomic operation that moves a specified amount from one account to another.`

- Include a `Core terms` header followed by at least one `- phrase` bullet.

  **Example (pass):**
  ```
  Core terms (absorbed from this module's Core terms list):
  - funds transfer
  - source account / destination account
  ```

- Include a `Shape hint:` line with free-form prose (not a `<<Tag>>`).

  **Example (pass):** `Shape hint: Both noun-shaped and verb-shaped — a thing-with-state and a named procedure.`

- Include at least one `**Extract — …**` block with a verbatim ```` ```source ```` body.

  **Example (pass):** An abstraction with two extracts, one whole and one partial.

#### DON'T

- Leave an abstraction with no `Intent:` line or only `Intent: …` / `Intent: {{placeholder}}`.

  **Example (fail):** A `### Key Abstraction: Wire Transfer` section with no `Intent:` line at all.

- Omit `Core terms` entirely or have zero bullet items under the header.

  **Example (fail):** `Core terms:` followed by blank lines and then the next heading.

- Skip the `Shape hint:` or use a stereotype tag instead of prose.

  **Example (fail):** `Shape hint: <<Entity>>` — tags are not allowed at this rung.

- Have a Key Abstraction with zero `**Extract — …**` blocks.

  **Example (fail):** Name + Intent + Core terms + Shape hint present, but no source extracts at all.

### Rule: Resolutions before abstractions

Every `## Module:` section (or the flat file when no modules exist) must have a `### Resolutions` block before the first `### Key Abstraction:`. This documents the settle pass — merges, splits, promotions, demotions, and closure of identification-phase tensions. Passing means `### Resolutions` appears and precedes the first abstraction. Failing means it is missing or appears after.

#### DO

- Place `### Resolutions` immediately after the module heading (and optional one-liner) but before the first `### Key Abstraction:`.

  **Example (pass):**
  ```
  ## Module: [Funds Transfer]

  ### Resolutions

  - **Merge / Split / Promotion / Demotion:** None.
  - **Wire Transfer vs Funds Transfer:** Closed — both retained. Evidence: …

  ### Key Abstraction: Funds Transfer
  ```

- In flat files (no `## Module:`), place `### Resolutions` under the H1 / front matter, before the first `### Key Abstraction:`.

  **Example (pass):** `### Resolutions` at line 8, first `### Key Abstraction:` at line 15.

- State explicitly when no structural moves occurred: "None" or "No merges, splits, promotions, or demotions."

  **Example (pass):** `- **Merge / Split / Promotion / Demotion:** None (two abstractions retained as-is).`

#### DON'T

- Omit `### Resolutions` entirely from a module section.

  **Example (fail):** `## Module: [Payments]` followed directly by `### Key Abstraction: Payment` with no Resolutions block between them.

- Place `### Resolutions` after one or more `### Key Abstraction:` sections.

  **Example (fail):** Two Key Abstractions listed, then `### Resolutions` appears at the bottom of the module.

- Leave draft `Tension:` lines unaddressed — every tension from identification must be closed in Resolutions or listed under `### Deferred tensions`.

  **Example (fail):** `Tension: Possible merge with Settlement` on a Key Abstraction but no mention of it in `### Resolutions` or `### Deferred tensions`.

### Rule: Source-grounded names for Key Abstractions

Every Key Abstraction name must be the noun phrase the source itself uses for the unit — not an invented generalization, compound glue word, or source-structure label. Passing means names come directly from the source vocabulary. Failing means names are invented, compound, or structural.

#### DO

- Use the noun phrase the source repeats when discussing this unit, capitalized once: `Funds Transfer`, `Settlement Window`, `Loyalty Point`.

  **Example (pass):** The source says "A funds transfer moves…" repeatedly — name it `Funds Transfer`.

- When the source uses multiple phrases for the same unit, pick one and absorb the others into Core terms.

  **Example (pass):** Source uses "wire transfer" and "outbound wire" — name is `Wire Transfer`; "outbound wire" goes into Core terms.

- Keep names short and singular where possible.

  **Example (pass):** `Settlement Window` not `Settlement Windows and Their Reconciliation Mechanics`.

#### DON'T

- Invent generalizing names the source never uses.

  **Example (fail):** `### Key Abstraction: Financial Instrument` — the source never says "financial instrument"; it says "funds transfer" and "wire transfer".

- Use compound glue names that merge two units or name a module inside an abstraction.

  **Example (fail):** `### Key Abstraction: Funds Transfer and Settlement` or `### Key Abstraction: Core Payment Mechanisms`.

- Use source-structure labels as names.

  **Example (fail):** `### Key Abstraction: Section 3.2` or `### Key Abstraction: Ch. 1 subsection 4`.

- Name after a quality or adjective rather than the thing itself.

  **Example (fail):** `### Key Abstraction: Compliance` when the source actually orbits `Wire Transfer Caps`.

### Rule: Text-orbits test for every Key Abstraction

Every Key Abstraction must pass the text-orbits test: the source speaks about it as a named unit with its own slice of vocabulary and its own sentences. If removing the candidate and folding its terms into another abstraction would not lose meaning the source actually carries, the candidate should be absorbed — not promoted to its own heading. Passing means every abstraction stands on its own vocabulary cluster. Failing means an abstraction exists that could be folded into another without losing source-carried meaning.

#### DO

- Confirm each abstraction has vocabulary the source treats as belonging to that unit and not to another.

  **Example (pass):** Wire Transfer has `per-transaction cap`, `daily cap`, `beneficiary-jurisdiction cap` — terms the source discusses in sentences about Wire Transfer specifically, not about Funds Transfer generically.

- Fold weak candidates (rules, properties, or clusters that hang off another unit) into the parent abstraction and record the fold in `Tension:` if uncertain.

  **Example (pass):** "Reconciliation Deadline" is not its own Key Abstraction because the source only mentions it as a property of Funds Transfer — absorbed into that abstraction's Core terms.

#### DON'T

- Promote a property, rule, or configuration value to its own Key Abstraction when the source treats it as vocabulary hanging off another unit.

  **Example (fail):** `### Key Abstraction: Per-Transaction Cap` — the source only discusses this as a rule belonging to Wire Transfer; it has no independent sentences or vocabulary cluster.

- Invent an abstraction the source does not orbit — one with no dedicated sentences, no repeated noun phrase, only a mention in passing.

  **Example (fail):** `### Key Abstraction: Compliance` — the source uses the word once in a sentence about Wire Transfer caps; it has no independent vocabulary cluster.

### Rule: Verbatim source blocks trace to disk

Every ```` ```source ```` block must contain text copied byte-for-byte from a file on disk. The `Source:` line must reference a resolvable path or a known partition entry — not agent memory, training data, or generated content. Passing means every extract can be traced to a real file. Failing means a Source line uses generated-content markers or points to a non-existent file.

#### DO

- Reference real files on disk in the `Source:` line (partition file, corpus chunk, or context directory file).

  **Example (pass):** `Source: module-partitioning.md — Module: [Funds Transfer] — "Funds Transfer (overview)"`

- Copy text character-for-character from the source — preserve OCR artifacts, page numbers, whitespace, and bullet formatting.

  **Example (pass):** The ```` ```source ```` body matches the file byte-for-byte when opened.

- Stop and report to the user when no source files exist on disk rather than generating content from memory.

  **Example (pass):** Agent says "No source files found under context/ — please load source material before running this skill."

#### DON'T

- Use markers that indicate generated content: `domain-knowledge`, `application-requirements`, `training data`, `from memory`, `reconstructed`, `agent knowledge`.

  **Example (fail):** `Source: domain-knowledge — "Settlement Rules"` — no file to verify.

- Paraphrase, clean up, or reformat the source text inside ```` ```source ```` blocks.

  **Example (fail):** Agent rewrites OCR-scanned bullet points into clean markdown before placing them in the source block.

- Proceed with extract creation when the referenced file does not exist on disk.

  **Example (fail):** `Source: context/rules/ch04-transfers.md` but that file is not present in the workspace.
<!-- execute_rules:bundle_rules:end -->
