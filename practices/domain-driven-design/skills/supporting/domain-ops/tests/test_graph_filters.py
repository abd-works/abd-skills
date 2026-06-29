"""Filter domain-model JSON by module or class names."""
from __future__ import annotations

from graph_filters import (
    filter_domain_model_to_class_names,
    filter_domain_model_to_module_names,
)


def _graph() -> dict:
    return {
        "schema": "abd-domain-model/v1",
        "product": "T",
        "scope": "s",
        "modules": [
            {
                "name": "ModA",
                "relationships": [],
                "key_abstractions": [
                    {
                        "name": "KA1",
                        "definition": "d",
                        "relationships": [],
                        "classes": [
                            {"name": "Alpha", "ka_anchor": True, "extends": None},
                            {"name": "Beta", "ka_anchor": False, "extends": None},
                        ],
                        "references": [],
                        "decisions": [],
                    }
                ],
                "boundary_domain": {"relationships": [], "classes": [], "references": [], "decisions": []},
            },
            {
                "name": "ModB",
                "relationships": [],
                "key_abstractions": [],
                "boundary_domain": {"relationships": [], "classes": [], "references": [], "decisions": []},
            },
        ],
    }


class TestFilterDomainModelByModuleNames:
  def test_keeps_only_named_modules(self) -> None:
      # Given
      data = _graph()
      # When
      out = filter_domain_model_to_module_names(data, {"ModA"})
      # Then
      assert [m["name"] for m in out["modules"]] == ["ModA"]


class TestFilterDomainModelByClassNames:
  def test_prunes_classes_within_module(self) -> None:
      # Given
      data = _graph()
      # When
      out = filter_domain_model_to_class_names(data, {"Alpha"})
      # Then
      classes = out["modules"][0]["key_abstractions"][0]["classes"]
      assert [c["name"] for c in classes] == ["Alpha"]
