#!/usr/bin/env python3
"""Build AGENTS.md from agents/abd-context-to-memory/reference/.

Section order and headings come from skill-config.json → agents_md.sections.
Edit the markdown files under reference/ only; do not hand-edit AGENTS.md.
"""
from __future__ import annotations

import json
from pathlib import Path

AGENT_ROOT = Path(__file__).resolve().parents[1]
CONTENT = AGENT_ROOT / "reference"
OUTPUT = AGENT_ROOT / "AGENTS.md"
CONFIG_PATH = AGENT_ROOT / "skill-config.json"

_DEFAULT_SECTIONS: list[dict[str, str]] = [
    {"heading": "Purpose", "file": "purpose.md"},
    {"heading": "Outline", "file": "outline.md"},
    {"heading": "Workspace (topic root) — config first", "file": "workspace.md"},
    {"heading": "Role", "file": "role.md"},
    {"heading": "Checklist", "file": "checklist.md"},
    {"heading": "Process", "file": "process.md"},
]


def _load_sections() -> tuple[str, list[dict[str, str]]]:
    if not CONFIG_PATH.is_file():
        return "abd-context-to-memory", list(_DEFAULT_SECTIONS)
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    agents_md = data.get("agents_md") or {}
    title = str(agents_md.get("title") or data.get("name") or "abd-context-to-memory")
    sections = agents_md.get("sections")
    if not isinstance(sections, list) or not sections:
        return title, list(_DEFAULT_SECTIONS)
    out: list[dict[str, str]] = []
    for item in sections:
        if not isinstance(item, dict):
            continue
        h, f = item.get("heading"), item.get("file")
        if isinstance(h, str) and isinstance(f, str) and h.strip() and f.strip():
            out.append({"heading": h.strip(), "file": f.strip()})
    return title, (out if out else list(_DEFAULT_SECTIONS))


def build() -> None:
    title, sections = _load_sections()
    parts: list[str] = [
        f"# AGENTS — {title}\n\n"
        "> **Maintain in `reference/` only.** Edit the `.md` files there, then run `python scripts/build.py` from this agent’s root. Do not hand-edit this file.\n"
    ]
    for spec in sections:
        heading = spec["heading"]
        filename = spec["file"]
        path = CONTENT / filename
        if not path.is_file():
            print(f"  SKIP  {filename} (not found)")
            continue
        body = path.read_text(encoding="utf-8").strip()
        parts.append(f"## {heading}\n\n{body}\n")
    OUTPUT.write_text("\n---\n\n".join(parts) + "\n", encoding="utf-8")
    print(f"  BUILT {OUTPUT.relative_to(AGENT_ROOT)} ({len(parts) - 1} sections)")


if __name__ == "__main__":
    build()
