# Corrections log

Project: key-abstractions skill
Source: key-abstractions skill (pipeline runs)

---

## Entry: Carry-forward enrichment caused unrecoverable heading drift; switch to per-phase output

- **Status:** confirmed
- **Context:** key-abstractions skill — enriching a `state: domain-language` module file in place
- **DO / DO NOT:** DO produce a self-contained file at `<workspace>/domain/<name>-key-abstractions.md` using the same flat shape as every other DDD phase skill: `## **KA** → ### term → bullets → ### references`. DO NOT enrich the prior phase's single growing file in place — that forces every later skill (domain-sketch, CRC, object-model) to preserve the exact heading layout this phase introduced, which in practice they do not.
- **Example (wrong):** key-abstractions enrichment inserted `### Ubiquitous Language` inside each `## **KA**`, with `#### **term**` sub-sections beneath. Domain-sketch then tried to add `### Domain Sketch` as a peer, and downstream phases produced inconsistent depths across KAs.
- **Example (correct):** key-abstractions writes a new file `paw-place-key-abstractions.md`:
  ```
  ## **Product Catalog**

  A product catalog is the primary browsable and searchable collection of pet supplies …

  ### **product catalog**           ← KA's own term, listed first
  - is the single source of truth for what is available for sale

  ### **product**
  - belongs to at least one category
  - exposes real-time stock availability

  ### references
  **Ref — Product catalog and browsing**
  …
  ```
- **Likely source:** prompt gap — the skill was written as an in-place enrichment of the previous phase's file.

---

## Entry: Every Key Abstraction needs a term that names the KA itself

- **Status:** confirmed
- **Context:** key-abstractions skill — KA blocks in the output
- **DO / DO NOT:** DO ensure every `## **KA**` heading is followed by a `### term` whose name matches the KA itself (lowercase or as written in the source), listed first under the KA. The KA's own term is the most important term to describe — it carries the abstraction's behaviors, identity, and invariants. Other terms grouped under the KA are subordinate concepts. DO NOT create a `## **KA**` whose body jumps directly into supporting terms.
- **Example (wrong):**
  ```
  ## **Product Catalog**

  Prose definition…

  ### **product**
  - …
  ### **category**
  - …
  ```
- **Example (correct):**
  ```
  ## **Product Catalog**

  Prose definition…

  ### **product catalog**           ← the KA's own term
  - owns the browsable searchable collection of pet supplies
  - is the single source of truth for product identity, stock truth, and review ownership

  ### **product**
  - …
  ### **category**
  - …
  ```
- **Likely source:** prompt gap — neither the skill nor the template stated that the KA itself must appear as a `### term` entry; templates showed only subordinate terms.

---

## Entry: Core terms list must group terms by Key Abstraction

- **Status:** confirmed
- **Context:** key-abstractions skill — module file header
- **DO / DO NOT:** DO keep the flat **Core terms** list unchanged from the partition phase, and add a **Key Abstractions (term grouping)** list alongside it that names each KA in bold followed by its terms. Both lists coexist: flat for traceability, grouped for structure. DO NOT replace the flat list with the grouped list — the flat inventory must remain auditable.
- **Example (wrong):**
  ```
  **Core terms**:
  - **Product Catalog**: product, category, customer review, stock availability
  - **Pet**: pet
  ```
  (Flat list overwritten with the grouped form.)
- **Example (correct):**
  ```
  **Core terms**:
  - product
  - category
  - customer review
  - stock availability
  - pet

  **Key Abstractions (term grouping)**:
  - **Product Catalog**: product, category, customer review, stock availability
  - **Pet**: pet
  ```
- **Likely source:** prompt gap — the original instruction said "update the Core terms list" without distinguishing the inventory from the grouping.

---

## Entry: Engagement prefix on output filename is optional

- **Status:** confirmed
- **Context:** DDD phase output filename
- **DO / DO NOT:** DO default to the bare phase name � `domain-language.md`, `key-abstractions.md`, `domain-sketch.md`, `crc.md`, `object-model.md`, `walkthrough.md`. DO add a `<name>-` engagement prefix only when you need disambiguation: multiple products in the same workspace, or the user asks for it. DO NOT mandate the prefix as the only valid form. The skill template comments now show `[<name>-]<phase>.md` to signal optionality.
- **Example (wrong, mandatory prefix):** Always writing `paw-place-domain-sketch.md` even though the engagement workspace only ever holds one product.
- **Example (correct):** Default to `domain-sketch.md`. If the same workspace also hosts a `barkery-` product line and a `paw-place-` product line, prefix both to disambiguate: `paw-place-domain-sketch.md`, `barkery-domain-sketch.md`.
- **Likely source:** the original skill text required `<name>-<phase>.md` unconditionally; in single-product engagements the prefix was redundant noise.