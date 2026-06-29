"""Typed walk model for ``ux-graph.json`` (abd-ux-graph/v1)."""
from __future__ import annotations

import graph_path_bootstrap  # noqa: F401
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from graph_dict_utils import dict_object_list, int_field, text_field
from graph_ops_common import read_json_text_file

GRAPH_SCHEMA = "abd-ux-graph/v1"

EMPTY_UX_GRAPH_DICT: Dict[str, Any] = {
    "schema": GRAPH_SCHEMA,
    "product": "",
    "scope": "",
    "flows": [],
    "connections": [],
}

VALID_LAYOUTS = frozenset({"sidebar", "split-screen", "form", "modal", "flyout", "stack"})
VALID_SLOTS = frozenset({"panel", "body", "left", "right", "header", "footer"})
VALID_REGION_TYPES = frozenset({
    "tree", "listbox", "context-menu", "toolbar-icons", "filter-bar", "browse-panel",
    "nav-tabs", "form", "list", "toolbar", "button-bar", "chrome",
})


class UxNode:
    def __init__(
        self,
        node_payload: Dict[str, Any],
        flow_idx: int,
        screen_idx: Optional[int] = None,
    ):
        self._payload = node_payload
        self._flow_idx = flow_idx
        self._screen_idx = screen_idx

    @property
    def data(self) -> Dict[str, Any]:
        return self._payload

    @property
    def flow_idx(self) -> int:
        return self._flow_idx

    @property
    def screen_idx(self) -> Optional[int]:
        return self._screen_idx

    @property
    def name(self) -> str:
        return text_field(self._payload, "name")

    @property
    def children(self) -> List["UxNode"]:
        return []


class Flow(UxNode):
    @property
    def screens(self) -> List["Screen"]:
        return [
            Screen(screen_payload, self._flow_idx, screen_idx)
            for screen_idx, screen_payload in enumerate(dict_object_list(self._payload, "screens"))
        ]

    @property
    def children(self) -> List[UxNode]:
        return list(self.screens)


class Region(UxNode):
    def __init__(self, node_payload: Dict[str, Any], flow_idx: int, screen_idx: int, region_idx: int):
        super().__init__(node_payload, flow_idx, screen_idx)
        self._region_idx = region_idx

    @property
    def slot(self) -> str:
        return text_field(self._payload, "slot")

    @property
    def region_type(self) -> str:
        return text_field(self._payload, "type")


class Screen(UxNode):
    @property
    def slug(self) -> str:
        return text_field(self._payload, "slug")

    @property
    def layout(self) -> str:
        return text_field(self._payload, "layout")

    @property
    def regions(self) -> List[Dict[str, Any]]:
        return list(dict_object_list(self._payload, "regions"))

    @property
    def children(self) -> List[UxNode]:
        screen_idx = self._screen_idx or 0
        return [
            Region(region_payload, self._flow_idx, screen_idx, region_idx)
            for region_idx, region_payload in enumerate(self.regions)
        ]


class UxGraph:
    def __init__(self, ux_graph: Dict[str, Any]):
        self._ux_graph = ux_graph

    @property
    def ux_graph(self) -> Dict[str, Any]:
        return self._ux_graph

    @classmethod
    def from_json_file(cls, path: Path | str) -> "UxGraph":
        file_path = Path(path)
        if not file_path.is_file():
            return cls(EMPTY_UX_GRAPH_DICT.copy())
        parsed = read_json_text_file(file_path)
        if not isinstance(parsed, dict):
            return cls(EMPTY_UX_GRAPH_DICT.copy())
        return cls(parsed)

    def flows(self) -> List[Flow]:
        return [
            Flow(flow_payload, flow_idx)
            for flow_idx, flow_payload in enumerate(dict_object_list(self._ux_graph, "flows"))
        ]

    def connections(self) -> List[Dict[str, Any]]:
        return list(dict_object_list(self._ux_graph, "connections"))

    def screen_names(self) -> List[str]:
        names: List[str] = []
        for flow in self.flows():
            for screen in flow.screens:
                if screen.name:
                    names.append(screen.name)
        return names

    def find_screen_by_name(self, screen_name: str) -> Optional[Screen]:
        for flow in self.flows():
            for screen in flow.screens:
                if screen.name == screen_name:
                    return screen
        return None

    def walk(self, node: UxNode) -> Iterator[UxNode]:
        yield node
        for child in node.children:
            yield from self.walk(child)

    def to_mockup_state_dict(self, target: str = "") -> Dict[str, Any]:
        screens: List[Dict[str, Any]] = []
        for flow in self.flows():
            for screen in flow.screens:
                screens.append({
                    "name": screen.name,
                    "layout": screen.layout,
                    "col": int_field(screen.data, "col"),
                    "row": int_field(screen.data, "row"),
                    "regions": [dict(region_payload) for region_payload in screen.regions],
                })
        return {
            "target": target,
            "screens": screens,
            "connections": [dict(connection_payload) for connection_payload in self.connections()],
        }
