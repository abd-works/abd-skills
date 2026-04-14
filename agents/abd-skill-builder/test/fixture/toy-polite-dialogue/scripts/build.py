#!/usr/bin/env python3
"""Toy build: merge process + phases into AGENTS.md (no external engine)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "content" / "parts"


def main() -> None:
    process = (PARTS / "process.md").read_text(encoding="utf-8")
    chunks = ["# AGENTS — toy-polite-dialogue\n", "\n", "## Process\n\n", process, "\n"]
    for name in ("greet", "introduce", "converse", "close"):
        p = PARTS / "phases" / f"{name}.md"
        chunks.append(f"\n## Phase: {name}\n\n")
        chunks.append(p.read_text(encoding="utf-8"))
    out = ROOT / "AGENTS.md"
    out.write_text("".join(chunks), encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
