"""UxGraph walk and lookup behaviors."""
from __future__ import annotations

from pathlib import Path

from ux_map import Screen, UxGraph


def _minimal() -> dict:
    return {
        "schema": "abd-ux-graph/v1",
        "product": "Test",
        "scope": "walk",
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
                            }
                        ],
                    },
                    {
                        "name": "Product Detail",
                        "slug": "product-detail",
                        "layout": "form",
                        "col": 1,
                        "row": 0,
                        "regions": [],
                    },
                ],
            }
        ],
        "connections": [
            {
                "from": "Search Results",
                "to": "Product Detail",
                "label": "selects product",
            }
        ],
    }


class TestUxGraphWalkDiscoversScreensAndRegions:
    """Walking from a flow yields screens and their regions."""

    def test_walk_lists_screens_and_regions(self) -> None:
        # Given
        graph = UxGraph(_minimal())
        flow = graph.flows()[0]
        # When
        kinds = [type(n).__name__ for n in graph.walk(flow)]
        # Then
        assert kinds == ["Flow", "Screen", "Region", "Screen"]

    def test_find_screen_by_name_returns_screen(self) -> None:
        # Given
        graph = UxGraph(_minimal())
        # When
        screen = graph.find_screen_by_name("Product Detail")
        # Then
        assert isinstance(screen, Screen)
        assert screen.slug == "product-detail"

    def test_to_mockup_state_dict_projects_screens_and_connections(self) -> None:
        # Given
        graph = UxGraph(_minimal())
        # When
        bundle = graph.to_mockup_state_dict(target="docs/ux/mockup/mockup.drawio")
        # Then
        assert bundle["target"] == "docs/ux/mockup/mockup.drawio"
        assert [s["name"] for s in bundle["screens"]] == ["Search Results", "Product Detail"]
        assert bundle["connections"][0]["label"] == "selects product"


class TestReferenceExampleScreenNames:
    """PawPlace example exposes expected screen names."""

    def test_example_contains_search_and_detail(self) -> None:
        # Given
        from conftest import PRACTICE_REFERENCES

        path = PRACTICE_REFERENCES / "ux-graph-example.json"
        graph = UxGraph.from_json_file(path)
        # When
        names = set(graph.screen_names())
        # Then
        assert {"Search Results", "Product Detail"} <= names

    def test_example_region_has_actions(self) -> None:
        # Given
        from conftest import PRACTICE_REFERENCES

        path = PRACTICE_REFERENCES / "ux-graph-example.json"
        graph = UxGraph.from_json_file(path)
        screen = graph.find_screen_by_name("Search Results")
        assert screen is not None
        # When
        list_region = next(r for r in screen.regions if r.get("type") == "list")
        # Then
        assert list_region.get("actions")
