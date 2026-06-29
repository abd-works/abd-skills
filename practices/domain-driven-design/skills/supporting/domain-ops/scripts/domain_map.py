"""Typed walk model for ``domain-model.json`` (abd-domain-model/v1).

Mirrors the lightweight ``story_map`` layer in story-graph-ops: dict-backed nodes,
tree walk, and name lookup — not a full mutation graph.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

SCHEMA = "abd-domain-model/v1"

EMPTY_DOMAIN_MODEL_DICT: Dict[str, Any] = {
    "schema": SCHEMA,
    "product": "",
    "scope": "",
    "modules": [],
}


class DomainNode:
    """Base node wrapping a JSON object fragment with positional indices."""

    def __init__(
        self,
        data: Dict[str, Any],
        module_idx: int,
        ka_idx: Optional[int] = None,
        class_idx: Optional[int] = None,
        *,
        boundary: bool = False,
    ):
        self.data = data
        self.module_idx = module_idx
        self.ka_idx = ka_idx
        self.class_idx = class_idx
        self.boundary = boundary

    @property
    def name(self) -> str:
        return str(self.data.get("name", ""))

    @property
    def children(self) -> List["DomainNode"]:
        return []

    def map_location(self, field: str = "name") -> str:
        if isinstance(self, Module):
            return f"modules[{self.module_idx}].{field}"
        if isinstance(self, KeyAbstraction):
            return f"modules[{self.module_idx}].key_abstractions[{self.ka_idx}].{field}"
        if isinstance(self, DomainClass):
            if self.boundary:
                return (
                    f"modules[{self.module_idx}].boundary_domain.classes"
                    f"[{self.class_idx}].{field}"
                )
            return (
                f"modules[{self.module_idx}].key_abstractions[{self.ka_idx}]"
                f".classes[{self.class_idx}].{field}"
            )
        return ""


class Module(DomainNode):
    @property
    def relationships(self) -> List[Dict[str, Any]]:
        return list(self.data.get("relationships") or [])

    @property
    def key_abstractions(self) -> List["KeyAbstraction"]:
        return [
            KeyAbstraction(ka, self.module_idx, ka_idx)
            for ka_idx, ka in enumerate(self.data.get("key_abstractions") or [])
            if isinstance(ka, dict)
        ]

    @property
    def boundary_domain(self) -> Dict[str, Any]:
        bd = self.data.get("boundary_domain")
        return bd if isinstance(bd, dict) else {}

    @property
    def boundary_classes(self) -> List["DomainClass"]:
        classes = self.boundary_domain.get("classes") or []
        return [
            DomainClass(cls, self.module_idx, class_idx=idx, boundary=True)
            for idx, cls in enumerate(classes)
            if isinstance(cls, dict)
        ]

    @property
    def children(self) -> List[DomainNode]:
        return list(self.key_abstractions)

    @property
    def all_classes(self) -> List["DomainClass"]:
        classes: List[DomainClass] = []

        def _collect(node: DomainNode) -> None:
            if isinstance(node, DomainClass):
                classes.append(node)
            for child in node.children:
                _collect(child)

        _collect(self)
        classes.extend(self.boundary_classes)
        return classes


class KeyAbstraction(DomainNode):
    def __init__(self, data: Dict[str, Any], module_idx: int, ka_idx: int):
        super().__init__(data, module_idx, ka_idx=ka_idx)

    @property
    def relationships(self) -> List[Dict[str, Any]]:
        return list(self.data.get("relationships") or [])

    @property
    def classes(self) -> List["DomainClass"]:
        return [
            DomainClass(cls, self.module_idx, self.ka_idx, class_idx)
            for class_idx, cls in enumerate(self.data.get("classes") or [])
            if isinstance(cls, dict)
        ]

    @property
    def children(self) -> List[DomainNode]:
        return list(self.classes)


class DomainClass(DomainNode):
    @property
    def term(self) -> str:
        return str(self.data.get("term", ""))

    @property
    def extends(self) -> Optional[str]:
        ext = self.data.get("extends")
        return str(ext) if ext else None

    @property
    def ka_anchor(self) -> bool:
        return bool(self.data.get("ka_anchor"))

    @property
    def properties(self) -> List[Dict[str, Any]]:
        return [p for p in (self.data.get("properties") or []) if isinstance(p, dict)]

    @property
    def operations(self) -> List[Dict[str, Any]]:
        return [o for o in (self.data.get("operations") or []) if isinstance(o, dict)]

    @property
    def children(self) -> List[DomainNode]:
        return []


class DomainMap:
    """In-memory view over a domain-model JSON dict."""

    def __init__(self, domain_model: Dict[str, Any]):
        self.domain_model = domain_model

    @classmethod
    def from_json_file(cls, path: Path | str) -> "DomainMap":
        p = Path(path)
        if not p.is_file():
            return cls(EMPTY_DOMAIN_MODEL_DICT.copy())
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        return cls(data)

    def modules(self) -> List[Module]:
        return [
            Module(mod, module_idx)
            for module_idx, mod in enumerate(self.domain_model.get("modules") or [])
            if isinstance(mod, dict)
        ]

    def find_module_by_name(self, module_name: str) -> Optional[Module]:
        for module in self.modules():
            if module.name == module_name:
                return module
        return None

    def find_class_by_name(self, class_name: str) -> Optional[DomainClass]:
        for module in self.modules():
            for cls in module.all_classes:
                if cls.name == class_name:
                    return cls
        return None

    def class_names(self) -> List[str]:
        names: List[str] = []
        for module in self.modules():
            for cls in module.all_classes:
                if cls.name:
                    names.append(cls.name)
        return names

    def walk(self, node: DomainNode) -> Iterator[DomainNode]:
        yield node
        for child in node.children:
            yield from self.walk(child)
