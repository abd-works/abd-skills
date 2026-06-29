"""Validated load/save for ``domain-model.json`` (abd-domain-model/v1)."""
from __future__ import annotations

import graph_path_bootstrap  # noqa: F401
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

from graph_dict_utils import stripped_field
from graph_cli_commands import load_validated_graph, save_validated_graph

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from domain_map import SCHEMA, DomainMap

_VALID_RELATIONSHIP_KINDS = frozenset({"association", "aggregation", "composition"})
_VALID_CARDINALITIES = frozenset({"1..1", "0..1", "1..*", "0..*"})


def _err(path: str, message: str) -> None:
    raise ValueError(f"{path}: {message}")


def _validate_property_step(step_path: str, step: Dict[str, Any]) -> None:
    if "return_type" not in step:
        _err(step_path, "property step requires return_type")


def _validate_operation_step(step_path: str, step: Dict[str, Any]) -> None:
    if "return_type" not in step:
        _err(step_path, "operation step requires return_type")
    if "object" not in step:
        _err(step_path, "operation step requires object")
    params = step["params"] if "params" in step else None
    if params is not None and not isinstance(params, list):
        _err(step_path, "params must be an array when present")


def _validate_interaction_object(step_path: str, step: Dict[str, Any]) -> None:
    if "property" in step:
        _validate_property_step(step_path, step)
        return
    if "operation" in step:
        _validate_operation_step(step_path, step)
        return
    if "return" in step and len(step) == 1:
        return
    _err(
        step_path,
        "interaction object must be {return_type, object, operation, params?}, "
        "{return_type, property}, {return}, or a plain string",
    )


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
        _validate_interaction_object(step_path, step)


def _validate_property_member(path: str, member_entry: Dict[str, Any]) -> None:
    if not stripped_field(member_entry, "name"):
        _err(path, "property name must be non-empty")
    if not stripped_field(member_entry, "return_type"):
        _err(path, "property requires return_type")
    interaction = member_entry["interaction"] if "interaction" in member_entry else None
    _validate_interaction(f"{path}.interaction", interaction)


def _validate_operation_member(path: str, member_entry: Dict[str, Any]) -> None:
    if not stripped_field(member_entry, "name"):
        _err(path, "operation name must be non-empty")
    if not stripped_field(member_entry, "return_type"):
        _err(path, "operation requires return_type")
    params = member_entry["parameter_types"] if "parameter_types" in member_entry else None
    if params is not None and not isinstance(params, list):
        _err(path, "parameter_types must be an array")
    interaction = member_entry["interaction"] if "interaction" in member_entry else None
    _validate_interaction(f"{path}.interaction", interaction)


def _validate_member_list(path: str, items: Any, *, kind: str) -> None:
    if items is None:
        return
    if not isinstance(items, list):
        _err(path, f"{kind} must be an array")
    for idx, member_entry in enumerate(items):
        member_path = f"{path}[{idx}]"
        if not isinstance(member_entry, dict):
            _err(member_path, f"{kind} entry must be an object")
        if kind == "property":
            _validate_property_member(member_path, member_entry)
        else:
            _validate_operation_member(member_path, member_entry)


def _validate_relationship_end(end_path: str, end: Dict[str, Any]) -> None:
    if not stripped_field(end, "class"):
        _err(end_path, "relationship end requires class")
    if not stripped_field(end, "role"):
        _err(end_path, "relationship end requires role")
    card = end["cardinality"] if "cardinality" in end else None
    if card not in _VALID_CARDINALITIES:
        _err(end_path, f"cardinality must be one of {sorted(_VALID_CARDINALITIES)}")


def _validate_relationship(rel_path: str, rel: Dict[str, Any]) -> None:
    if not stripped_field(rel, "name"):
        _err(rel_path, "relationship name must be non-empty")
    kind = rel["kind"] if "kind" in rel else None
    if kind not in _VALID_RELATIONSHIP_KINDS:
        _err(rel_path, f"relationship kind must be one of {sorted(_VALID_RELATIONSHIP_KINDS)}")
    ends = rel["ends"] if "ends" in rel else None
    if not isinstance(ends, list) or len(ends) != 2:
        _err(rel_path, "relationship ends must be an array of exactly two ends")
    for end_idx, end in enumerate(ends):
        end_path = f"{rel_path}.ends[{end_idx}]"
        if not isinstance(end, dict):
            _err(end_path, "relationship end must be an object")
        _validate_relationship_end(end_path, end)


def _validate_relationships(path: str, relationships: Any) -> None:
    if relationships is None:
        return
    if not isinstance(relationships, list):
        _err(path, "relationships must be an array")
    for idx, rel in enumerate(relationships):
        rel_path = f"{path}[{idx}]"
        if not isinstance(rel, dict):
            _err(rel_path, "relationship must be an object")
        _validate_relationship(rel_path, rel)


def _validate_class(path: str, class_payload: Dict[str, Any], *, boundary: bool) -> None:
    if not stripped_field(class_payload, "name"):
        _err(path, "class name must be non-empty")
    if "extends" not in class_payload:
        _err(path, "class requires extends (use null when not a subtype)")
    if boundary and not stripped_field(class_payload, "owned_by"):
        _err(path, "boundary class requires owned_by")
    props = class_payload["properties"] if "properties" in class_payload else None
    ops = class_payload["operations"] if "operations" in class_payload else None
    _validate_member_list(f"{path}.properties", props, kind="property")
    _validate_member_list(f"{path}.operations", ops, kind="operation")


def _validate_key_abstraction_classes(path: str, classes: List[Dict[str, Any]]) -> Set[str]:
    class_names: Set[str] = set()
    anchor_count = 0
    for idx, class_payload in enumerate(classes):
        class_path = f"{path}.classes[{idx}]"
        _validate_class(class_path, class_payload, boundary=False)
        name = stripped_field(class_payload, "name")
        if name in class_names:
            _err(class_path, f"duplicate class name '{name}' in key abstraction")
        class_names.add(name)
        if class_payload["ka_anchor"] if "ka_anchor" in class_payload else False:
            anchor_count += 1
    if classes and anchor_count != 1:
        _err(path, "key abstraction must have exactly one ka_anchor class when classes are present")
    return class_names


def _validate_key_abstraction(path: str, ka_payload: Dict[str, Any]) -> Set[str]:
    if not stripped_field(ka_payload, "name"):
        _err(path, "key abstraction name must be non-empty")
    rels = ka_payload["relationships"] if "relationships" in ka_payload else None
    _validate_relationships(f"{path}.relationships", rels)
    classes = ka_payload["classes"] if "classes" in ka_payload else None
    if not isinstance(classes, list):
        _err(f"{path}.classes", "classes must be an array")
    class_dicts = [class_entry for class_entry in classes if isinstance(class_entry, dict)]
    return _validate_key_abstraction_classes(path, class_dicts)


def _validate_boundary_classes(path: str, boundary_classes: List[Dict[str, Any]], known: Set[str]) -> None:
    for idx, class_payload in enumerate(boundary_classes):
        class_path = f"{path}.boundary_domain.classes[{idx}]"
        _validate_class(class_path, class_payload, boundary=True)
        name = stripped_field(class_payload, "name")
        if name in known:
            _err(class_path, f"duplicate class name '{name}' in module")


def _validate_boundary_domain(path: str, boundary_domain: Dict[str, Any], known: Set[str]) -> None:
    rels = boundary_domain["relationships"] if "relationships" in boundary_domain else None
    _validate_relationships(f"{path}.boundary_domain.relationships", rels)
    boundary_classes = boundary_domain["classes"] if "classes" in boundary_domain else None
    if boundary_classes is None:
        _err(f"{path}.boundary_domain.classes", "boundary_domain.classes is required")
    if not isinstance(boundary_classes, list):
        _err(f"{path}.boundary_domain.classes", "boundary_domain.classes must be an array")
    class_dicts = [class_entry for class_entry in boundary_classes if isinstance(class_entry, dict)]
    _validate_boundary_classes(path, class_dicts, known)


def _validate_module_key_abstractions(path: str, module_payload: Dict[str, Any]) -> Set[str]:
    kas = module_payload["key_abstractions"] if "key_abstractions" in module_payload else None
    if not isinstance(kas, list):
        _err(f"{path}.key_abstractions", "key_abstractions must be an array")
    module_class_names: Set[str] = set()
    for idx, ka_payload in enumerate(kas):
        if not isinstance(ka_payload, dict):
            _err(f"{path}.key_abstractions[{idx}]", "key abstraction must be an object")
        ka_names = _validate_key_abstraction(f"{path}.key_abstractions[{idx}]", ka_payload)
        overlap = module_class_names.intersection(ka_names)
        if overlap:
            _err(f"{path}.key_abstractions[{idx}]", f"class names already defined in module: {sorted(overlap)}")
        module_class_names.update(ka_names)
    return module_class_names


def _validate_module(path: str, module_payload: Dict[str, Any]) -> None:
    if not stripped_field(module_payload, "name"):
        _err(path, "module name must be non-empty")
    rels = module_payload["relationships"] if "relationships" in module_payload else None
    _validate_relationships(f"{path}.relationships", rels)
    module_class_names = _validate_module_key_abstractions(path, module_payload)
    boundary_domain = module_payload["boundary_domain"] if "boundary_domain" in module_payload else None
    if boundary_domain is None:
        _err(f"{path}.boundary_domain", "boundary_domain is required (may be empty)")
    if not isinstance(boundary_domain, dict):
        _err(f"{path}.boundary_domain", "boundary_domain must be an object")
    _validate_boundary_domain(path, boundary_domain, module_class_names)


def _validate_extends_references(domain_model: Dict[str, Any]) -> None:
    domain_map = DomainMap(domain_model)
    for module in domain_map.modules():
        known = {domain_class.name for domain_class in module.all_classes}
        for domain_class in module.all_classes:
            parent = domain_class.extends
            if parent and parent not in known:
                _err(
                    domain_class.map_location(),
                    f"extends '{parent}' — no such class in module '{module.name}'",
                )


def _validate_module_entries(modules: List[Any]) -> None:
    module_names: Set[str] = set()
    for idx, module_payload in enumerate(modules):
        path = f"modules[{idx}]"
        if not isinstance(module_payload, dict):
            _err(path, "module must be an object")
        name = stripped_field(module_payload, "name")
        if name in module_names:
            _err(path, f"duplicate module name '{name}'")
        module_names.add(name)
        _validate_module(path, module_payload)


def validate_domain_model_dict(domain_model: Dict[str, Any]) -> None:
    if not isinstance(domain_model, dict):
        raise TypeError("domain model root must be a JSON object")
    schema = domain_model["schema"] if "schema" in domain_model else None
    if schema is not None and schema != SCHEMA:
        _err("schema", f"expected {SCHEMA!r}, got {schema!r}")
    modules = domain_model["modules"] if "modules" in domain_model else None
    if modules is None:
        _err("modules", "modules is required")
    if not isinstance(modules, list):
        _err("modules", "modules must be an array")
    _validate_module_entries(modules)
    _validate_extends_references(domain_model)


def load_domain_model_dict(path: Path | str) -> Dict[str, Any]:
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(file_path)
    return load_validated_graph(file_path, validate_domain_model_dict)


def save_domain_model_dict(path: Path | str, domain_model: Dict[str, Any]) -> None:
    save_validated_graph(Path(path), domain_model, validate_domain_model_dict)
