"""DomainMap walk and lookup behaviors."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from domain_map import DomainClass, DomainMap, KeyAbstraction, Module


def _minimal() -> dict:
    return {
        "schema": "abd-domain-model/v1",
        "product": "Test",
        "scope": "walk",
        "modules": [
            {
                "name": "Check Resolution",
                "relationships": [],
                "key_abstractions": [
                    {
                        "name": "Check",
                        "definition": "KA",
                        "relationships": [],
                        "classes": [
                            {
                                "name": "Check",
                                "ka_anchor": True,
                                "term": "check",
                                "extends": None,
                                "constructor": {"parameter_types": []},
                                "properties": [],
                                "operations": [],
                            },
                            {
                                "name": "OpposedCheck",
                                "ka_anchor": False,
                                "term": "opposed check",
                                "extends": "Check",
                                "constructor": {"parameter_types": []},
                                "properties": [],
                                "operations": [],
                            },
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


# =============================================================================
# STORY: tree walk discovers classes
# =============================================================================


class TestDomainMapWalkDiscoversClasses:
    """Walking from a module yields key abstractions and their classes."""

    def test_walk_lists_core_classes(self) -> None:
        # Given
        dm = DomainMap(_minimal())
        module = dm.modules()[0]
        # When
        kinds = [type(n).__name__ for n in dm.walk(module)]
        # Then
        assert kinds == ["Module", "KeyAbstraction", "DomainClass", "DomainClass"]

    def test_find_class_by_name_returns_subtype(self) -> None:
        # Given
        dm = DomainMap(_minimal())
        # When
        cls = dm.find_class_by_name("OpposedCheck")
        # Then
        assert isinstance(cls, DomainClass)
        assert cls.extends == "Check"


# =============================================================================
# STORY: reference example class inventory
# =============================================================================


class TestReferenceExampleClassNames:
    """Check Resolution example exposes expected class names."""

    def test_example_contains_check_and_trait(self) -> None:
        # Given
        from conftest import PRACTICE_REFERENCES

        path = PRACTICE_REFERENCES / "domain-model-example.json"
        dm = DomainMap.from_json_file(path)
        # When
        names = set(dm.class_names())
        # Then
        assert {"Check", "Trait", "Rank", "OpposedCheck", "DifficultyClass"} <= names
