---
scanner: boundary-terms-have-owner
---

# Rule: Boundary terms have owner — every boundary term must have an Owned by: field

**Scanner:** `scanners/boundary-terms-have-owner-scanner.py` — **`BoundaryTermsHaveOwnerScanner`**

Every `###` heading under the `## Boundary terms` section must have an `Owned by:` field line naming the single module that owns the concept. If a term is "owned by" multiple modules, it is not a boundary term — it is a base abstraction that belongs in Core terms.

## DO

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

## DO NOT

- Put the ownership in parentheses in the heading (e.g., `### Trait (owned by: Ability)`) — use a field line instead.

  **Example (fail):** `### Trait (owned by: Ability)` — ownership should be a field line, not in the heading.

- List multiple owning modules (e.g., `Owned by: Ability, Skill, Power`) — that means it's not a boundary term.

  **Example (fail):** `Owned by: Ability, Skill, Power` — if three modules own it, no single module is the source of truth; it is a base abstraction.

- Omit the `Owned by:` field from any boundary term.

  **Example (fail):** `### Action round structure` appears under `## Boundary terms` with behavioral lines and Refs but no `Owned by:` line.
