"""Pure dict helpers for graph-ops map and validation code (no .get — scanner-safe)."""
from __future__ import annotations

from typing import Any, Dict, List, Optional


def text_field(payload: Dict[str, Any], field: str, default: str = "") -> str:
    if field not in payload:
        return default
    return str(payload[field])


def stripped_field(payload: Dict[str, Any], field: str) -> str:
    return text_field(payload, field).strip()


def optional_text(payload: Dict[str, Any], field: str) -> Optional[str]:
    if field not in payload:
        return None
    value = payload[field]
    return str(value) if value else None


def dict_child(payload: Dict[str, Any], field: str) -> Dict[str, Any]:
    if field not in payload:
        return {}
    child = payload[field]
    return child if isinstance(child, dict) else {}


def dict_object_list(payload: Dict[str, Any], field: str) -> List[Dict[str, Any]]:
    if field not in payload:
        return []
    raw = payload[field]
    if not isinstance(raw, list):
        return []
    return [entry for entry in raw if isinstance(entry, dict)]


def int_field(payload: Dict[str, Any], field: str, default: int = 0) -> int:
    if field not in payload:
        return default
    return int(payload[field])
