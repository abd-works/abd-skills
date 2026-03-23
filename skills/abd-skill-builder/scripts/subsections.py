"""Extract markdown subsections by HTML comment markers."""

from __future__ import annotations

from pathlib import Path


def extract_section(text: str, section_name: str) -> str | None:
    """Return content between ``<!-- section: name -->`` and ``<!-- /section: name -->``."""
    start_marker = f"<!-- section: {section_name} -->"
    end_marker = f"<!-- /section: {section_name} -->"
    if start_marker not in text:
        return None
    start = text.index(start_marker) + len(start_marker)
    if end_marker in text:
        end = text.index(end_marker, start)
        return text[start:end].strip()
    return text[start:].strip()


def extract_section_from_file(path: Path, section_name: str) -> str | None:
    """Read *path* and extract *section_name*."""
    if not path.is_file():
        return None
    return extract_section(path.read_text(encoding="utf-8"), section_name)
