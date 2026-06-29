"""Round-trip and validation for :mod:`ux_graph_file`.

Behaviors covered:
- save then load returns equivalent graph content
- load rejects screens with empty names
- practice reference example validates
"""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

import pytest

from ux_graph_file import load_ux_graph_dict, save_ux_graph_dict

_MINIMAL: Dict[str, Any] = {
    "schema": "abd-ux-graph/v1",
    "product": "Test",
    "scope": "minimal",
    "flows": [
        {
            "name": "Shop in store",
            "screens": [
                {
                    "name": "Search Results",
                    "slug": "search-results",
                    "layout": "sidebar",
                    "col": 0,
                    "row": 0,
                    "regions": [
                        {
                            "name": "search filter",
                            "slot": "header",
                            "type": "filter-bar",
                            "placeholder": "Search…",
                        }
                    ],
                }
            ],
        }
    ],
    "connections": [],
}


def given_ux_graph_path(workspace: Path) -> Path:
    """Given: a path for ux-graph.json under the workspace."""
    return workspace / "ux-graph.json"


def when_save_then_load(path: Path, data: Dict[str, Any]) -> Dict[str, Any]:
    """When: graph dict is saved then loaded from disk."""
    save_ux_graph_dict(path, data)
    return load_ux_graph_dict(path)


def when_load_expecting_validation_error(path: Path) -> None:
    """When: load_ux_graph_dict is invoked (expected to raise)."""
    load_ux_graph_dict(path)


def then_roundtrip_preserves_flow_and_raw_json(path: Path, loaded: Dict[str, Any]) -> None:
    """Then: flow name matches and file bytes match parsed dict."""
    assert loaded["flows"][0]["name"] == "Shop in store"
    assert json.loads(path.read_text(encoding="utf-8")) == loaded


class TestUxGraphLoadSaveRoundTrip:
    """Persisting and reloading a UX graph yields the same structure."""

    def test_roundtrip_matches_disk_and_model(self, tmp_path: Path) -> None:
        # Given
        path = given_ux_graph_path(tmp_path)
        # When
        loaded = when_save_then_load(path, _MINIMAL)
        # Then
        then_roundtrip_preserves_flow_and_raw_json(path, loaded)


class TestUxGraphLoadRejectsInvalidScreens:
    """Invalid graph content fails fast with a clear error."""

    def test_rejects_empty_screen_name(self, tmp_path: Path) -> None:
        # Given
        bad = deepcopy(_MINIMAL)
        bad["flows"][0]["screens"][0]["name"] = ""
        path = given_ux_graph_path(tmp_path)
        path.write_text(json.dumps(bad), encoding="utf-8")
        # When / Then
        with pytest.raises(ValueError, match="screen name must be non-empty"):
            when_load_expecting_validation_error(path)

    def test_rejects_connection_to_unknown_screen(self, tmp_path: Path) -> None:
        # Given
        bad = deepcopy(_MINIMAL)
        bad["connections"] = [{"from": "Search Results", "to": "Missing", "label": "go"}]
        path = given_ux_graph_path(tmp_path)
        path.write_text(json.dumps(bad), encoding="utf-8")
        # When / Then
        with pytest.raises(ValueError, match="no such screen"):
            when_load_expecting_validation_error(path)

    def test_rejects_invalid_region_type(self, tmp_path: Path) -> None:
        # Given
        bad = deepcopy(_MINIMAL)
        bad["flows"][0]["screens"][0]["regions"][0]["type"] = "datagrid"
        path = given_ux_graph_path(tmp_path)
        path.write_text(json.dumps(bad), encoding="utf-8")
        # When / Then
        with pytest.raises(ValueError, match="type must be one of"):
            when_load_expecting_validation_error(path)


class TestPracticeReferenceFixturesValidate:
    """Shipped reference JSON files pass ux-ops validation."""

    @pytest.mark.parametrize(
        "fixture_name",
        ["ux-graph-outline.json", "ux-graph-example.json"],
    )
    def test_reference_fixture_loads(self, fixture_name: str) -> None:
        # Given
        from conftest import PRACTICE_REFERENCES

        path = PRACTICE_REFERENCES / fixture_name
        assert path.is_file(), f"missing reference fixture: {path}"
        # When
        data = load_ux_graph_dict(path)
        # Then
        assert data["schema"] == "abd-ux-graph/v1"
        assert data["flows"]
