---
name: domain-terms
catalog_garden_order: 2
description: >-
  Extract domain terms, group them into Key Abstractions, and produce a single
  domain-terms file — the shared vocabulary and building blocks for the module.
---
# abd-domain-terms

## Purpose

Build a shared, rigorous vocabulary for each module — the terms, behaviors, and rules that domain experts and modelers agree on — and immediately structure them into **Key Abstractions** (named building blocks) so that every conversation, document, and downstream artifact uses the same language without translation.

This is a single-pass skill. It does not produce a flat term list first and a KA file second. It reads source, identifies terms, groups them into KAs, and writes one file.

---

## When to use

- The user asks to "extract Domain Terms," "define terms," "identify key abstractions," "build the Domain Terms," or "what are the building blocks."
- The next modeling step needs defined term behavior and stable domain units — not just a flat name list.

---

## Core concepts

### Key Abstraction (KA)

A **Key Abstraction** is a named domain building block that groups related terms. The KA name is itself the primary term — the concept that anchors the group, owns the core responsibility, and enforces the rules that keep the abstraction coherent.

The KA's intro paragraph opens with a definition of the KA as a term: "*KAName* is …" and weaves together five aspects:

- **Role** — the unique purpose this KA serves that no other does.
- **Boundary** — what it owns (single source of truth), what's external, how it collaborates.
- **Relationships** — explicit connections between terms and other KAs.
- **Responsibilities** — the specific behaviors it performs and services it provides.
- **Rules / invariants** — non-negotiable truths that must always hold.

There is no separate `### ka_name_as_a_term` entry. The KA intro paragraph is the term definition. Subordinate terms follow as `### term` blocks beneath it.

### Domain term

A named concept from the module's domain. For each term, the skill captures *what it does* — behavior, interactions, rules, and flows — as short prose statements grounded in source material. Every claim traces back to the source it came from.

### Two tests for every KA candidate

**1. Independence test.** Does this concept exist and make sense on its own, without the parent it came from? If it has no meaning outside another concept, it stays as a subordinate term, not its own KA.

**2. Module-fit test.** Does this concept fundamentally connect to the core purpose of this module, or does it only touch it tangentially? If only one of its many uses relates to this module, it doesn't belong here.

A typical module has 3–8 Key Abstractions.

### Three outcomes for each candidate term

- **Keep under a KA** — passes both tests. Group under the right KA.
- **Move to boundary** — independent, but this module depends on it without owning it. Add to `# Boundary Domain` with `*(owned by: Module)*`.
- **Move to another module** — independent, but this module does not depend on it at all. Record in `**Moved to other modules**`.

### Boundary terms

A concept this module depends on but does not own. Another module is the single source of truth for it. Appears under `# Boundary Domain` as `### term *(owned by: Module)*`.

---

## Output file

One file:

```
<deliverables-folder>/[<name>-]domain-terms.md
```

Default filename: `domain-terms.md`. Add `<name>-` prefix only for disambiguation (multiple products in same workspace, or user asks). For multi-module engagements: `<deliverables-folder>/modules/<module-name>-domain-terms.md`.

**Resolving `<deliverables-folder>`:**

1. The path the user told you to use.
2. Where the engagement already keeps deliverables.
3. The workspace root.

---

## Consistent shape

```
## KAName

KAName is [definition as term — role, boundary, responsibilities, relationships,
invariants woven naturally. This paragraph IS the term definition for the KA.]

### subordinate_term
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

1. **Read the source.** Read all source material the user provides or the engagement makes available. If a `<name>-module-partition.md` exists, follow its term list and Refs.
2. **Extract terms.** Identify all candidate terms in the source — named concepts with behavior, rules, or interactions.
3. **Apply independence and module-fit tests** to every candidate. Record outcomes: keep under KA, move to boundary, or move out entirely.
4. **Group into Key Abstractions.** Name each KA from the source's own vocabulary. A typical module has 3–8 KAs. List the grouping in the file header under `**Key Abstractions (term grouping)**`.
5. **Write each KA block** under `# Core Domain`:
   - `## KAName` heading (no bold).
   - Intro paragraph that opens with "*KAName* is …" — this is the term definition for the KA itself. Include role, boundary, responsibilities, relationships, and invariants woven naturally. Make it rich enough for a domain expert to challenge.
   - `### subordinate_term` (no bold) for each subordinate term, with behavioral bullets using *italicized domain terms*.
   - `### Decisions made` and `### References` per term, immediately after its bullets.
   - `---` separator after every term block.
6. **Write boundary terms** under `# Boundary Domain` as `### boundary_term *(owned by: Module)*`, behavioral bullets, per-term `### Decisions made` and `### References`.
7. **Italicize every domain term** in behavioral bullets and KA intro paragraphs.
8. **Set state marker** to `domain-terms`.
9. **Write the file** to `<deliverables-folder>/<name>-domain-terms.md`. Follow `templates/domain-terms-template.md`.

---

## Validate

1. **One file.** Named `<name>-domain-terms.md`. No separate key-abstractions file.
2. **KA inventory in header.** A `**Key Abstractions (term grouping)**` list names every KA and its subordinate terms.
3. **No Core terms flat list.** Do not add a `**Core terms**` bullet list in the header — terms are listed in the KA grouping and as headings below.
4. **Every KA has an intro paragraph.** Opens with "*KAName* is …" — this serves as the term definition for the KA itself.
5. **No separate KA-as-term entry.** The KA intro paragraph is the definition. Do not add a `### ka_name` block that duplicates it.
6. **Every subordinate term has behavioral bullets.** At least one bullet per `### term`.
7. **Decisions and References per term.** `### Decisions made` (when modeling calls were made) and `### References` immediately after each term's bullets, not bundled per KA.
8. **Separators.** A `---` horizontal rule follows every term block (after its References), before the next heading.
9. **Every Ref has a source block.** Every `**Ref —**` is followed by a fenced ```source``` block with verbatim text.
10. **Domain terms italicized.** Every domain term in behavioral bullets and KA intro paragraphs.
11. **No bold on headings.** `## KAName` and `### term` carry no bold.
12. **Boundary terms have owners.** Every `### boundary_term` heading carries `*(owned by: Module)*`.
13. **State marker.** Front matter reads `state: domain-terms`.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Single output file — domain-terms.md

**Scanner:** Manual review

This skill produces exactly one file: `<name>-domain-terms.md`. It does not produce a separate key-abstractions file, and it does not enrich a prior file in place.

#### DO

- Write all output to `<name>-domain-terms.md`.

#### DO NOT

- Produce a flat `domain-terms.md` then a separate `key-abstractions.md`.
- Enrich a prior file in place.

### Rule: KA intro paragraph is the term definition — no separate KA-as-term entry

**Scanner:** AI review

The KA's intro paragraph opens with "*KAName* is …" and serves as the full term definition for the KA itself. There is no separate `### ka_name_as_a_term` block beneath the intro.

#### DO

- Open the KA intro with "*KAName* is [definition]…" and weave in role, boundary, responsibilities, relationships, and invariants naturally.

  **Example (pass):**
  ```
  ## Crowd

  A *crowd* is a named collection of characters sharing a scene position and a
  common display configuration. It owns the roster of *crowd members*...
  ```

#### DO NOT

- Add a `### crowd` heading that repeats the intro as bullets.

  **Example (fail):**
  ```
  ## Crowd

  [intro paragraph]

  ### crowd                   ← redundant; the intro already IS the definition
  - a crowd is a named collection of characters
  ```

### Rule: No Core terms flat list in header

**Scanner:** Manual review

Do not add a `**Core terms**: - term1 - term2` bullet list in the file header. Terms appear in the `**Key Abstractions (term grouping)**` list and as `### term` headings in the body.

#### DO

- Use only `**Key Abstractions (term grouping)**` in the header.

#### DO NOT

- Add `**Core terms**:` flat bullet list.

### Rule: Independence and module-fit tests applied; decisions recorded

**Scanner:** Manual review

Every KA must pass both tests. Every subordinate-term decision (stay, boundary, move) must be recorded under `### Decisions made`.

#### DO

- Record each independence-test result, module-fit result, and grouping choice under `### Decisions made`.

#### DO NOT

- Promote every term to its own KA without analysis.

### Rule: Domain terms italicized in behavioral lines and KA intro

**Scanner:** AI review

Every domain term in behavioral bullets and KA intro paragraphs must be italicized using `*term*`.

#### DO

- `A *check* is *d20* + *trait rank* vs *DC*; equal or above is *success*.`

#### DO NOT

- `A check is d20 + trait rank vs DC; equal or above is success.`

### Rule: Per-term Decisions made and References; separators between terms

**Scanner:** Manual review

Every term block has its own `### Decisions made` (when modeling calls were made) and `### References` immediately after its behavioral lines, followed by `---`.

#### DO

- Place `### Decisions made` and `### References` per term, not bundled per KA.
- Follow each term block with `---`.

#### DO NOT

- Bundle all references at the end of the KA.
- Omit `---` separators between term blocks.

### Rule: Boundary terms have owners

**Scanner:** Manual review

Every `### boundary_term` heading under `# Boundary Domain` must carry `*(owned by: Module)*` naming exactly one owning module.

#### DO

- `### **content** *(owned by: Content Management)*`

#### DO NOT

- List multiple owning modules.
- Omit the `*(owned by: …)*` suffix.

### Rule: No class-level commitments

**Scanner:** Manual review

No UML stereotypes, typed properties, method signatures, or cardinality notation. Behavioral lines stay as plain prose.

#### DO

- Keep behavioral lines as plain prose bullets with *italicized domain terms*.

#### DO NOT

- Use `<<Entity>>`, typed properties, method signatures, or cardinality.
<!-- execute_rules:bundle_rules:end -->
