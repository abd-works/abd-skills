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
| `domain-scan-results.md`   | **Source map** for the corpus: how major sections/topics relate (scan Step 2 in **`phases/domain-scan`**). It is **not** the anchor roster — that lives in **`term-registry.md`** (Notes: `High Confidence Anchor`, `Sibling Candidate`, `Tension`, …) and in **`domain-scan-model.md`** (module sections and `<<Anchor>>` on the core class). |
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
4. If no single class emerges after exploration, record the cluster as a **tension** in **`term-registry.md`** (and reference it from the scan map in **`domain-scan-results.md`** if useful) and defer

<!-- abd:begin domain-scan -->

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

<!-- abd:end domain-scan -->

