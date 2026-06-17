"""Action intents and the action state file for manual board mode.

Domain area   : Kanban Board — Action State
Responsibilities: read, append, and clear action intents from the action state
                  file; raise domain exceptions for missing files or invalid intents

domain model:
  ActionIntent  — record specifying which skill to execute on which ticket
                   by which team member agent
  action state file — file the app writes action intents to; kanban lead
                      watches for changes
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .delivery_model import _read_json, _write_json, now_iso

ACTION_STATE_FILENAME = "action-state.json"

_INTENTS_KEY = "intents"
_REQUIRED_INTENT_FIELDS = frozenset({"ticket_id", "skill", "agent_role"})


class NoActionStateFileError(Exception):
    """Raised when the action state file does not exist."""


class InvalidActionIntentError(Exception):
    """Raised when an action intent is missing required fields."""


@dataclass
class ActionIntent:
    """A single action intent: execute a skill on a ticket by a role.

    domain model responsibilities:
      - identify target ticket, skill, and agent role
      - carry creation timestamp
      - serialise / deserialise for the action state file
    """
    ticket_id: str
    skill: str
    agent_role: str
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "ticket_id": self.ticket_id,
            "skill": self.skill,
            "agent_role": self.agent_role,
            "created_at": self.created_at or now_iso(),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ActionIntent:
        _validate_intent_fields(d)
        return cls(
            ticket_id=d["ticket_id"],
            skill=d["skill"],
            agent_role=d["agent_role"],
            created_at=d.get("created_at", ""),
        )


def _validate_intent_fields(d: dict[str, Any]) -> None:
    missing = _REQUIRED_INTENT_FIELDS - d.keys()
    if missing:
        raise InvalidActionIntentError(
            f"Action intent missing required fields: {sorted(missing)}"
        )


def _action_state_path(war_room: Path) -> Path:
    return war_room / ACTION_STATE_FILENAME


def action_state_file_exists(war_room: Path) -> bool:
    """Check if action-state.json exists."""
    return _action_state_path(war_room).is_file()


def load_action_intents(war_room: Path) -> list[ActionIntent]:
    """Read all unprocessed intents from action-state.json."""
    path = _action_state_path(war_room)
    if not path.is_file():
        raise NoActionStateFileError(f"Action state file not found: {path}")
    raw = _read_json(path)
    return [ActionIntent.from_dict(entry) for entry in raw.get(_INTENTS_KEY, [])]


def append_action_intent(war_room: Path, intent: ActionIntent) -> None:
    """Append an intent to action-state.json. Creates file if missing."""
    path = _action_state_path(war_room)
    raw = _read_existing_or_empty(path)
    raw.setdefault(_INTENTS_KEY, []).append(intent.to_dict())
    _write_json(path, raw)


def _read_existing_or_empty(path: Path) -> dict[str, Any]:
    if path.is_file():
        return _read_json(path)
    return {_INTENTS_KEY: []}


def clear_processed_intents(war_room: Path) -> None:
    """Clear all intents after processing."""
    path = _action_state_path(war_room)
    if not path.is_file():
        return
    raw = _read_json(path)
    raw[_INTENTS_KEY] = []
    raw["cleared_at"] = now_iso()
    _write_json(path, raw)


def remove_action_intent(war_room: Path, intent: ActionIntent) -> None:
    """Remove one intent after an agent starts work (claim consumes the drop)."""
    path = _action_state_path(war_room)
    if not path.is_file():
        return
    raw = _read_json(path)
    entries = raw.get(_INTENTS_KEY, [])
    raw[_INTENTS_KEY] = [
        entry
        for entry in entries
        if not (
            entry.get("ticket_id") == intent.ticket_id
            and entry.get("skill") == intent.skill
            and entry.get("agent_role") == intent.agent_role
        )
    ]
    _write_json(path, raw)


def find_first_intent_for_role(war_room: Path, role: str) -> ActionIntent | None:
    """Oldest unprocessed intent for a role (FIFO)."""
    try:
        intents = load_action_intents(war_room)
    except NoActionStateFileError:
        return None
    for intent in intents:
        if intent.agent_role == role:
            return intent
    return None


def count_intents_by_role(war_room: Path) -> dict[str, int]:
    """Pending intent counts per agent role."""
    try:
        intents = load_action_intents(war_room)
    except NoActionStateFileError:
        return {}
    counts: dict[str, int] = {}
    for intent in intents:
        counts[intent.agent_role] = counts.get(intent.agent_role, 0) + 1
    return counts
