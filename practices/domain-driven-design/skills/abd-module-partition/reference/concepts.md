# Module Partition — Concepts

## What is module partitioning?

A **module** is a named region of the domain — a slice of the source the modeler intends to treat as one bounded scope in later passes. At this fidelity, a module is **only** a name + a body of source extracts; it carries **no classes, no anchors, no behavior**.

A **partition** is the assignment of every meaningful chunk of source to exactly one of:

1. A **named module** (top-level or — only when the source supports it — a sub-module of one),
2. **`Unallocated`** — text that clearly matters but whose home is undecided,
3. **`Rejected`** — text that is intentionally **out of scope** (front matter, marketing prose, settings/adventures, license, etc.).

**Partitioning is a commitment.** Each piece of source has one home. If you find yourself wanting to put the same passage in two modules, that is a **tension** — record it under the module you chose and note the alternative, or move it to `Unallocated` until a later pass resolves it.

### Hard prerequisite — source files must exist

**STOP** if there are no readable source files (corpus chunks, scanned documents, or user-supplied context files) on disk. This skill copies verbatim text from source files into module sections. If the source files do not exist, there is nothing to copy and the skill **cannot run**.

## What is — and is not — a module (DDD-grounded)

> "MODULES are a communications mechanism. The meaning of the objects being partitioned needs to drive the choice of MODULES. When you place some classes together in a MODULE, you are telling the next developer who looks at your design to **think about them together**." — Eric Evans, *Domain-Driven Design*, Ch. 5

A module in this skill is the same **MODULE** Evans describes in DDD: a named, **high-cohesion / low-coupling** region of the domain. It is **not** a heading, a feature, a single concept, or a section title in the source.

### The independence test

For any candidate boundary, ask:

> **Can a reader, modeler, or downstream pass reason about *this* slice with meaningful independence from the *other* slices — without needing to constantly cross-reference them?**

- If two clusters of source **must** be reasoned about together, they belong in **one** module.
- If a cluster can be **discussed, modified, taught, or modeled** with only an arm's-length reference to its neighbours, it earns its own boundary.

#### Standalone-mechanic test (sharper form for procedural domains)

For each *pair of mechanics* inside a candidate module, ask:

> **Can mechanic A run completely without mechanic B?**

- If yes — A and B do **not** belong in the same module.
- If no — they are the **same** mechanism in different applications, and they belong together.

### Cohesion and coupling, in practice

- **Cohesion (inside the boundary):** Every extract in the module shares a single overarching subject. The terms, rules, and invariants reinforce each other.
- **Coupling (across the boundary):** Modules will reference each other — that's fine — but the references are *named pointers*, not a shared web of intermingled rules.

### Modules are not the source's headings

A book's chapter, section, or subsection structure is **organizational scaffolding for readers**, not a domain partition. A single source heading often belongs *inside* a module. A single module often spans **multiple** source headings.

### Watch for kind-mixing

When a source heading shelves content of **multiple kinds** under one umbrella, the heading is **editorial shelving**, not a domain partition. After drafting modules, ask of each one: ***what kind of thing is this module about?*** If the answer is "more than one kind", split.

Common kinds (rough catalog):

- **Resolution** — how outcomes of uncertain operations are determined.
- **Scaling / Measure** — how trait or quantity values translate to real-world values.
- **Actor** — entities that take action.
- **Temporal structure** — billing cycle, turn, phase, sequence.
- **State vocabulary** — statuses, modes, lifecycle stages.
- **Resource economies / meta-currency** — internal currencies that gate behavior.
- **Behavior catalogs** — explicit lists of capabilities, products, or features.
- **Constraint systems** — limits, thresholds, regulatory rules.

### Modules are not single concepts — but they ARE single-kind

A module is a **collection** of related domain content of a single kind. A small, single-kind bounded scope **is** a legitimate module. A single concept that does not carry its own vocabulary or invariants is an anchor inside another module, not a module itself.

### Heuristics for naming a real module

**Single-noun rule.** If you can pick a single noun (or tight noun phrase) the source itself uses for the kind, that is the right name. If you keep reaching for compounds or generic glue, you are almost certainly trying to name a multi-kind bag — split.

### Module decisions coevolve with the model

Module boundaries are **not** final on first pass — but they are deliberately costlier to change than later artifacts. Choose conservative, well-justified boundaries now; expect them to refine as downstream skills reveal deeper structure.

## Workspace and output shape

Files produced:
- `abd-domain-driven-design/module-partition.md` — root index listing all modules
- `abd-domain-driven-design/modules/<module-name>.md` — one per module, with source file references
- `abd-domain-driven-design/modules/rejected.md` — rejected files with reasons
- `abd-domain-driven-design/modules/unallocated.md` — (optional) pending allocation decisions

### Modules — flat by default, hierarchical only when the source earns it

- **Default shape is flat.** Most corpora produce **4–10 top-level modules for the entire corpus**. If you produce more than ~10, re-apply the independence test and collapse aggressively.
- **Nest only when the source itself supports a real sub-module** — a self-contained slice that has its own bounded behavior, terminology, and extract set.
- **Do not nest just to organize.** A nested heading without its own non-trivial extract set is wrong.

### Section titles

- Each module: `## Module: [Name]` at top level. Sub-modules: `### [Name]`.
- Brackets around the name; **no** ` module` suffix.
- Reserved names: `## Module: [Unallocated]`, `## Module: [Rejected]`.

### Allocation rules

1. **Pick the module** whose scope best matches the file's primary subject.
2. **Decide whole vs partial.** Whole references allocate the entire file.
3. **Reference the source file on disk.** Every `Source:` line must point to a real file.
4. **Label.** Every reference gets a header block with locator, whole/partial, and — if partial — a clause naming which part is allocated.
5. **Stop when the file has a home.** Do not add paraphrases alongside the reference.

### Core terms — a lightweight read-out

Each module section carries a short, source-grounded **Core terms** list directly under the module heading and scope statement. Source-grounded noun phrases only, in source order. No targets, values, stereotypes, evidence IDs, or tables.

### Tensions inside an allocation

If an extract is allocated to a module but also has meaningful pull toward another, add an `Also relates to:` line in its header. This is not a second allocation — the extract still lives in exactly one section.

## Reference format

### Reference header (required for every source file)

```
**Ref — {{short title}}**
Source: {{relative_path_to_source_file}}
Locator: {{chapter / page / lines / topic}}
Extract: {{whole | partial}}
{{Part: {{which slice is relevant — required when Extract: partial}}}}
{{Also relates to: [{{other module name}}] — {{one-line why}}}}
{{Reason: {{why this lives in Unallocated or Rejected — required in those sections}}}}
```

### No verbatim copy — reference only

The reference header points to the source file; the file itself is the authoritative content. Downstream agents read the module file to learn which source files belong to the module, then read those files directly.

### One reference = one allocation

If a single source file has two unrelated parts that belong in two different modules, that is **two references** — one in each module file, each with `Extract: partial` + `Part:` line.
