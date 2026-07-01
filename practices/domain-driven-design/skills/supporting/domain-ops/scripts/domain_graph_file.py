"""Validated load/save for ``domain-model.json`` (abd-domain-model/v1).

Use from domain-ops CLI or DDD practice skills so JSON round-trips go through the
same walk validation as ``domain_graph_cli`` / ``domain_map.DomainMap``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from domain_map import SCHEMA, DomainClass, DomainMap, KeyAbstraction, Module

_VALID_RELATIONSHIP_KINDS = frozenset({"association", "aggregation", "composition"})
_VALID_CARDINALITIES = frozenset({"1..1", "0..1", "1..*", "0..*"})
_VALID_STEREOTYPES = frozenset(
    {
        "Entity",
        "ValueObject",
        "Service",
        "Factory",
        "Repository",
        "DomainEvent",
        "Boundary",
    }
)


def _err(path: str, message: str) -> None:
    raise ValueError(f"{path}: {message}")


def _validate_interaction(path: str, interaction: Any) -> None:
    if interaction is None:
        return
    if not isinstance(interaction, list):
        _err(path, "interaction must be an array")
    for idx, step in enumerate(interaction):
        step_path = f"{path}[{idx}]"
        if isinstance(step, str):
            continue
        if not isinstance(step, dict):
            _err(step_path, "interaction step must be a string or object")
        if "property" in step:
            if "return_type" not in step:
                _err(step_path, "property step requires return_type")
            continue
        if "operation" in step:
            if "return_type" not in step:
                _err(step_path, "operation step requires return_type")
            if "object" not in step:
                _err(step_path, "operation step requires object")
            params = step.get("params")
            if params is not None and not isinstance(params, list):
                _err(step_path, "params must be an array when present")
            continue
        if "return" in step and len(step) == 1:
            continue
        _err(
            step_path,
            "interaction object must be {return_type, object, operation, params?}, "
            "{return_type, property}, {return}, or a plain string",
        )


def _validate_named_parameters(path: str, parameters: Any) -> None:
    """Optional ``parameters: [{name, type}]`` — parallel to ``parameter_types``."""
    if parameters is None:
        return
    if not isinstance(parameters, list):
        _err(path, "parameters must be an array")
    for idx, param in enumerate(parameters):
        ppath = f"{path}[{idx}]"
        if not isinstance(param, dict):
            _err(ppath, "parameter entry must be an object")
        if not str(param.get("name", "")).strip():
            _err(ppath, "parameter requires name")
        if not str(param.get("type", "")).strip():
            _err(ppath, "parameter requires type")


def _validate_member_list(
    path: str,
    items: Any,
    *,
    kind: str,
    require_name: bool = True,
) -> None:
    if items is None:
        return
    if not isinstance(items, list):
        _err(path, f"{kind} must be an array")
    for idx, item in enumerate(items):
        item_path = f"{path}[{idx}]"
        if not isinstance(item, dict):
            _err(item_path, f"{kind} entry must be an object")
        if require_name and not str(item.get("name", "")).strip():
            _err(item_path, f"{kind} name must be non-empty")
        if kind == "property" and not str(item.get("return_type", "")).strip():
            _err(item_path, "property requires return_type")
        if kind == "operation":
            if not str(item.get("return_type", "")).strip():
                _err(item_path, "operation requires return_type")
            params = item.get("parameter_types")
            if params is not None and not isinstance(params, list):
                _err(item_path, "parameter_types must be an array")
            _validate_named_parameters(f"{item_path}.parameters", item.get("parameters"))
            phase = item.get("phase")
            if phase is not None and not isinstance(phase, str):
                _err(item_path, "operation phase must be a string when present")
        note = item.get("note")
        if note is not None and not isinstance(note, str):
            _err(item_path, f"{kind} note must be a string when present")
        _validate_interaction(f"{item_path}.interaction", item.get("interaction"))


def _validate_relationships(path: str, relationships: Any) -> None:
    if relationships is None:
        return
    if not isinstance(relationships, list):
        _err(path, "relationships must be an array")
    for idx, rel in enumerate(relationships):
        rel_path = f"{path}[{idx}]"
        if not isinstance(rel, dict):
            _err(rel_path, "relationship must be an object")
        if not str(rel.get("name", "")).strip():
            _err(rel_path, "relationship name must be non-empty")
        kind = rel.get("kind")
        if kind not in _VALID_RELATIONSHIP_KINDS:
            _err(rel_path, f"relationship kind must be one of {sorted(_VALID_RELATIONSHIP_KINDS)}")
        ends = rel.get("ends")
        if not isinstance(ends, list) or len(ends) != 2:
            _err(rel_path, "relationship ends must be an array of exactly two ends")
        for end_idx, end in enumerate(ends):
            end_path = f"{rel_path}.ends[{end_idx}]"
            if not isinstance(end, dict):
                _err(end_path, "relationship end must be an object")
            if not str(end.get("class", "")).strip():
                _err(end_path, "relationship end requires class")
            if not str(end.get("role", "")).strip():
                _err(end_path, "relationship end requires role")
            card = end.get("cardinality")
            if card not in _VALID_CARDINALITIES:
                _err(end_path, f"cardinality must be one of {sorted(_VALID_CARDINALITIES)}")


def _validate_class(path: str, cls: Dict[str, Any], *, boundary: bool) -> None:
    if not str(cls.get("name", "")).strip():
        _err(path, "class name must be non-empty")
    if "extends" not in cls:
        _err(path, "class requires extends (use null when not a subtype)")
    if boundary and not str(cls.get("owned_by", "")).strip():
        _err(path, "boundary class requires owned_by")
    stereotype = cls.get("stereotype")
    if stereotype is not None:
        if not isinstance(stereotype, str):
            _err(path, "stereotype must be a string when present")
        if stereotype not in _VALID_STEREOTYPES:
            _err(path, f"stereotype must be one of {sorted(_VALID_STEREOTYPES)}")
    stereotype_note = cls.get("stereotype_note")
    if stereotype_note is not None and not isinstance(stereotype_note, str):
        _err(path, "stereotype_note must be a string when present")
    initialisation = cls.get("initialisation")
    if initialisation is not None and not isinstance(initialisation, str):
        _err(path, "initialisation must be a string when present")
    note = cls.get("note")
    if note is not None and not isinstance(note, str):
        _err(path, "class note must be a string when present")
    ctor = cls.get("constructor")
    if isinstance(ctor, dict):
        _validate_named_parameters(f"{path}.constructor.parameters", ctor.get("parameters"))
    _validate_member_list(f"{path}.properties", cls.get("properties"), kind="property")
    _validate_member_list(f"{path}.operations", cls.get("operations"), kind="operation")


def _validate_key_abstraction(path: str, ka: Dict[str, Any]) -> Set[str]:
    if not str(ka.get("name", "")).strip():
        _err(path, "key abstraction name must be non-empty")
    _validate_relationships(f"{path}.relationships", ka.get("relationships"))
    classes = ka.get("classes")
    if not isinstance(classes, list):
        _err(f"{path}.classes", "classes must be an array")
    class_names: Set[str] = set()
    anchor_count = 0
    for idx, cls in enumerate(classes):
        if not isinstance(cls, dict):
            _err(f"{path}.classes[{idx}]", "class must be an object")
        _validate_class(f"{path}.classes[{idx}]", cls, boundary=False)
        name = str(cls.get("name", "")).strip()
        if name in class_names:
            _err(f"{path}.classes[{idx}]", f"duplicate class name '{name}' in key abstraction")
        class_names.add(name)
        if cls.get("ka_anchor"):
            anchor_count += 1
    if classes and anchor_count != 1:
        _err(path, "key abstraction must have exactly one ka_anchor class when classes are present")
    return class_names


def _validate_module(path: str, module: Dict[str, Any]) -> None:
    if not str(module.get("name", "")).strip():
        _err(path, "module name must be non-empty")
    intro = module.get("intro")
    if intro is not None and not isinstance(intro, str):
        _err(path, "module intro must be a string when present")
    _validate_relationships(f"{path}.relationships", module.get("relationships"))
    kas = module.get("key_abstractions")
    if not isinstance(kas, list):
        _err(f"{path}.key_abstractions", "key_abstractions must be an array")
    module_class_names: Set[str] = set()
    for idx, ka in enumerate(kas):
        if not isinstance(ka, dict):
            _err(f"{path}.key_abstractions[{idx}]", "key abstraction must be an object")
        ka_names = _validate_key_abstraction(f"{path}.key_abstractions[{idx}]", ka)
        overlap = module_class_names.intersection(ka_names)
        if overlap:
            _err(
                f"{path}.key_abstractions[{idx}]",
                f"class names already defined in module: {sorted(overlap)}",
            )
        module_class_names.update(ka_names)
    bd = module.get("boundary_domain")
    if bd is None:
        _err(f"{path}.boundary_domain", "boundary_domain is required (may be empty)")
    if not isinstance(bd, dict):
        _err(f"{path}.boundary_domain", "boundary_domain must be an object")
    bd_intro = bd.get("intro")
    if bd_intro is not None and not isinstance(bd_intro, str):
        _err(f"{path}.boundary_domain", "boundary_domain intro must be a string when present")
    _validate_relationships(f"{path}.boundary_domain.relationships", bd.get("relationships"))
    boundary_classes = bd.get("classes")
    if boundary_classes is None:
        _err(f"{path}.boundary_domain.classes", "boundary_domain.classes is required")
    if not isinstance(boundary_classes, list):
        _err(f"{path}.boundary_domain.classes", "boundary_domain.classes must be an array")
    for idx, cls in enumerate(boundary_classes):
        if not isinstance(cls, dict):
            _err(f"{path}.boundary_domain.classes[{idx}]", "class must be an object")
        _validate_class(f"{path}.boundary_domain.classes[{idx}]", cls, boundary=True)
        name = str(cls.get("name", "")).strip()
        if name in module_class_names:
            _err(f"{path}.boundary_domain.classes[{idx}]", f"duplicate class name '{name}' in module")


def validate_domain_model_dict(data: Dict[str, Any]) -> None:
    """Walk the graph and raise ValueError on structural violations."""
    if not isinstance(data, dict):
        raise TypeError("domain model root must be a JSON object")
    schema = data.get("schema")
    if schema is not None and schema != SCHEMA:
        _err("schema", f"expected {SCHEMA!r}, got {schema!r}")
    modules = data.get("modules")
    if modules is None:
        _err("modules", "modules is required")
    if not isinstance(modules, list):
        _err("modules", "modules must be an array")
    module_names: Set[str] = set()
    for idx, module in enumerate(modules):
        path = f"modules[{idx}]"
        if not isinstance(module, dict):
            _err(path, "module must be an object")
        name = str(module.get("name", "")).strip()
        if name in module_names:
            _err(path, f"duplicate module name '{name}'")
        module_names.add(name)
        _validate_module(path, module)

    # Post-walk: subtype extends must resolve within the same module
    dm = DomainMap(data)
    for module in dm.modules():
        known = {cls.name for cls in module.all_classes}
        for cls in module.all_classes:
            parent = cls.extends
            if parent and parent not in known:
                _err(
                    cls.map_location(),
                    f"extends '{parent}' — no such class in module '{module.name}'",
                )


def load_domain_model_dict(path: Path | str) -> Dict[str, Any]:
    """Read JSON from *path*, validate, return the dict."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(p)
    data = json.loads(p.read_text(encoding="utf-8"))
    validate_domain_model_dict(data)
    return data


def save_domain_model_dict(path: Path | str, data: Dict[str, Any]) -> None:
    """Validate *data* then write indented UTF-8 JSON to *path*."""
    validate_domain_model_dict(data)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
