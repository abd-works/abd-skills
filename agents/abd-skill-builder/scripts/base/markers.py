"""
markers — two kinds of HTML-comment markers used in skill content files.

Phase-scope markers (abd:begin / abd:end):
    <!-- abd:begin <phase-slug> -->
    ... phase-specific content ...
    <!-- abd:end <phase-slug> -->

When assembling instructions for *phase-slug*:
  - Include all lines outside any begin/end pair (shared "core"), and
  - Include lines inside a pair whose slug equals *phase-slug*.
  - Marker lines themselves are never emitted.

Section markers (section: / /section:):
    <!-- section: name -->
    ... content ...
    <!-- /section: name -->

Extract named sections from library or template files.
"""
from __future__ import annotations

import re
from pathlib import Path

# --- phase markers -----------------------------------------------------------

_BEGIN = re.compile(r"^\s*<!--\s*abd:begin\s+([a-zA-Z0-9\-_]+)\s*-->\s*$")
_END = re.compile(r"^\s*<!--\s*abd:end\s+([a-zA-Z0-9\-_]+)\s*-->\s*$")
_ANY_BEGIN = re.compile(r"<!--\s*abd:begin\s+")


def has_phase_markers(text: str) -> bool:
    return _ANY_BEGIN.search(text) is not None


def filter_library_for_phase(text: str, phase_slug: str | None) -> str:
    """Return a slice of *text* for the given assembly phase.

    If *phase_slug* is None or *text* has no phase markers, returns *text* unchanged.
    """
    if phase_slug is None or not has_phase_markers(text):
        return text

    lines = text.splitlines(keepends=True)
    out: list[str] = []
    current: str | None = None

    for line in lines:
        m_begin = _BEGIN.match(line)
        if m_begin:
            current = m_begin.group(1)
            continue
        m_end = _END.match(line)
        if m_end:
            if current is not None and m_end.group(1) == current:
                current = None
            continue
        if current is None or current == phase_slug:
            out.append(line)

    return "".join(out)


# --- section markers ---------------------------------------------------------

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
