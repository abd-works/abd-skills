# Content placement (abd-skill-builder)

**Rule:** Normative, mergeable bodies for this skill live under **`content/parts/`**, not under **`docs/`**.

| Location | Purpose |
|----------|---------|
| **`content/parts/library/`** | Cross-cutting standards: documentation voice, workspace keys, delivery modes, authoring checklist, skill repo index, full §3 copy, builder vs operator summary. **`scripts/build.py`** merges these into **`AGENTS.md`** in a fixed order. |
| **`content/parts/phases/`** | Phase markdown (e.g. **`scaffold.md`**, **`migrate.md`**) — sequenced work units. |
| **`content/parts/process.md`** | Process table + pipeline overview; links into **`library/`** and **`phases/`**. |
| **`rules/`** | Governance rules (this file, scanners binding) — **not** merged as full library bodies unless you explicitly add them to **`build.py`**. |
| **`docs/`** | **Non-runtime** only: planning deltas (**`standards-delta.md`**), short **stubs** pointing at **`content/parts/library/`** for humans browsing the repo, and copies like **`docs/authoring-checklist.md`** in **other** skills. |

**Do not** put instruction bodies that **`build.py`** must merge only under **`docs/`** — move them to **`library/`** or **`phases/`** and leave **`docs/`** as index or narrative.
