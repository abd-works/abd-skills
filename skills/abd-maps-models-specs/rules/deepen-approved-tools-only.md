---
rule_id: deepen-approved-tools-only
phase_files:
  - deepen.md
---

## Deepen: approved tooling only

**Phase 6** — responsibilities, evidence, `depends_on`, cross-type structure.

Deepening is **reasoning-heavy**. You may use **chat**, **agent sessions**, or **small drivers** that the skill **documents** (see phase file and [`execution-and-success.md`](../content/parts/library/execution-and-success.md)).

If this repo adds a **pair-chat** or similar driver, it belongs **here** as an **approved** path with the same token/scope discipline as the phase doc—not as a rogue script that bypasses review.

When `scripts/` gains a deepen helper, this rule **does not** ban it—it bans **unapproved** automation. Update **`deepen.md`** and this file together when the approved surface changes.

**DO**

- Deepen through **documented** steps: phase instructions, approved chat sessions, or **`scripts/`** helpers that are reviewed like validators.

```text
deepen.md → approved tool list → edit map-model-spec / JSON per contract
```

**DON'T**

- Introduce **one-off merge scripts** that splice JSON **outside** the documented pipeline, or “fix” the model by **bulk string replace** without reconciling chunk evidence and story alignment.

```text
merge_maps.py --left a.json --right b.json  # not in repo docs / not approved
```

Unapproved merge—**violation** (hides provenance, breaks repeatability).
