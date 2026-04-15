"""
Phase-scoped slices for library markdown.

HTML comments pair as:
  <!-- abd:begin <phase-slug> -->
  ... content ...
  <!-- abd:end <phase-slug> -->

When assembling instructions for *phase-slug*, include:
  - every line outside any begin/end pair (the shared "core"), and
  - lines inside a pair whose slug equals *phase-slug*.

Lines inside other slugs' pairs are omitted. Marker lines themselves are never emitted.

*phase-slug* should match a name from skill-config ``phase_files`` (e.g. ``plan-script-build``).
If the file has no ``abd:begin`` markers, the full text is returned unchanged.
"""

from __future__ import annotations

import re

_BEGIN = re.compile(r"^\s*<!--\s*abd:begin\s+([a-zA-Z0-9\-_]+)\s*-->\s*$")
_END = re.compile(r"^\s*<!--\s*abd:end\s+([a-zA-Z0-9\-_]+)\s*-->\s*$")
_ANY_BEGIN = re.compile(r"<!--\s*abd:begin\s+")


def has_phase_markers(text: str) -> bool:
    return _ANY_BEGIN.search(text) is not None


def filter_library_for_phase(text: str, phase_slug: str | None) -> str:
    """Return a slice of *text* for the given assembly phase.

    If *phase_slug* is None (e.g. ``agents_front``), or *text* has no phase markers,
    returns *text* unchanged.
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
