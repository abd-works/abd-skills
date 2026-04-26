---
name: extract-domain-logic
description: >-
  Per-module domain logic as short prose lines (behavior, interactions, rules).
  Flexible order vs key-abstraction-identification. Anti-drift: seed new file
  by copying upstream artifact then refine. Output: abd-ooad/extracted-domain-logic.md.
  Use before object-sketch when the team splits logic extraction from sketching.
---

# extract-domain-logic

## Purpose

Produce **`extracted-domain-logic.md`**: for each **`## Module: [...]`**, **how that slice of the domain behaves** in **short lines of plain prose**—outcome-changing rules, flows, handoffs between actors or ideas, structure—readable by a non-technical reviewer and checkable against the real source.

This skill is **not** key-abstraction settlement and **not** object sketching. It consolidates **module-level domain logic** so **`object-sketch`** (or a parallel pass) can hang **concepts** on agreed mechanics without inventing behavior in the sketch.

## Pipeline position (flexible)

Rough progression by **context size**: **`module-partitioning`** (coarse scope cut) **`key-abstraction-identification`** (named units, smaller window) **`extract-domain-logic`** (module behavior lines) **`object-sketch`** (concepts + extracts).

The engagement may run **`extract-domain-logic` before or after `key-abstraction-identification`**; both orders are valid. It always assumes **`module-partitioning.md`** and/or **`key-abstractions.md`** may exist, plus access to authoritative source.

## Anti-drift handoff (always first when the output is new)

When **`abd-ooad/extracted-domain-logic.md` does not exist** yet:

1. **Pick a seed file** (team choice; if unstated: use **`key-abstractions.md`** if it exists, otherwise **`module-partitioning.md`**).
2. **Copy the entire seed file** into **`abd-ooad/extracted-domain-logic.md`** as the **first persisted version** (full duplicate so nothing is silently dropped).
3. **Refine** that copy toward this skill's shape (**`templates/extracted-domain-logic-template.md`**): preserve **`## Module:`** order; ensure each module has **`### Extract`** (inventory bullets with **`Source:`** / **`Locator:`**) and **`## Domain-logic`** (short lines). Fold or remove shapes that belong only to the seed (for example Key Abstraction subsections) **without losing** traceability—domain-logic lines must still be defensible from the seed or corpus.

**Canon:** When this skill completes, **`extracted-domain-logic.md`** is the **authoritative hand-off for module-level domain logic** into **`object-sketch`**. Upstream files remain for **history and audit**; for overlapping content, **downstream work follows this file**, not a stale duplicate in an older artifact.

## Inputs / outputs

| Input | Output |
| --- | --- |
| `abd-ooad/module-partitioning.md` and/or `abd-ooad/key-abstractions.md`, plus source as needed | `abd-ooad/extracted-domain-logic.md` |

## Agent instructions

1. If **`extracted-domain-logic.md`** is missing, run **Anti-drift handoff** before substantive edits.
2. Emit using **`templates/extracted-domain-logic-template.md`**; set **Seed:** in the header to the file that was copied first.
3. **Domain-logic lines** favor **interactions and behavior**, not only hard constraints; one main idea per line where possible.
4. **`[Unallocated]`** / **`[Rejected]`** modules follow the same pattern when the engagement uses them.

## Validate

- Header has **Scope**, **Sources**, and **Seed:**.
- Every in-scope **`## Module:`** opens with **`### Extract`**, then **`## Domain-logic`**, or documents **`Reason:`** when intentionally thin.
- No in-scope source slice disappears: inventory bullets or domain-logic lines point to evidence.

## Hand-off

**`object-sketch`** seeds from **`extracted-domain-logic.md`** when present (see **`object-sketch`**). **`elaborate-business-logic`** later still produces post-CRC **`business-logic.md`** (lifecycle / invariants); that file name is **not** this artifact.

---

<!-- execute_rules:bundle_rules:begin -->
<!-- No rules/*.md for this skill yet. -->
<!-- execute_rules:bundle_rules:end -->
