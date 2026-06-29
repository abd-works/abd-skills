"""Filter ux-graph JSON by flow or screen names."""
from __future__ import annotations

from graph_filters import filter_ux_graph_to_flow_names, filter_ux_graph_to_screen_names


def _graph() -> dict:
    return {
        "schema": "abd-ux-graph/v1",
        "product": "T",
        "scope": "s",
        "flows": [
            {
                "name": "FlowA",
                "screens": [
                    {
                        "name": "Alpha",
                        "slug": "alpha",
                        "layout": "form",
                        "col": 0,
                        "row": 0,
                        "regions": [],
                    },
                    {
                        "name": "Beta",
                        "slug": "beta",
                        "layout": "form",
                        "col": 1,
                        "row": 0,
                        "regions": [],
                    },
                ],
            },
            {
                "name": "FlowB",
                "screens": [
                    {
                        "name": "Gamma",
                        "slug": "gamma",
                        "layout": "stack",
                        "col": 0,
                        "row": 0,
                        "regions": [],
                    }
                ],
            },
        ],
        "connections": [
            {"from": "Alpha", "to": "Beta", "label": "next"},
            {"from": "Beta", "to": "Gamma", "label": "jump"},
        ],
    }


class TestFilterUxGraphByFlowNames:
    def test_keeps_only_named_flows(self) -> None:
        # Given
        data = _graph()
        # When
        out = filter_ux_graph_to_flow_names(data, {"FlowA"})
        # Then
        assert [f["name"] for f in out["flows"]] == ["FlowA"]


class TestFilterUxGraphByScreenNames:
    def test_prunes_screens_and_connections(self) -> None:
        # Given
        data = _graph()
        # When
        out = filter_ux_graph_to_screen_names(data, {"Alpha", "Beta"})
        # Then
        screens = out["flows"][0]["screens"]
        assert [s["name"] for s in screens] == ["Alpha", "Beta"]
        assert out["connections"] == [{"from": "Alpha", "to": "Beta", "label": "next"}]
