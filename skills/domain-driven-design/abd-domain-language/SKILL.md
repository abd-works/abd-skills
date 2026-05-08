---
name: domain-language
catalog_garden_order: 2
description: >-
  Build a shared, rigorous vocabulary for each module so every conversation,
  document, and artifact uses the same domain language without translation.
---
# domain-language

## Purpose

Build a shared, rigorous vocabulary for each module — the terms, behaviors, and rules that domain experts and modelers agree on — so that every conversation, document, and downstream artifact uses the same language without translation.

## When to use

- The user asks to "extract domain language," "define terms," "build the domain language," or "what does each term mean."
- The next modeling step needs defined term behavior — not just a flat name list.

---

## Core concepts

### Domain language

A shared, rigorous vocabulary agreed between domain experts and modelers — every term has one meaning used in conversations, documents, and code without translation. When the language changes, the model changes with it.

### What each term carries

A **term** is a named concept from the module's domain. For each term, the skill captures *what it does* — its behavior, interactions, rules, and flows — as short prose statements grounded in source material. Every claim traces back to the context it came from.

### Boundary terms

A concept this module depends on but does not own. Another module is the single source of truth for it. If a term appears to be owned by multiple modules simultaneously, it is probably not a boundary term — it is a base abstraction that belongs in this module's Core terms.

### Found terms

Terms discovered in the source during extraction that were not in the original Core terms list but clearly belong to this module. They appear inline among Core terms in the order they were discovered (or alphabetically), not in a separate section.

---

## Output file

This skill produces a **standalone, self-contained file** at:

```
<deliverables-folder>/[<name>-]domain-language.md
```

**File name:** Default to `domain-language.md`. Add a `<name>-` engagement prefix only when you need disambiguation — multiple products living in the same workspace, or the user asks for it explicitly. Both `domain-language.md` and `<name>-domain-language.md` are valid. For multi-module engagements (with `abd-module-partition` output), the module name is the disambiguator: `<deliverables-folder>/modules/<module-name>-domain-language.md`.

The file is **not enriched in place** by later phase skills. Each later phase skill (`abd-key-abstractions`, `abd-domain-sketch`, `abd-class-responsibility-collaborator`, `abd-object-model`) writes its own file using the **same flat heading shape** so the deliverables stay in sync without copy-merge contortion.

**Resolving `<deliverables-folder>`** — pick in this order:

1. **The path the user told you to use.** If the user names a file or folder, use exactly that.
2. **Where the engagement already keeps deliverables.** Look at the workspace; if previous phase output (or other engagement docs like `story-map.md`, `process.md`, `corrections-log.md`) already lives in a folder, write next to them in the **same** folder.
3. **The workspace root.** If neither applies, write to the workspace root.

Do **not** assume a predetermined folder name like `domain/` or `stories/`. The only DDD/story skill that creates a sub-folder is **`abd-module-partition`**, which deliberately uses `modules/<module-name>-…` to carve a partition.

For a multi-module engagement (with `abd-module-partition` output), use `<deliverables-folder>/modules/<module-name>-domain-language.md` — i.e. the `modules/` sub-folder lives **inside** the resolved `<deliverables-folder>`.

---

## Consistent shape (used by every DDD phase skill)

```
## **{{KAName}}**            (h2 — only present from key-abstractions onwards)

[Optional intro paragraph]

### **{{term / concept / class / object}}**    (h3 — name evolves stage-to-stage)
- bullet (content depends on the phase)
- bullet

### **{{another term}}**
- bullet

### references                                  (h3 — peer to terms; one per KA)
**Ref — title**
Source: ...
Locator: ...
Extract: whole

```source
verbatim
```
```

In the **domain-language** phase no KAs have been identified yet, so the file uses the same shape **without** the `## **KA**` wrapper:

```
# Core Domain

### **term**
- behavioral line
- behavioral line

### **another term**
- behavioral line

### references
**Ref — title**
Source: ...
Locator: ...
Extract: whole

```source
verbatim
```
```

The key-abstractions phase later wraps these terms in `## **KA**` groups.

---

## Build

1. **Read the source context.** Read the source material the user provides or that the engagement makes available. If a `<deliverables-folder>/<name>-module-partition.md` exists, follow its `**Core terms**` list and Refs.
2. **List Core terms in the header.** The file header carries a `**Core terms**:` flat bullet list — the inventory.
3. **Describe each Core term.** For each term, write a `### **term**` heading directly under `# Core Domain` with verb-light behavioral bullets (no sub-headings). Cover behavior, interactions, rules, and flows. Add found terms inline if discovered during extraction.
4. **Add a single `### references` section** after the last Core term, listing all `**Ref —**` entries with full `Source:`, `Locator:`, `Extract:` fields and a fenced `source` block of verbatim text beneath each.
5. **Write boundary terms.** Concepts this module depends on but does not own go under `# Boundary Domain` as `### **boundary_term** *(owned by: Module)*` headings, each followed by behavioral bullets. A single `### references` section closes the section.
6. **Set the state marker** to `domain-language`.
7. **Write the file** to `<deliverables-folder>/<name>-domain-language.md`. Follow the template in `templates/domain-language-template.md`.

---

## Validate

1. **Per-phase output file.** The file is named `<name>-domain-language.md`, not `<name>.md`. No prior or later phase content lives in this file.
2. **Every Core term present.** Every term from the `**Core terms**` list appears as a `### **term**` heading.
3. **Behavior described per term.** Every `### **term**` has at least one behavioral bullet.
4. **References present.** A single `### references` section exists in `# Core Domain` with at least one full-format Ref entry, each backed by a fenced `source` block of verbatim text.
5. **Boundary terms have owners.** Every `### **boundary_term**` heading carries `*(owned by: Module)*` naming exactly one owning module.
6. **No multi-owner boundaries.** If a boundary term is "owned by" multiple modules, it is a base abstraction — move to Core.
7. **State marker.** Front matter reads `state: domain-language`.
8. **No sub-headings under terms.** Bullets live directly under each `### **term**` heading — no `#### Domain Language`, `#### References`, or other sub-sections.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Per-phase file with consistent flat shape

**Scanner:** Manual review

The domain-language skill writes a self-contained file at `<deliverables-folder>/<name>-domain-language.md` (or `<deliverables-folder>/modules/<module-name>-domain-language.md` for multi-module engagements). The file uses the consistent flat heading shape every DDD phase skill shares: `### **term**` directly under `# Core Domain`, with bullets directly beneath the heading and a single `### references` section per group. No sub-headings (`#### Domain Language`, `#### References`) appear under terms.

#### DO

- Write the file to `<deliverables-folder>/<name>-domain-language.md`.

  **Example (pass):** `domain/paw-place-domain-language.md`.

- Place behavioral bullets directly under the `### **term**` heading.

  **Example (pass):**
  ```
  ### **product**
  - A product is a pet supply item available for purchase.
  - Every product has images, a description, and weight or dimensions where relevant.
  ```

- Use one `### references` section per group (Core Domain block, Boundary Domain block).

  **Example (pass):**
  ```
  ### **product**
  - bullet

  ### **category**
  - bullet

  ### references
  **Ref — Product catalog and browsing**
  …
  ```

#### DO NOT

- Enrich a single growing file (`<name>.md`) that subsequent phase skills modify in place.

  **Example (fail):** `paw-place.md` written at `state: domain-language`, then `state: key-abstractions`, then `state: domain-sketch` — phase-to-phase heading drift becomes irrecoverable.

- Insert sub-headings under terms.

  **Example (fail):**
  ```
  ### **product**

  #### Domain Language
  - bullet

  #### References
  **Ref —** …
  ```
  Bullets and refs belong directly under their parent — no `#### Domain Language` or `#### References` sub-headings.

**Source:** Engagement convention (DDD phase-skill simplification).

### Rule: All Core terms present — every term in the list appears as a `### **term**`

**Scanner:** Manual review

Every term listed in the file header `**Core terms**:` bullet list must appear as a `### **term**` heading under `# Core Domain`. No term may be silently dropped.

#### DO

- For each `**Core terms**:` bullet, write a matching `### **term**` heading under `# Core Domain`.

  **Example (pass):** Header lists 24 Core terms; the file has 24 `### **term**` headings under Core Domain.

- Match terms case-insensitively (e.g. `### **Difficulty Class (DC)**` matches the bullet `- Difficulty Class (DC)`).

#### DO NOT

- Silently skip a Core term because it seems redundant or covered by another term's bullets.

  **Example (fail):** Header lists `routine check` but no `### **routine check**` heading appears.

- Fold two Core terms into one heading without documenting the merge — each term gets its own heading.

  **Example (fail):** `### **degree of success / degree of failure**` as one heading when the partition lists them separately.

**Source:** Inherited from the original `all-core-terms-present` rule.

### Rule: Boundary terms have owner — every boundary term names exactly one owning module

**Scanner:** Manual review

Every `### **boundary_term**` heading under `# Boundary Domain` must carry `*(owned by: Module)*` naming exactly one owning module. If a term appears owned by multiple modules, it is a base abstraction — move to Core.

#### DO

- Place `*(owned by: Module)*` in italics directly inside the `### **boundary_term**` heading.

  **Example (pass):**
  ```
  ### **content** *(owned by: Content Management)*
  - bullet
  ```

- Name exactly one owning module per boundary term.

  **Example (pass):** `*(owned by: Power)*`

#### DO NOT

- List multiple owning modules.

  **Example (fail):** `### **trait** *(owned by: Ability, Skill, Power)*` — if three modules own it, no single module is the source of truth; it is a base abstraction.

- Omit the owning module suffix.

  **Example (fail):** `### **action round structure**` under `# Boundary Domain` with no `*(owned by: …)*`.

**Source:** Inherited from the original `boundary-terms-have-owner` rule.

### Rule: Refs grouped at the section level, with verbatim source blocks

**Scanner:** Manual review

References live in a single `### references` section per group (Core Domain block, Boundary Domain block, or per-KA block in later phases). Every `**Ref —**` entry carries `Source:`, `Locator:`, `Extract:` fields and is followed by a fenced ```source``` block containing verbatim text from disk.

#### DO

- Place all Refs in one `### references` section per group, after the term headings.

  **Example (pass):**
  ```
  ### **check**
  - bullet

  ### **DC**
  - bullet

  ### references

  **Ref — Game Play**
  Source: context/rules/HeroesHandbook-rules__chunk_009.md
  Locator: lines 809–874
  Extract: whole

  ```source
  GAME PLAY
  …verbatim text…
  ```
  ```

- Include a fenced ```source``` block with verbatim text under every Ref.

#### DO NOT

- Put `#### References` sub-headings under each term.

  **Example (fail):**
  ```
  ### **check**
  - bullet

  #### References
  **Ref — …**
  ```

- Leave a Ref entry without a fenced source block.

  **Example (fail):** Ref entry followed immediately by the next `### **term**` heading with no source block.

**Source:** Inherited and adapted from the original `refs-per-term` rule.
<!-- execute_rules:bundle_rules:end -->
