#!/usr/bin/env python3
"""
Assemble OOAD instruction docs from library parts under content/parts/ and content/library/.

Merges:
- content/parts/*.md — core methodology documentation (step 0, step 1, extraction rules, etc.)
- content/library/*.md — constraints and requirements (abd-diagrams usage, actor tracking, etc.)

Same idea as abd-diagrams: library parts → AGENTS.md at skill root (IDEs load it).

Usage:
  python scripts/build_instructions.py
  python scripts/build_instructions.py --out path/to/custom.md
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "content" / "parts"
LIBRARY = ROOT / "content" / "library"

# Order matters: parts first (methodology), then library (constraints/requirements)
PART_FILES = [
    "domain-scan.md",
    "raw-candidate-list.md",
    "nouns-verbs-rules-and-states.md",
    "responsibilities-before-operations.md",
    "relationships-and-cardinality.md",
    "invariants-in-the-model.md",
    "model-state-transitions.md",
    "thing-vs-data-about-a-thing.md",
    "prefer-composition.md",
    "inheritance-when-behavior-generalizes.md",
    "abstract-classes-and-interfaces.md",
    "smashed-abstractions-and-hidden-roles.md",
    "watch-for-bloated-classes.md",
    "what-changes-together.md",
    "tension-as-a-signal.md",
    "add-properties-semantically-tight.md",
    "turn-verbs-into-operations.md",
    "refine-names.md",
    "iterative-refinement.md",
    "model-in-layers.md",
    "validate-with-scenarios.md",
]

LIBRARY_FILES = [
    "abd-diagrams-requirement.md",
]


def assemble_body() -> str:
    chunks: list[str] = []
    chunks.append(
        "# AGENTS — abd-ooad\n\n"
        "_Merged OOAD library from `content/parts/*.md` (methodology) and `content/library/*.md` (constraints). "
        "Edit those files, then run `python scripts/build_instructions.py`. "
        "**OOAD skill overview:** this skill's `SKILL.md`. "
        "**Diagram standards:** sibling **`abd-diagrams`** (`../abd-diagrams/AGENTS.md`)._\n\n"
        "---\n\n"
    )

    # Add parts (methodology)
    chunks.append("## Methodology\n\n")
    for name in PART_FILES:
        path = PARTS / name
        if path.is_file():
            chunks.append(f"<!-- source: content/parts/{name} -->\n\n")
            chunks.append(path.read_text(encoding="utf-8").strip())
            chunks.append("\n\n---\n\n")

    # Add library files (constraints/requirements)
    chunks.append("## Constraints & Requirements\n\n")
    for name in LIBRARY_FILES:
        path = LIBRARY / name
        if path.is_file():
            chunks.append(f"<!-- source: content/library/{name} -->\n\n")
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
    p = argparse.ArgumentParser(description="Merge content/parts/ + content/library/ OOAD docs into AGENTS.md.")
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
