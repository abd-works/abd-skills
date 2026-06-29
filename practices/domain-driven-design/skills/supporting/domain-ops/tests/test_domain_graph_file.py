"""Round-trip and validation for :mod:`domain_graph_file`.

Behaviors covered:
- save then load returns equivalent graph content
- load rejects classes with empty names
- practice reference example validates
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

from domain_graph_file import load_domain_model_dict, save_domain_model_dict

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

_MINIMAL: Dict[str, Any] = {
    "schema": "abd-domain-model/v1",
    "product": "Test",
    "scope": "minimal",
    "modules": [
        {
            "name": "Catalog",
            "relationships": [],
            "key_abstractions": [
                {
                    "name": "Product Catalog",
                    "definition": "Catalog KA",
                    "relationships": [],
                    "classes": [
                        {
                            "name": "Product",
                            "ka_anchor": True,
                            "term": "product",
                            "extends": None,
                            "constructor": {"parameter_types": []},
                            "properties": [
                                {
                                    "name": "sku",
                                    "return_type": "Identifier",
                                    "invariants": [],
                                }
                            ],
                            "operations": [],
                        }
                    ],
                    "references": [],
                    "decisions": [],
                }
            ],
            "boundary_domain": {
                "relationships": [],
                "classes": [],
                "references": [],
                "decisions": [],
            },
        }
    ],
}


def given_domain_model_path(workspace: Path) -> Path:
    """Given: a path for domain-model.json under the workspace."""
    return workspace / "domain-model.json"


def when_save_then_load(path: Path, data: Dict[str, Any]) -> Dict[str, Any]:
    """When: graph dict is saved then loaded from disk."""
    save_domain_model_dict(path, data)
    return load_domain_model_dict(path)


def when_load_expecting_validation_error(path: Path) -> None:
    """When: load_domain_model_dict is invoked (expected to raise)."""
    load_domain_model_dict(path)


def then_roundtrip_preserves_module_and_raw_json(path: Path, loaded: Dict[str, Any]) -> None:
    """Then: module name matches and file bytes match parsed dict."""
    assert loaded["modules"][0]["name"] == "Catalog"
    assert json.loads(path.read_text(encoding="utf-8")) == loaded


# =============================================================================
# STORY: load / save round-trip
# =============================================================================


class TestDomainGraphLoadSaveRoundTrip:
    """Persisting and reloading a domain model yields the same structure."""

    def test_roundtrip_matches_disk_and_model(self, tmp_path: Path) -> None:
        # Given
        path = given_domain_model_path(tmp_path)
        # When
        loaded = when_save_then_load(path, _MINIMAL)
        # Then
        then_roundtrip_preserves_module_and_raw_json(path, loaded)


# =============================================================================
# STORY: validation on load
# =============================================================================


class TestDomainGraphLoadRejectsInvalidClasses:
    """Invalid graph content fails fast with a clear error."""

    def test_rejects_empty_class_name(self, tmp_path: Path) -> None:
        # Given
        bad = dict(_MINIMAL)
        bad["modules"][0]["key_abstractions"][0]["classes"][0]["name"] = ""
        path = given_domain_model_path(tmp_path)
        path.write_text(json.dumps(bad), encoding="utf-8")
        # When / Then
        with pytest.raises(ValueError, match="class name must be non-empty"):
            when_load_expecting_validation_error(path)

    def test_rejects_invalid_relationship_kind(self, tmp_path: Path) -> None:
        # Given
        bad = dict(_MINIMAL)
        bad["modules"][0]["relationships"] = [
            {
                "name": "bad",
                "kind": "inheritance",
                "ends": [
                    {"class": "A", "role": "a", "cardinality": "1..1"},
                    {"class": "B", "role": "b", "cardinality": "1..1"},
                ],
            }
        ]
        path = given_domain_model_path(tmp_path)
        path.write_text(json.dumps(bad), encoding="utf-8")
        # When / Then
        with pytest.raises(ValueError, match="relationship kind"):
            when_load_expecting_validation_error(path)


# =============================================================================
# STORY: practice reference fixtures validate
# =============================================================================


class TestPracticeReferenceFixturesValidate:
    """Shipped reference JSON files pass domain-ops validation."""

    @pytest.mark.parametrize(
        "fixture_name",
        ["domain-model-outline.json", "domain-model-example.json"],
    )
    def test_reference_fixture_loads(self, fixture_name: str) -> None:
        # Given
        from conftest import PRACTICE_REFERENCES

        path = PRACTICE_REFERENCES / fixture_name
        assert path.is_file(), f"missing reference fixture: {path}"
        # When
        data = load_domain_model_dict(path)
        # Then
        assert data["schema"] == "abd-domain-model/v1"
        assert data["modules"]
