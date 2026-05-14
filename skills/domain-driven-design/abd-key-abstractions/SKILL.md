---
name: key-abstractions
catalog_garden_order: 3
description: >-
  Group domain-language terms into named Key Abstractions with prose
  definitions and verbatim source extracts, elevating a flat term list into
  defined domain building blocks.
---
# key-abstractions

## Purpose

A shared vocabulary names the pieces of the domain, but it doesn't tell you which concepts carry the weight — which ones anchor the model, own specific responsibilities, and enforce the rules that keep the domain coherent. This skill identifies those **Key Abstractions** and defines each one: what role it plays, what it owns, how it relates to other abstractions, and what must always be true about it. The result is a set of stable domain building blocks that everyone — modelers, developers, domain experts — can reason about consistently.

---

## When to use this skill

- A `<deliverables-folder>/<name>-domain-language.md` exists.
- The user asks to "identify key abstractions," "define the abstractions," "run key abstractions," or "what are the building blocks."
- The next modeling step needs defined domain units — not just a flat term list.

## Prerequisites

This skill **requires a list of domain terms** to work with. If no domain-language file exists, **first run `abd-domain-language`** (and `abd-module-partition` upstream of that if no term list exists). Do not invent terms from memory — read the source.

---

## Core concepts

### Key Abstraction

A **Key Abstraction** is a named domain building block that groups related terms and carries a prose definition explaining what it owns, what it does, and what rules it enforces. It transforms a flat vocabulary into an architecture — stable units that modelers, developers, and domain experts can reason about without ambiguity.

Each KA definition is 1–2 paragraphs of flowing prose that weaves together five aspects:

- **Role** — the unique purpose this KA serves that no other does, including its behavior and interactions with other KAs.
- **Boundary** — what it owns (single source of truth for its concepts), what's external, and how it collaborates with other KAs and the constraints of those connections.
- **Relationships** — explicit connections between terms and other abstractions, with cardinality where obvious and natural.
- **Responsibilities** — the specific behaviors it performs and the services it provides to the rest of the system.
- **Rules / invariants** — non-negotiable truths that must always hold for the KA to exist and operate correctly.

### Every KA must have a term that names the KA itself

The first `### term` listed under each `## KA` heading **must be the KA's own term** — the one whose name matches the KA. This is the most important term to describe: it carries the abstraction's behavior, identity, and invariants. Other terms grouped under the KA are subordinate concepts.

For example, under `## Product Catalog`, the first `### term` is `### product catalog`, followed by `### product`, `### category`, etc.

### Two tests for every candidate

Not every term deserves promotion to a Key Abstraction. Apply both tests before promoting:

**1. Independence test.** Does this concept exist and make sense on its own, without the parent it came from? If it is just a component or output of another concept and has no meaning outside it, it stays as a term under a KA, not its own KA. Example: "degree of success" has no meaning outside a check, so it stays under Check.

**2. Module-fit test.** Does this concept fundamentally connect to the core purpose of THIS module, or does it just touch it tangentially? If only one of its many uses relates to this module, it doesn't belong here. Example: "hero point" is independent, but only one of six spend types touches checks — it belongs in Combat, not Check Resolution.

### Three outcomes for each term

- **Keep as KA term** — passes both tests. Group under a KA.
- **Move to boundary** — independent, but this module *depends on* it without owning it. Add to `# Boundary Domain` with `*(owned by: Module)*`.
- **Move to another module** — independent, but this module does not depend on it at all. Remove entirely and record in `**Moved to other modules**`.

Be ruthlessly critical on both tests. A typical module has 3–8 Key Abstractions.

### Decisions made and References — per term

Every term carries its own `### Decisions made` list (when modeling calls were made) and `### References` section immediately after its behavioral lines. This keeps reasoning and evidence co-located with the term they support. Do not bundle decisions or references at the KA level. The KA's own term typically carries the heaviest `### Decisions made` section (independence-test results, module-fit results, grouping rationale).

---

## Output file

This skill produces a **standalone, self-contained file** at:

```
<deliverables-folder>/[<name>-]key-abstractions.md
```

**File name:** Default to `key-abstractions.md`. Add a `<name>-` engagement prefix only when you need disambiguation — multiple products living in the same workspace, or the user asks for it explicitly. Both `key-abstractions.md` and `<name>-key-abstractions.md` are valid. For multi-module engagements (with `abd-module-partition` output), the module name is the disambiguator: `<deliverables-folder>/modules/<module-name>-key-abstractions.md`.

The file is **not enriched in place** by later phase skills. The next phase (`abd-domain-sketch`) writes its own file using the same heading shape.

**Resolving `<deliverables-folder>`** — pick in this order:

1. **The path the user told you to use.** If the user names a file or folder, use exactly that.
2. **Where the engagement already keeps deliverables.** Look at the workspace; if previous phase output (or other engagement docs like `story-map.md`, `process.md`, `corrections-log.md`) already lives in a folder, write next to them in the **same** folder.
3. **The workspace root.** If neither applies, write to the workspace root.

Do **not** assume a predetermined folder name like `domain/` or `stories/`. The only DDD/story skill that creates a sub-folder is **`abd-module-partition`**, which deliberately uses `modules/<module-name>-…` to carve a partition.

For a multi-module engagement (with `abd-module-partition` output), use `<deliverables-folder>/modules/<module-name>-key-abstractions.md` — i.e. the `modules/` sub-folder lives **inside** the resolved `<deliverables-folder>`.

---

## Consistent shape (used by every DDD phase skill)

```
## KAName

[Analytical intro paragraph(s) with *italicized domain terms* — role, boundary,
responsibilities, relationships, invariants, woven naturally]

### ka_name_as_a_term              ← MUST appear first; matches the KA
- behavioral line with *italicized domain terms*

### Decisions made
- independence-test result, module-fit result, grouping call

### References
**Ref — title**
Source: ...
Locator: ...
Extract: whole

```source
verbatim
```

---

### another_term
- behavioral line with *italicized domain terms*

### References
**Ref — title**
Source: ...

---
```

---

## Build

1. **Read the prerequisite file.** Read `<deliverables-folder>/<name>-domain-language.md`. Confirm it has a `**Core terms**` list and `### term` headings with behavioral bullets and references. Read source material referenced by the Refs.
2. **Group terms into Key Abstractions.** Apply both the independence test and the module-fit test to every candidate. Name each KA using the source's own vocabulary. Three outcomes per term: keep under a KA, move to boundary, or move to another module.
3. **Write the file header.** Keep the flat **Core terms** list from the domain-language file (it is the inventory). Add a **Key Abstractions (term grouping)** list — each bullet names the KA in bold followed by its terms (e.g. `- **Product Catalog**: product catalog, product, category, customer review, stock availability`). Add a `**Moved to other modules**` list if any term was moved out.
4. **Write each KA block under `# Core Domain`.**
   - `## KAName` heading (no bold).
   - Analytical intro paragraph(s) with *italicized domain terms* — rich enough for a domain expert to challenge. Covers role, boundary, responsibilities, relationships, and invariants woven naturally.
   - `### ka_name_as_a_term` (no bold) — the KA's own term, listed FIRST, with behavioral bullets using *italicized domain terms*.
   - `### Decisions made` and `### References` for the KA's own term, immediately after its bullets.
   - `---` separator.
   - `### another_term` (no bold) for each subordinate term, with behavioral bullets using *italicized domain terms* (carried over from domain-language; meaning unchanged, phrasing may adapt). Each term gets its own `### References`, followed by `---`.
5. **Write boundary terms** under `# Boundary Domain` as `## boundary_module` with `Owned by: Module`, then `### boundary_term` with behavioral bullets using *italicized domain terms*, per-term `### Decisions made` and `### References`.
6. **Italicize every domain term** in behavioral bullets and KA intro paragraphs. Non-domain words stay plain.
7. **Set the state marker** to `key-abstractions`.
8. **Write the file** to `<deliverables-folder>/<name>-key-abstractions.md`. Follow the template in `templates/key-abstractions-template.md`.

---

## Validate

1. **Per-phase output file.** The file is named `<name>-key-abstractions.md`. No prior or later phase content lives in it.
2. **Every Core term placed.** Every term from the `**Core terms**` list is either: under exactly one `## KA` as a `### term`, under `# Boundary Domain`, or in `**Moved to other modules**`.
3. **Every KA has a term that names it.** Every `## KA` heading is followed by a `### term` whose name matches the KA itself, listed first.
4. **Every KA has an analytical intro.** Paragraph(s) with *italicized domain terms* immediately after the `## KA` heading — rich enough for a domain expert to challenge.
5. **Domain terms italicized.** Every domain term in behavioral bullets and KA intro paragraphs is *italicized*. Consistent throughout the file.
6. **No bold on headings.** KA headings (`## KAName`) and term headings (`### term`) use no bold.
7. **Decisions and References per term.** Each term has its own `### Decisions made` (where modeling calls were made) and `### References` immediately after its bullets. Not bundled per KA.
8. **Separators between terms.** A `---` horizontal rule follows every term block (after its References), before the next term heading.
9. **Every Ref has a source block.** Every `**Ref —**` is followed by a fenced ```source``` block with verbatim text from disk.
10. **Boundary terms have owners.** `Owned by: Module` on every boundary section.
11. **State marker.** Front matter reads `state: key-abstractions`.
12. **No sub-headings under terms.** Bullets live directly under each `### term` heading. No `####` sub-sections.
13. **No old-model jargon.** No `Intent:`, `Shape hint:`, `Tension:`, or labeled definition sections.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Per-phase file with consistent flat shape

**Scanner:** Manual review

The key-abstractions skill writes a self-contained file at `<deliverables-folder>/<name>-key-abstractions.md`. It does **not** enrich the prior phase's file in place.

#### DO

- Write the file to `<deliverables-folder>/<name>-key-abstractions.md`.

  **Example (pass):** `domain/paw-place-key-abstractions.md`.

- Use `## KAName` (h2, no bold), `### term` (h3, no bold), `### Decisions made` (h3), `### References` (h3) — per term, not per KA.

  **Example (pass):**
  ```
  ## Product Catalog

  [analytical intro with *italicized domain terms*]

  ### product catalog
  - owns the browsable searchable collection of *pet supplies*

  ### Decisions made
  - ...

  ### References
  **Ref —** …

  ---

  ### product
  - belongs to at least one *category*

  ### References
  **Ref —** …

  ---
  ```

#### DO NOT

- Enrich the previous phase's file in place.

- Use bold on KA or term headings.

  **Example (fail):** `## **Product Catalog**` or `### **product**`.

- Insert intermediate sub-headings between the KA and its terms.

**Source:** Engagement convention (DDD phase-skill simplification).

### Rule: Every Key Abstraction has a term that names the KA itself

**Scanner:** AI review

Every `## KA` heading must be followed by a `### term` whose name matches the KA itself, listed **first** under the KA.

#### DO

- List the KA's own term first under the `## KA` heading.

  **Example (pass):**
  ```
  ## Product Catalog

  [analytical intro]

  ### product catalog                   ← first; matches the KA
  - owns the browsable searchable collection of *pet supplies*

  ### Decisions made
  - ...

  ### References
  **Ref —** …

  ---

  ### product
  - ...
  ```

#### DO NOT

- Skip the KA's own term and start with a subordinate term.

**Source:** Correction — engagement repo (paw-place).

### Rule: Domain terms italicized in behavioral lines

**Scanner:** AI review

Every domain term referenced in a behavioral line or KA intro paragraph must be italicized using `*term*`. This makes the ubiquitous language visually precise and self-documenting.

#### DO

- Italicize every domain term when it appears in a behavioral line or KA intro paragraph.

  **Example (pass):**
  ```
  - A *check* is *d20* + *trait rank* (plus *modifiers*) vs *DC*; equal or above is *success*.
  ```

- Italicize terms consistently throughout the file.

#### DO NOT

- Leave domain terms as plain text.

  **Example (fail):**
  ```
  - A check is d20 + trait rank (plus modifiers) vs DC; equal or above is success.
  ```

**Source:** Correction — check-resolution engagement demonstrated superior precision; adopted as standard.

### Rule: Per-term Decisions made and References

**Scanner:** Manual review

Every term block has its own `### Decisions made` (when modeling calls were made) and `### References` immediately after its behavioral lines, followed by a `---` separator.

#### DO

- Place `### Decisions made` and `### References` per term, immediately after its bullets.

  **Example (pass):**
  ```
  ### check
  - A *check* is *d20* + *trait rank* vs *DC*...

  ### Decisions made
  - *Degree of success* stays under *Check* — no meaning outside a check (independence test).

  ### References
  **Ref — Game Play**
  Source: ...

  ---

  ### Difficulty Class (DC)
  - The *DC* is a number set by the *GM*...

  ### References
  **Ref — Ch1 The Basics**
  Source: ...

  ---
  ```

#### DO NOT

- Bundle all decisions and references at the end of the KA.

**Source:** Correction — check-resolution engagement established per-concept structure.

### Rule: Core terms list flat; KA grouping list separate

**Scanner:** Manual review

The file header carries two lists: `**Core terms**:` (flat inventory from domain-language) and `**Key Abstractions (term grouping)**:` (each bullet names a KA in bold followed by its terms).

#### DO

- Keep both lists in the header.

#### DO NOT

- Replace the flat list with the grouped list.

**Source:** Correction — engagement repo (paw-place).

### Rule: Independence and module-fit tests applied; decisions recorded

**Scanner:** Manual review

Every KA must pass both the independence test and the module-fit test. Decisions for each test outcome must be recorded under `### Decisions made`.

#### DO

- Record each independence-test result, module-fit result, and grouping choice as a bullet under `### Decisions made`.

  **Example (pass):**
  ```
  ### Decisions made
  - *Customer review* stays under *Product Catalog*, not its own KA — a review has no meaning outside a *product* (independence test).
  - *Hero point* belongs in *Combat*, not here — only one of six spend types touches *checks* (module-fit test).
  ```

#### DO NOT

- Promote terms to KAs without applying both tests.

  **Example (fail):** Twenty Core terms become twenty KAs — flat inventory, no analysis.

**Source:** Inherited from prior key-abstractions guidance.

### Rule: No class-level commitments

**Scanner:** Manual review

The key-abstractions file contains no UML stereotypes, typed properties, method signatures, or cardinality notation. Behavioral lines stay as plain prose.

#### DO

- Keep behavioral lines as plain prose bullets with *italicized domain terms*.

#### DO NOT

- Use `<<Entity>>`, `<<ValueObject>>`, `<<Aggregate>>`, typed properties, method signatures, or cardinality.

**Source:** Inherited from prior key-abstractions guidance.

### Rule: State marker is key-abstractions

**Scanner:** Manual review

After this skill runs, the file's YAML front matter must contain `state: key-abstractions`.

#### DO

- Set the front matter to exactly `state: key-abstractions`.

#### DO NOT

- Leave the marker at `domain-language` or omit the front matter.

**Source:** Inherited from prior key-abstractions guidance.
<!-- execute_rules:bundle_rules:end -->
