"""Unit tests for library phase markers (section_markers)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from section_markers import filter_library_for_phase, has_phase_markers


def test_no_markers_returns_full_text() -> None:
    text = "# Hello\n\nNo markers here.\n"
    assert filter_library_for_phase(text, "plan-script-build") is text
    assert not has_phase_markers(text)


def test_none_phase_returns_full_text_even_with_markers() -> None:
    text = """# X
<!-- abd:begin plan-script-build -->
inner
<!-- abd:end plan-script-build -->
"""
    assert has_phase_markers(text)
    assert filter_library_for_phase(text, None) == text


def test_core_plus_matching_block() -> None:
    text = """# Core line

<!-- abd:begin plan-script-build -->
Only plan
<!-- abd:end plan-script-build -->

Tail
"""
    out = filter_library_for_phase(text, "plan-script-build")
    assert "Core line" in out
    assert "Only plan" in out
    assert "Tail" in out

    out_other = filter_library_for_phase(text, "scaffold")
    assert "Core line" in out_other
    assert "Only plan" not in out_other
    assert "Tail" in out_other


def test_end_must_match_current_begin() -> None:
    text = """<!-- abd:begin a -->
inside a
<!-- abd:end wrong -->
still inside until real end
<!-- abd:end a -->
"""
    out = filter_library_for_phase(text, "a")
    assert "inside a" in out
    assert "still inside until real end" in out

