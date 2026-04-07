## Role

You are the **domain modeler and OOAD practitioner** using this skill: you provide source material (specifications, code, transcripts, policy), set the active workspace, step through the 24-phase methodology (starting with workspace-and-config → domain-scan → extraction → refinement), use `scripts/drawio_cli.py` for all class diagram generation and layout, and iterate to produce a validated domain model aligned with the source material and architectural goals.


---

## Principles

# Principles

1. **Orientation before extraction** — domain-scan is observation and mapping, not yet data collection. Identify 3–7 high-confidence anchors and suspected tensions before extracting candidates.

2. **Things before data** — Model the domain's real entities, responsibilities, and relationships first. Do not invent data fields just because templates have room.

3. **Nouns → verbs → structure** — Extract domain concepts (nouns) as candidates, turn relevant verbs into operations, then build relationships and invariants that encode domain rules.

4. **Model incrementally, validate constantly** — Build the model phase by phase, consulting key scenarios and use cases at domain-scan, raw-candidate-list, add-properties-semantically-tight, smashed-abstractions-and-hidden-roles, and model-in-layers. Tensions and contradictions are signals for refinement.

5. **Diagram and Markdown stay synchronized** — Maintain both class diagram (.drawio) and Markdown documentation side-by-side. Changes to one must be reflected in the other.

6. **Domain facts trump templates** — If the source material contradicts a standard pattern or template, favor the domain truth. Document the deviation and the reason.

7. **Inheritance is a last resort** — Prefer composition and aggregation. Use inheritance only when behavior generalizes cleanly across a family of related classes.

8. **Names matter** — Refine names throughout the process. A clear, honest name reveals the model's intent; ambiguous or misleading names hide problems.

9. **Diagram CLI is non-negotiable** — Class diagrams must be created and validated using `scripts/drawio_cli.py` and the templates in `templates/`. Do not hand-write Draw.io XML or invent diagram conventions.

10. **Workspace awareness** — Always know which project workspace you are writing to. All outputs go under `<workspace>/abd-ooad/`, never to ad-hoc locations.


---

## Phase

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


---

## Library



---

### `domain-model.md`

# Domain model Markdown

This skill’s **domain model** is captured in Markdown (and optionally a parallel **Draw.io** class diagram). Use the checked-in **`templates/domain model template.md`** when starting a new companion doc; keep the same semantics as **`templates/domain model template.drawio`** when both exist.

---

## Domain concept template

Each **domain concept** (class, interface, value object, or aggregate) is documented under a clear heading, for example:

```markdown
## **Payment**

**Responsibilities:** …

### Properties
- Money amount
- …

### Operations
- initiate() → Authorization
```

From **Step 5** onward, prefer **typed** members (see **Notation evolution** below). Earlier steps stay **pre-notation** (bullets and prose).

---

## Continual refinement — class definition + diagram

**Continual refinement** means you **grow** the model across steps: each step file may add or tighten concepts. The Markdown spec and the class diagram are **two views of the same model** — update both when your project uses dual artifacts so they do not drift (see **[Class diagrams](class-diagrams.md)**).

---

## **newly added** tag

In the **worked example** threads (e.g. payments), the marker **`**newly added**`** (bold tag on a line) means: this **property** or **operation** line appears for the **first time** in *this* step’s file. Use it to see the **delta** from the previous step.

---

## Notation evolution

| Phase | Markdown style |
|--------|------------------|
| **Steps 1–4** | Informal: bullets, short phrases, responsibilities, candidate names. **No** required `- <type> property` lines yet. |
| **Step 5+** | Formal typed members: `- <Type> propertyName`, `operationName(...) → ReturnType`. |

---

## Subtype sections

When you introduce substitutable specializations, add an explicit subtype heading so the structure is visible in the spec and in diagrams:

```markdown
### **Subtype** : **PaymentMethod**
```

Put **`**newly added**`** on subtype **operation** (or property) lines when that member is **first** introduced for that subtype.

---

## Invariants

Attach invariants to the **property** or **operation** they constrain, using a dedicated line:

```markdown
**Invariant:** …
```

Mark **`**newly added**`** when you **first** attach an invariant to a given member line.

---

## Early steps: terms, mechanisms, story map

Before typed properties exist, align extracted **nouns, verbs, rules, states** with your workspace’s **terms & mechanisms** and **shaped story map** (or equivalent). That is the same “grow the model as you go” idea: informal extraction first, then formal types.

---

## Class diagram and spec (visual twin)

When you maintain a machine-readable spec such as **`map-model-spec.json`**, re-run your project’s class-diagram render script (for example **`render_map_model_class_diagram.py`**) after material changes so the **Draw.io** diagram stays the **visual twin** of the spec.

- **[Class diagrams](class-diagrams.md)** — templates, relationship types, keeping `.md` and `.drawio` aligned.  
- **[Using the Diagram CLI](using-diagram-cli.md)** — building diagrams with **`scripts/drawio_cli.py`**.

---

## Related library shards

| Topic | File |
|--------|------|
| Term tracking across steps | [term-registry.md](term-registry.md) |
| Strategy-led runs | [strategy-led-generation.md](strategy-led-generation.md) |
| Layout and lanes | [class-diagram-layout-rules.md](class-diagram-layout-rules.md) |


---

### `anchors.md`

# Anchors

An **anchor** is a module. It is the most stable, central thing you have found in the domain — the concepts you are confident will survive the entire modeling process without being renamed or restructured away.

---

## What an anchor is

An anchor is three things at once:

1. **A module frame** — a named, dashed container in the diagram that groups related classes
2. **A core class** with the same name as the frame — the primary class in that module
3. **A scope boundary** — everything inside the frame belongs to this module; everything outside relates to it via its core class

The module name, frame title, and core class name must all match. If they don't, the anchor is not yet correctly identified.

---

## The anchor test

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

---

## What an anchor is NOT

- **A chapter in the source** — a chapter is an organization of the source, not a domain concept. Multiple real anchors can come from one chapter; one chapter alone does not make an anchor.
- **A concept with a dedicated section** — many things have dedicated sections. The anchor test is structural (other anchors reference it independently), not documentary.
- **A grouping of related concepts** — if you find 3–4 concepts that are related but none of them clearly dominates, keep exploring. The anchor will be the one that the others depend on. If none dominates, record the cluster as a tension.

---

## Anchor as module — what it looks like in outputs


| Output                     | What anchor produces                                                                                                            |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `domain-scan-results.md`   | Row in the anchors table: Module name, core class name, scan-visible supporting classes, basis                                  |
| `domain-scan-model.md`     | Module section header (`## [… module]`) + **core class** with `<<Anchor>>` + other classes in that section with **no** stereotype (grouping by section is enough; no per-line `[supporting class — …]` tags). See **`phases/domain-scan` → Notation in domain-scan-model.md**.    |
| `domain-scan-model.drawio` | One dashed frame per anchor; core class inside; supporting classes inside; cross-module relationships between core classes only |
| `term-registry.md`         | Core class of a module → Classification **`anchor (class + module)`**; supporting classes → **`class`** with owning module in **Notes** (e.g. `Supporting class — Character module`). Use **Status** for lifecycle (e.g. **Tension**, **Candidate**) — not a duplicate of Classification.   |


---

## Anchors in later phases

Anchor status is not permanent. Anchors are your highest-confidence starting point, but subsequent phases will test and revise them:

- **nouns-verbs-rules-and-states (NOUNS):** All bolded and defined terms in the source are extracted. Anchors can be re-evaluated here, new candidates emerge willl challenge or subdivide existing anchor boundaries.
- **candidate-list (CANDS):** Candidates are sorted and scored. At this stage, watch for candidates that score high enough on the anchor test to be promoted — or anchors whose core class fails the independence test and should be demoted.
- **thing-vs-data-about-a-thing (THINGS):** Supporting classes inside anchor frames are evaluated here — each gets a class/property decision. If a supporting class earns class status, it may eventually warrant its own module frame in later phases.
- **All subsequent phases:** Anchors drive the backbone of the model. Relationship decisions, responsibility assignments, and inheritance structures are all organized relative to anchor modules. Changes to anchor boundaries affect the whole model — flag them explicitly in the term registry before proceeding.

---

## Incomplete anchor signal

The absence of a matching core class is the clearest signal that you have not yet found the anchor. When you encounter this situation:

1. Do not force a name — generic names produce models that are hard to reason about
2. Read the relevant chapter(s) more carefully — the anchor often has its own defined term or dedicated section
3. Ask: if another module needed to reference this cluster, what single class would it name?
4. If no single class emerges after exploration, record the cluster as a **tension** in domain-scan-results.md and defer


## Anchor as Module

An **anchor** is a module. Every anchor in the domain scan is both:

1. **A module frame** in the diagram — a named, dashed container that groups the anchor's core class and its close subordinates
2. **A core class** with the same name as the module, sitting inside that frame

This is not optional. The module name and the core class name must match. If they don't, you have a frame with a name, not an anchor.

### The core class requirement

The core class is the most important single concept in the module. It is:
- Named exactly what the module is named (e.g., module `Character` → core class `Character`)
- The thing other modules reference when they need to talk about this concept
- Identifiable by name from the source material — you should be able to point to a section that defines it

**If you cannot find a natural core class name for a cluster of related concepts, you have not found the anchor yet.** This is a signal to explore further, not to invent a placeholder name. A generic name like "Foundation", "Basics", or "Mechanics" with no matching class is an anti-pattern — it means you are grouping by chapter proximity rather than by conceptual identity.

### What to do when you find a cluster but no core class

When the scan surfaces 3–4 closely related concepts from the same chapter but none of them clearly dominates:

1. **Ask:** which concept would other modules reference by name? That one is probably the anchor.
2. **Ask:** if another module needed to point to this cluster, what would it say? The answer is the core class name.
3. **Explore the relevant chapter(s) more carefully** — do a targeted read of the section titles, defined terms, and opening paragraphs. The anchor often has its own dedicated section.
4. **You will typically get 1–2 real anchors**, not one grouped one. Separating them is usually correct.
5. If after exploration you still cannot find a core class, record the cluster as a **tension** and leave it unresolved for now — do not force an anchor.

### What an anchor module looks like in the outputs

- **Diagram:** a dashed frame labeled with the anchor name, containing the core class (same name) and any supporting classes you are confident belong to this module at scan fidelity
- **Model.md:** the module's core class listed with its fields and the names of supporting classes noted inside it
- **Term registry:** the core class row has Classification = `anchor (class + module)`; supporting classes inside the frame have Classification = `class` with a note naming the module they belong to (**Status** tracks Ambiguous / Tension / Candidate / etc.)

### Initial model sketch

After the scan, before producing files:

- **Name each anchor module:** one-line responsibility statement from the source — do not invent
- **Identify the core class:** confirm it has a name you can point to in the source
- **Identify supporting classes:** 0–3 classes that clearly belong inside the same frame at this fidelity level
- **Do not add detail:** if you only know a class name and broad responsibility from the scan, the sketch only contains that — do not fill in properties, methods, or relationships you haven't confirmed

**CRITICAL CONSTRAINT:** The diagram must match the sketch fidelity exactly. If the sketch has 4 anchor modules with their core classes only, the diagram has 4 frames each containing one core class.

### Anchor module rule

Every anchor gets:
- A core class with the same name (the most important concept in the module)
- A dashed frame enclosing the core class and any supporting classes that clearly belong at this fidelity level
- Fields on the core class for concepts you found but have not yet decided are classes vs. properties

> Core class gets the frame. Supporting classes that are confident enough go inside the frame. Everything else is a field on the core class — evaluated in `thing-vs-data-about-a-thing`.

Example: `Character` module has a `Character` core class with `abilities: AbilitySet` as a field. If `Ability` is clearly its own class at this fidelity, it goes inside the Character frame as a supporting class. If uncertain, it stays as a field.


---

### `strategy-led-generation.md`

# Strategy-led generation

Domain scan (OOAD **phase 1**) does not only produce a single “results” file. It establishes a **small set of workspace files** under `<workspace>/abd-ooad/` that work together. Some are **frozen findings** from the scan; others are **living documents** you update as modeling continues.

**Slices start at global Phase 2:** Source-slice work (e.g. **S1**, **S2** in `strategy.md` and **`Anchor`** `S1=…` / `S2=…` in `term-registry.md`) uses the **same global OOAD phase numbers** as the process table for everything **after** scan. The **first** per-slice extraction step is **Phase 2** (`nouns-verbs-rules-and-states`), **not** a slice-local “Phase 1.” Phase **1** is workspace-wide **domain-scan** only. See **`term-registry.md` → Slices and global phase numbers**.

For the scan procedure itself, see the **Domain scan** phase. This page explains **what each artifact is for** and how **`strategy.md`** relates to **`domain-scan-results.md`**.

**Checkbox discipline:** Live ticks for pipeline position and phase steps belong only under **`<workspace>/abd-ooad/progress/`** — see **`library/strategy-execution-and-checklists.md`**. Do not put tick tables in `strategy.md`.

---

## The five scan outputs (always)

Created during domain scan under `<workspace>/abd-ooad/`:

| File | Role | Updates after scan? |
|------|------|---------------------|
| `domain-scan-results.md` | **Findings snapshot:** source map, anchor table, tensions. | Rarely — only if you correct a scan error. Do not put the forward plan here; that belongs in `strategy.md`. |
| `strategy.md` | **Living strategy:** **modeling scope**; **§1 source slices** (table: Order, Goal, **Source** — chapters, files, modules, or mixed — **Coverage**, **Importance**); **§2 slice plan** (per-slice **goal restated** + **phases**); **coverage across steps**; **cross-slice integration**; **anchor and subdomain elaboration**; **execution plan (normative)** — phase slugs with **slice IDs** on every line; plus **approach** and **dated pivots**. | **Yes** — whenever scope, order, slice depth, subdomain mapping, or integration changes. |
| `domain-scan-model.md` | Class sketch (markdown) at scan fidelity. | Yes, in later phases — not only during scan. |
| `domain-scan-model.drawio` | Diagram at scan fidelity. | Same as model.md. |
| `term-registry.md` | Terms, **Classification** (model role), **Status** (OOAD scale), confidence — seeded at scan. | **Yes** — every later phase updates Step, Classification, and Status as the model evolves. |

**Plus** (when workspace is configured): **`progress/`** checklists — see **`library/strategy-execution-and-checklists.md`**. **`generate.py`** creates **`process-checklist.md`**, **`<phase>-checklist.md`**, and (abd-ooad) **`strategy-run-checklist.md`** when templates exist and files are missing. Normative phase steps stay in **`content/parts/phases/<phase>.md`**. These are the **only** place for session tick marks.

Walkthrough diagrams (`.md` / `.drawio`) are **not** required at scan fidelity; they start when the skill’s later phases call for them.

---

## What `strategy.md` is for

- Created at the end of domain scan as a **workspace file**, then **kept current** through extraction and later phases.
- **Purpose:** (1) **scope** — what product or corpus you model; (2) **§1 source slices** — ordered table (**Goal**, **Source**, **Coverage**, **Importance**); **Source** is any locator (chapters, page ranges, repo paths, modules — not only document sections); (3) **§2 slice plan** — per slice, **goal restated** and **phases** (execution steps); (4) **coverage across steps** — matrix proving every in-scope slice is addressed or deferred; (5) **cross-slice integration** — handoffs between slices; (6) **anchor and subdomain elaboration** — attached types (e.g. Ability, Skill, Advantage) mapped to **slice IDs** and execution **§**; (7) **execution plan** — each line names **slice IDs**; breadth steps must **include** subdomain slices in **nouns-verbs** / **raw-candidate-list** where relevant; (8) **Approach** + **Ongoing strategic decisions**. Scan mechanics stay in **`domain-scan-results.md`**.
- **Template:** `templates/strategy.md`. Install as **`strategy.md`** (lowercase; avoid duplicate `STRATEGY.md` on case-insensitive disks).
- After you finalize the execution plan, align **`progress/strategy-run-checklist.md`** with it (same phases and scope); that file holds **checkboxes** for “which phase is done,” while **`strategy.md`** stays **normative text** (no `- [ ]`).

---

## Checklist vs results vs strategy

| Question | Answer |
|----------|--------|
| Where is the source map and anchor list? | `domain-scan-results.md` |
| Where do I define **which slices** exist (chapters, files, modules, …), **depth**, **subdomains per anchor**, and **which phases** hit which? | `strategy.md` → **§1 Source slices**, **§2 Slice plan**, **Coverage across steps**, **Cross-slice integration**, **Anchor and subdomain elaboration**, **Execution plan (normative)** |
| Where do I tick **which phases** we ran, **in order**, with **scope**? | **`abd-ooad/progress/strategy-run-checklist.md`** (keep in sync with `strategy.md`) |
| Where do I tick **full** pipeline position (all phases)? | **`abd-ooad/progress/process-checklist.md`** (optional reference) |
| Where do I tick **steps inside** the current phase? | **`abd-ooad/progress/<phase>-checklist.md`** |
| Where do I tick domain-scan action steps? | **`abd-ooad/progress/domain-scan-checklist.md`** |
| Can I merge checklist into strategy? | **No** — strategy holds the plan; ticks only under **`progress/`** |

---

## Going forward (phases after scan)

1. **Strategy** — Keep **`strategy.md`** aligned with reality; append *Ongoing strategic decisions* when you pivot.
2. **Strategy execution** — Tick **`progress/strategy-run-checklist.md`** as you **complete** each phase for its declared scope.
3. **Phase work** — For the active phase, run **`generate.py --phase <slug>`** and tick **`progress/<slug>-checklist.md`** for action steps.
4. **Registry** — Keep `term-registry.md` aligned with the current phase (Step, Classification, Status).
5. **Results** — Touch `domain-scan-results.md` only for corrections to the original scan snapshot.

---

## References

- Templates: `templates/domain-scan-results.md`, `templates/strategy.md`, `templates/strategy-run-checklist.md`
- Strategy vs checklists: **`library/strategy-execution-and-checklists.md`**
- Anchors: `anchors` in this library
- Term registry: `term-registry` in this library
- Checklist norm: `library/strategy-execution-and-checklists.md`


---

### `strategy-execution-and-checklists.md`

# Strategy execution and checklists (abd-ooad)

**Canonical doc** for: (1) **strategy** vs **live ticks**, (2) **which files** hold checkboxes, (3) **how** `generate.py` creates workspace **`progress/`** files. Does **not** replace **[process.md](../process.md)** (process tables, `generate` / `build`) or **[skill-structure-and-concepts.md](../base/skill-structure-and-concepts.md)** (repo layout).

Only **`strategy.md`** defines **scope** and **which phases in what order**; checklists are where you **tick** progress.

---

## Workflow

1. **Domain scan** — produce scan artifacts (see **`strategy-led-generation`**).
2. **Strategy** — fill **`strategy.md`** from **`templates/strategy.md`**:
   - **Modeling scope** — corpus or product boundary; **source type** (book vs repo vs mixed).
   - **§1 Source slices** — ordered table: **Goal**, **Source** (chapters, files, modules, APIs — whatever locates work), **Coverage** (depth this pass), **Importance**; stable **slice IDs** reused everywhere.
   - **§2 Slice plan** — per slice: **goal restated**, **unit kind**, **phases** (execution step numbers / slugs), produces, depends-on.
   - **Coverage across steps** — matrix: every slice → which **execution plan** steps touch it → **depth** → deferrals.
   - **Cross-slice integration** — cross-boundary types and ordering (From → To + narrative).
   - **Anchor and subdomain elaboration** (when anchors have attached types) — map subdomains to slices and execution §.
   - **Execution plan (normative)** — ordered phase **slugs**; **each line cites slice IDs** (mirror **`strategy-run-checklist.md`**).
   - **Approach going forward** + **Ongoing strategic decisions** — short narrative and dated pivots.
3. **Align live checklists** — keep **`strategy-run-checklist.md`** in sync with the execution plan (same order and scope). Optional **`templates/strategy-run-checklist.md`** seed; optional **`templates/progress-README.md`** → **`progress/README.md`** for slice-specific files under **`progress/slices/`**.
4. **Run phases** — for the **current** phase: `python scripts/base/generate.py --phase <slug>`. Tick **`strategy-run-checklist.md`** when a phase is **done** for its declared scope; tick **`<slug>-checklist.md`** for **steps inside** that phase.

---

## Three layers (what you tick)

| Layer | File | What you tick |
| --- | --- | --- |
| **Strategy execution** | **`progress/strategy-run-checklist.md`** | **Which phases** you will run, **in order**, each with **scope** that **includes the same slice IDs** as **`strategy.md` → Execution plan**. Optional: **`progress/slices/<slice-id>-checklist.md`** per slice — see **`progress/README.md`** in the workspace (if present). |
| **Full pipeline (reference)** | **`progress/process-checklist.md`** | **Every** phase in **`phase_files`** — useful as a map; optional if you rely only on strategy-run. |
| **Phase steps** | **`progress/<phase>-checklist.md`** | **Action checklist** copied from **`content/parts/phases/<phase>.md` → ## Action Checklist**. |

**Implementation:** **`scripts/base/workspace_checklists.py`** (paths, behavior, `--no-ensure-checklists`).

---

## How workspace checklist files are created (mechanical)

| Kind | What it tracks | Where it lives | How it gets there |
| --- | --- | --- | --- |
| **Normative reference** | Rules in **this document** — strategy vs ticks, layers, `generate.py` behavior | **`content/parts/library/strategy-execution-and-checklists.md`** | Authored in the skill; **not** created by **`generate.py`**. |
| **Pipeline position** | Which **phase** of the pipeline you are in | **`<active_skill_workspace>/<skill_name>/progress/process-checklist.md`** | **Created** on first **`python scripts/base/generate.py --phase <slug>`** when that file is **missing**, if **`skill-config.json` → `workspace.active_skill_workspace`** is set. One `- [ ]` line per slug in **`phase_files`** (labels from **`phase_section_headings`** when present). **Does not overwrite** an existing file. |
| **Phase action steps** | **Steps inside** the current phase | **`<active_skill_workspace>/<skill_name>/progress/<phase-slug>-checklist.md`** | **Created** in the **same** `generate.py` run when that file is **missing**. Steps are taken from **`## Action Checklist`** in **`content/parts/phases/<phase-slug>.md`**, or from task lines (`- [ ]` / `- [x]`) in that file if the section is absent. **Does not overwrite** an existing file. |
| **Strategy execution** (workspace) | Ordered phases matching **`strategy.md`** | **`progress/strategy-run-checklist.md`** | Seeded from template when **`generate.py`** / workspace checklist logic creates it; **you** align it with **`strategy.md`**. |

### Names and workspace

- **`skill_name`** — **`skill-config.json` → `name`** (fallback: skill directory name). Used in **`…/<skill_name>/progress/`**.
- **`active_skill_workspace`** — Must point at the **project / engagement tree** where **`progress/`** checklists belong, **not** the skill install folder. See **`skill-config.json` → `workspace`** and **[workspace-and-config.md](phases/workspace-and-config.md)**.

### Flags

- **`python scripts/base/generate.py --phase <slug> --no-ensure-checklists`** — run the phase prompt **without** creating missing **`progress/`** checklist files (see **`workspace_checklists.py`**).

---

## What not to do

- Do not put **checkboxes** in **`strategy.md`** — keep execution plan as **normative numbered/bulleted text**; ticks live under **`progress/`**.
- Do not record pipeline or phase **session** progress by ticking boxes in **`content/parts/process.md`** or **`content/parts/phases/*.md`** — those stay **normative**; live ticks go **only** under **`…/progress/`**.
- Do not let **`strategy-run-checklist.md`** drift from **`strategy.md`** — after a pivot, update both and append a line under *Ongoing strategic decisions*.

---

## Phase slugs

Use exact slugs from **`skill-config.json` → `phase_files`** (e.g. `nouns-verbs-rules-and-states`, `domain-scan`). Labels for humans are in **`phase_section_headings`**.

---

## References

- **`strategy-led-generation.md`** — artifact roles, **`strategy.md`** vs **`domain-scan-results.md`**
- **`templates/strategy.md`**, **`templates/progress-README.md`**
- **`scripts/base/workspace_checklists.py`**


---

### `term-registry.md`

# Term Registry

## What a Term Is

A **Term** is any concept identified from the source material that may become part of the domain model. At the time of identification, a Term is not committed to a model role — it might become a class, a property, a value type, an association, or nothing at all. The registry tracks Terms as the modeling phases determine what each one actually is.

This is distinct from other uses of "actor" in this domain:
- In MM3E and FoundryVTT, "Actor" has a specific system meaning (a character, creature, or entity in the game world).
- In the registry, everything is a Term until the model says otherwise.

**File:** `<workspace>/abd-ooad/term-registry.md`
**Never embedded** inside step outputs — it lives in its own file and is referenced from each step's model doc.

---

## Step Reference — Short Names

Use these short names in the **Step** column of the registry when adding or updating a row.

| Short Name | Phase | Description |
|-----------|-------|-------------|
| SETUP | workspace-and-config | Workspace initialization |
| SCAN | domain-scan | Source scan and anchor identification |
| NOUNS | nouns-verbs-rules-and-states | Extract nouns, verbs, rules, states |
| CANDS | raw-candidate-list | Raw candidate class list |
| THINGS | thing-vs-data-about-a-thing | Separate things from data-about-things |
| RESP | responsibilities-before-operations | Assign responsibilities |
| PROPS | add-properties-semantically-tight | Add semantically tight properties |
| OPS | turn-verbs-into-operations | Turn verbs into operations |
| RELS | relationships-and-cardinality | Relationships and cardinality |
| INV | invariants-in-the-model | Identify invariants |
| BLOAT | watch-for-bloated-classes | Detect bloated classes |
| ROLES | smashed-abstractions-and-hidden-roles | Uncover hidden roles |
| INHERIT | inheritance-when-behavior-generalizes | Apply inheritance |
| ABST | abstract-classes-and-interfaces | Abstract classes and interfaces |
| COMP | prefer-composition | Prefer composition over inheritance |
| STATES | model-state-transitions | Model state transitions |
| ITER | iterative-refinement | Iterative refinement pass |
| TENSION | tension-as-a-signal | Resolve tensions |
| COHESION | what-changes-together | What changes together |
| VALIDATE | validate-with-scenarios | Validate with scenarios |
| NAMES | refine-names | Refine class and concept names |
| LAYERS | model-in-layers | Model in layers |

---

## Slices and global phase numbers (normative)

The **OOAD process table** (see **`process.md`** / built **AGENTS.md** — “Process Table”) assigns **global phase numbers** **0–21** to phase **slugs** (e.g. **Phase 2** = `nouns-verbs-rules-and-states`, **Phase 3** = `raw-candidate-list`, **Phase 4** = `thing-vs-data-about-a-thing`).

- **Phase 1** (`domain-scan`, short name **SCAN**) runs **once per workspace** (or once per strategy engagement). It produces anchors, `strategy.md`, `domain-scan-results.md`, and seeds **`term-registry.md`**. It is **not** repeated as “each slice’s Phase 1.”
- **Per-slice modeling** (folders or **Anchor** columns **`S1=…`**, **`S2=…`**, …) **aligns with the same global numbers from Phase 2 onward:** the **first** extraction artifact in a slice is always **Phase 2** (**NOUNS**), then **3** (**CANDS**), **4** (**THINGS**), etc. Do **not** label slice-local nouns-verbs files as Phase 1 — that collides with **SCAN**.
- **Phase notes** in italics (optional): `*[Sn · Phase N]*` where **N** is the **global** process-table number. Add slug, tension id, or short reminder *after* the tag on the same line if needed (e.g. *thing-vs-data*, *registry Tn*). For early “likely class” judgments: `*[S1 · Phase 3]* Likely class : …`.

---

## Registry Columns

| Column | Values | Notes |
|--------|--------|-------|
| **Term** | Concept name from the source | Exact word or phrase as found — rename in the NAMES step if needed |
| **Classification** | See **Classification** below | **What we want to model this as** — target shape in the domain model (not lifecycle) |
| **Step** | Short name from table above (SCAN, NOUNS, …) | Step that first identified or last materially updated this Term |
| **Confidence** | High / Medium / Low | How sure we are this belongs in the model |
| **Status** | See **Status (OOAD scale)** below | Where this Term sits in the modeling workflow |
| **Notes** | Free text | Anchor-test results, owning module for supporting classes (`Supporting class — X module`), competing interpretations, pointers to tensions in `domain-scan-results.md`, and follow-ups |

---

## Classification — what we want to model this as

Use **one** value per row. This is the **intended model role**, not how “mature” the idea is (that is **Status**).

| Value | Meaning |
|--------|---------|
| **anchor (class + module)** | Passes the anchor test: this concept is a **core class** and owns a **module** (dashed frame + same-named core class). Use only for backbone modules. |
| **class** | A domain **class** that is not its own module yet — e.g. supporting class inside a frame, or a type you expect to become a class without its own module. |
| **property** | Modeled as a **semantic property** (attribute / value on a class), not a separate type. |
| **field** | Modeled as a **typed field / slot** (data member, possibly simple type or value object). |
| **example (instance)** | An **illustrative instance**, sample, or scenario object — not a type in the model. |
| **relationship** | An **association**, link, or dependency between concepts — may become an association, association class, or navigable role. |
| **invariant (rule)** | A **domain rule**, constraint, or policy — often becomes behavior, guard, or explicit rule text on a class. |

**Diagram mapping (when relevant):** `anchor (class + module)` → module frame + core class; `class` → class box; `relationship` → association; `invariant (rule)` → note, constraint, or operation; `property` / `field` → attributes on a class.

---

## Status (OOAD scale)

**Status** is **lifecycle / confidence in the workflow**, not the model shape. Pick the value that best fits; states are **not** always a strict left-to-right pipeline.

| Status | When to use |
|--------|-------------|
| **Ambiguous** | You cannot yet say what the Term is or how it sits next to others. |
| **Tension** | Competing interpretations, overlapping boundaries, or conflicting source pulls — needs resolution before the model can commit. |
| **Candidate** | Plausible model role; narrowed but not yet locked (often after scan, before THINGS/RELS). |
| **Deferred** | Explicitly parked — revisit in a named later step or phase. |
| **Active** | In current modeling scope; being updated in this pass. |
| **Solidified** | Named, placed, and stable in the model for the current iteration — ready to treat as “done” unless source or scope changes. |

**Typical (non-binding) progression:** Ambiguous → Tension or Candidate → Active → Solidified. **Deferred** can apply after any stage. A Term can return from Deferred to Active when scope returns to it.

---

## Registry format (wide Notes)

**Prefer an HTML `<table>` with `<colgroup>`** so the **Notes** column gets most of the width (~50–55%). **Classification** labels can be long — give that column ~12–14% if needed. Plain Markdown pipe tables allocate columns evenly and make long Notes hard to read in the editor and in preview.

Use this skeleton (adjust `width` percentages if needed):

```html
<table>
<colgroup>
  <col style="width:9%" />
  <col style="width:14%" />
  <col style="width:6%" />
  <col style="width:9%" />
  <col style="width:9%" />
  <col style="width:53%" />
</colgroup>
<thead>
<tr>
  <th>Term</th>
  <th>Classification</th>
  <th>Step</th>
  <th>Confidence</th>
  <th>Status</th>
  <th>Notes</th>
</tr>
</thead>
<tbody>
<tr>
  <td>Character</td>
  <td>anchor (class + module)</td>
  <td>SCAN</td>
  <td>High</td>
  <td>Active</td>
  <td>Central entity; all rules attach to it</td>
</tr>
<tr>
  <td>Power</td>
  <td>class</td>
  <td>SCAN</td>
  <td>High</td>
  <td>Active</td>
  <td>Supporting class — Character module. Core capability unit.</td>
</tr>
<tr>
  <td>Device</td>
  <td>class</td>
  <td>SCAN</td>
  <td>Medium</td>
  <td>Tension</td>
  <td>Removable Power vs Equipment? Boundary unclear — see T2.</td>
</tr>
</tbody>
</table>
```

For very small registries only, a Markdown pipe table is acceptable:

```markdown
| Term | Classification | Step | Confidence | Status | Notes |
|------|----------------|------|------------|--------|-------|
| Character | anchor (class + module) | SCAN | High | Active | Short note only |
```


---

### `using-diagram-cli.md`

# Using the Diagram CLI

## The Rule

**All class diagrams must be created and maintained using `scripts/drawio_cli.py`.**

Do not hand-write `.drawio` XML. Do not create ad-hoc rectangle layouts. The CLI produces proper UML swimlane class components with separate sections for name, fields, and methods — matching the `templates/domain model template.drawio` visual standard.

---

## Diagram Build Routine

Every class diagram is built from the `.md` companion file. The `.md` is always created first and is the authoritative record. The diagram is then derived from it, component by component.

### Step 1 — Read the MD file line by line

Before writing a single CLI command, read the entire `.md` companion and extract:
- Every class name and its stereotype
- Every **scalar field** (primitive type, not a reference to another class)
- Every invariant `{ }` line
- Every multi-valued reference (these become arrows, NOT diagram fields)
- Every single-valued reference to another class (also an arrow)

**Diagram fields = scalars + invariants only.** Any field whose type is another class in the model must become a relationship arrow. Do not add it as a text field in the diagram — it is already represented by the arrow.

### Step 2 — Add each class one at a time

For each class:
1. `add-class <Name> --stereotype <phase>` — stereotype goes in the class header, not as a field row
2. Add only scalar fields: `add-field <Name> "+ fieldName: PrimitiveType"`
3. Add invariants: `add-field <Name> "{ constraint text }"` — these will be post-processed to taller cell heights
4. After each class, check the class rendered correctly before moving to the next

**Stereotype rule:** Always use `--stereotype scan` (or the current phase) on `add-class`. Never add `<<scan>>` as a separate field row — this causes it to render as `<>` because draw.io HTML interprets `<scan>` as an HTML tag.

**Type completeness rule:** Every type referenced in a field must have a class in the diagram. If `Character` has `powers: Power [0..*]`, then `Power` must be drawn as a class. There are no phantom types — if it appears in a field, it exists in the model.

### Step 3 — Post-process constraint cell heights

After all classes are added, run the height fixup:
```python
for cell in root.iter('mxCell'):
    val = cell.get('value', '')
    if val.startswith('{'):
        geom = cell.find('mxGeometry')
        if geom is not None:
            geom.set('height', '52' if len(val) <= 60 else '78')
```

### Step 4 — Add module frames

Run `add-frame` for each module, listing all member classes. Frames must be added AFTER all classes.

### Step 5 — Add relationships

For each relationship identified in Step 1:
- Composition: `add-composition Whole Part --mult "n..*"` — multiplicity goes at the **part** (many) end, near the part class
- Association: `add-association From To --label "name" --to-mult "0..*"`
- Dependency: `add-dependency From To --stereotype "label"`

Cross-module relationships connect core classes only (not frames). Before drawing any cross-module arrow, confirm there is a field on the source class that references the target — see `class-diagrams` → "Associations Require a Connecting Field".

### Step 6 — Verify and fix layout

```bash
# Fix edge styles first (V3/V4)
python scripts/drawio_cli.py fix-edge-styles --file <output>.drawio

# Fix shared connection points (V5) — always run after adding relationships
python scripts/drawio_cli.py fix-shared-endpoints --file <output>.drawio

# Fix arrow-class overlaps (V6) — routes edges around classes they cross
python scripts/drawio_cli.py fix-arrow-overlaps --file <output>.drawio

# Verify — check all rules V1–V6
python scripts/drawio_cli.py verify --file <output>.drawio
```

The `fix-shared-endpoints` command detects classes where 2+ edges arrive or
leave without explicit `entryX/Y` / `exitX/Y` constraints. It determines the
dominant approach side (top / bottom / left / right) and distributes port
coordinates evenly so arrowheads no longer pile up.

The `fix-arrow-overlaps` command detects edges whose straight-line path passes
through an unrelated class body (V6). It automatically inserts 1–2 waypoints to
route the edge around all obstacles, using a recursive shortest-path algorithm
with up to 2 bypass points. V4 info messages about explicit waypoints on
previously-fixed edges are expected and can be ignored.

After verify, address any remaining warnings:

| Code | Severity | Meaning | Action |
|------|----------|---------|--------|
| V1 | ERROR | Class bounding boxes overlap | `relayout` |
| V2 | ERROR | Subclass above superclass | `relayout` |
| V3 | WARN | Wrong edge style for relationship type | `fix-edge-styles` |
| V4 | WARN | Explicit waypoints on orthogonal edges | `fix-edge-styles` |
| V5 | WARN | 2+ edges share unconstrained connection point | `fix-shared-endpoints` |
| V6 | WARN | Straight edge passes through unrelated class | `fix-arrow-overlaps` |

Then run the frame containment check (Python XML script) to confirm all classes are inside their frames.

### Step 7 — AI layout pass

The programmatic build will produce correct structure but imperfect visual routing. After running verify (with 0 errors), open the diagram and inspect for:
- Labels obscured by other elements (drag to clear space)
- Any class that is outside its frame boundary (fix with `add-frame` or XML edit)
- Any remaining V6 warnings after `fix-arrow-overlaps` — move the blocking class manually as a last resort

`fix-arrow-overlaps` automatically routes edges around any class they pass through, inserting 1–2 waypoints using a recursive shortest-path algorithm. Re-run it if V6 warnings remain after the initial fix.

---

### Standard workflow (single classes, no modules)

Every class diagram follows this sequence:

```
new → add-class (×N) → add-field (×N) → add-method (×N) → add-relationships → fix-edge-styles → fix-shared-endpoints → fix-arrow-overlaps → verify
```

```bash
# 1. Create the diagram file
python scripts/drawio_cli.py new --file <workspace>/abd-ooad/<output>.drawio

# 2. Add each class (use --x/--y to set explicit 2D positions — never rely on relayout alone)
python scripts/drawio_cli.py add-class <ClassName> --x <n> --y <n> --file <output>.drawio

# 3. Add fields to classes
python scripts/drawio_cli.py add-field <ClassName> "+ <name>: <Type>" --file <output>.drawio

# 4. Add methods to classes
python scripts/drawio_cli.py add-method <ClassName> "+ <name>(<param>: <Type>): <ReturnType>" --file <output>.drawio

# 5. Add relationships (choose the right type)
python scripts/drawio_cli.py add-composition <Whole> <Part> --mult <n> --label "<label>" --file <output>.drawio
python scripts/drawio_cli.py add-aggregation <Whole> <Part> --file <output>.drawio
python scripts/drawio_cli.py add-association <From> <To> --label "<label>" --from-mult "<m>" --to-mult "<n>" --file <output>.drawio
python scripts/drawio_cli.py add-inheritance <Subclass> <Superclass> --file <output>.drawio
python scripts/drawio_cli.py add-dependency <From> <To> --stereotype "<label>" --file <output>.drawio

# 6. Fix edge styles, spread shared endpoints, fix overlaps, then verify
python scripts/drawio_cli.py fix-edge-styles --file <output>.drawio
python scripts/drawio_cli.py fix-shared-endpoints --file <output>.drawio
python scripts/drawio_cli.py fix-arrow-overlaps --file <output>.drawio
python scripts/drawio_cli.py verify --file <output>.drawio
```

---

### Module/anchor workflow (domain-scan — anchors as modules)

When the diagram represents anchor modules (domain-scan phase), each anchor needs a **dashed frame** enclosing its core class and any supporting classes. The module name = the frame title = the core class name.

```
new → add-class (core classes + supporting classes) → add-field → add-frame (×N, one per module) → add-relationships → fix-edge-styles → fix-shared-endpoints → fix-arrow-overlaps → verify
```

```bash
# 1. Create the diagram file
python scripts/drawio_cli.py new --file <workspace>/abd-ooad/<output>.drawio

# 2. Add ALL classes first (core + supporting), with explicit positions
#    Core classes positioned first; supporting classes near their core class
python scripts/drawio_cli.py add-class <CoreClass> --x <n> --y <n> --file <output>.drawio
python scripts/drawio_cli.py add-class <SupportingClass> --x <n> --y <n> --file <output>.drawio

# 3. Add fields to core classes
python scripts/drawio_cli.py add-field <CoreClass> "<<scan>>" --file <output>.drawio
python scripts/drawio_cli.py add-field <CoreClass> "+ <field>: <Type>" --file <output>.drawio

# 4. Add module frames (AFTER all classes are in the diagram)
#    Frame name = anchor/module name = core class name
python scripts/drawio_cli.py add-frame "<ModuleName>" --classes "<CoreClass>,<SupportingClass1>" --file <output>.drawio

# 5. Add relationships BETWEEN modules (core-class to core-class)
python scripts/drawio_cli.py add-composition <CoreA> <CoreB> --file <output>.drawio
python scripts/drawio_cli.py add-dependency <CoreA> <CoreB> --stereotype "<label>" --file <output>.drawio

# 6. Fix edge styles, spread shared endpoints, fix overlaps, then verify
python scripts/drawio_cli.py fix-edge-styles --file <output>.drawio
python scripts/drawio_cli.py fix-shared-endpoints --file <output>.drawio
python scripts/drawio_cli.py fix-arrow-overlaps --file <output>.drawio
python scripts/drawio_cli.py verify --file <output>.drawio
```

**Important rules for module frames:**
- `add-frame` must be called AFTER all classes are in the diagram
- Frame title must match the core class name exactly
- Do NOT call `relayout` after `add-frame` — relayout ignores frame membership and will scatter classes outside their frames
- Cross-module relationships always connect core classes, never the frames themselves
- A frame with no matching core class = an incomplete anchor identification (explore further)

**Describe / inspect:**
```bash
python scripts/drawio_cli.py describe --file <output>.drawio
python scripts/drawio_cli.py list-classes --file <output>.drawio
python scripts/drawio_cli.py show-class <ClassName> --file <output>.drawio
```

**Inline invariants** — add as a field entry with curly braces (brief, one-line constraints):
```bash
python scripts/drawio_cli.py add-field <ClassName> "{ invariant text }" --file <output>.drawio
```
Example: `add-field Check "{ result = d20 + modifier; succeeds if result >= dc }"`

**Note invariants** (longer — multiple lines): the CLI does not support notes. Add manually in draw.io after CLI build: Insert → Shape → Note, enclose text in `{ }`, connect to class with a dashed line. See `class-diagrams` in this library for full invariant guidance.

---

## Domain Realization (Sequence) Diagram — Workflow

Sequence/walkthrough diagrams use the checked-in template rather than the CLI:

```bash
# 1. Duplicate the template
cp "templates/domain realization template.drawio" <workspace>/abd-ooad/<output>.drawio

# 2. Edit the .drawio file to replace placeholder lifelines, messages, and notes
#    with the actual actors and interactions from the walkthrough

# 3. Create the companion markdown
cp "templates/domain walkthrough template.md" <workspace>/abd-ooad/<output>.md
#    Fill in the scenario description, step-by-step walkthrough, and notes
```

---

## Markdown Companion — Always Paired

Every `.drawio` class diagram has a `.md` companion. Use `templates/domain model template.md` as the starting structure:

```
<ClassName> : <BaseClass>
+ <property>: <Type>
     opt  <CollaboratingClass>, ...
      Invariant: <constraint>
+ <method>(<param>: <Type>): <ReturnType>
      <CollaboratingClass>, ...
      Invariant: <constraint>
-----
```

Keep both files in sync — when you add a class to the `.drawio`, add the same class to the `.md` in the same pass.

---

## Per-Phase Diagram Rules

| Phase | What to Show | Properties | Methods | Relationships |
|-------|-------------|------------|---------|---------------|
| domain-scan | Anchor modules: one dashed frame per anchor, core class inside frame + confirmed supporting classes | Scan-identified fields on core class only | None | High-confidence only, between core classes |
| nouns-verbs → raw-candidate-list | Candidates added | None | None | Structural only |
| responsibilities → turn-verbs-into-operations | All confirmed classes | Semantic properties | Confirmed methods | All known |
| relationships → model-state-transitions | Refined model | Full | Full | Full with cardinality |
| iterative-refinement → model-in-layers | Final layered model | Full | Full | Full |

**Domain-scan constraint:** The diagram fidelity must match the sketch exactly. One frame per anchor module. Core class inside each frame has the same name as the frame. If you cannot find a core class for a frame, the anchor is incomplete — explore further before drawing.

---

## Relationship Type Guide

| Relationship | Command | When to Use |
|-------------|---------|-------------|
| Composition | `add-composition` | WHOLE owns PART; PART cannot exist without WHOLE |
| Aggregation | `add-aggregation` | WHOLE references PART; PART exists independently |
| Association | `add-association` | General directed relationship between two classes |
| Inheritance | `add-inheritance` | IS-A — subclass extends superclass |
| Dependency | `add-dependency` | Uses or creates — ephemeral, not structural |

---

## Templates Reference

| Template | Path | Use for |
|----------|------|---------|
| Class diagram (Draw.io) | `templates/domain model template.drawio` | All class structure diagrams |
| Class diagram (Markdown) | `templates/domain model template.md` | All class diagram companions |
| Walkthrough (Draw.io) | `templates/domain realization template.drawio` | Sequence/realization diagrams |
| Walkthrough (Markdown) | `templates/domain walkthrough template.md` | Walkthrough narrative companions |

**Never** create a class diagram without using the CLI. **Never** create a walkthrough without using the realization template. These conventions encode the visual and structural standards for the domain model.

---

See also: `class-diagrams.md`, `class-diagram-layout-rules.md`, `sequence-diagrams.md`, `sequence-diagram-layout-rules.md` in this library for full rules on layout, edge styles, and verification codes.


---

### `class-diagrams.md`

# Class Diagrams (Draw.io and Markdown)

## Templates — use these for every create/update

All class-structure work should **start from** or **stay aligned with** the checked-in templates under the skill **`templates/`** folder (paths relative to the skill root):

| Role | Template file | When to use it |
|------|----------------|----------------|
| **Draw.io** | `templates/domain model template.drawio` | **New diagram:** duplicate this file into the workspace, rename, then edit. **Existing diagram:** when adding classes or relationships, keep the same swimlane style, member layout, and collaborator-line conventions as the template. |
| **Markdown** | `templates/domain model template.md` | **New companion doc:** copy structure and headings from this file. **Updates:** when you change the `.drawio` or the `.md`, update the **other** artifact in the same pass and preserve the template’s patterns (classes, `opt` collaborators, `Invariant:` lines). |

Do **not** invent a one-off Markdown shape or Draw.io layout for class models unless the user explicitly opts out — the templates encode Jeff’s notation (collaborators on the second line in Draw.io, matching `opt` / invariants in Markdown).

**CLI:** New diagrams can be created with `scripts/drawio_cli.py`; even then, prefer matching the **visual and structural** conventions of `domain model template.drawio` (or duplicate the template and extend it) so `verify` / layout rules apply cleanly.

## What to keep in sync

When the user asks to **create or update** modeling diagrams:

| Artifact | Draw.io | Markdown companion |
|----------|---------|-------------------|
| **Class structure** | `*.drawio` (see template above; CLI: `drawio_cli.py`) | Same structure and semantics as `templates/domain model template.md` |

**Rule:** If both files exist for a topic, **update both** in the same pass so comments and collaborator lists do not drift. If only one exists, create the missing companion **from the templates** unless the user opts out.

**Speech-to-text note:** “Vast diagram” or “Lost diagram” in informal notes usually means **class diagram**.

## Class diagram — parallel “comments”

Jeff’s style embeds **collaborators** (and optionally **invariants**) next to fields and methods:

- In **Draw.io**, that is the second line in the member cell (indented), as in **`templates/domain model template.drawio`**.
- In **Markdown**, use **`templates/domain model template.md`**: optional collaborators after `opt`, and `Invariant:` lines.

Keep the **same** collaborators and constraints in both places when maintaining dual files.

## Relationship Type Guide

Use this decision tree to pick the correct relationship. When in doubt, choose the weaker type and upgrade it in a later phase when the ownership model is confirmed.

**Decision tree:**

1. Does A hold a permanent reference to B?
   - **No** → `add-dependency` (transient — B is a parameter or local variable only)
   - **Yes** → go to 2

2. Is A the owner of B (part-whole)?
   - **No** → `add-association` (peer relationship — A knows B, no ownership)
   - **Yes** → go to 3

3. Can B exist without A?
   - **No** → `add-composition` (strong ownership — B dies when A dies)
   - **Yes** → `add-aggregation` (loose ownership — B can be shared or outlive A)

**Quick reference:**

| Type | CLI command | Symbol | Strength | Key test |
|------|-------------|--------|----------|----------|
| Composition | `add-composition` | ◆── | Strongest | Delete A → B is destroyed |
| Aggregation | `add-aggregation` | ◇── | Strong | Delete A → B survives |
| Association | `add-association` | →  | Moderate | A holds a reference to B; neither owns the other |
| Dependency | `add-dependency` | --> | Weakest | A uses B only inside a method — no stored reference |
| Inheritance | `add-inheritance` | --▷ | n/a | IS-A — subclass extends superclass |

**Scan-phase defaults:** At domain-scan fidelity, prefer conservative choices:
- Use `add-dependency` for any relationship that is clearly transient (produced by, resolved via, creates)
- Use `add-composition` only when the source material explicitly states ownership or lifecycle coupling
- Use `add-association` for all other confirmed structural relationships
- Leave aggregation for refinement phases when shared ownership is confirmed

**Prompt to check yourself:**
> "I am modeling [Class A] → [Class B]. Does A store B permanently? Is A the owner? If A is destroyed, does B die too? Is B a physical/logical part of A?"

---

## Collection Class Anti-Pattern

Never invent wrapper types to represent multi-valued fields. Using `SkillSet`, `AbilitySet`, `PowerList`, or `AdvantageList` as class names implies there is a meaningful class there — but these are just collections with no behavior. They pollute the model.

**Wrong:**
```
+ skills: SkillSet
```

**Right:**
```
+ skills: Skill [0..*]
```

Use cardinality notation directly on the field. The cardinality brackets go on the field entry in the diagram:

```bash
drawio_cli.py add-field Character "+ skills: Skill [0..*]"
drawio_cli.py add-field Character "+ abilities: Ability [1..*]"
drawio_cli.py add-field Character "+ powers: Power [0..*]"
```

The `[0..*]` or `[1..*]` tells you both the type and the multiplicity without introducing a phantom class. Only model a collection type as a real class if the collection itself has behavior, identity, or invariants of its own.

---

## Associations Require a Connecting Field

Before drawing an association or dependency between two classes, you must be able to point to a **field** on the source class that holds a reference to the target. No field = no arrow.

**Wrong:** Drawing `Character → Effect` because "Character uses Effects somewhere" — there is no field on Character that holds an Effect reference directly.

**Right:** Tracing the actual path — `Character` has `powers: Power [0..*]`, and a `Power` wraps an `Effect`. The relationship between Character and Effect is therefore **through Power**, not direct. Draw `Character ◆── Power` and `Power → Effect`, not `Character → Effect` directly.

**Protocol before drawing a cross-module relationship:**
1. Identify the field on the source class that connects to the target
2. If no such field exists yet, investigate the source material more deeply before drawing
3. If the connection is definitely real but indirect (via an intermediate class), model the intermediate explicitly
4. If after investigation you cannot find a direct field, the relationship does not exist at this fidelity — leave it out until extraction reveals the path

This applies at all phases. At scan fidelity, prefer omitting a relationship over drawing an unsupported one.

---

## Invariants in Class Diagrams

Invariants document constraints that must hold for a class to be valid — business rules, system constraints, range limits, and lifecycle rules. They are shown in the diagram at two levels of detail:

### Inline invariant (brief — fits on one line)
Add directly inside the class box as a field entry, using curly braces:

```
{ result = d20 + modifier; succeeds if result >= dc }
{ rank 0 = average; rank 20 = cosmic }
```

Use `add-field ClassName "{ invariant text }"` in the CLI. Place inline invariants immediately after the field or section they constrain.

### Note invariant (longer — multiple lines or complex expression)
Use a note (folded-corner rectangle) connected to the class by a dashed line:

```
{ pool resets to 1 each session
  earn: from Complications or heroic acts
  spend: reroll Check, extra action, boost rank +1, recover Condition }
```

The CLI does not yet support notes — add them manually in draw.io after CLI build. Use: Insert → Shape → Note. Connect to the target class with a dashed edge. Enclose invariant text in `{ }`.

**Module / package (UML frame) notes:** For commentary that applies to a whole **module** (the outer `umlFrame` / package boundary from `add-frame`), attach the same Note shape to the **frame’s perimeter** (snap the connector to the frame edge), not to an inner class. Use the same dashed connector style as class notes. This keeps module-level invariants or scope reminders visually tied to the subsystem boundary.

### When to add invariants

| Phase | Add invariants? |
|-------|----------------|
| domain-scan | Yes — add the invariants you found during the scan (inline preferred at this fidelity) |
| domain-noun-verb (Step 1) | No — extraction only; invariants captured in registry notes |
| raw-candidate-list through responsibilities | Yes — as invariants become confirmed, add to diagram |
| Full model phases | Yes — invariants are a required part of the final model |

### Markdown companion notation

In the `.md` companion file, invariants appear as `Invariant:` lines under the field they constrain:

```
+ modifier: int
      Invariant: modifier = sum of applicable trait ranks + circumstance bonuses
```

---

## Crucial Visual Layout Rules for Class Diagrams

- **Hierarchical Flow:** Superclasses/abstract classes must sit vertically above their subclasses.
- **Orthogonal Routing:** Use right-angled (stepped) routing for associations/compositions. Inheritance arrows must point straight up.
- **Anchor Points:** Lines must snap to the perimeter of class boxes. Never leave them floating or intersecting text.
- **Clear Intersections:** Actively rearrange boxes to minimize crossing lines. Keep labels at the immediate ends of connector lines, and bring text to the front (Z-order) so it isn't obscured.

## File naming (suggested)

| Pair | Example |
|------|---------|
| Class | `orders-model.drawio` + `orders-model.md` |

Shared stem makes sync obvious.


---

### `class-diagram-layout-rules.md`

# Draw.io Class Diagram Layout Rules

This document defines what "correct" looks like at the XML level so that
the `verify` command and any reviewing agent have unambiguous ground truth.

**Templates:** New or updated class diagrams should follow the structure and style of **`templates/domain model template.drawio`**; Markdown companions should follow **`templates/domain model template.md`** (see `content/parts/class-diagrams.md`).

---

## Crucial Visual Layout Rules for Class Diagrams

These spatial expectations must be followed whether the agent is creating or evaluating diagrams (either directly via the CLI's relayout and fix-edge-styles, or through manual editing instructions):

- **Vertical Hierarchy:** Superclasses and abstract classes must be positioned vertically above their subclasses, with the diagram flowing from general (top) to specific (bottom).
- **Horizontal Peers:** Peer associations and composition relationships are arranged horizontally to balance the diagram's footprint.
- **Anchor Points:** Relationship lines must snap to the fixed connection anchor points on the perimeter of the class boxes. Lines should never float unattached, terminate inside the box, or intersect with text.
- **Line Routing:** Use orthogonal (right-angled/stepped) routing for associations and compositions. Inheritance arrows must point straight up.
- **Avoid Crossings:** When tweaking layouts manually, actively rearrange boxes to minimize the number of relationship lines that cross over one another.
- **Z-Ordering & Labels:** Ensure text labels (like multiplicities) are kept clearly at the immediate ends of connector lines, and bring text/labels to the front (Z-order) so they aren't obscured by lines or grid elements.

---

## 1. Class bounding boxes must never overlap (V1)

### What overlap means in XML

A class is a `<mxCell>` with `style` containing `swimlane` whose `<mxGeometry>`
gives its bounding rectangle: `x`, `y`, `width`, `height`.

Two classes A and B overlap when ALL FOUR of these are true simultaneously:

```
A.x          < B.x + B.width    (A's left edge is left of B's right edge)
A.x + A.width > B.x             (A's right edge is right of B's left edge)
A.y          < B.y + B.height   (A's top edge is above B's bottom edge)
A.y + A.height > B.y            (A's bottom edge is below B's top edge)
```

### ❌ Overlapping example

```xml
<!-- Car: x=100 y=100 w=200 h=242  →  right=300 bottom=342 -->
<mxCell id="Car" value="Car" style="swimlane;..." vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="242" as="geometry" />
</mxCell>

<!-- CreditCard: x=200 y=200 w=200 h=190  →  overlaps Car by 100×142px -->
<mxCell id="CC" value="CreditCard" style="swimlane;..." vertex="1" parent="1">
  <mxGeometry x="200" y="200" width="200" height="190" as="geometry" />
</mxCell>
```

### ✓ Non-overlapping example

```xml
<!-- Car: x=100 y=100 h=242  →  bottom=342 -->
<mxCell id="Car" ...>
  <mxGeometry x="100" y="100" width="200" height="242" as="geometry" />
</mxCell>

<!-- CreditCard starts 80px below Car's bottom -->
<mxCell id="CC" ...>
  <mxGeometry x="100" y="422" width="200" height="190" as="geometry" />
</mxCell>
```

**Fix:** run `relayout` — it computes actual heights and spaces rows correctly.

---

## 2. Child class must be below parent class (V2)

In a UML class diagram the inheritance arrow points FROM subclass TO superclass,
meaning the arrow goes **upward** on the canvas.  The subclass must therefore
have a **larger `y` value** (lower on the page) than its superclass.

Draw.io coordinate system: `y=0` is the TOP of the canvas, y increases downward.

### ❌ Wrong direction (subclass above parent)

```xml
<!-- Vehicle (superclass) at y=400 — BELOW Car -->
<mxCell id="Vehicle" ...>
  <mxGeometry x="100" y="400" width="200" height="164" as="geometry" />
</mxCell>

<!-- Car (subclass) at y=100 — ABOVE Vehicle — WRONG -->
<mxCell id="Car" ...>
  <mxGeometry x="100" y="100" width="200" height="242" as="geometry" />
</mxCell>

<!-- Inheritance arrow Car→Vehicle goes DOWN, but it should go UP -->
<mxCell style="endArrow=block;dashed=1;endFill=0;..." edge="1"
        source="Car" target="Vehicle" .../>
```

### ✓ Correct direction (subclass below parent)

```xml
<!-- Vehicle (superclass) at y=100 — TOP -->
<mxCell id="Vehicle" ...>
  <mxGeometry x="100" y="100" width="200" height="164" as="geometry" />
</mxCell>

<!-- Car (subclass) at y=344 — BELOW Vehicle (100+164+80 gap) -->
<mxCell id="Car" ...>
  <mxGeometry x="100" y="344" width="200" height="242" as="geometry" />
</mxCell>

<!-- Inheritance arrow goes UP from Car to Vehicle ✓ -->
<mxCell style="endArrow=block;dashed=1;endFill=0;endSize=12;html=1;rounded=0;"
        edge="1" source="Car" target="Vehicle" .../>
```

**Fix:** run `relayout` — it assigns rows by inheritance depth (depth 0 = top).

---

## 3. Edge styles by relationship type (V3)

### 3a. Inheritance — straight diagonal line (NO edgeStyle)

Inheritance uses a **plain straight line** between the two class boxes.
Draw.io draws a straight diagonal when no `edgeStyle` token is present.

**✓ Correct inheritance style:**
```xml
<mxCell style="endArrow=block;dashed=1;endFill=0;endSize=12;html=1;rounded=0;"
        edge="1" source="Car" target="Vehicle" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```
Key: `dashed=1`, `endArrow=block`, `endFill=0`, **no `edgeStyle=`**.

**❌ Wrong — inheritance with orthogonal routing:**
```xml
<!-- edgeStyle=orthogonalEdgeStyle on inheritance creates ugly zig-zags -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;endArrow=block;dashed=1;..."
        edge="1" source="Car" target="Vehicle" .../>
```

### 3b. Association — orthogonal routing (right-angle corners)

```xml
<!-- ✓ Correct association: orthogonal routing, open arrow -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;
               jettySize=auto;html=1;"
        edge="1" source="Person" target="Car" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 3c. Composition — orthogonal routing, filled diamond at WHOLE end

```xml
<!-- ✓ Correct: diamond at the Car (whole) end, orthogonal routing -->
<!-- Edge goes FROM part (Wheel) TO whole (Car); diamond is endArrow -->
<mxCell style="endArrow=diamondThin;endFill=1;endSize=24;html=1;rounded=0;
               edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;"
        edge="1" source="Wheel" target="Car" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 3d. Aggregation — orthogonal routing, hollow diamond at WHOLE end

```xml
<!-- ✓ Correct: hollow diamond at Fleet (whole), line to Plane (part) -->
<!-- Edge goes FROM whole (Fleet) TO part (Plane); diamond is startArrow -->
<mxCell style="endArrow=open;html=1;endSize=12;
               startArrow=diamondThin;startSize=14;startFill=0;
               edgeStyle=orthogonalEdgeStyle;rounded=0;"
        edge="1" source="Fleet" target="Plane" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 3e. Dependency — dashed open arrow (no edgeStyle needed)

```xml
<!-- ✓ Stereotype label on a dependency -->
<mxCell style="endArrow=open;endSize=12;dashed=1;html=1;rounded=0;"
        edge="1" source="Car" target="CarFactory" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<!-- stereotype label child -->
<mxCell style="edgeLabel;html=1;align=center;..." value="&lt;&lt;created by&gt;&gt;"
        vertex="1" connectable="0" parent="EDGE_ID">
  <mxGeometry x="0" y="0" relative="1" as="geometry" />
</mxCell>
```

---

## 4. Explicit waypoints cause extra bends (V4)

Draw.io's orthogonal auto-router finds the minimum-bend path automatically.
Explicit `<Array as="points">` waypoints override that, often producing
unnecessary bends when classes are repositioned.

**❌ Edge with hard-coded waypoints (fragile):**
```xml
<mxCell style="edgeStyle=orthogonalEdgeStyle;..." edge="1"
        source="Fleet" target="Plane" parent="1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="140" y="-120" />
      <mxPoint x="720" y="-120" />
    </Array>
  </mxGeometry>
</mxCell>
```

**✓ Same edge without waypoints — router picks the clean path:**
```xml
<mxCell style="edgeStyle=orthogonalEdgeStyle;..." edge="1"
        source="Fleet" target="Plane" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

**Fix:** run `fix-edge-styles` — it removes all `<Array as="points">` elements.

---

## 5. Multiple edges must not share an unconstrained connection point (V5)

When two or more edges arrive at (or leave from) the same class without explicit
`entryX`/`entryY` (or `exitX`/`exitY`) port constraints in their `style` string,
Draw.io stacks them all at the same default midpoint — producing a visual pile-up
where multiple arrowheads overlap and the diagram becomes unreadable.

### ❌ Six compositions converging at the same bottom-centre of Character

```xml
<!-- All six arrive at the default bottom-centre of Character — they pile up -->
<mxCell style="endArrow=diamondThin;endFill=1;edgeStyle=orthogonalEdgeStyle;..."
        edge="1" source="Ability"      target="Character" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<mxCell style="endArrow=diamondThin;endFill=1;edgeStyle=orthogonalEdgeStyle;..."
        edge="1" source="Skill"        target="Character" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<!-- … same for HeroPoint, Advantage, Complication, Power … -->
```

### ✓ Spread across the bottom side with explicit entry points

```xml
<!-- entryX evenly distributes 6 arrows across the bottom edge -->
<mxCell style="endArrow=diamondThin;endFill=1;edgeStyle=orthogonalEdgeStyle;...
               entryX=0.143;entryY=1;entryDx=0;entryDy=0;"
        edge="1" source="Ability"  target="Character" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<mxCell style="endArrow=diamondThin;endFill=1;edgeStyle=orthogonalEdgeStyle;...
               entryX=0.286;entryY=1;entryDx=0;entryDy=0;"
        edge="1" source="Skill"    target="Character" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<!-- … and so on up to entryX=0.857 for the sixth arrow … -->
```

**Fix:** run `fix-shared-endpoints` — it determines the dominant approach side
(top / bottom / left / right) and distributes `entryX`/`entryY` (or
`exitX`/`exitY`) evenly across it for all unconstrained edges in the group.

> **Preferred over bare entry-point spreading:** see Section 5a below — anchor
> each composition to its specific field row instead. This fully eliminates V5
> and produces a far more readable diagram.

---

## 5a. Field-anchored composition — the preferred routing pattern

When a parent class (e.g. `Character`) owns several child classes through
composition, the cleanest layout is to:

1. **Add a field row** inside the parent for each owned type (e.g. `+ abilities: Ability`)  
2. **Connect the diamond to that field row**, not to the parent class border  
3. **Exit from the SIDE of the child class** (left or right, never top or bottom)  
4. **Keep the diamond co-linear with the line** (diamond faces the same direction as the line segment it is part of — never sideways)  
5. **Use as few waypoints as possible** — ideally zero or one  

### Visual goal

```
[Character]                     [Ability]
┌───────────────────────┐       ┌──────────────┐
│ + powerLevel: int     │       │ + rank: int  │
│─────────────────────  │       │              │
│ + abilities: Ability ◆│───────│              │
│ + skills: Skill      ◆│       └──────────────┘
└───────────────────────┘
```

The diamond (`◆`) sits at the **field row** and points toward the child class.
The line exits the **right or left side** of the child and enters the field row.

### Layout recommendation

Place child classes **to the left or right of the parent**, not directly below.
This allows clean horizontal routing with zero or one waypoint and avoids
long vertical runs that pass through other classes.

```
[Advantage]──────◆ advantages: Advantage  │
[Ability]────────◆ abilities: Ability      │ Character
[HeroPoint]──────◆ heroPoints: HeroPoint  │
[Skill]──────────◆ skills: Skill          │
```

### ✓ Correct XML pattern

```xml
<!-- Source = child class; Target = field row cell inside parent;
     endArrow=diamondThin places the diamond at the field row.
     Child exits from its RIGHT side (exitX=1) toward the field row. -->
<mxCell id="edge-ability" value=""
        style="endArrow=diamondThin;endFill=1;endSize=24;
               edgeStyle=orthogonalEdgeStyle;
               exitX=1;exitY=0.5;exitDx=0;exitDy=0;"
        parent="1" source="AbilityClass" target="AbilitiesFieldRow" edge="1">
  <mxGeometry as="geometry" />
</mxCell>

<!-- The field row cell must have portConstraint=eastwest so the
     diamond connects to its LEFT or RIGHT side, not top/bottom -->
<mxCell id="AbilitiesFieldRow"
        value="+ abilities: Ability"
        style="text;...;portConstraint=eastwest;"
        parent="CharacterClass" vertex="1">
  <mxGeometry y="118" width="300" height="26" as="geometry"/>
</mxCell>
```

Key style attributes:

| Attribute | Value | Reason |
|-----------|-------|--------|
| `source` | child class cell id | composition originates at child |
| `target` | field row cell id (inside parent) | diamond lands at the field |
| `endArrow` | `diamondThin` | filled diamond at target (field row) |
| `exitX=1;exitY=0.5` | right-side exit of child | side exit = clean orthogonal route |
| `portConstraint=eastwest` | on field row | constrains diamond to left or right side |

### ❌ Anti-pattern: diamond entering from the top or bottom

```xml
<!-- Diamond arrives at the parent's bottom edge — produces V5 pile-up
     AND diamond appears sideways or flipped relative to the line -->
<mxCell style="endArrow=diamondThin;endFill=1;
               entryX=0.5;entryY=1;..."   <!-- ← bottom of CHARACTER class -->
        target="CharacterClass" ...>
```

### Rule: diamond co-linearity

The composition diamond must always face **in the same direction as the line
segment it terminates**. If the last segment arrives from the left, the diamond
opens to the left. A sideways diamond (arriving vertically but pointing
horizontally) indicates a mismatched `exitX`/`exitY` or `entryX`/`entryY` and
must be corrected.

### Minimum-waypoint routing

| Child position relative to parent | Typical exit | Waypoints needed |
|------------------------------------|-------------|-----------------|
| Directly left or right, same Y     | right/left   | 0 |
| Left/right but offset vertically   | right/left   | 1 (adjust Y) |
| Below or above (avoid)             | top/bottom   | 2+ (not ideal) |

Prefer placing child classes **laterally** (left/right) so that routes remain
single-segment or single-bend. Stacking child classes directly below the parent
forces multi-waypoint routes and risks V6 overlaps.

---

## 6. Straight-line edges must not pass through unrelated classes (V6)

Dependency edges (`dashed=1`, no `edgeStyle`) draw a straight diagonal line.
When source and target are on opposite sides of the canvas that line can slice
through intermediate class boxes, hiding those classes behind an unrelated arrow.

The `verify` command checks straight-line edges by testing the segment from
source-centre to target-centre against every third class's bounding box
(shrunk by 5 px to avoid false positives at shared borders).

### ❌ Dependency passes through an unrelated class

```
[Check] ————————————————→ [Effect]
           ╱ Power ╲         (Power's box sits on the direct path)
```

### ✓ Resolved options

1. **Run `fix-arrow-overlaps`** — automatically inserts 1–2 waypoints using a
   recursive shortest-path algorithm to route the dependency around all blockers;
   then rerun `verify` to confirm V6 is clear.
2. **Reposition the blocking class** — move it off the arrow corridor as a last
   resort if `fix-arrow-overlaps` cannot find a clean path.

> Note: V6 is a **WARN** (not ERROR) because the obstruction is a layout
> issue. `fix-arrow-overlaps` resolves most cases automatically.

---

## 7. Readability: left-to-right, top-to-bottom reading order

A diagram reads well when:

- Abstract/root classes are at the **top** (small y)
- Concrete subclasses are below (larger y)
- Closely related classes are **horizontally adjacent** (similar x)
- Unrelated groups are visually separated

The `relayout` command implements this automatically by assigning
`y` based on inheritance depth. Within each depth level, siblings
are kept together next to their parent.

---

## Quick summary table

| Relationship    | endArrow         | dashed | edgeStyle         | Diamond  |
|----------------|-----------------|--------|-------------------|----------|
| Inheritance    | `block`          | yes    | **none**          | —        |
| Association    | (default open)   | no     | `orthogonalEdge…` | —        |
| Composition    | `diamondThin`    | no     | `orthogonalEdge…` | filled ◆ |
| Aggregation    | `open` + start   | no     | `orthogonalEdge…` | hollow ◇ |
| Dependency     | `open`           | yes    | none              | —        |


---

### `sequence-diagrams.md`

# Sequence Diagrams and Walkthroughs (Draw.io and Markdown)

## Templates — use these for every create/update

All walkthrough / sequence work should **start from** or **stay aligned with** the checked-in templates under the skill **`templates/`** folder (paths relative to the skill root):

| Role | Template file | When to use it |
|------|----------------|----------------|
| **Draw.io** | `templates/domain realization template.drawio` | **New diagram:** duplicate this file into the workspace, rename, replace `{{placeholders}}`, then edit lifelines and messages. **Existing diagram:** when adding lifelines or messages, keep lifeline alignment, execution bars, and arrow-to-activation conventions as in the template. |
| **Markdown** | `templates/domain walkthrough template.md` | **New companion doc:** copy its scenario / walk / pseudo-code structure. **Updates:** when you change the `.drawio` or the `.md`, update the **other** artifact in the same pass so steps and activations stay aligned. |

Optional: add a **Mermaid** `sequenceDiagram` block in the Markdown file for quick preview (GitHub / readers), using **participant names that match** the lifeline headers in the `.drawio` file.

There is **no** `drawio_cli.py` automation for sequence lifelines yet — **always** ground new Draw.io work in `domain realization template.drawio`.

## Terminology (same concept)

These names refer to the **same** kind of artifact:

- **Domain walkthrough**
- **Domain realization**
- **Domain interaction**
- **Sequence diagram**

Use whichever label the user prefers. In deliverables, pick one label per document and stay consistent.

## What to keep in sync

When the user asks to **create or update** modeling diagrams:

| Artifact | Draw.io | Markdown companion |
|----------|---------|-------------------|
| **Sequence / walkthrough** | `*.drawio` (start from `templates/domain realization template.drawio`) | Same structure as `templates/domain walkthrough template.md` |

**Rule:** If both files exist for a topic, **update both** in the same pass so walk steps do not drift. If only one exists, create the missing companion **from those templates** unless the user opts out.

## Sequence / walkthrough — Draw.io (what the template encodes)

`templates/domain realization template.drawio` illustrates:

- **Initiator** lifeline (optional actor driving the scenario)
- **Object lifelines** (`{{object}}:{{Class}}`)
  - **Alignment:** All participant lifelines must be perfectly aligned horizontally at the top of the canvas.
- **Synchronous messages** (filled arrow) and **returns** (open arrow, dashed)
  - **Crucial Connection Rule:** Message arrows must *always* snap exactly to the outer edge of the **execution bar (activation rectangle)**, NEVER to the center dashed lifeline itself.
  - **Message Angles:** All message arrows must be perfectly horizontal (0-degree angle).
- **Nested execution** (activation bars / self-segment notation)
  - **Positioning:** Execution bars must be placed *exactly centered* on the vertical dashed line of the lifeline.
  - **Nesting:** For internal behavior or nested calls, the nested execution bar must be stacked precisely on the right edge of the parent execution bar, offset slightly downwards to indicate time progression.
  - **Time Flow:** Vertical space strictly represents time. Elements must flow downwards cleanly without any vertical overlap of independent, sequential operations.
- Small **edge labels** for `new`, parameters, and call text

There is **no** `drawio_cli.py` automation for lifelines yet. **New diagrams:** duplicate the template into the workspace (see **Templates** above), replace placeholders, then adjust lifeline heights and messages as needed.

## Sequence / walkthrough — Markdown

**Narrative + pseudo-code** — Follow `templates/domain walkthrough template.md` (required structure; see **Templates** above):
- One **Scenario** block per flow.
- **Walk N: Covers** — scope (what responsibilities this walk exercises).
- Indented pseudo-code showing object creation, calls, returns, and nesting (same story as the Draw.io diagram).

## Creating Sequence Diagrams from Walkthroughs (Step-by-step)

### Step 1: Extract Lifelines from Pseudo-code

Read the walkthrough pseudo-code and identify all **distinct objects/participants**:

```
{object}: {Type} = new {Class}()
{result}: {Type} = {object}.{method}()
    {collaborator}: {CollaboratingClass} = {getter}
    {inner}: {InnerType} = {collaborator}.{method}()
```

**Participants:**
- `{object}:{Class}` ← lifeline 1
- `{collaborator}:{CollaboratingClass}` ← lifeline 2
- Any other objects mentioned ← additional lifelines

### Step 2: Translate Pseudo-code to Messages

For each call in the pseudo-code, create a **message arrow** in Draw.io:

| Pseudo-code | Draw.io Message |
|-------------|-----------------|
| `{object}.{method}()` | Synchronous message arrow (filled) from **{object}** to **{collaborator}** labeled `method()` with params |
| `return {value}` | Return arrow (dashed, open) from callee back to caller labeled with `{value}` (if non-void) |
| `{var} = new {Class}()` | Create message (labeled `«new»`) from initiator to the new object's lifeline |
| Nested calls | Stack activation bars (execution rectangles) vertically; nested calls go to the right edge of parent activation |

### Step 3: Align with Template

When creating the `.drawio` file:

1. **Duplicate** `templates/domain realization template.drawio`
2. **Replace placeholder lifelines** with actual participant names from Step 1
3. **Add messages** following the order in the pseudo-code (top to bottom = time flow)
4. **Verify alignment:**
   - All lifelines top-aligned (horizontal line at y=0)
   - All message arrows **horizontal** (0° angle)
   - Message arrows snap to **outer edge of execution bars**, not center lifeline
   - Execution bars centered on lifeline, nested bars stacked right

### Step 4: Keep Markdown ↔ Draw.io in Sync

- **If updating the `.drawio`:** Update the `.md` pseudo-code to match new messages/lifelines
- **If updating the `.md`:** Update the `.drawio` diagram to match new pseudo-code steps
- **Test alignment:** Trace each line of pseudo-code to a message in the diagram; each message should appear in the `.md`

### Example: Character Creation Scenario

**Markdown pseudo-code (Walk 1: Create ability):**
```
player: Player = initiator
character: Character = new Character(power_level: 5)
    abilities: Ability[] = []
strength_ability: Ability = new Ability(type: Strength, rank: 3)
character.add_ability(strength_ability)
    character.spend_power_points(cost: 3)
return character with Strength:3
```

**Lifelines in `.drawio`:**
1. `player:Player`
2. `character:Character`
3. `strength_ability:Ability`

**Messages in `.drawio`:**
1. `player` → `character` : `create(power_level: 5)`
2. `character` → `abilities` : `add(strength_ability)`
3. `character` → `character` : `spend_power_points(3)` (self-call)
4. Return: `character` → `player` : character object

## File naming (suggested)

| Pair | Example |
|------|---------|
| Model + Walkthrough | `step-1-model.md` (domain model) + `step-1-walkthrough.md` (scenarios & walks) + `step-1-walkthrough.drawio` (sequence diagram) |
| Pattern | `{step-name}-model.md`, `{step-name}-walkthrough.md`, `{step-name}-walkthrough.drawio` |

Use `{step-name}` consistently across all three artifacts so their relationship is obvious.

---

## Tips for Large Walkthroughs

If a single scenario has **many walks** (e.g., 5+ different message flows):

- **Option 1:** Create **one `.drawio`** per walk (e.g., `step-1-walkthrough-create.drawio`, `step-1-walkthrough-combat.drawio`)
- **Option 2:** Create **one merged `.md`** with all walks, but only extract **critical walks** to `.drawio` (mark non-diagrammed walks with `[Not diagrammed]`)

**Rule:** Keep the pairing obvious (shared stem) and the `.drawio` count manageable (1–3 per major flow).


---

### `sequence-diagram-layout-rules.md`

# Draw.io Sequence Diagram Layout Rules

This document defines what "correct" looks like for Domain Walkthroughs / Sequence Diagrams in Draw.io. Since sequence diagrams rely heavily on spatial meaning (horizontal = objects, vertical = time), these rules are critical for a valid diagram.

**Templates:** New or updated sequence diagrams should start from **`templates/domain realization template.drawio`**; Markdown walkthroughs should follow **`templates/domain walkthrough template.md`** (see `content/parts/sequence-diagrams.md`).

---

## Crucial Visual Layout Rules for Sequence Diagrams

These spatial expectations must be followed whether the agent is creating or evaluating diagrams:

- **Lifeline Alignment:** All participant lifelines must be perfectly aligned horizontally at the top of the canvas.
- **Execution Bar Placement:** Execution bars (activations) must be placed exactly centered on the vertical dashed line of the lifeline.
- **Nested Executions:** For nested method calls or internal behavior, the nested execution bar must be stacked precisely on the right edge of the parent execution bar and offset slightly downwards to indicate time progression.
- **Strict Time Flow:** Vertical space strictly represents time; there should be no vertical overlap of independent sequential operations.
- **Crucial Connection Anchors:** Message arrows must always snap exactly to the outer edge of the execution bar (activation rectangle), NEVER to the center dashed lifeline itself.
- **Message Angles:** All message arrows must be perfectly horizontal (0-degree angle) without any diagonals.
- **Return Messages:** Returns (dashed open arrows) must originate from the bottom edge of the returning execution bar and snap back to the original caller's execution bar.

---

## 1. Lifeline Alignment

All participant lifelines (the boxes at the top containing object/class names) must be perfectly aligned horizontally.

**Rule:** Every lifeline header cell must share the exact same `y` coordinate.

### ✓ Correct Alignment
```xml
<!-- Initiator at y=40 -->
<mxCell id="lifeline1" value="Initiator" style="shape=umlLifeline;..." vertex="1" parent="1">
  <mxGeometry x="100" y="40" width="100" height="600" as="geometry" />
</mxCell>

<!-- API Controller at y=40 -->
<mxCell id="lifeline2" value="api:Controller" style="shape=umlLifeline;..." vertex="1" parent="1">
  <mxGeometry x="300" y="40" width="100" height="600" as="geometry" />
</mxCell>
```

---

## 2. Execution Bar (Activation) Positioning

Execution bars (the vertical rectangles showing when an object is active) must be perfectly centered on their parent lifeline's dashed line.

**Rule:** Assuming the execution bar has `width=10` and the parent lifeline has `width=100`, the `x` offset of the execution bar *relative to its parent* must be exactly `45` (i.e., `(100 - 10) / 2`).

### ✓ Correct Execution Bar
```xml
<mxCell id="exec1" value="" style="html=1;points=[];perimeter=orthogonalPerimeter;..." vertex="1" parent="lifeline2">
  <mxGeometry x="45" y="80" width="10" height="160" as="geometry" />
</mxCell>
```

---

## 3. Nested Executions (Self-Calls)

When an object makes a call to itself or has a nested execution block, the child execution bar must be visually stacked to the right of the parent bar.

**Rule:** A nested execution bar must have its left edge exactly touching the right edge of its parent. Relative to the parent lifeline, if the parent execution bar is at `x=45` with `width=10`, the nested execution bar must be at `x=55` (with a `y` offset greater than the parent's `y` to show time passing).

### ✓ Correct Nested Execution
```xml
<!-- Parent Execution -->
<mxCell id="exec_parent" value="" style="..." vertex="1" parent="lifeline2">
  <mxGeometry x="45" y="80" width="10" height="160" as="geometry" />
</mxCell>

<!-- Nested Execution (e.g. private method call) -->
<mxCell id="exec_child" value="" style="..." vertex="1" parent="lifeline2">
  <!-- x=55 touches the right edge of the parent (45+10) -->
  <!-- y=110 starts after the parent started (80) -->
  <mxGeometry x="55" y="110" width="10" height="60" as="geometry" />
</mxCell>
```

---

## 4. Message Connections (Crucial)

Message arrows must ALWAYS connect to the edges of the **Execution Bars**, NEVER directly to the dashed center line of the Lifeline.

**Rule:**
- A **synchronous call** (solid line) must originate from the right or left edge of the sender's execution bar and terminate at the top-left edge of the receiver's newly created execution bar.
- A **return message** (dashed line) must originate from the bottom edge (or bottom-left/right edge) of the receiver's execution bar and return to the edge of the sender's execution bar.

*Note: Draw.io handles this via `source` and `target` attributes pointing to the IDs of the execution bars, not the lifelines.*

### ❌ Wrong Connection (Connected to Lifeline)
```xml
<!-- WRONG: source and target point to the lifelines themselves -->
<mxCell id="msg1" edge="1" source="lifeline1" target="lifeline2">
  ...
</mxCell>
```

### ✓ Correct Connection (Connected to Execution Bars)
```xml
<!-- CORRECT: source and target point to the execution rectangles -->
<mxCell id="msg1" edge="1" source="exec1" target="exec2">
  ...
</mxCell>
```

---

## 5. Message Angles

Time flows strictly downwards. A single message happens conceptually in an instant of visual time.

**Rule:** All message lines (calls and returns) must be perfectly horizontal (0-degree angle). The `y` coordinate of the start point must equal the `y` coordinate of the end point. Diagonal message lines are strictly prohibited.

### ❌ Wrong (Diagonal Message)
```xml
<!-- A message originating at y=150 but arriving at y=170 -->
```

### ✓ Correct (Horizontal Message)
```xml
<!-- The message stays perfectly horizontal -->
```

*(In Draw.io XML, when correctly snapped to execution bars, the orthogonal router ensures horizontal lines if the target execution bar's `y` placement matches the origin point's `y`).*

---

## 6. Time Flow Overlaps

Vertical space represents time.

**Rule:** Independent, sequential operations must not overlap vertically. If Object A calls Object B, and then waits, and then calls Object C, the execution bar for Object C must have a `y` coordinate that starts *after* (is numerically greater than) the bottom edge of Object B's execution bar.

### ✓ Correct Time Flow
```xml
<!-- Call to B happens first -->
<mxCell id="execB" ...>
  <!-- starts at y=100, ends at y=160 -->
  <mxGeometry x="45" y="100" width="10" height="60" as="geometry" />
</mxCell>

<!-- Call to C happens sequentially AFTER B returns -->
<mxCell id="execC" ...>
  <!-- starts at y=180, which is > 160 -->
  <mxGeometry x="45" y="180" width="10" height="50" as="geometry" />
</mxCell>
```


---

## Rules

*No rules for this phase. List rule stems (filename without `.md`) under `skill-config.json` → `phase_rules` for this phase slug, and optionally `every_phase_rules` for rules that apply to every phase. See `parts/library/process-phases.md` § Phase bundle — rules.*


---
