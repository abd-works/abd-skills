"""Tests for append_plan_revision: entries prepended, header preserved, plan sha recorded."""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path


_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "append_plan_revision.py"


def _load():
    spec = importlib.util.spec_from_file_location("append_plan_revision", _SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_first_append_creates_file_with_header(tmp_path):
    mod = _load()
    plan = tmp_path / "agile-delivery-plan.md"
    plan.write_text("# Plan\n", encoding="utf-8")
    changelog = tmp_path / "agile-delivery-plan.changelog.md"
    mod.append_entry(
        changelog_path=changelog,
        plan_path=plan,
        summary="First revision",
        rationale="Initial plan approved",
        strategy_shift=None,
    )
    text = changelog.read_text(encoding="utf-8")
    assert text.startswith(mod._HEADER)
    assert "First revision" in text
    assert "Initial plan approved" in text
    # Plan sha is recorded
    expected_sha = hashlib.sha256(plan.read_bytes()).hexdigest()
    assert expected_sha in text


def test_second_append_prepends_under_header(tmp_path):
    mod = _load()
    plan = tmp_path / "agile-delivery-plan.md"
    plan.write_text("# Plan v1\n", encoding="utf-8")
    changelog = tmp_path / "agile-delivery-plan.changelog.md"
    mod.append_entry(changelog_path=changelog, plan_path=plan,
                     summary="Entry one", rationale=None, strategy_shift=None,
                     now_iso="2026-04-22T10:00:00+00:00")
    plan.write_text("# Plan v2\n", encoding="utf-8")
    mod.append_entry(changelog_path=changelog, plan_path=plan,
                     summary="Entry two", rationale=None, strategy_shift="custom",
                     now_iso="2026-04-22T11:00:00+00:00")
    text = changelog.read_text(encoding="utf-8")
    # Entry two should come before entry one (most recent at top, under header)
    idx_two = text.index("Entry two")
    idx_one = text.index("Entry one")
    assert idx_two < idx_one
    # Header appears once
    assert text.count(mod._HEADER) == 1


def test_strategy_shift_field_rendered(tmp_path):
    mod = _load()
    changelog = tmp_path / "changelog.md"
    mod.append_entry(
        changelog_path=changelog,
        plan_path=None,
        summary="switched strategies",
        rationale=None,
        strategy_shift="strategies/regulatory-compliance-heavy.md",
    )
    text = changelog.read_text(encoding="utf-8")
    assert "**Strategy shift:** strategies/regulatory-compliance-heavy.md" in text


def test_missing_plan_path_omits_sha(tmp_path):
    mod = _load()
    changelog = tmp_path / "changelog.md"
    mod.append_entry(
        changelog_path=changelog,
        plan_path=None,
        summary="no plan yet",
        rationale=None,
        strategy_shift=None,
    )
    text = changelog.read_text(encoding="utf-8")
    assert "Plan sha" not in text
