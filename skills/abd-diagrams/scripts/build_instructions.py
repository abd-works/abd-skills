#!/usr/bin/env python3
"""
Assemble diagram instruction docs from the four library parts under content/parts/.

Same idea as abd-skill-builder: library parts → AGENTS.md at the skill root (IDEs load it).

Usage:
  python scripts/build_instructions.py
  python scripts/build_instructions.py --out path/to/custom.md
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "content" / "parts"

PART_FILES = [
    "class-diagrams.md",
    "class-diagram-layout-rules.md",
    "sequence-diagrams.md",
    "sequence-diagram-layout-rules.md",
]


def assemble_body() -> str:
    chunks: list[str] = []
    chunks.append(
        "# AGENTS — abd-diagrams\n\n"
        "_Merged diagram library from `content/parts/*.md`. Edit those four files, then run "
        "`python scripts/build_instructions.py`. **Diagram skill overview:** this skill’s "
        "`SKILL.md`. **Linear OOAD walkthrough** (from raw material): sibling **`abd-ooad`** "
        "(`../abd-ooad/SKILL.md`)._\n\n"
        "---\n\n"
    )
    for name in PART_FILES:
        path = PARTS / name
        if not path.is_file():
            raise FileNotFoundError(path)
        chunks.append(f"<!-- source: content/parts/{name} -->\n\n")
        chunks.append(path.read_text(encoding="utf-8").strip())
        chunks.append("\n\n---\n\n")
    return "".join(chunks).rstrip() + "\n"


def build(out_path: Path | None = None) -> list[Path]:
    text = assemble_body()
    written: list[Path] = []

    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        written.append(out_path)
        return written

    # Default: skill root (what you open in the repo) + mirror under content/built/
    built_dir = ROOT / "content" / "built"
    built_dir.mkdir(parents=True, exist_ok=True)

    for path in (ROOT / "AGENTS.md", built_dir / "AGENTS.md"):
        path.write_text(text, encoding="utf-8")
        written.append(path)

    return written


def main() -> None:
    p = argparse.ArgumentParser(description="Merge content/parts diagram library into AGENTS.md.")
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Single output path (optional; default writes AGENTS.md at root and content/built/)",
    )
    args = p.parse_args()
    paths = build(out_path=args.out)
    for path in paths:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
