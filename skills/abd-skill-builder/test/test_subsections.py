"""Unit tests for subsections.extract_section."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from subsections import extract_section  # noqa: E402


def test_extract_section_basic() -> None:
    text = """# Doc

<!-- section: foo -->
inner
<!-- /section: foo -->

tail
"""
    assert extract_section(text, "foo") == "inner"


def test_extract_section_missing() -> None:
    assert extract_section("no markers", "foo") is None
