"""Round-trip and validation for :mod:`domain_graph_file`.

Behaviors covered:
- save then load returns equivalent graph content
- load rejects classes with empty names
- practice reference example validates
"""
from __future__ import annotations

import copy
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
        bad = copy.deepcopy(_MINIMAL)
        bad["modules"][0]["key_abstractions"][0]["classes"][0]["name"] = ""
        path = given_domain_model_path(tmp_path)
        path.write_text(json.dumps(bad), encoding="utf-8")
        # When / Then
        with pytest.raises(ValueError, match="class name must be non-empty"):
            when_load_expecting_validation_error(path)

    def test_rejects_invalid_relationship_kind(self, tmp_path: Path) -> None:
        # Given
        bad = copy.deepcopy(_MINIMAL)
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


# =============================================================================
# STORY: specification-fidelity optional fields validate
#
# Schema extension for abd-domain-specification migration — see
# docs/domain-multi-backend-planning.md P1.1. All new fields are optional;
# model-fidelity graphs without them must still round-trip (covered by
# TestDomainGraphLoadSaveRoundTrip above).
# =============================================================================


def _given_spec_fidelity_graph() -> Dict[str, Any]:
    """Given: a minimal graph that uses every new optional spec-fidelity field."""
    return {
        "schema": "abd-domain-model/v1",
        "product": "Test",
        "scope": "spec-fidelity",
        "modules": [
            {
                "name": "Catalog",
                "intro": "Module-scope paragraph carried from markdown.",
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
                                "stereotype": "Entity",
                                "stereotype_note": "Aggregate root",
                                "initialisation": "constructed by Catalog.add()",
                                "constructor": {
                                    "parameter_types": ["Identifier"],
                                    "parameters": [{"name": "sku", "type": "Identifier"}],
                                },
                                "properties": [
                                    {
                                        "name": "sku",
                                        "return_type": "Identifier",
                                        "invariants": [],
                                        "note": "Carried over from legacy SKU format.",
                                    }
                                ],
                                "operations": [
                                    {
                                        "name": "rename",
                                        "parameter_types": ["FreeText"],
                                        "parameters": [{"name": "newName", "type": "FreeText"}],
                                        "return_type": "void",
                                        "visibility": "public",
                                        "collaborators": [],
                                        "invariants": [],
                                        "phase": "self-care",
                                    }
                                ],
                            }
                        ],
                        "references": [],
                        "decisions": [],
                    }
                ],
                "boundary_domain": {
                    "intro": "External systems the Catalog integrates with.",
                    "relationships": [],
                    "classes": [],
                    "references": [],
                    "decisions": [],
                },
            }
        ],
    }


class TestSpecFidelityOptionalFields:
    """New optional fields added for abd-domain-specification round-trip."""

    def test_full_spec_fidelity_graph_round_trips(self, tmp_path: Path) -> None:
        # Given
        path = given_domain_model_path(tmp_path)
        # When
        loaded = when_save_then_load(path, _given_spec_fidelity_graph())
        # Then
        cls = loaded["modules"][0]["key_abstractions"][0]["classes"][0]
        assert cls["stereotype"] == "Entity"
        assert cls["stereotype_note"] == "Aggregate root"
        assert cls["initialisation"].startswith("constructed by")
        assert cls["constructor"]["parameters"] == [{"name": "sku", "type": "Identifier"}]
        assert cls["operations"][0]["parameters"] == [{"name": "newName", "type": "FreeText"}]
        assert cls["operations"][0]["phase"] == "self-care"
        assert loaded["modules"][0]["intro"].startswith("Module-scope")
        assert loaded["modules"][0]["boundary_domain"]["intro"].startswith("External systems")

    def test_rejects_unknown_stereotype(self, tmp_path: Path) -> None:
        # Given
        bad = _given_spec_fidelity_graph()
        bad["modules"][0]["key_abstractions"][0]["classes"][0]["stereotype"] = "ProxyController"
        path = given_domain_model_path(tmp_path)
        path.write_text(json.dumps(bad), encoding="utf-8")
        # When / Then
        with pytest.raises(ValueError, match="stereotype must be one of"):
            when_load_expecting_validation_error(path)

    def test_rejects_named_parameter_missing_type(self, tmp_path: Path) -> None:
        # Given
        bad = _given_spec_fidelity_graph()
        bad["modules"][0]["key_abstractions"][0]["classes"][0]["operations"][0]["parameters"] = [
            {"name": "newName"}
        ]
        path = given_domain_model_path(tmp_path)
        path.write_text(json.dumps(bad), encoding="utf-8")
        # When / Then
        with pytest.raises(ValueError, match="parameter requires type"):
            when_load_expecting_validation_error(path)

    def test_model_fidelity_graph_without_optional_fields_still_validates(
        self, tmp_path: Path
    ) -> None:
        # Given: a fresh copy of the minimal graph (no spec-only fields)
        clean = copy.deepcopy(_MINIMAL)
        path = given_domain_model_path(tmp_path)
        # When
        loaded = when_save_then_load(path, clean)
        # Then: no spec-fidelity fields, but still valid
        cls = loaded["modules"][0]["key_abstractions"][0]["classes"][0]
        assert "stereotype" not in cls
        assert "initialisation" not in cls
        assert "intro" not in loaded["modules"][0]
