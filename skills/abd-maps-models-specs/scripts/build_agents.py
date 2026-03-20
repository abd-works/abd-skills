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
    "context.md",
    "modules-epics.md",
    "concept-classification.md",
    "concept-classes-stories.md",
    "integrate-harmonize.md",
    "evidence.md",
    "structure.md",
    "finalize.md",
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
            content = p.read_text(encoding="utf-8").strip()
            # Rewrite same-dir links (e.g. [evidence](evidence.md)) to parts/ so they resolve from AGENTS.md
            for step in ("context", "modules-epics", "concept-classification", "concept-classes-stories",
                        "integrate-harmonize", "evidence", "structure", "finalize"):
                content = content.replace(f"]({step}.md)", f"](parts/{step}.md)")
            parts.append(content)
            parts.append("\n\n---\n\n")

    text = "".join(parts).rstrip()
    if text.endswith("\n\n---"):
        text = text[:-4]
    output_path.write_text(text + "\n", encoding="utf-8")
    return output_path


if __name__ == "__main__":
    out = build_agents()
    print(f"Wrote {out}")
