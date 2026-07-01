"""Convert ``domain-specification.md`` -> ``abd-domain-model/v1`` JSON.

Behaviors covered:
- module heading and intro lift cleanly
- KA heading, intro, and class blocks split correctly
- class header lifts name, stereotype, stereotype_note, and ``Child : Parent`` extends
- constructor / property / operation lines parse with named parameters
- invariants and interaction blocks attach to the right member
- ``<< composition >>`` etc. on properties synthesise a relationship at KA scope
- phase headers (``**Onboarding operations** ...``) lift onto each operation
- ``### references`` and ``### decisions made`` sections lift at KA scope
- Boundary Domain classes lift with ``owned_by`` and ``intro``
- the parser exits 2 (UnrecognisedFormatError) on a non-spec file
- the parsed dict round-trips through ``validate_domain_model_dict``
"""
from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any, Dict

import pytest

from domain_graph_file import validate_domain_model_dict
from md_domain_specification_to_domain_graph import (
    UnrecognisedFormatError,
    main,
    parse_specification,
)


# =============================================================================
# HELPERS
# =============================================================================


def given_spec_markdown(tmp_path: Path, body: str) -> Path:
    """Given: a tmp file containing the supplied markdown body."""
    p = tmp_path / "domain-specification.md"
    p.write_text(textwrap.dedent(body), encoding="utf-8")
    return p


def when_parsed(md_path: Path) -> Dict[str, Any]:
    """When: parser lifts the markdown into a canonical dict."""
    return parse_specification(md_path)


def when_validated(graph: Dict[str, Any]) -> None:
    """When: the parsed graph is run through the schema validator."""
    validate_domain_model_dict(graph)


# =============================================================================
# STORY: minimal happy path lifts and validates
# =============================================================================


_MINIMAL_SPEC = """\
    ---
    state: class-model
    ---

    # Module: [demo]

    Module intro paragraph carrying short scope.

    ---

    # Core Domain

    ## **Catalog**

    Catalog KA intro paragraph.

    ### **Catalog** << Service >>

    Initialisation: singleton per session
    ------
    + plans: List<Plan>
    ----
    + fetch(): List<Plan>
    \tInvariant: cached after first call
    \tInteraction:
    \t\tplans = repo.fetch()
    \t\treturn plans

    ### **Plan** << ValueObject >>

    ------
    + id: Identifier
    + price: Money
    \tInvariant: price > 0

    ### references

    **Ref — Catalog source**
    Source: `src/catalog.ts`
    Locator: `Catalog`
    Extract: whole

    ### decisions made

    - Catalog is a Service with cached state.
    - Plan has no behaviour.

    ---
"""


class TestMinimalSpecLiftsAndValidates:
    """A small specification round-trips through parser and validator."""

    def test_module_heading_and_intro(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _MINIMAL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        assert graph["schema"] == "abd-domain-model/v1"
        module = graph["modules"][0]
        assert module["name"] == "demo"
        assert "Module intro paragraph" in module["intro"]

    def test_ka_and_classes(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _MINIMAL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        ka = graph["modules"][0]["key_abstractions"][0]
        assert ka["name"] == "Catalog"
        assert "Catalog KA intro" in ka["definition"]
        names = [c["name"] for c in ka["classes"]]
        assert names == ["Catalog", "Plan"]
        anchors = [c["ka_anchor"] for c in ka["classes"]]
        assert anchors == [True, False]

    def test_stereotypes_and_initialisation(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _MINIMAL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        catalog = graph["modules"][0]["key_abstractions"][0]["classes"][0]
        assert catalog["stereotype"] == "Service"
        assert catalog["initialisation"] == "singleton per session"
        plan = graph["modules"][0]["key_abstractions"][0]["classes"][1]
        assert plan["stereotype"] == "ValueObject"

    def test_property_and_operation_with_invariant_and_interaction(
        self, tmp_path: Path
    ) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _MINIMAL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        catalog = graph["modules"][0]["key_abstractions"][0]["classes"][0]
        assert catalog["properties"][0]["name"] == "plans"
        assert catalog["properties"][0]["return_type"] == "List<Plan>"
        fetch = catalog["operations"][0]
        assert fetch["name"] == "fetch"
        assert fetch["return_type"] == "List<Plan>"
        assert fetch["invariants"] == ["cached after first call"]
        assert fetch["interaction"] == ["plans = repo.fetch()", "return plans"]

    def test_references_and_decisions_attach_to_ka(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _MINIMAL_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        ka = graph["modules"][0]["key_abstractions"][0]
        assert ka["references"] == [
            {
                "title": "Catalog source",
                "source": "src/catalog.ts",
                "locator": "`Catalog`",
                "extract": "whole",
            }
        ]
        assert ka["decisions"] == [
            "Catalog is a Service with cached state.",
            "Plan has no behaviour.",
        ]

    def test_round_trips_through_validator(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _MINIMAL_SPEC)
        # When
        graph = when_parsed(md)
        # Then (no exception)
        when_validated(graph)


# =============================================================================
# STORY: rich features — constructor, named params, phases, relationships, extends
# =============================================================================


_RICH_SPEC = """\
    ---
    state: class-model
    ---

    # Module: [pml-my]

    Module-scope paragraph.

    ---

    # Core Domain

    ## **Customer**

    Customer KA intro.

    ### **Customer** << Entity >>

    + Customer(email: EmailAddress, password: Password)
    ------
    + << composition >> identity: Identity
    + billing: Billing
    \tInvariant: billing.id must be present
    ----
    **Onboarding operations** (metadata.verified = false):

    + searchNumber(keyword: Keyword): List<NumberOption>
    \tInvariant: keyword is up to 5 characters

    **Self-care operations** (metadata.verified = true):

    + changePlan(plan: Plan): Order
    \tInvariant: roaming plans require a support ticket

    ### **EnterpriseIdentity : Identity** << ValueObject >>

    ------
    + headOffice: FreeText

    ### **Identity** << ValueObject >>

    ------
    + email: EmailAddress

    ---
"""


class TestRichSpecFeatures:
    """Constructor params, phases, ``<< composition >>``, and ``Child : Parent``."""

    def test_constructor_named_parameters(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _RICH_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        customer = graph["modules"][0]["key_abstractions"][0]["classes"][0]
        assert customer["constructor"]["parameter_types"] == [
            "EmailAddress",
            "Password",
        ]
        assert customer["constructor"]["parameters"] == [
            {"name": "email", "type": "EmailAddress"},
            {"name": "password", "type": "Password"},
        ]

    def test_operation_named_parameters_and_phase(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _RICH_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        customer = graph["modules"][0]["key_abstractions"][0]["classes"][0]
        ops = {op["name"]: op for op in customer["operations"]}
        assert ops["searchNumber"]["parameters"] == [
            {"name": "keyword", "type": "Keyword"}
        ]
        assert ops["searchNumber"]["phase"] == "onboarding"
        assert ops["changePlan"]["phase"] == "self-care"

    def test_composition_synthesises_relationship(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _RICH_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        ka = graph["modules"][0]["key_abstractions"][0]
        rels = {r["name"]: r for r in ka["relationships"]}
        assert "identity" in rels
        assert rels["identity"]["kind"] == "composition"
        ends = rels["identity"]["ends"]
        assert ends[0]["class"] == "Customer"
        assert ends[1]["class"] == "Identity"

    def test_property_without_stereotype_does_not_synthesise(
        self, tmp_path: Path
    ) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _RICH_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        ka = graph["modules"][0]["key_abstractions"][0]
        rel_names = {r["name"] for r in ka["relationships"]}
        # ``billing: Billing`` carries no ``<< X >>`` prefix → no relationship
        assert "billing" not in rel_names

    def test_extends_parses_from_child_colon_parent_heading(
        self, tmp_path: Path
    ) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _RICH_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        classes = {
            c["name"]: c for c in graph["modules"][0]["key_abstractions"][0]["classes"]
        }
        assert classes["EnterpriseIdentity"]["extends"] == "Identity"
        assert classes["Identity"]["extends"] is None

    def test_rich_spec_validates(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _RICH_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        when_validated(graph)


# =============================================================================
# STORY: boundary domain section lifts intro, classes, and refs
# =============================================================================


_BOUNDARY_SPEC = """\
    # Module: [demo]

    Module scope.

    ---

    # Core Domain

    ## **Core**

    Core KA intro.

    ### **Core** << Entity >>

    ------
    + id: Identifier

    ---

    # Boundary Domain

    External adapters this domain depends on.

    ### **Cognito** << Service >> [AWS IAM]

    Initialisation: AWS Amplify singleton
    ------
    ----
    + signIn(email: EmailAddress, password: Password): SessionTokens

    ### references

    **Ref — Cognito boundary**
    Source: `src/services/aws/cognito.ts`
    Locator: whole
    Extract: whole

    ### decisions made

    - Cognito is a Service in the Boundary layer.
"""


class TestBoundaryDomain:
    """Boundary Domain section lifts classes, intro, refs, and decisions."""

    def test_boundary_intro_lifts(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _BOUNDARY_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        bd = graph["modules"][0]["boundary_domain"]
        assert "External adapters" in bd["intro"]

    def test_boundary_class_owned_by_and_stereotype_note(
        self, tmp_path: Path
    ) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _BOUNDARY_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        cognito = graph["modules"][0]["boundary_domain"]["classes"][0]
        assert cognito["name"] == "Cognito"
        assert cognito["owned_by"] == "demo"
        assert cognito["stereotype"] == "Service"
        assert cognito["stereotype_note"] == "AWS IAM"
        assert cognito["initialisation"] == "AWS Amplify singleton"

    def test_boundary_operation_with_named_params(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _BOUNDARY_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        cognito = graph["modules"][0]["boundary_domain"]["classes"][0]
        sign_in = cognito["operations"][0]
        assert sign_in["name"] == "signIn"
        assert sign_in["parameters"] == [
            {"name": "email", "type": "EmailAddress"},
            {"name": "password", "type": "Password"},
        ]
        assert sign_in["return_type"] == "SessionTokens"

    def test_boundary_refs_and_decisions(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _BOUNDARY_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        bd = graph["modules"][0]["boundary_domain"]
        assert bd["references"][0]["title"] == "Cognito boundary"
        assert bd["decisions"] == ["Cognito is a Service in the Boundary layer."]

    def test_boundary_spec_validates(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _BOUNDARY_SPEC)
        # When
        graph = when_parsed(md)
        # Then
        when_validated(graph)


# =============================================================================
# STORY: unrecognised format fails fast with exit 2
# =============================================================================


class TestUnrecognisedFormat:
    """Files lacking the format signature exit 2 — caller can fall back."""

    def test_missing_module_heading_raises(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, "# Not a module heading\n\nbody.\n")
        # When / Then
        with pytest.raises(UnrecognisedFormatError, match="no '# Module:"):
            when_parsed(md)

    def test_missing_ka_heading_raises(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(
            tmp_path,
            "# Module: [demo]\n\nintro.\n\n# Core Domain\n\nno KAs here.\n",
        )
        # When / Then
        with pytest.raises(UnrecognisedFormatError, match="no '## "):
            when_parsed(md)

    def test_cli_exits_2_on_unrecognised(self, tmp_path: Path) -> None:
        # Given
        bad = tmp_path / "bad.md"
        bad.write_text("# Not a domain spec\n", encoding="utf-8")
        out = tmp_path / "out.json"
        # When
        result = subprocess.run(
            [
                sys.executable,
                str(
                    Path(__file__).resolve().parents[1]
                    / "scripts"
                    / "md_domain_specification_to_domain_graph.py"
                ),
                str(bad),
                str(out),
            ],
            capture_output=True,
            text=True,
        )
        # Then
        assert result.returncode == 2, result.stderr
        assert not out.exists()


# =============================================================================
# STORY: CLI round-trip
# =============================================================================


class TestCli:
    """CLI invocation writes a validated JSON file."""

    def test_main_writes_validated_json(self, tmp_path: Path) -> None:
        # Given
        md = given_spec_markdown(tmp_path, _RICH_SPEC)
        out = tmp_path / "out.json"
        # When
        rc = main([str(md), str(out)])
        # Then
        assert rc == 0
        assert out.is_file()
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["schema"] == "abd-domain-model/v1"
        # Re-validate from disk for parity with domain_graph_file API
        validate_domain_model_dict(data)


# =============================================================================
# STORY: real-world specs in the workspace lift cleanly
#
# These tests run against actual project domain specs when present. They are
# skipped if the file is not checked out, so the suite stays portable.
# =============================================================================


_REAL_WORLD_SPECS = [
    # (path-from-workspace-root, expected_module_name, min_kas, min_core_classes)
    (
        Path("c:/dev/paradise-mobile/pml-my/docs/domain/specification/domain-specification.md"),
        "pml-my",
        6,
        20,
    ),
]


class TestRealWorldSpecs:
    """Real project specs round-trip through the converter and validator."""

    @pytest.mark.parametrize(
        "md_path, expected_module, min_kas, min_classes",
        _REAL_WORLD_SPECS,
    )
    def test_real_spec_parses_and_validates(
        self,
        md_path: Path,
        expected_module: str,
        min_kas: int,
        min_classes: int,
        tmp_path: Path,
    ) -> None:
        if not md_path.is_file():
            pytest.skip(f"spec not present: {md_path}")
        # Given a real spec path; When parsed; Then it validates and meets size floor
        graph = parse_specification(md_path)
        when_validated(graph)
        module = graph["modules"][0]
        assert module["name"] == expected_module
        assert len(module["key_abstractions"]) >= min_kas
        total_classes = sum(
            len(ka["classes"]) for ka in module["key_abstractions"]
        )
        assert total_classes >= min_classes
