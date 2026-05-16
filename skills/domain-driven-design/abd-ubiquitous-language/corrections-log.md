# Corrections log

Project: ubiquitous-language skill
Source: ubiquitous-language skill (pipeline runs)

---

## Entry: Bundled `rules/` and `scanners/` are stale relative to the new flat shape

- **Status:** confirmed
- **Context:** Engagement run on `paw-place-ubiquitous-language.md`. After the DDD phase-skill simplification (per-phase standalone files, flat `## **KA** → ### **concept** → ### references → ### decisions made` shape), the bundled `rules/*.md` files and `scanners/*.py` under `abd-ubiquitous-language/` still target the old shape: they look for `### Ubiquitous Language` sub-sections, `#### **concept**` h4 headings, `#### Decisions made` and `#### References` sub-headings, and the old `---- separator` convention.
- **Symptom 1:** Scanners can no longer be invoked because `scanner_runner` was hosted under a different scripts path that has since moved/been removed (`ModuleNotFoundError: No module named 'scanner_runner'`). The runner needs to be wired again or the scanners need to switch to a self-contained runner.
- **Symptom 2:** Even if runnable, the scanners would fail correctly-shaped files because they hardcode `_CONCEPT_H4_RE = ^#### \*\*…\*\*$` and look for `### Ubiquitous Language` sub-section headings, both forbidden by the new bundled rules in `SKILL.md`.
- **DO:** Bring `rules/` and `scanners/` into alignment with the bundled rules in `SKILL.md`:
  - Concept headings are `### **concept**` (h3), not `#### **concept**` (h4).
  - No `### Ubiquitous Language`, `### Ubiquitous Language`, `#### References`, or `#### Decisions made` sub-sections inside KA blocks.
  - One `### references` and one `### decisions made` per KA, peer to concepts.
  - Subtypes use `### **Subtype** *is a type of* **Base**`.
  - Front matter `state: ubiquitous-language`.
- **DO NOT:** Remove the bundled rules from `SKILL.md`; those are the authoritative source. The standalone files in `rules/` should mirror them.
- **Likely source:** When the DDD phase-skill simplification refactor landed, the SKILL.md and templates/ were updated but the `rules/` and `scanners/` folders were not refreshed. They are now an outdated copy of the old contract.
- **Action for next maintenance turn:** rewrite `rules/*.md` to mirror the SKILL.md bundled rules, and either rewrite or remove the scanners. Until then, validation runs as an AI pass against the bundled rules in `SKILL.md`.

---

## Entry: Concept defined inline as property instead of its own concept block

- **Status:** confirmed
- **Context:** ubiquitous-language — check-resolution module, `### condition > Ubiquitous Language`
- **DO:** When a named domain concept is first introduced as a tracked property or reference on another concept, give it its own `### concept-name` block in the Ubiquitous Language. Do not embed the concept's full definition inline as a parenthetical on another concept's bullet.
- **Example (wrong):**
  `- tracks its *condition source* — the *power*, *effect*, *attacker*, or *event/situation* that imposed it — and carries an *active* or *inactive* status`
  The full definition of *Condition Source* was embedded inline inside `### condition` rather than extracted as its own `### condition source` concept block.
- **Example (correct):**
  The inline definition was trimmed to `- tracks its *condition source* and carries an *active* or *inactive* status`. A separate `### condition source` concept block was added with its own `#### Ubiquitous Language` bullets, `#### Decisions made`, and `#### References`.
- **Likely source:** prompt gap — the ubiquitous-language skill does not instruct checking whether a named concept introduced as a property on another concept warrants its own block before embedding its definition inline.

---

## Entry: Boundary concept placed in Core Domain instead of Boundary Domain

- **Status:** confirmed
- **Context:** ubiquitous-language — check-resolution module, `### ongoing effect`
- **DO:** When a concept is owned by another module and only touches this module at its edge, model it in the `# Boundary Domain` section under the correct owning module heading — not as a `### concept-name` block in Core Domain. Ask: does this module *own* the concept's lifecycle, or does it only *observe* a quality of it?
- **Example (wrong):**
  `### ongoing effect` was created as a Core Domain concept block with its own `#### Ubiquitous Language`, `#### Decisions made`, and `#### References`. A decision note even stated it was "not a synonym for *power effect*" — but it was still placed in Core.
- **Example (correct):**
  The block was removed from Core Domain. The "ongoing" quality was modeled as Ubiquitous Language bullets on the `## Effect / power effect` Boundary Domain entry: whether an effect is ongoing is the Power module's concern; this module only owns the check-resolution behavior (what happens when the resistance check succeeds or fails).
- **Likely source:** prompt gap — the ubiquitous-language skill does not instruct checking the owning module of a concept before placing it in Core vs. Boundary Domain.

---

## Entry: Effect behavior described on a condition concept bullet

- **Status:** confirmed
- **Context:** ubiquitous-language — check-resolution module, `### condition > Ubiquitous Language`
- **DO:** Each behavior bullet on a concept must describe what *that concept* does or is. Do not embed the behavior or decision logic of a collaborating concept inline as a parenthetical.
- **Example (wrong):**
  `- is imposed *failed resistance checks* (the effect defines which *condition* applies at each *degree of failure*), *fatigue* from *extra effort*, *environmental hazards*, or *power effects*`
  The parenthetical describes *effect* behavior (degree-of-failure → condition mapping) inside a `### condition` bullet.
- **Example (correct):**
  Trimmed to: `- is imposed by its *condition source* — a *failed resistance check*, *fatigue* from *extra effort*, an *environmental hazard*, or a *power effect* directly`. The degree-of-failure logic belongs in `## Effect / power effect` Ubiquitous Language.
- **Likely source:** prompt gap — the ubiquitous-language skill does not instruct verifying that each bullet's subject matches the concept being described before writing parentheticals that cross into a collaborator's responsibility.

---

## Entry: Carry-forward enrichment caused unrecoverable heading drift; switch to per-phase output

- **Status:** confirmed
- **Context:** ubiquitous-language skill — enriching a `state: key-abstractions` module file in place
- **DO / DO NOT:** DO produce a self-contained file at `<workspace>/domain/<name>-ubiquitous-language.md` using the same flat shape as every other DDD phase skill: `## **KA** → ### term → bullets → ### references`. DO NOT graft `### Ubiquitous Language` onto an existing key-abstractions file alongside `### Ubiquitous Language` and `#### References` — phase-to-phase enrichment of a single file forces every later skill to preserve the exact heading shape of the previous skill, which in practice it does not.
- **Example (wrong):** A `paw-place.md` at `state: key-abstractions` was enriched in place. The skill added `### Ubiquitous Language` as a peer to `### Ubiquitous Language`, but earlier passes had already structured the file with `#### Domain Language`, `#### References`, etc. — every restructure attempt broke a different invariant and required a new round of correction.
- **Example (correct):** Skill writes a new file `paw-place-ubiquitous-language.md` containing:
  ```
  ## **Product Catalog**
  ### **product catalog**
  - owns the browsable searchable collection of pet supplies
  - **Invariant:** must be the single source of truth for product identity, stock truth, and review ownership
  ### **product**
  - belongs to at least one category
  - exposes real-time stock availability
  ### references
  **Ref — Product catalog and browsing**
  Source: external-context/requirements-chat-with-product-owner.md
  Locator: lines 3–5
  Extract: whole
  ```source
  …verbatim…
  ```
  ```
- **Likely source:** prompt gap — the skill was written as an enrichment of the prior phase's file rather than a fresh artifact in a consistent shape.

---

## Entry: Every Key Abstraction needs a term that names the KA itself

- **Status:** confirmed
- **Context:** ubiquitous-language skill — ubiquitous-language additions on `## **KA**` blocks
- **DO / DO NOT:** DO ensure every `## **KA**` block contains a `### term` whose name matches the KA itself (lowercase or as written in the source), listed first. The KA's own term carries the abstraction's behavior, invariants, and identity — it is the most important term to describe. DO NOT model only subordinate terms (e.g. only `### product`, `### category` under `## **Product Catalog**` with no `### product catalog`).
- **Example (wrong):**
  ```
  ## **Notification**
  ### **notification preferences**
  - …
  ### **restock alert**
  - …
  ```
- **Example (correct):**
  ```
  ## **Notification**
  ### **notification**
  - delivers transactional and marketing messages
  - **Invariant:** transactional always; marketing only with opt-in
  ### **notification preferences**
  - …
  ### **restock alert**
  - …
  ```
- **Likely source:** prompt gap — the template showed only subordinate terms; the rule that the KA's own term must appear was never stated.

---

## Entry: Behavior and its produced result written as separate bullets

- **Status:** confirmed
- **Context:** ubiquitous-language — check-resolution module, `### check > Ubiquitous Language`
- **DO:** When a behavior bullet directly produces a result, write the result on the same line as the behavior. Do not separate them into two bullets.
- **Example (wrong):**
  ```
  - is resolved by *rolling* a *d20*, adding the *trait rank* and the *circumstance modifier* and comparing the *roll total* to the *difficulty class*
  - produces a *check result*
  ```
  Two separate bullets when the second is the direct output of the first.
- **Example (correct):**
  `- is resolved by *rolling* a *d20*, adding the *trait rank* and the *circumstance modifier* and comparing the *roll total* to the *difficulty class*, producing a *check result*`
  Cause and result on the same line.
- **Likely source:** prompt gap — the ubiquitous-language skill does not instruct combining a behavior and its immediate produced result onto a single bullet.

---

---

## Entry: Engagement prefix on output filename is optional

- **Status:** confirmed
- **Context:** DDD phase output filename
- **DO / DO NOT:** DO default to the bare phase name � `domain-language.md`, `key-abstractions.md`, `ubiquitous-language.md`, `crc.md`, `object-model.md`, `walkthrough.md`. DO add a `<name>-` engagement prefix only when you need disambiguation: multiple products in the same workspace, or the user asks for it. DO NOT mandate the prefix as the only valid form. The skill template comments now show `[<name>-]<phase>.md` to signal optionality.
- **Example (wrong, mandatory prefix):** Always writing `paw-place-ubiquitous-language.md` even though the engagement workspace only ever holds one product.
- **Example (correct):** Default to `ubiquitous-language.md`. If the same workspace also hosts a `barkery-` product line and a `paw-place-` product line, prefix both to disambiguate: `paw-place-ubiquitous-language.md`, `barkery-ubiquitous-language.md`.
- **Likely source:** the original skill text required `<name>-<phase>.md` unconditionally; in single-product engagements the prefix was redundant noise.
---

## Entry: Customer review missed authorship by customer account

- **Status:** confirmed
- **Context:** abd-ubiquitous-language � PawPlace engagement, Product Catalog KA, `customer review` concept block.
- **DO / DO NOT:** DO surface authorship as a first-class relationship on any concept that is **created by an actor**: a review is **authored by exactly one customer account**, an order is **placed by a customer account or guest checkout**, an appointment is **booked by a customer account**, etc. Authorship belongs in **both** the authored concept's bullets and the authoring KA's invariants/aggregations, plus in the owning KA's `### decisions made` block as a two-sided relationship statement. DO NOT treat authored artifacts as floating facts attached only to their target (the product, in this case) � that hides the trust anchor and leaves invariants like `no anonymous reviews` undocumented.
- **Example (wrong):**
  ```
  ### **customer review**
  - attaches a one-to-five star rating, optional written text, and optional photo to a product
  - contributes to the product's aggregate rating
  - **Invariant:** must always be attached to exactly one product
  ```
  (No author. Implies anonymous reviews are allowed.)
- **Example (correct):**
  ```
  ### **customer review**
  - is **authored by exactly one customer account** � anonymous reviews are not allowed
  - attaches a one-to-five star rating, optional written text, and optional photo to a product
  - contributes to the product's aggregate rating
  - **Invariant:** must always be attached to exactly one product **and** authored by exactly one customer account; guest checkout sessions cannot leave reviews
  ```
  Plus on Customer Account: aggregates `�and authored customer reviews`.
  Plus in Product Catalog `### decisions made`: `Customer review **authorship** belongs to **Customer Account**. Product Catalog *owns* the review system; Customer Account *authors* each review. Two-sided relationship.`
- **Likely source:** the bundled rules in `abd-ubiquitous-language/SKILL.md` enforce concept verbs and invariants but don't explicitly demand an **authorship / created-by** relationship on any concept that an actor produces. A new bundled rule should require: for every concept that is the artifact of an actor's behavior, name the authoring KA explicitly in the concept's bullets, in the authoring KA's aggregations, and in the owning KA's `### decisions made` as a two-sided relationship statement.