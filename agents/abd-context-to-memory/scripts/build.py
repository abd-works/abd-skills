#!/usr/bin/env python3
"""Build AGENTS.md from content/ parts.

Parts are concatenated in order with section headings:
  purpose.md  → ## Purpose
  outline.md  → ## Outline
  role.md     → ## Role
  process.md  → ## Process
"""
from pathlib import Path

AGENT_ROOT = Path(__file__).resolve().parents[1]
CONTENT = AGENT_ROOT / "content"
OUTPUT = AGENT_ROOT / "AGENTS.md"

PARTS = [
    ("Purpose", "purpose.md"),
    ("Outline", "outline.md"),
    ("Role", "role.md"),
    ("Process", "process.md"),
]


def build() -> None:
    sections: list[str] = ["# AGENTS — abd-context-to-memory\n"]
    for heading, filename in PARTS:
        path = CONTENT / filename
        if not path.exists():
            print(f"  SKIP  {filename} (not found)")
            continue
        body = path.read_text(encoding="utf-8").strip()
        sections.append(f"## {heading}\n\n{body}\n")
    OUTPUT.write_text("\n---\n\n".join(sections) + "\n", encoding="utf-8")
    print(f"  BUILT {OUTPUT.relative_to(AGENT_ROOT)}")


if __name__ == "__main__":
    build()
