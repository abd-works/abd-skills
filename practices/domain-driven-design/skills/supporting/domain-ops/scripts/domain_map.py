"""Typed walk model for ``domain-model.json`` (abd-domain-model/v1)."""
from __future__ import annotations

import graph_path_bootstrap  # noqa: F401
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from graph_dict_utils import dict_child, dict_object_list, optional_text, stripped_field, text_field
from graph_ops_common import read_json_text_file

SCHEMA = "abd-domain-model/v1"

EMPTY_DOMAIN_MODEL_DICT: Dict[str, Any] = {
    "schema": SCHEMA,
    "product": "",
    "scope": "",
    "modules": [],
}


def _read_json_object(path: Path | str) -> Dict[str, Any]:
    file_path = Path(path)
    if not file_path.is_file():
        return EMPTY_DOMAIN_MODEL_DICT.copy()
    parsed = read_json_text_file(file_path)
    return parsed if isinstance(parsed, dict) else EMPTY_DOMAIN_MODEL_DICT.copy()


class DomainNode:
    def __init__(
        self,
        node_payload: Dict[str, Any],
        module_idx: int,
        ka_idx: Optional[int] = None,
        class_idx: Optional[int] = None,
        *,
        boundary: bool = False,
    ):
        self._payload = node_payload
        self._module_idx = module_idx
        self._ka_idx = ka_idx
        self._class_idx = class_idx
        self._boundary = boundary

    @property
    def data(self) -> Dict[str, Any]:
        return self._payload

    @property
    def module_idx(self) -> int:
        return self._module_idx

    @property
    def ka_idx(self) -> Optional[int]:
        return self._ka_idx

    @property
    def class_idx(self) -> Optional[int]:
        return self._class_idx

    @property
    def boundary(self) -> bool:
        return self._boundary

    @property
    def name(self) -> str:
        return text_field(self._payload, "name")

    @property
    def children(self) -> List["DomainNode"]:
        return []

    def map_location(self, field: str = "name") -> str:
        if isinstance(self, Module):
            return f"modules[{self._module_idx}].{field}"
        if isinstance(self, KeyAbstraction):
            return f"modules[{self._module_idx}].key_abstractions[{self._ka_idx}].{field}"
        if isinstance(self, DomainClass):
            if self._boundary:
                return (
                    f"modules[{self._module_idx}].boundary_domain.classes"
                    f"[{self._class_idx}].{field}"
                )
            return (
                f"modules[{self._module_idx}].key_abstractions[{self._ka_idx}]"
                f".classes[{self._class_idx}].{field}"
            )
        return ""


class Module(DomainNode):
    @property
    def relationships(self) -> List[Dict[str, Any]]:
        return list(dict_object_list(self._payload, "relationships"))

    @property
    def key_abstractions(self) -> List["KeyAbstraction"]:
        return [
            KeyAbstraction(ka_payload, self._module_idx, ka_idx)
            for ka_idx, ka_payload in enumerate(dict_object_list(self._payload, "key_abstractions"))
        ]

    @property
    def boundary_domain(self) -> Dict[str, Any]:
        return dict_child(self._payload, "boundary_domain")

    @property
    def boundary_classes(self) -> List["DomainClass"]:
        boundary = self.boundary_domain
        return [
            DomainClass(class_payload, self._module_idx, class_idx=idx, boundary=True)
            for idx, class_payload in enumerate(dict_object_list(boundary, "classes"))
        ]

    @property
    def children(self) -> List[DomainNode]:
        return list(self.key_abstractions)

    @property
    def all_classes(self) -> List["DomainClass"]:
        classes: List[DomainClass] = []

        def collect(node: DomainNode) -> None:
            if isinstance(node, DomainClass):
                classes.append(node)
            for child in node.children:
                collect(child)

        collect(self)
        classes.extend(self.boundary_classes)
        return classes


class KeyAbstraction(DomainNode):
    def __init__(self, node_payload: Dict[str, Any], module_idx: int, ka_idx: int):
        super().__init__(node_payload, module_idx, ka_idx=ka_idx)

    @property
    def relationships(self) -> List[Dict[str, Any]]:
        return list(dict_object_list(self._payload, "relationships"))

    @property
    def classes(self) -> List["DomainClass"]:
        return [
            DomainClass(class_payload, self._module_idx, self._ka_idx, class_idx)
            for class_idx, class_payload in enumerate(dict_object_list(self._payload, "classes"))
        ]

    @property
    def children(self) -> List[DomainNode]:
        return list(self.classes)


class DomainClass(DomainNode):
    @property
    def term(self) -> str:
        return text_field(self._payload, "term")

    @property
    def extends(self) -> Optional[str]:
        return optional_text(self._payload, "extends")

    @property
    def ka_anchor(self) -> bool:
        return bool(self._payload["ka_anchor"]) if "ka_anchor" in self._payload else False

    @property
    def properties(self) -> List[Dict[str, Any]]:
        return list(dict_object_list(self._payload, "properties"))

    @property
    def operations(self) -> List[Dict[str, Any]]:
        return list(dict_object_list(self._payload, "operations"))

    @property
    def children(self) -> List[DomainNode]:
        return []


class DomainMap:
    def __init__(self, domain_model: Dict[str, Any]):
        self._domain_model = domain_model

    @property
    def domain_model(self) -> Dict[str, Any]:
        return self._domain_model

    @classmethod
    def from_json_file(cls, path: Path | str) -> "DomainMap":
        return cls(_read_json_object(path))

    def modules(self) -> List[Module]:
        return [
            Module(module_payload, module_idx)
            for module_idx, module_payload in enumerate(dict_object_list(self._domain_model, "modules"))
        ]

    def find_module_by_name(self, module_name: str) -> Optional[Module]:
        for module in self.modules():
            if module.name == module_name:
                return module
        return None

    def find_class_by_name(self, class_name: str) -> Optional[DomainClass]:
        for module in self.modules():
            for domain_class in module.all_classes:
                if domain_class.name == class_name:
                    return domain_class
        return None

    def class_names(self) -> List[str]:
        names: List[str] = []
        for module in self.modules():
            for domain_class in module.all_classes:
                if domain_class.name:
                    names.append(domain_class.name)
        return names

    def walk(self, node: DomainNode) -> Iterator[DomainNode]:
        yield node
        for child in node.children:
            yield from self.walk(child)
