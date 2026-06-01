#!/usr/bin/env python3
"""Project-wide mechanism registry — updated by architecture skills, not kanban lead.

Skills (abd-architecture-reference, abd-architecture-template) register mechanisms
after a create pass. Later tickets read the registry during their own skill run.
"""
from __future__ import annotations

import json
from pathlib import Path

from delivery_model import now_iso, war_room_dir


def registry_path(workspace: Path) -> Path:
    return war_room_dir(workspace) / "mechanism-registry.json"


def load_registry(workspace: Path) -> dict[str, dict]:
    path = registry_path(workspace)
    if not path.is_file():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return dict(raw.get("mechanisms", {}))


def save_registry(workspace: Path, mechanisms: dict[str, dict]) -> None:
    path = registry_path(workspace)
    path.write_text(
        json.dumps({"mechanisms": mechanisms, "updated": now_iso()}, indent=2) + "\n",
        encoding="utf-8",
    )


def register_mechanisms(
    workspace: Path,
    ticket_id: str,
    skill: str,
    mechanism_names: list[str],
    reference_path: str = "",
) -> None:
    reg = load_registry(workspace)
    ts = now_iso()
    for name in mechanism_names:
        if not name.strip():
            continue
        reg[name.strip()] = {
            "ticket_id": ticket_id,
            "skill": skill,
            "reference_path": reference_path,
            "completed_at": ts,
        }
    save_registry(workspace, reg)
