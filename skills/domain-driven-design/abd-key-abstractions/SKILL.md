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

The first `### **term**` listed under each `## **KA**` heading **must be the KA's own term** — the one whose name matches the KA. This is the most important term to describe: it carries the abstraction's behavior, identity, and invariants. Other terms grouped under the KA are subordinate concepts.

For example, under `## **Product Catalog**`, the first `### **term**` is `### **product catalog**`, followed by `### **product**`, `### **category**`, etc.

### Two tests for every candidate

Not every term deserves promotion to a Key Abstraction. Apply both tests before promoting:

**1. Independence test.** Does this concept exist and make sense on its own, without the parent it came from? If it is just a component or output of another concept and has no meaning outside it, it stays as a term under a KA, not its own KA. Example: "degree of success" has no meaning outside a check, so it stays under Check.

**2. Module-fit test.** Does this concept fundamentally connect to the core purpose of THIS module, or does it just touch it tangentially? If only one of its many uses relates to this module, it doesn't belong here. Example: "hero point" is independent, but only one of six spend types touches checks — it belongs in Combat, not Check Resolution.

### Three outcomes for each term

- **Keep as KA term** — passes both tests. Group under a KA.
- **Move to boundary** — independent, but this module *depends on* it without owning it. Add to `# Boundary Domain` with `*(owned by: Module)*`.
- **Move to another module** — independent, but this module does not depend on it at all. Remove entirely and record in `**Moved to other modules**`.

Be ruthlessly critical on both tests. A typical module has 3–8 Key Abstractions.

### Decisions made

Every Key Abstraction carries a `### decisions made` list — the specific judgment calls the modeler had to make. Each decision is a short statement that names the choice and enough reasoning that a domain expert can challenge it.

### Source extracts

Every KA carries a `### references` section grouping all `**Ref —**` entries for the terms in that KA. Each entry has `Source:`, `Locator:`, `Extract:` and is followed by a fenced ```source``` block of verbatim text from disk.

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
## **{{KAName}}**

[1–2 paragraphs of flowing prose defining the KA — role, boundary, responsibilities, relationships, invariants, woven naturally]

### **{{ka_name as a term}}**       ← MUST appear first; name matches the KA
- behavioral line about the KA itself

### **{{another term in this KA}}**
- behavioral line

### references
**Ref — title**
Source: ...
Locator: ...
Extract: whole

```source
verbatim
```

### decisions made
- judgment call with reasoning
- open question
```

---

## Build

1. **Read the prerequisite file.** Read `<deliverables-folder>/<name>-domain-language.md`. Confirm it has a `**Core terms**` list and `### **term**` headings with behavioral bullets and references. Read source material referenced by the Refs.
2. **Group terms into Key Abstractions.** Apply both the independence test and the module-fit test to every candidate. Name each KA using the source's own vocabulary. Three outcomes per term: keep under a KA, move to boundary, or move to another module.
3. **Write the file header.** Keep the flat **Core terms** list from the domain-language file (it is the inventory). Add a **Key Abstractions (term grouping)** list — each bullet names the KA in bold followed by its terms (e.g. `- **Product Catalog**: product catalog, product, category, customer review, stock availability`). Add a `**Moved to other modules**` list if any term was moved out.
4. **Write each KA block under `# Core Domain`.**
   - `## **KAName**` heading.
   - 1–2 paragraphs of prose definition.
   - `### **ka_name_as_a_term**` — the KA's own term, listed FIRST, with behavioral bullets describing what the KA owns and enforces.
   - `### **another term**` for each subordinate term, with behavioral bullets carried over from the domain-language file (unchanged in meaning; phrasing may be adapted to read naturally under the KA).
   - `### references` grouping all `**Ref —**` entries for terms in this KA, each followed by a fenced `source` block of verbatim text.
   - `### decisions made` listing independence-test results, module-fit results, grouping calls, and open questions.
5. **Write boundary terms** under `# Boundary Domain`, each as `### **boundary_term** *(owned by: Module)*` with behavioral bullets, then a single `### references` and `### decisions made`.
6. **Set the state marker** to `key-abstractions`.
7. **Write the file** to `<deliverables-folder>/<name>-key-abstractions.md`. Follow the template in `templates/key-abstractions-template.md`.

---

## Validate

1. **Per-phase output file.** The file is named `<name>-key-abstractions.md`. No prior or later phase content lives in it.
2. **Every Core term placed.** Every term from the `**Core terms**` list is either: under exactly one `## **KA**` as a `### **term**`, under `# Boundary Domain`, or in `**Moved to other modules**`.
3. **Every KA has a term that names it.** Every `## **KA**` heading is followed by a `### **term**` whose name matches the KA itself, listed first.
4. **Every KA has a prose definition.** 1–2 paragraphs immediately after the `## **KA**` heading.
5. **Every KA has decisions recorded.** A `### decisions made` bullet list closes each KA block.
6. **Every Ref has a source block.** Every `**Ref —**` is followed by a fenced ```source``` block with verbatim text from disk.
7. **Boundary terms have owners.** `*(owned by: Module)*` on every boundary term.
8. **State marker.** Front matter reads `state: key-abstractions`.
9. **No sub-headings under terms.** Bullets live directly under each `### **term**` heading. No `#### Domain Language`, `#### References`, or `#### Decisions made` sub-sections.
10. **No old-model jargon.** No `Intent:`, `Shape hint:`, `Tension:`, or labeled definition sections.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Per-phase file with consistent flat shape

**Scanner:** Manual review

The key-abstractions skill writes a self-contained file at `<deliverables-folder>/<name>-key-abstractions.md`. It does **not** enrich the prior phase's file in place. The output uses the consistent flat heading shape every DDD phase skill shares.

#### DO

- Write the file to `<deliverables-folder>/<name>-key-abstractions.md`.

  **Example (pass):** `domain/paw-place-key-abstractions.md`.

- Use `## **KA**` (h2) for KA groupings, `### **term**` (h3) for terms inside, `### references` (h3) for the per-KA reference list, `### decisions made` (h3) for the per-KA decisions list — all peers under each `## **KA**`.

  **Example (pass):**
  ```
  ## **Product Catalog**

  [prose definition]

  ### **product catalog**
  - bullet

  ### **product**
  - bullet

  ### references
  **Ref —** …

  ### decisions made
  - …
  ```

#### DO NOT

- Enrich the previous phase's file (`<name>-domain-language.md` or a single growing `<name>.md`) in place.

  **Example (fail):** Add `## **KA**` wrappers and decisions to `paw-place-domain-language.md` instead of writing a new `paw-place-key-abstractions.md`.

- Insert intermediate sub-headings like `### Ubiquitous Language` or `#### Domain Language` between the KA and its terms.

  **Example (fail):**
  ```
  ## **Product Catalog**
  ### Ubiquitous Language
  #### **product**
  ```

**Source:** Engagement convention (DDD phase-skill simplification).

### Rule: Every Key Abstraction has a term that names the KA itself

**Scanner:** AI review

Every `## **KA**` heading must be followed by a `### **term**` whose name matches the KA itself (lowercased or as written in the source), listed **first** under the KA. The KA's own term is the most important term to describe — it carries the abstraction's behavior, identity, and invariants.

#### DO

- List the KA's own term first under the `## **KA**` heading.

  **Example (pass):**
  ```
  ## **Product Catalog**

  [prose definition]

  ### **product catalog**          ← first; matches the KA
  - owns the browsable searchable collection of pet supplies
  - is the single source of truth for product identity, stock truth, and review ownership

  ### **product**
  - bullet

  ### **category**
  - bullet
  ```

- When the KA name has no natural lowercase term equivalent, use the same name in lowercase or as the source uses it.

  **Example (pass):** `## **Check**` → `### **check**` first.

#### DO NOT

- Skip the KA's own term and start with a subordinate term.

  **Example (fail):**
  ```
  ## **Product Catalog**

  [prose definition]

  ### **product**          ← subordinate term first; missing ### **product catalog**
  - bullet
  ```

- Place the KA's own term anywhere other than first.

  **Example (fail):** `### **product catalog**` appears third under `## **Product Catalog**` after `### **product**` and `### **category**`.

**Source:** Correction — engagement repo (paw-place); KA's own term must be the most important term modeled.

### Rule: Core terms list flat; KA grouping list separate

**Scanner:** Manual review

The file header carries two lists side by side:
- `**Core terms**:` — flat inventory copied from the domain-language file (auditable).
- `**Key Abstractions (term grouping)**:` — each bullet names a KA in bold followed by its terms.

#### DO

- Keep both lists in the header. The flat one is the inventory; the grouped one is the structure.

  **Example (pass):**
  ```
  **Core terms**:
  - product
  - category
  - customer review
  - stock availability
  - pet

  **Key Abstractions (term grouping)**:
  - **Product Catalog**: product catalog, product, category, customer review, stock availability
  - **Pet**: pet
  ```

#### DO NOT

- Replace the flat list with the grouped list.

  **Example (fail):**
  ```
  **Core terms**:
  - **Product Catalog**: product, category, customer review, stock availability
  - **Pet**: pet
  ```
  (Flat inventory destroyed.)

**Source:** Correction — engagement repo (paw-place).

### Rule: Independence and module-fit tests applied; decisions recorded

**Scanner:** Manual review

Every KA must pass both the independence test and the module-fit test. Every term grouped under a KA must have failed the independence test (or has no meaning outside the KA). Decisions for each test outcome must be recorded under `### decisions made`.

#### DO

- Record each independence-test result, module-fit result, and grouping choice as a bullet under `### decisions made`.

  **Example (pass):**
  ```
  ### decisions made
  - Customer review stays under Product Catalog, not its own KA — a review has no meaning outside a product (independence test).
  - Hero point belongs in Combat, not here — only one of six spend types touches checks (module-fit test).
  ```

#### DO NOT

- Promote terms to KAs without applying both tests.

  **Example (fail):** Twenty Core terms become twenty KAs — flat inventory, no analysis.

**Source:** Inherited from prior key-abstractions guidance.

### Rule: References grouped per KA with verbatim source blocks

**Scanner:** Manual review

Each `## **KA**` block has exactly one `### references` section listing all `**Ref —**` entries for terms in that KA. Every `**Ref —**` carries `Source:`, `Locator:`, `Extract:` and is followed by a fenced ```source``` block containing verbatim text copied from disk.

#### DO

- Place all Refs for a KA in one `### references` section after the term headings.

  **Example (pass):**
  ```
  ### references

  **Ref — Product catalog and browsing**
  Source: external-context/requirements-chat-with-product-owner.md
  Locator: lines 3–5
  Extract: whole

  ```source
  …verbatim text…
  ```
  ```

#### DO NOT

- Put `#### References` sub-headings under each term.

  **Example (fail):**
  ```
  ### **product**
  - bullet

  #### References
  **Ref —** …
  ```

- Leave a `**Ref —**` without a fenced source block.

**Source:** Adapted from the original key-abstractions ref-and-source-block rules.

### Rule: No class-level commitments

**Scanner:** Manual review

The key-abstractions file contains no UML stereotypes, typed properties, method signatures, or cardinality notation. Behavioral lines stay as plain prose.

#### DO

- Keep behavioral lines as plain prose bullets.

  **Example (pass):** `- A check is d20 + trait rank (plus modifiers) vs DC; equal or above is success.`

#### DO NOT

- Use `<<Entity>>`, `<<ValueObject>>`, `<<Aggregate>>`, typed properties, method signatures, or cardinality.

  **Example (fail):** `<<Entity>> with lifecycle states` or `resolve(modifier, dc) -> Result` or `1..*`.

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
