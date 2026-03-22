#!/usr/bin/env python3
"""Merge library + process + phases into AGENTS.md (explicit merge order).

Also writes the same bundle to ``content/built/AGENTS.md`` when ``delivery.mode`` is ``static_built``
(see ``docs/delivery.md``).
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "content" / "parts"
LIBRARY = PARTS / "library"
BUILT_DIR = ROOT / "content" / "built"

# Order matters: cross-cutting standards first, then index + §3, then builder summary.
LIBRARY_FILES = (
    "documentation-standards.md",
    "workspace-config.md",
    "delivery-modes.md",
    "process-approach.md",
    "authoring-checklist.md",
    "skill-repo-standards.md",
    "skill-standards-section-3.md",
    "builder-vs-operator.md",
)

PHASE_FILES = ("scaffold", "migrate")

BUILT_README = """# content/built/ — static_built outputs

This directory holds **pre-merged** agent instructions for **`static_built`** delivery.

| File | Role |
| --- | --- |
| **`AGENTS.md`** | Byte-for-byte same merge as repo root **`AGENTS.md`** produced by **`scripts/build.py`**. |

Sources and merge order: **`docs/delivery.md`**. Regenerate with:

```bash
python scripts/build.py
```
"""


def build_agents_text() -> str:
    chunks: list[str] = ["# AGENTS — abd-skill-builder\n\n"]

    process = (PARTS / "process.md").read_text(encoding="utf-8")
    chunks.append("## Process\n\n")
    chunks.append(process)
    chunks.append("\n")

    chunks.append("## Library (merged standards)\n\n")
    for name in LIBRARY_FILES:
        p = LIBRARY / name
        if not p.is_file():
            raise FileNotFoundError(f"Missing library file: {p.relative_to(ROOT)}")
        chunks.append(f"### Library: {name}\n\n")
        chunks.append(p.read_text(encoding="utf-8"))
        chunks.append("\n")

    for slug in PHASE_FILES:
        p = PARTS / "phases" / f"{slug}.md"
        chunks.append(f"\n## Phase: {slug}\n\n")
        chunks.append(p.read_text(encoding="utf-8"))

    return "".join(chunks)


def main() -> None:
    text = build_agents_text()
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


if __name__ == "__main__":
    main()
