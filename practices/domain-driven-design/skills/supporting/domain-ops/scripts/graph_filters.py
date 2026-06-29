"""Filter domain-model JSON by module or class names."""
from __future__ import annotations

import graph_path_bootstrap  # noqa: F401
from copy import deepcopy
from typing import Any, Dict, List, Optional, Set

from graph_dict_utils import stripped_field


def _filter_class_list(classes: List[Any], class_names: Set[str]) -> List[Dict[str, Any]]:
    filtered: List[Dict[str, Any]] = []
    for class_entry in classes:
        if not isinstance(class_entry, dict):
            continue
        if stripped_field(class_entry, "name") in class_names:
            filtered.append(dict(class_entry))
    return filtered


def _filter_key_abstraction(ka_payload: Dict[str, Any], class_names: Set[str]) -> Optional[Dict[str, Any]]:
    classes = _filter_class_list(ka_payload["classes"] if "classes" in ka_payload else [], class_names)
    if not classes:
        return None
    filtered = dict(ka_payload)
    filtered["classes"] = classes
    return filtered


def _filter_module_classes(module_entry: Dict[str, Any], class_names: Set[str]) -> Optional[Dict[str, Any]]:
    module_copy = dict(module_entry)
    kas_out: List[Dict[str, Any]] = []
    for ka_entry in module_copy["key_abstractions"] if "key_abstractions" in module_copy else []:
        if not isinstance(ka_entry, dict):
            continue
        filtered_ka = _filter_key_abstraction(ka_entry, class_names)
        if filtered_ka:
            kas_out.append(filtered_ka)
    if not kas_out:
        return None
    module_copy["key_abstractions"] = kas_out
    return module_copy


def filter_domain_model_to_module_names(
    domain_model: Dict[str, Any],
    module_names: Set[str],
) -> Dict[str, Any]:
    result = deepcopy(domain_model)
    result["modules"] = [
        dict(module_entry)
        for module_entry in result["modules"] or []
        if isinstance(module_entry, dict) and stripped_field(module_entry, "name") in module_names
    ]
    return result


def filter_domain_model_to_class_names(
    domain_model: Dict[str, Any],
    class_names: Set[str],
) -> Dict[str, Any]:
    result = deepcopy(domain_model)
    modules_out: List[Dict[str, Any]] = []
    for module_entry in result["modules"] or []:
        if not isinstance(module_entry, dict):
            continue
        filtered_module = _filter_module_classes(module_entry, class_names)
        if filtered_module:
            modules_out.append(filtered_module)
    result["modules"] = modules_out
    return result
