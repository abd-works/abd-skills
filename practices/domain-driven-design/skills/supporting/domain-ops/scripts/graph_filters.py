"""Filter and subset operations on raw domain-model JSON dicts."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional, Set


def _filter_class_list(classes: List[Any], class_names: Set[str]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for cls in classes:
        if isinstance(cls, dict) and cls.get("name") in class_names:
            out.append(dict(cls))
    return out


def _filter_key_abstraction(ka: Dict[str, Any], class_names: Set[str]) -> Optional[Dict[str, Any]]:
    classes = _filter_class_list(ka.get("classes") or [], class_names)
    if not classes:
        return None
    out = dict(ka)
    out["classes"] = classes
    return out


def filter_domain_model_to_module_names(
    domain_model: Dict[str, Any], module_names: Set[str]
) -> Dict[str, Any]:
    """Return a deep copy containing only modules whose names are in *module_names*."""
    data = deepcopy(domain_model)
    data["modules"] = [
        dict(m)
        for m in data.get("modules") or []
        if isinstance(m, dict) and m.get("name") in module_names
    ]
    return data


def filter_domain_model_to_class_names(
    domain_model: Dict[str, Any], class_names: Set[str]
) -> Dict[str, Any]:
    """Return a deep copy whose KAs and boundary classes only include named classes."""
    data = deepcopy(domain_model)
    filtered_modules: List[Dict[str, Any]] = []
    for module in data.get("modules") or []:
        if not isinstance(module, dict):
            continue
        mod_out = dict(module)
        kas_out: List[Dict[str, Any]] = []
        for ka in module.get("key_abstractions") or []:
            if not isinstance(ka, dict):
                continue
            fka = _filter_key_abstraction(ka, class_names)
            if fka:
                kas_out.append(fka)
        mod_out["key_abstractions"] = kas_out
        bd = dict(module.get("boundary_domain") or {})
        bd["classes"] = _filter_class_list(bd.get("classes") or [], class_names)
        mod_out["boundary_domain"] = bd
        if kas_out or bd.get("classes"):
            filtered_modules.append(mod_out)
    data["modules"] = filtered_modules
    return data
