---
name: module-partition
catalog_garden_tier: practice
catalog_garden_order: 1
catalogue_one_liner: >-
  Partition source corpus into modules by allocating file references; scope cut before modeling.
description: >-
  After domain scan, partition the source corpus into modules by allocating
  source file references to per-module index files. No classes, no anchors —
  only module boundaries and file references to the source that belongs to
  each. Supports an Unallocated bucket for pending decisions and a Rejected
  bucket for out-of-scope context. Use when the user asks to "partition the
  source", "allocate context to modules", "draw module boundaries", or needs
  a defensible scope cut before any class-level modeling.
---
# abd-module-partition

## Purpose

Produce a **root index** (`module-partition.md`) plus **per-module files** under `abd-domain-driven-design/modules/` — each containing scope, core terms, and **source file references** (not verbatim copies). No classes, no anchors, no UML, no stereotypes. Just boundaries and pointers to the source text that lives inside them.

This is the *scope cut* before any class identification. It answers a single question for every chunk of source: **which module does this text belong to** — or is it **unallocated** (pending) or **rejected** (out of scope)?

**Why references, not verbatim copies:** When the source is already structured as individually addressable files, copying their full content into the partition document is pure duplication. The partition's real value is the **allocation decision**. Downstream agents read the module file to get the file list, then read the actual source files as needed.

---

## Output file

**Deliverables folder:** `<active_skill_workspace>/abd-domain-driven-design/` — this is the **only** DDD skill that creates a sub-folder. See `../agent-protocol.md` for the general output file resolution convention.

**Files produced:**
- `abd-domain-driven-design/module-partition.md` — root index
- `abd-domain-driven-design/modules/<module-name>.md` — one per module
- `abd-domain-driven-design/modules/rejected.md` — rejected files with reasons
- `abd-domain-driven-design/modules/unallocated.md` — (optional) pending allocation decisions

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what module partitioning is, what is and is not a module (independence test, standalone-mechanic test, kind-mixing, single-noun naming), workspace and output shape, allocation rules, core terms, reference format, and tensions.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/module-partition-template.md` | Root index `module-partition.md` listing all modules with scope, core terms, chunk ranges, and links to per-module files. |
| `templates/module-file-template.md` | One file per module with scope, core terms, and source file references. Also `rejected.md` and optionally `unallocated.md`. |

**Source files on disk are the only allowed input.** Every `Source:` reference must point to a file the reviewer can open and verify. If no source files exist, **stop and tell the user**.

**Quality bar:** 4–10 top-level modules for the entire corpus. Every module passes the independence test and kind-test. Single-noun names. No kind-mixing. Source file references only — no verbatim content, no generated content. Every source file appears in exactly one allocation.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-module-partition \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Read the partition as a boundary reviewer — coverage and traceability.

- **Coverage** — every module file has at least one source reference. `rejected.md` exists. High and medium signal rows from scan results each appear somewhere.
- **Allocation discipline** — no source file in two modules (unless partial). Every partial has a `Part:` line. Every reference in unallocated/rejected has a `Reason:` line.
- **Boundary discipline** — module names are source-grounded. No generic placeholders. Nesting justified by source. `Also relates to:` flags present where the boundary is contested.
- **Core terms list** — every module has source-grounded noun phrases. No targets, values, evidence IDs, or stereotypes.
- **Kind-test** — every module names its kind in one word. Core terms cluster as one kind, not two vocabularies stuck together.
- **Standalone-mechanic test** — for procedural domains, no bag of co-located mechanisms.
- **Source references only** — no `Source: domain-knowledge` or other generated-content markers.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
