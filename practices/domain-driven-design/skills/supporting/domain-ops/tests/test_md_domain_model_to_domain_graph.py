"""Convert ``domain-model.md`` (model fidelity) -> ``abd-domain-model/v1`` JSON.

Behaviours covered:
- KA heading + class block parse without ``<< Stereotype >>`` markers
- Members parse without ``+`` visibility prefix
- Parameters are types-only (no ``name: type``) — ``parameters`` field is absent
- Indented ``CollaboratorType`` lines lift to ``operations[].collaborators``
- ``- privateMethod(...)`` marks ``visibility: private``
- ``Child : Parent`` extends notation still works
- ``Interaction:`` and phase headers are ignored (not part of model fidelity)
- The parsed dict validates against the schema
- ``UnrecognisedFormatError`` raised on missing module / KA headings
"""
from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Any, Dict

import pytest

from domain_graph_file import validate_domain_model_dict
from md_domain_model_to_domain_graph import (
    UnrecognisedFormatError,
    parse_model,
)


# =============================================================================
# HELPERS
# =============================================================================


def given_model_markdown(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "domain-model.md"
    p.write_text(textwrap.dedent(body), encoding="utf-8")
    return p


def when_parsed(md_path: Path) -> Dict[str, Any]:
    return parse_model(md_path)


def when_validated(graph: Dict[str, Any]) -> None:
    validate_domain_model_dict(graph)


# =============================================================================
# STORY: model-fidelity markdown lifts and validates
# =============================================================================


_MODEL_SPEC = """\
    # Module: [demo]

    Scope paragraph.

    **Core terms**:
    - product
    - sku

    ---

    # Core Domain

    ## **Catalog**

    Catalog KA intro paragraph.

    ### **Catalog**

    Catalog(Identifier)
    ------
    plans: List<Plan>
    \tInvariant: catalog refresh every 24h
    ----
    fetch(): List<Plan>
    \tHttpClient
    \tInvariant: cached after first call
    - refresh(): void

    ### **Plan**

    Plan(Identifier, Money)
    ------
    id: Identifier
    price: Money
    \tInvariant: price > 0

    ### **PremiumPlan : Plan**

    PremiumPlan(Identifier, Money)
    ------
    ----
    discount(Percentage): Money

    ### references

    **Ref — Catalog source**
    Source: `src/catalog.ts`
    Locator: `Catalog`
    Extract: whole

    ### decisions made

    - Catalog has cached state.

    ---

    # Boundary Domain

    External adapters.

    ### **HttpClient**

    ------
    ----
    get(Url): Response
"""


class TestModelFidelityLiftsAndValidates:
    """A model-fidelity markdown parses into a valid graph."""

    def test_module_and_intro(self, tmp_path: Path) -> None:
        # Given
        md = given_model_markdown(tmp_path, _MODEL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        assert graph["modules"][0]["name"] == "demo"
        assert "Scope paragraph" in graph["modules"][0]["intro"]

    def test_classes_have_no_stereotype(self, tmp_path: Path) -> None:
        # Given
        md = given_model_markdown(tmp_path, _MODEL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        ka = graph["modules"][0]["key_abstractions"][0]
        for cls in ka["classes"]:
            assert "stereotype" not in cls

    def test_constructor_types_only_no_named_params(self, tmp_path: Path) -> None:
        # Given
        md = given_model_markdown(tmp_path, _MODEL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        catalog = graph["modules"][0]["key_abstractions"][0]["classes"][0]
        assert catalog["constructor"]["parameter_types"] == ["Identifier"]
        assert "parameters" not in catalog["constructor"]

    def test_operation_types_only_no_named_params(self, tmp_path: Path) -> None:
        # Given
        md = given_model_markdown(tmp_path, _MODEL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        catalog = graph["modules"][0]["key_abstractions"][0]["classes"][0]
        fetch = catalog["operations"][0]
        assert fetch["name"] == "fetch"
        assert fetch["parameter_types"] == []
        assert "parameters" not in fetch

    def test_collaborator_line_lifts(self, tmp_path: Path) -> None:
        # Given
        md = given_model_markdown(tmp_path, _MODEL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        catalog = graph["modules"][0]["key_abstractions"][0]["classes"][0]
        fetch = catalog["operations"][0]
        assert fetch["collaborators"] == ["HttpClient"]
        assert fetch["invariants"] == ["cached after first call"]

    def test_dash_prefix_marks_private(self, tmp_path: Path) -> None:
        # Given
        md = given_model_markdown(tmp_path, _MODEL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        catalog = graph["modules"][0]["key_abstractions"][0]["classes"][0]
        refresh = next(op for op in catalog["operations"] if op["name"] == "refresh")
        assert refresh["visibility"] == "private"

    def test_property_invariants_attach(self, tmp_path: Path) -> None:
        # Given
        md = given_model_markdown(tmp_path, _MODEL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        plan = graph["modules"][0]["key_abstractions"][0]["classes"][1]
        price = next(p for p in plan["properties"] if p["name"] == "price")
        assert price["invariants"] == ["price > 0"]

    def test_extends_via_child_colon_parent(self, tmp_path: Path) -> None:
        # Given
        md = given_model_markdown(tmp_path, _MODEL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        names = {
            c["name"]: c["extends"]
            for c in graph["modules"][0]["key_abstractions"][0]["classes"]
        }
        assert names["PremiumPlan"] == "Plan"
        assert names["Catalog"] is None

    def test_references_and_decisions(self, tmp_path: Path) -> None:
        # Given
        md = given_model_markdown(tmp_path, _MODEL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        ka = graph["modules"][0]["key_abstractions"][0]
        assert ka["references"][0]["title"] == "Catalog source"
        assert ka["decisions"] == ["Catalog has cached state."]

    def test_boundary_domain_classes(self, tmp_path: Path) -> None:
        # Given
        md = given_model_markdown(tmp_path, _MODEL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        bd = graph["modules"][0]["boundary_domain"]
        assert "External adapters" in bd["intro"]
        assert bd["classes"][0]["name"] == "HttpClient"
        assert bd["classes"][0]["owned_by"] == "demo"

    def test_round_trips_through_validator(self, tmp_path: Path) -> None:
        # Given
        md = given_model_markdown(tmp_path, _MODEL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        when_validated(graph)


# =============================================================================
# STORY: relationships are empty at model fidelity (no synthesis)
# =============================================================================


class TestNoRelationshipSynthesisAtModelFidelity:
    """Model fidelity does not declare ``<< composition >>``, so KA rels stay empty."""

    def test_ka_relationships_empty(self, tmp_path: Path) -> None:
        # Given
        md = given_model_markdown(tmp_path, _MODEL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        for ka in graph["modules"][0]["key_abstractions"]:
            assert ka["relationships"] == []


# =============================================================================
# STORY: unrecognised format
# =============================================================================


class TestUnrecognisedFormat:
    """Files lacking the format signature raise UnrecognisedFormatError."""

    def test_missing_module_heading(self, tmp_path: Path) -> None:
        # Given
        md = given_model_markdown(tmp_path, "## **KA**\n\n### **Class**\n")
        # When / Then
        with pytest.raises(UnrecognisedFormatError, match="no '# Module:"):
            when_parsed(md)

    def test_missing_ka_heading(self, tmp_path: Path) -> None:
        # Given
        md = given_model_markdown(
            tmp_path, "# Module: [demo]\n\nintro.\n\n# Core Domain\n"
        )
        # When / Then
        with pytest.raises(UnrecognisedFormatError, match="no '## "):
            when_parsed(md)
