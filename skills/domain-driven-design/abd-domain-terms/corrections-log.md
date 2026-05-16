# Corrections log

Project: domain-terms skill
Source: domain-terms skill (pipeline runs)

---

## Entry: Per-phase output, no carry-forward

- **Status:** confirmed
- **Context:** domain-terms skill — output file
- **DO / DO NOT:** DO produce a self-contained file at `<workspace>/domain/<name>-domain-terms.md` using the same flat shape every other DDD phase skill uses: `## **KA** → ### term → bullets → ### references`. DO NOT write a single growing file (e.g. `<name>.md`) that subsequent phases (`key-abstractions`, `ubiquitous-language`) enrich in place — that pattern produced unrecoverable heading drift across phases.
- **Example (wrong):** `paw-place.md` written at `state: domain-terms`, then `state: key-abstractions` adds intermediate `### Ubiquitous Language` headings, then `state: ubiquitous-language` adds `### Ubiquitous Language` peers — depth becomes inconsistent across KAs and every later phase has to reconcile the earlier shape.
- **Example (correct):** `paw-place-domain-terms.md` standalone:
  ```
  ## **Product Catalog**
  ### **product**
  - A product is a pet supply item available for purchase.
  - Every product has images, description, weight and dimensions where relevant.
  ### references
  **Ref — Product catalog and browsing**
  Source: external-context/requirements-chat-with-product-owner.md
  Locator: lines 3–5
  Extract: whole
  ```source
  …verbatim…
  ```
  ```
  Subsequent phase produces `paw-place-key-abstractions.md` independently, in the same shape.
- **Likely source:** prompt gap — the skill was written as the start of an in-place enrichment chain rather than the first of a series of standalone files.

---

## Entry: Engagement prefix on output filename is optional

- **Status:** confirmed
- **Context:** DDD phase output filename
- **DO / DO NOT:** DO default to the bare phase name � `domain-terms.md`, `key-abstractions.md`, `ubiquitous-language.md`, `crc.md`, `object-model.md`, `walkthrough.md`. DO add a `<name>-` engagement prefix only when you need disambiguation: multiple products in the same workspace, or the user asks for it. DO NOT mandate the prefix as the only valid form. The skill template comments now show `[<name>-]<phase>.md` to signal optionality.
- **Example (wrong, mandatory prefix):** Always writing `paw-place-ubiquitous-language.md` even though the engagement workspace only ever holds one product.
- **Example (correct):** Default to `ubiquitous-language.md`. If the same workspace also hosts a `barkery-` product line and a `paw-place-` product line, prefix both to disambiguate: `paw-place-ubiquitous-language.md`, `barkery-ubiquitous-language.md`.
- **Likely source:** the original skill text required `<name>-<phase>.md` unconditionally; in single-product engagements the prefix was redundant noise.