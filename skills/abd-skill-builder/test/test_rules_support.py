"""Unit tests for rules_support (phase rule stems + frontmatter strip)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "base"))

from rules import parse_rule_frontmatter, rule_body_text, stems_for_phase_rules  # noqa: E402


def test_parse_rule_frontmatter_strips_and_keeps_rule_id() -> None:
    raw = """---
rule_id: foo-bar
---
## Body

Hello.
"""
    meta, body = parse_rule_frontmatter(raw)
    assert meta.get("rule_id") == "foo-bar"
    assert "## Body" in body
    assert "Hello." in body


def test_rule_body_text() -> None:
    assert rule_body_text("# No frontmatter\n\nx") == "# No frontmatter\n\nx"


def test_stems_for_phase_rules_order_and_dedupe() -> None:
    cfg = {
        "every_phase_rules": ["a", "b", "a"],
        "phase_rules": {"p1": ["c", "b"], "p2": []},
    }
    assert stems_for_phase_rules(cfg, "p1") == ["a", "b", "c"]
    assert stems_for_phase_rules(cfg, "p2") == ["a", "b"]
    assert stems_for_phase_rules({}, "x") == []
