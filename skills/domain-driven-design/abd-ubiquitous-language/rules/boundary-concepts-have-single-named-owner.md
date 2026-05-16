# Rule: Boundary concepts have a single named owning module

**Scanner:** Manual review

Every boundary entry under `# Boundary Domain` carries `Owned by: Module` (as a field line under the heading) naming exactly one module. Passing means every boundary entry has exactly one owner. Failing means the owner is missing, multiple owners are listed, or ownership is in body prose instead of the field line.

## DO

- Place `Owned by: {{module}}` as the first line after the `## boundary_concept` heading.

  **Example (pass):**
  ```
  ## Effect / power effect

  Owned by: Power

  - has a *rank* that determines the *resistance check* DC
  ```

- Name exactly one owning module.

  **Example (pass):** `Owned by: Power` — one module.

## DO NOT

- List multiple owning modules.

  **Example (fail):** `Owned by: Ability, Skill, Power` — three modules cannot all be the single source of truth.

- Omit the `Owned by:` field.

  **Example (fail):** `## power effect` with bullets but no `Owned by:` line.

- Put ownership in the heading instead of a field line.

  **Example (fail):** `## power effect *(owned by: Power)*` — ownership belongs on its own line below, not in the heading.

**Source:** Inherited from abd-domain-language — boundary terms have a single named owner.
