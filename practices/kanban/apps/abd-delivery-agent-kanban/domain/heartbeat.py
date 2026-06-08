"""
heartbeat.py

Domain area   : Kanban Board — Heartbeat
Responsibilities: timestamp of last activity, age in seconds, determine liveness
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STALE_THRESHOLD_SECONDS = 120.0


@dataclass(frozen=True)
class Heartbeat:
    """A point-in-time liveness signal from an agent.

    domain model responsibilities:
      - timestamp of last activity
      - age in seconds
      - determine liveness → Agent, Ticket
    """

    agent_role: str
    instance: int
    timestamp: str
    status: str
    note: str = ""

    @property
    def age_seconds(self) -> float:
        dt = datetime.fromisoformat(self.timestamp.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).total_seconds()

    @property
    def is_live(self) -> bool:
        age = self.age_seconds
        return age >= 0 and age <= STALE_THRESHOLD_SECONDS

    @property
    def is_working(self) -> bool:
        return self.is_live and self.status == "working"

    @property
    def is_stale(self) -> bool:
        return not self.is_live

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "agent_role": self.agent_role,
            "role": self.agent_role,
            "instance": self.instance,
            "ts": self.timestamp,
            "status": self.status,
        }
        if self.note:
            payload["note"] = self.note
        return payload

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Heartbeat":
        return cls(
            agent_role=d.get("agent_role") or d.get("role", "unknown"),
            instance=int(d.get("instance") or 1),
            timestamp=d.get("ts") or d.get("timestamp", ""),
            status=d.get("status", "unknown"),
            note=d.get("note", ""),
        )

    @classmethod
    def from_file(cls, path: Path) -> "Heartbeat | None":
        if not path.is_file():
            return None
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            return cls.from_dict(raw)
        except (json.JSONDecodeError, ValueError, TypeError):
            return None

    # ------------------------------------------------------------------
    # Factory: create and persist a new heartbeat
    # ------------------------------------------------------------------

    @classmethod
    def write(cls, war_room: Path, role: str, status: str, note: str = "", instance: int = 1) -> "Heartbeat":
        """Create a heartbeat and persist it to disk."""
        now = datetime.now(timezone.utc).isoformat()
        hb = cls(agent_role=role, instance=instance, timestamp=now, status=status, note=note)
        path = _heartbeat_path(war_room, role, instance)
        path.write_text(json.dumps(hb.to_dict(), indent=2) + "\n", encoding="utf-8")
        return hb

    # ------------------------------------------------------------------
    # Pool queries
    # ------------------------------------------------------------------

    @classmethod
    def list_for_role(cls, war_room: Path, role: str) -> list["Heartbeat"]:
        """Load all heartbeat files for a role."""
        heartbeats: list[Heartbeat] = []
        for path in _list_heartbeat_files(war_room, role):
            hb = cls.from_file(path)
            if hb is not None:
                heartbeats.append(hb)
        return heartbeats

    @classmethod
    def count_live(cls, war_room: Path, role: str, stale_seconds: float = STALE_THRESHOLD_SECONDS) -> int:
        """Count agents with fresh heartbeats."""
        return sum(1 for hb in cls.list_for_role(war_room, role) if hb.age_seconds <= stale_seconds)

    @classmethod
    def count_working(cls, war_room: Path, role: str, stale_seconds: float = STALE_THRESHOLD_SECONDS) -> int:
        """Count agents actively working (live + status=working)."""
        return sum(
            1 for hb in cls.list_for_role(war_room, role)
            if hb.age_seconds <= stale_seconds and hb.status == "working"
        )


# ---------------------------------------------------------------------------
# File path helpers (package-private)
# ---------------------------------------------------------------------------

def _heartbeat_path(war_room: Path, role: str, instance: int = 1) -> Path:
    if instance <= 1:
        return war_room / f"heartbeat-{role}.json"
    return war_room / f"heartbeat-{role}-{instance}.json"


def _list_heartbeat_files(war_room: Path, role: str) -> list[Path]:
    primary = war_room / f"heartbeat-{role}.json"
    numbered = sorted(war_room.glob(f"heartbeat-{role}-*.json"))
    paths: list[Path] = []
    if primary.is_file():
        paths.append(primary)
    paths.extend(p for p in numbered if p not in paths)
    return paths
