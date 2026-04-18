# content/built/ — static_built outputs

This directory holds **pre-merged** agent instructions for **`static_built`** delivery.

| Path | Role |
| --- | --- |
| **`AGENTS.md`** | Byte-for-byte same merge as repo root **`AGENTS.md`** produced by **`scripts/base/build.py`**. |
| **`phases/<slug>.md`** | Per-phase snapshots for **`--mode static`** (see **`phases/README.md`**). |

Sources and merge order: **`README.md`** (Delivery & merge order). Regenerate with:

```bash
python scripts/base/build.py
```
