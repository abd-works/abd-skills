---
scanner: every-term-under-one-ka
---

# Rule: Every term accounted for — no drops

After key-abstractions enrichment, every term from the original `**Core terms**` bullet list must be accounted for in exactly one of three places:

1. As a `#### term` heading under exactly one `### KA` section inside `## Key Abstractions`.
2. As a `### term` heading under `## Boundary terms` (if the KA step determined the term is depended on but not owned by this module).
3. As an entry in the `**Moved to other modules**` list (if the KA step determined the term does not belong in this module at all), AND the destination module's `**Core terms**` bullet list must contain the term.

No term dropped, no term duplicated across KAs, no term vanished without a trace.

## DO

- Place every term that was under `## Core terms` in the UDL stage as a `#### term` heading under exactly one `### KA` section inside `## Key Abstractions`.

  **Example (pass):** `#### check`, `#### DC`, and `#### modifier` all appear under `### Check` and nowhere else.

- When a term is moved to another module, record it in the `**Moved to other modules**` list with its destination.

  **Example (pass):**
  ```
  **Moved to other modules**:
  - hero point → Combat
  - extra effort → Combat
  ```

  And `combat.md`'s `**Core terms**` list includes `hero point` and `extra effort`.

- Keep the `**Core terms**` bullet list in the module header as a reference inventory (minus moved terms).

## DO NOT

- Drop a term that existed in the UDL stage without recording where it went.

  **Example (fail):** `#### routine check` existed in UDL but does not appear under any `### KA` section, is not in `## Boundary terms`, and is not in the moved list.

- Place the same term under two different KAs.

  **Example (fail):** `#### modifier` appears under both `### Check` and `### Degree`.

- Record a moved term without actually adding it to the destination module.

  **Example (fail):** `- hero point → Combat` in the moved list, but `combat.md`'s Core terms does not include `hero point`.
