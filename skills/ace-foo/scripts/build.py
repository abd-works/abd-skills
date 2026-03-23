#!/usr/bin/env python3
"""Merge process + phases + library into AGENTS.md (abd-skill-builder–style layout).

Merge order: ``process.md`` → each ``PHASE_FILES`` slug → each ``LIBRARY_FILES`` shard.
Document changes in ``README.md`` if you alter this order.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "content" / "parts"

LIBRARY_FILES = (
    "core-definitions.md",
    "intro.md",
    "output-structure.md",
    "shaping-process.md",
    "validation.md",
    "script-invocation.md",
)

PHASE_FILES = ("workspace-and-config",)


def main() -> None:
    chunks: list[str] = ["# AGENTS — ace-foo\n\n", "## Process\n\n"]
    chunks.append((PARTS / "process.md").read_text(encoding="utf-8"))
    chunks.append("\n")
    for slug in PHASE_FILES:
        p = PARTS / "phases" / f"{slug}.md"
        chunks.append("\n")
        chunks.append(p.read_text(encoding="utf-8"))
    chunks.append("\n## Library\n\n")
    for name in LIBRARY_FILES:
        chunks.append((PARTS / "library" / name).read_text(encoding="utf-8"))
        chunks.append("\n\n")
    out = ROOT / "AGENTS.md"
    out.write_text("".join(chunks), encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
