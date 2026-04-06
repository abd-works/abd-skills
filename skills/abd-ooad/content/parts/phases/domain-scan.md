# Domain scan

**Outcome:** You have a source map, 3–7 high-confidence anchor modules (each with a named core class), and a list of suspected tensions — enough orientation to begin extraction as a targeted pass rather than a mechanical word sweep.

For the full anchor definition, the three-part anchor test, and guidance on incomplete anchors — see `anchors` in this library.

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
| **High-confidence anchors** | 3–7 modules that are clearly central and stable enough to start modeling from. Each anchor is a module: a named thing with a clear core class you can identify by name. If you cannot name the core class, you have not found the anchor yet — see Anchor as Module below. |
| **Suspected tensions** | 1–3 places where the material seems inconsistent, ambiguous, or overloaded |
| **Scan strategy decision** | Which source-type technique will drive extraction |

---

## Term Registry

The registry is maintained in its own file — see `term-registry` in this library for column definitions, step short-name reference, and update protocol.

**At this step:** Add your 3–7 anchor modules with Classification = `anchor` and Step = `SCAN`. Add each supporting class inside an anchor's module frame as `candidate` with a note stating "supporting class in [ModuleName] module — promoted from field". Add any tensions already visible with Classification = `tension`. Do not add other candidates yet — that happens at NOUNS/CANDS.

---

## Verification Checklist

Before completing this step, verify all of these:

- [ ] Have you identified which source type you are working with?
- [ ] Do you have at least three anchors you are confident about?
- [ ] Have you flagged at least one suspected tension or ambiguous boundary?
- [ ] Have you recorded your scan strategy decision?
- [ ] Have all four output files been produced? (results, model.md, model.drawio, term-registry)
- [ ] Does `term-registry.md` exist and contain at least the anchors from this scan?
- [ ] Does every Term in the registry have a confidence level?

If any of these are missing, extend the scan before proceeding.

---

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
- **Term registry:** the core class row has Classification = `anchor`; supporting classes inside the frame have Classification = `candidate` with a note naming the module they belong to

### Initial model sketch

After the scan, before producing files:

- **Name each anchor module:** one-line responsibility statement from the source — do not invent
- **Identify the core class:** confirm it has a name you can point to in the source
- **Identify supporting classes:** 0–3 classes that clearly belong inside the same frame at this fidelity level
- **Do not add detail:** if you only know a class name and broad responsibility from the scan, the sketch only contains that — do not fill in properties, methods, or relationships you haven't confirmed

**CRITICAL CONSTRAINT:** The diagram must match the sketch fidelity exactly. If the sketch has 4 anchor modules with their core classes only, the diagram has 4 frames each containing one core class.

---

## Required Output Files

Every domain-scan produces **four files**. All go under `<workspace>/abd-ooad/`:

| File | Template | Content |
|------|----------|---------|
| `domain-scan-results.md` | `templates/domain-scan-results.md` | Source map, anchors, tensions, scan strategy decision |
| `domain-scan-model.md` | `templates/domain model template.md` | Class notation listing for each anchor — name, fields with cardinality notation, supporting classes |
| `domain-scan-model.drawio` | built via `scripts/drawio_cli.py` | Anchor modules as frames, core class + supporting classes inside each frame, intra-module and cross-module relationships |
| `term-registry.md` | see `term-registry` in library | Seeded with anchors and visible tensions from the scan |

> Walkthrough diagrams are not produced at scan fidelity. The scan does not yet have the resolution needed for a meaningful sequence scenario. Walkthroughs begin at the nouns-verbs phase.

**Anchor module rule:**
Every anchor gets:
- A core class with the same name (the most important concept in the module)
- A dashed frame enclosing the core class and any supporting classes that clearly belong at this fidelity level
- Fields on the core class for concepts you found but have not yet decided are classes vs. properties

> Core class gets the frame. Supporting classes that are confident enough go inside the frame. Everything else is a field on the core class — evaluated in `thing-vs-data-about-a-thing`.

Example: `Character` module has a `Character` core class with `abilities: AbilitySet` as a field. If `Ability` is clearly its own class at this fidelity, it goes inside the Character frame as a supporting class. If uncertain, it stays as a field.

For diagram CLI commands, module frame workflow, and layout rules — see `using-diagram-cli` in this library.

For CLI commands, templates, and layout rules — see `using-diagram-cli` in this library.
