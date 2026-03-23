#!/usr/bin/env python3
"""Merge library + process + phases into AGENTS.md; write phases/built/*.md (derived).

Merge order and delivery policy: skill root ``README.md`` — Delivery & merge order.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from assembler import ContentAssembler, load_skill_config

BUILT_DIR = ROOT / "content" / "built"

BUILT_README = """# content/built/ — static_built outputs

This directory holds **pre-merged** agent instructions for **`static_built`** delivery.

| File | Role |
| --- | --- |
| **`AGENTS.md`** | Byte-for-byte same merge as repo root **`AGENTS.md`** produced by **`scripts/build.py`**. |

Sources and merge order: **`README.md`** (Delivery & merge order). Regenerate with:

```bash
python scripts/build.py
```
"""

PHASES_BUILT_README = """# parts/phases/built/ — derived per-phase prompts

Files here are **generated** by **`scripts/build.py`**. Sources of truth: **`skill-config.json`**
(`PHASE_LIBRARY_SLICES`, `phase_rules`, …) and **`parts/`** / **`rules/`**.

Regenerate:

```bash
python scripts/build.py
```

**Runtime:** `python scripts/generate_prompt.py --phase <slug> --mode static` reads these files when present; otherwise assembles from sources (`dynamic`).
"""


def main() -> None:
    cfg = load_skill_config(ROOT)
    asm = ContentAssembler(ROOT, cfg)
    text = asm.build_agents_text()
    out = ROOT / "AGENTS.md"
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")

    BUILT_DIR.mkdir(parents=True, exist_ok=True)
    built_agents = BUILT_DIR / "AGENTS.md"
    built_agents.write_text(text, encoding="utf-8")
    print(f"Wrote {built_agents.relative_to(ROOT)}")

    built_readme = BUILT_DIR / "README.md"
    built_readme.write_text(BUILT_README, encoding="utf-8")
    print(f"Wrote {built_readme.relative_to(ROOT)}")

    parts = asm.parts
    built_phase_dir = parts / "phases" / "built"
    built_phase_dir.mkdir(parents=True, exist_ok=True)
    for p in asm.write_built_phases(built_phase_dir):
        print(f"Wrote {p.relative_to(ROOT)}")
    (built_phase_dir / "README.md").write_text(PHASES_BUILT_README, encoding="utf-8")
    print(f"Wrote {(built_phase_dir / 'README.md').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
