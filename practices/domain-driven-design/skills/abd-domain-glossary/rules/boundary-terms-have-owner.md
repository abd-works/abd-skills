---
scanner: boundary-terms-have-owner
---

# Rule: Boundary terms have owner — every boundary term must name its owning module

**Scanner:** `scanners/boundary-terms-have-owner-scanner.py` — **`BoundaryTermsHaveOwnerScanner`**

Every `###` heading under the `# Boundary Domain` section must include `*(owned by: ModuleName)*` naming the single module that owns the concept. If a term is owned by multiple modules, it is not a boundary term — it is a base abstraction that belongs in Core Domain.

## DO

- Include ownership in the heading: `### term *(owned by: ModuleName)*`.

  **Example (pass):**
  ```
  ### Power Effect *(owned by: Power)*

  - A *power effect* sets the *DC* for resistance *checks*.
  ```

- Name exactly one owning module per boundary term.

  **Example (pass):** `### Trait *(owned by: Ability)*` — one module named.

- If you discover a boundary term is owned by multiple modules, move it to Core Domain as a base abstraction.

  **Example (pass):** `Trait` initially listed as boundary with multiple owners — recognized as a base abstraction and moved to Core Domain.

## DO NOT

- Omit the ownership annotation from any boundary term heading.

  **Example (fail):** `### Action round structure` appears under `# Boundary Domain` with no `*(owned by: …)*`.

- List multiple owning modules — that means it's not a boundary term.

  **Example (fail):** `### Trait *(owned by: Ability, Skill, Power)*` — if three modules own it, no single module is the source of truth.
