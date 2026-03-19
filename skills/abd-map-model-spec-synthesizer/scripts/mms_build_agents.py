#!/usr/bin/env python3
"""Build AGENTS.md from parts/*.md. Assembles process, domain, story-map, and step instructions."""
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent
_PARTS_DIR = _SKILL_DIR / "parts"
_OUTPUT_PATH = _SKILL_DIR / "AGENTS.md"

# Order: process overview first, then format specs, then step instructions
_CONTENT_ORDER = [
    "process.md",
    "domain.md",
    "story-map.md",
    "step1-discover.md",
    "step2-deepen.md",
    "step3-canonicalize.md",
    "step4-evidence.md",
    "step5-structure.md",
    "step6-finalize.md",
]


def build_agents(skill_path: Path | None = None) -> Path:
    """Assemble parts into AGENTS.md. Returns output path."""
    skill_path = skill_path or _SKILL_DIR
    skill_path = skill_path.resolve()
    parts_dir = skill_path / "parts"
    output_path = skill_path / "AGENTS.md"

    parts: list[str] = []
    for fname in _CONTENT_ORDER:
        p = parts_dir / fname
        if p.exists():
            parts.append(p.read_text(encoding="utf-8").strip())
            parts.append("\n\n---\n\n")

    text = "".join(parts).rstrip()
    if text.endswith("\n\n---"):
        text = text[:-4]
    output_path.write_text(text + "\n", encoding="utf-8")
    return output_path


if __name__ == "__main__":
    out = build_agents()
    print(f"Wrote {out}")
