---
name: domain-language
description: >-
  Build a shared, rigorous vocabulary for each module so every conversation,
  document, and artifact uses the same domain language without translation.
---
# domain-language

## Purpose

Build a shared, rigorous vocabulary for each module â€” the terms, behaviors, and rules that domain experts and modelers agree on â€” so that every conversation, document, and downstream artifact uses the same language without translation.

## When to use

- The user asks to "extract domain language," "define terms," "build the domain language," or "what does each term mean."
- The next modeling step needs defined term behavior â€” not just a flat name list.


## Core concepts

### Domain language

A shared, rigorous vocabulary agreed between domain experts and modelers — every term has one meaning used in conversations, documents, and code without translation. When the language changes, the model changes with it.

### What each term carries

A **term** is a named concept from the module's domain. For each term, the skill captures *what it does* â€” its behavior, interactions, rules, and flows â€” as short prose statements grounded in source material. Every claim traces back to the context it came from. The emphasis is on observable behavior and interactions, not just definitions or constraints.

### Boundary terms

A concept this module depends on but does not own. Another module is the single source of truth for it. If a term appears to be owned by multiple modules simultaneously, it is probably not a boundary term â€” it is a base abstraction that belongs in this module's Core terms.

### Found terms

Terms discovered in the source during extraction that were not in the original Core terms list but clearly belong to this module.

---

## Output file

The growing module file lives at `<workspace>/abd-domain-driven-design/modules/<module-name>.md`. Each skill phase enriches this same file in place â€” no separate output file per phase.

**Copy-output mode:** when the user says "copy output," write your additions to the growing file AND produce a snapshot at `<workspace>/abd-domain-driven-design/modules/<module-name>-domain-language.md`. The snapshot is read-only after creation.

## Build

1. **Start from the module file.** If `<module-name>.md` exists, enrich it in place. If not, create it with the module name, scope, and a Core terms list.
2. **Read all referenced context.** Follow the Ref entries in the module file and read the source material they point to. If the module has no Refs yet, read the source material the user provides or that the engagement makes available. Understand what each term means in context.
3. **Describe each Core term.** Expand each term into a `###` heading under `# Core Domain` containing two sub-sections: `#### Domain language` (short prose bullets describing behavior, interactions, rules, flows) and `#### References` (full Ref entries). Preserve the Core terms order.
4. **Trace each claim back to source.** Every statement about a term's behavior gets a Ref entry in `#### References` pointing to the context that evidences it.
5. **Add found terms.** Terms discovered during extraction that belong to this module go as `###` headings after all Core terms, before `# Boundary Domain`.
6. **Write boundary terms.** Concepts this module depends on but does not own go under `# Boundary Domain` as `##` headings, each with an `Owned by:` field, `#### Domain language` bullets, and `#### References`.
7. **Bump state** to `domain-language`.
8. **Write the file** back to the same path. Follow the template in `templates/domain-language-template.md`.

---

## Validate

After completion, check:

1. **Every Core term present.** Every term from the partition's Core terms list appears as a `###` heading under `# Core Domain`.
2. **Partition order preserved.** Core term headings follow the same sequence as the partition's bullet list.
3. **Behavior described per term.** Every `###` term has an `#### Domain language` section with at least one prose statement describing its behavior.
4. **Refs per term.** Every `###` term has an `#### References` section with at least one full-format Ref entry.
5. **Boundary terms have owners.** Every `##` heading under `# Boundary Domain` has an `Owned by:` field naming exactly one module.
6. **No multi-owner boundaries.** If a boundary term appears owned by multiple modules, it is a base abstraction â€” move to Core terms.
7. **State marker.** Front matter reads `state: domain-language`.
8. **No source gaps.** Every in-scope source slice is evidenced by at least one Ref entry somewhere in the file.

---

<!-- execute_rules:bundle_rules:begin -->
﻿---
scanner: all-core-terms-present
---

### Rule: All core terms present â€” every Core term from module-partition must appear

**Scanner:** `scanners/all-core-terms-present-scanner.py` â€” **`AllCoreTermsPresentScanner`**

Every term listed under `**Core terms**:` in the module-partition file (`abd-domain-driven-design/modules/<module>.md`) must appear as a `###` heading in the DL file (`abd-domain-driven-design/domain-language.md`) under the matching `# Module:` section. No term may be silently dropped.

#### DO

- For each module, read its Core terms list from the partition file and confirm every term appears as a `###` heading in the DL.

  **Example (pass):** Partition lists 27 Core terms; DL has 27 `###` headings in the Core terms section, each matching a partition bullet.

- Match terms case-insensitively (e.g., "Difficulty Class (DC)" matches `### Difficulty Class (DC)`).

  **Example (pass):** Partition bullet `- Difficulty Class (DC)` matches DL heading `### Difficulty Class (DC)`.

- Flag any Core term that has no matching `###` heading.

  **Example (pass):** Scanner reports "Core term 'routine check' missing as ### heading" â€” the agent adds the missing heading.

#### DO NOT

- Silently skip a Core term because it seems redundant or covered by another term's behavioral lines.

  **Example (fail):** The partition lists `routine check` but the DL has no `### routine check` heading â€” the agent decided it was "just a variant of check."

- Fold two Core terms into one heading without documenting the merge â€” each partition term gets its own heading.

  **Example (fail):** `### degree of success / degree of failure` as a single heading when the partition lists them separately.

- Assume found terms (terms discovered during extraction) substitute for missing Core terms â€” both must be present.

  **Example (fail):** `### critical hit` appears as a found term but `### critical hit` was already in the partition's Core terms list and is not present as a Core term heading.

### Rule: Boundary terms have owner — every boundary term must have an Owned by: field

**Scanner:** `scanners/boundary-terms-have-owner-scanner.py` — **`BoundaryTermsHaveOwnerScanner`**

Every `###` heading under the `## Boundary terms` section must have an `Owned by:` field line naming the single module that owns the concept. If a term is "owned by" multiple modules, it is not a boundary term — it is a base abstraction that belongs in Core terms.

#### DO

- Place `Owned by: {{module_name}}` as the first line after the `###` heading, before behavioral lines.

  **Example (pass):**
  ```
  ### Effect / power effect

  Owned by: Power

  - An effect is the basic building block of a power…
  ```

- Name exactly one owning module per boundary term.

  **Example (pass):** `Owned by: Power` — one module named.

- If you discover a boundary term is owned by multiple modules, move it to Core terms as a base abstraction.

  **Example (pass):** `Trait` initially listed as boundary with `Owned by: Ability, Skill, Power` — recognized as a base abstraction and moved to Core terms.

#### DO NOT

- Put the ownership in parentheses in the heading (e.g., `### Trait (owned by: Ability)`) — use a field line instead.

  **Example (fail):** `### Trait (owned by: Ability)` — ownership should be a field line, not in the heading.

- List multiple owning modules (e.g., `Owned by: Ability, Skill, Power`) — that means it's not a boundary term.

  **Example (fail):** `Owned by: Ability, Skill, Power` — if three modules own it, no single module is the source of truth; it is a base abstraction.

- Omit the `Owned by:` field from any boundary term.

  **Example (fail):** `### Action round structure` appears under `## Boundary terms` with behavioral lines and Refs but no `Owned by:` line.

### Rule: Refs per term — every term must carry at least one Ref entry

**Scanner:** `scanners/refs-per-term-scanner.py` — **`RefsPerTermScanner`**

Every `###` term heading in the DL file must be followed by at least one full-format Ref entry (`**Ref — …**` with `Source:`, `Locator:`, `Extract:` lines) before the next `###` heading. Refs are allocated per term, not collected in a separate inventory.

#### DO

- Place Ref entries directly after the behavioral lines of each term, before the next `###` heading.

  **Example (pass):**
  ```
  ### check

  - A check is d20 + trait rank vs DC; equal or above is success.

  **Ref — Game Play**
  Source: context/rules/HeroesHandbook-rules__chunk_009.md
  Locator: lines 809–874
  Extract: whole
  ```

- Use the full format for every Ref: `**Ref — title**`, `Source:`, `Locator:`, `Extract:`.

  **Example (pass):** All four fields present on every Ref entry.

- Ensure every term — Core terms, found terms, and boundary terms — has at least one Ref.

  **Example (pass):** Scanner reports zero terms without Refs.

#### DO NOT

- Collect Refs in a separate inventory section at the top of the file — they belong with the term they evidence.

  **Example (fail):** A `## References` section at the end lists all Refs by chunk number, with no connection to individual terms.

- Leave a term with behavioral lines but no Ref entry — every behavioral claim must be traceable.

  **Example (fail):** `### routine check` has three behavioral lines but no `**Ref —**` entry beneath them.

- Use an abbreviated inline format instead of the full format.

  **Example (fail):** `Refs: chunk_004 (lines 202–243)` — missing `Source:`, `Locator:`, `Extract:` structure.

﻿---
scanner: terms-in-partition-order
---

### Rule: Terms in partition order â€” Core terms must follow module-partition sequence

**Scanner:** `scanners/terms-in-partition-order-scanner.py` â€” **`TermsInPartitionOrderScanner`**

The `###` headings for Core terms in the DL file must appear in the same sequence as the `**Core terms**:` list in the module-partition file. Found terms (added during extraction) appear after all Core terms and before `## Boundary terms`. Boundary terms follow their own section.

#### DO

- Preserve the exact order of the partition's Core terms list when creating `###` headings.

  **Example (pass):** Partition lists `d20`, `check`, `Difficulty Class (DC)` in that order; DL headings appear in the same sequence.

- Place found terms (terms not in the partition list but discovered in the source) after the last Core term heading and before `## Boundary terms`.

  **Example (pass):** Core terms end with `### surprised`; found terms `### staggered` and `### incapacitated` appear next, then `## Boundary terms`.

#### DO NOT

- Reorder Core terms for thematic grouping â€” the partition order is the contract.

  **Example (fail):** Agent groups all condition terms together, moving `### dazed` before `### modifier` even though the partition lists modifier first.

- Interleave found terms among Core terms â€” found terms go after all Core terms.

  **Example (fail):** `### team check` (a found term) inserted between `### check` and `### Difficulty Class (DC)`.

- Place boundary terms before the `## Boundary terms` section marker.

  **Example (fail):** `### Effect / power effect` with `Owned by: Power` appears among the Core terms instead of under `## Boundary terms`.
<!-- execute_rules:bundle_rules:end -->
