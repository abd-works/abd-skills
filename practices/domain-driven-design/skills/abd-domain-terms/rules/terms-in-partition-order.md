---
scanner: terms-in-partition-order
---

# Rule: Terms in partition order — Core terms must follow module-partition sequence

**Scanner:** `scanners/terms-in-partition-order-scanner.py` — **`TermsInPartitionOrderScanner`**

The `###` headings for Core terms in the DL file must appear in the same sequence as the `**Core terms**:` list in the module-partition file. Found terms (added during extraction) appear after all Core terms and before `## Boundary terms`. Boundary terms follow their own section.

## DO

- Preserve the exact order of the partition's Core terms list when creating `###` headings.

  **Example (pass):** Partition lists `d20`, `check`, `Difficulty Class (DC)` in that order; DL headings appear in the same sequence.

- Place found terms (terms not in the partition list but discovered in the source) after the last Core term heading and before `## Boundary terms`.

  **Example (pass):** Core terms end with `### surprised`; found terms `### staggered` and `### incapacitated` appear next, then `## Boundary terms`.

## DO NOT

- Reorder Core terms for thematic grouping — the partition order is the contract.

  **Example (fail):** Agent groups all condition terms together, moving `### dazed` before `### modifier` even though the partition lists modifier first.

- Interleave found terms among Core terms — found terms go after all Core terms.

  **Example (fail):** `### team check` (a found term) inserted between `### check` and `### Difficulty Class (DC)`.

- Place boundary terms before the `## Boundary terms` section marker.

  **Example (fail):** `### Effect / power effect` with `Owned by: Power` appears among the Core terms instead of under `## Boundary terms`.
