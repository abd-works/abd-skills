"""Typed walk model for ``ux-graph.json`` (abd-ux-graph/v1)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

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
    def __init__(self, data: Dict[str, Any], flow_idx: int, screen_idx: Optional[int] = None):
        self.data = data
        self.flow_idx = flow_idx
        self.screen_idx = screen_idx

    @property
    def name(self) -> str:
        return str(self.data.get("name", ""))

    @property
    def children(self) -> List["UxNode"]:
        return []


class Flow(UxNode):
    @property
    def screens(self) -> List["Screen"]:
        return [
            Screen(sc, self.flow_idx, idx)
            for idx, sc in enumerate(self.data.get("screens") or [])
            if isinstance(sc, dict)
        ]

    @property
    def children(self) -> List[UxNode]:
        return list(self.screens)


class Region(UxNode):
    def __init__(self, data: Dict[str, Any], flow_idx: int, screen_idx: int, region_idx: int):
        super().__init__(data, flow_idx, screen_idx)
        self.region_idx = region_idx

    @property
    def slot(self) -> str:
        return str(self.data.get("slot", ""))

    @property
    def region_type(self) -> str:
        return str(self.data.get("type", ""))


class Screen(UxNode):
    def __init__(self, data: Dict[str, Any], flow_idx: int, screen_idx: int):
        super().__init__(data, flow_idx, screen_idx)

    @property
    def slug(self) -> str:
        return str(self.data.get("slug", ""))

    @property
    def layout(self) -> str:
        return str(self.data.get("layout", ""))

    @property
    def regions(self) -> List[Dict[str, Any]]:
        return [r for r in (self.data.get("regions") or []) if isinstance(r, dict)]

    @property
    def children(self) -> List[UxNode]:
        return [
            Region(r, self.flow_idx, self.screen_idx or 0, idx)
            for idx, r in enumerate(self.regions)
        ]


class UxGraph:
    def __init__(self, graph: Dict[str, Any]):
        self.graph = graph

    @classmethod
    def from_json_file(cls, path: Path | str) -> "UxGraph":
        p = Path(path)
        if not p.is_file():
            return cls(EMPTY_UX_GRAPH_DICT.copy())
        with open(p, encoding="utf-8") as f:
            return cls(json.load(f))

    def flows(self) -> List[Flow]:
        return [
            Flow(flow, idx)
            for idx, flow in enumerate(self.graph.get("flows") or [])
            if isinstance(flow, dict)
        ]

    def connections(self) -> List[Dict[str, Any]]:
        return [c for c in (self.graph.get("connections") or []) if isinstance(c, dict)]

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
        """Project graph to legacy drawio-mockup bundle shape."""
        screens: List[Dict[str, Any]] = []
        for flow in self.flows():
            for screen in flow.screens:
                screens.append({
                    "name": screen.name,
                    "layout": screen.layout,
                    "col": screen.data.get("col", 0),
                    "row": screen.data.get("row", 0),
                    "regions": [dict(r) for r in screen.regions],
                })
        return {
            "target": target,
            "screens": screens,
            "connections": [dict(c) for c in self.connections()],
        }
