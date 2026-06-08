---
scanner: ka-term-count
---

# Rule: KA and term count — modules must have 4–7 KAs, each KA must have 4–7 terms

**Scanner:** `scanners/ka-term-count-scanner.py` — **`KaTermCountScanner`**

Every module file must contain 4–7 Key Abstraction headings (`## KAName`) under `# Core Domain`. Each KA must contain 4–7 subordinate term headings (`### term`). Boundary terms under `# Boundary Domain` are excluded from the per-KA count.

## DO

- Target 4–7 `## KAName` headings per module. If source supports fewer than 4, the module may be too narrow — consider merging with a neighbour. If source demands more than 7, the module may be too broad — consider splitting.

  **Example (pass):** A module has 5 KA headings under `# Core Domain`.

- Target 4–7 `### term` headings under each KA. If a KA has fewer than 4 terms, it may not justify its own KA — fold terms into a neighbouring KA. If a KA has more than 7 terms, it may cover two distinct concerns — split the KA.

  **Example (pass):** `## Check` has 5 subordinate terms: `### Difficulty Class (DC)`, `### degree of success`, `### degree of failure`, `### modifier`, `### critical success`.

- Every `## KAName` must have an intro paragraph opening with `*KAName* is …` — this paragraph is the KA's term definition.

  **Example (pass):**
  ```
  ## Check

  A *check* is the core resolution mechanic…
  ```

## DO NOT

- Create single-term KAs — a KA with only one `###` term is not a grouping.

  **Example (fail):** `## Damage` has only `### damage roll` beneath it.

- Create KAs with more than 7 terms without considering a split.

  **Example (fail):** `## Combat` has 12 `### term` headings — this likely covers multiple concerns.

- Count boundary terms toward any KA's term count — boundary terms live under `# Boundary Domain`, not under a KA.
