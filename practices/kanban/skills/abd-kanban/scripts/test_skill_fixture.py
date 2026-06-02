"""Tests for skill_fixture harness application."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from skill_fixture import apply_skill_fixture, is_fixture_mode, pick_fixture_entry


@pytest.fixture
def stub_workspace(tmp_path: Path) -> Path:
    seed = (
        Path(__file__).resolve().parents[3]
        / "apps"
        / "abd-delivery-agent-kanban"
        / "tests"
        / "e2e"
        / "_seed"
        / "pawplace-stubs"
    )
    import shutil

    shutil.copytree(seed, tmp_path, dirs_exist_ok=True)
    return tmp_path


def test_is_fixture_mode(stub_workspace: Path):
    assert is_fixture_mode(stub_workspace) is True


def test_pick_fixture_entry_scope_all(stub_workspace: Path):
    fixtures = json.loads((stub_workspace / "skill-fixtures.json").read_text(encoding="utf-8"))
    entry = pick_fixture_entry(fixtures, "abd-story-mapping", "all")
    assert any(c["target"].endswith("shaping/story-map.md") for c in entry["copies"])


def test_apply_module_partition(stub_workspace: Path):
    from delivery_model import load_board

    board = load_board(stub_workspace)
    board["active"][0]["skill_progress"] = {
        "abd-module-partition": {
            "execution_status": "in_progress",
            "agent": "business-expert",
            "review_status": "not_started",
        }
    }
    from delivery_model import save_board

    save_board(stub_workspace, board)

    result = apply_skill_fixture(
        stub_workspace,
        "project-all",
        "abd-module-partition",
        "business-expert",
    )
    assert result["event"] == "skill_fixture_applied"
    assert (stub_workspace / "docs/end-to-end/shaping/module-partition.md").is_file()

    board = load_board(stub_workspace)
    sp = board["active"][0]["skill_progress"]["abd-module-partition"]
    assert sp["execution_status"] == "done"
    assert sp["review_status"] == "done"
