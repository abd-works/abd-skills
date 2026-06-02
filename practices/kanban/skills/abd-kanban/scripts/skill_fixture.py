"""Skill fixture helpers — copy harness artifacts and mark skills done (E2E / stub mode)."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from agent import Agent
from delivery_model import (
    Ticket,
    append_metrics_log,
    find_ticket_in_board,
    load_board,
    load_kanban_board,
    now_iso,
)

FIXTURE_NOTES = "fixture_mode: copied from skill-fixtures"


def is_fixture_mode(workspace: Path) -> bool:
    context = workspace / "CONTEXT.md"
    if not context.is_file():
        return False
    text = context.read_text(encoding="utf-8")
    if not re.search(r"fixture_mode", text, re.IGNORECASE):
        return False
    return bool(re.search(r"fixture_mode[^\n]*\btrue\b", text, re.IGNORECASE))


def load_fixtures_index(workspace: Path) -> dict:
    path = workspace / "skill-fixtures.json"
    if not path.is_file():
        raise FileNotFoundError(f"skill-fixtures.json not found at {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def pick_fixture_entry(fixtures: dict, skill: str, scope_level: str) -> dict:
    skill_entries = fixtures.get("fixtures", {}).get(skill)
    if not skill_entries:
        raise KeyError(f"No fixture entry for skill {skill!r}")

    scope_key = f"scope_{scope_level}"
    if scope_key in skill_entries:
        return skill_entries[scope_key]
    if "default" in skill_entries:
        return skill_entries["default"]
    # First non-scope key fallback
    for key, entry in skill_entries.items():
        if not key.startswith("scope_"):
            return entry
    raise KeyError(f"No fixture variant for skill {skill!r} scope {scope_level!r}")


def _skills_repo_root() -> Path:
    # .../practices/kanban/skills/abd-kanban/scripts/skill_fixture.py -> repo root
    return Path(__file__).resolve().parents[5]


def _run_post_copy(workspace: Path, commands: list[str]) -> list[dict]:
    results: list[dict] = []
    skills_root = _skills_repo_root()
    for cmd in commands:
        proc = subprocess.run(
            cmd,
            shell=True,
            cwd=skills_root if (skills_root / "skills").is_dir() else workspace,
            capture_output=True,
            text=True,
        )
        results.append({
            "command": cmd,
            "returncode": proc.returncode,
            "stdout": proc.stdout[-500:] if proc.stdout else "",
            "stderr": proc.stderr[-500:] if proc.stderr else "",
        })
        if proc.returncode != 0:
            raise RuntimeError(
                f"post_copy failed ({proc.returncode}): {cmd}\n{proc.stderr}"
            )
    return results


def copy_fixture_files(workspace: Path, entry: dict) -> list[dict]:
    copied: list[dict] = []
    for item in entry.get("copies", []):
        src = workspace / item["source"]
        dst = workspace / item["target"]
        if not src.is_file():
            raise FileNotFoundError(f"Fixture source missing: {src}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append({"source": item["source"], "target": item["target"]})
    return copied


def apply_skill_fixture(
    workspace: Path,
    ticket_id: str,
    skill: str,
    role: str,
    instance: int = 1,
) -> dict:
    if not is_fixture_mode(workspace):
        raise RuntimeError(f"fixture_mode is not active for workspace {workspace}")

    board = load_board(workspace)
    match = find_ticket_in_board(board, ticket_id)
    if match is None:
        raise ValueError(f"Ticket not found: {ticket_id}")
    _bucket, _index, ticket = match
    ticket_obj = Ticket.from_dict(ticket) if isinstance(ticket, dict) else ticket

    fixtures = load_fixtures_index(workspace)
    entry = pick_fixture_entry(fixtures, skill, ticket_obj.scope_level)

    copied = copy_fixture_files(workspace, entry)
    post_copy_results: list[dict] = []
    if entry.get("post_copy"):
        post_copy_results = _run_post_copy(workspace, entry["post_copy"])

    ag = Agent(workspace, role, instance)
    complete1 = ag.complete_skill(ticket_id, skill, FIXTURE_NOTES)
    complete2 = ag.complete_skill(ticket_id, skill, FIXTURE_NOTES)

    event = {
        "event": "skill_fixture_applied",
        "ts": now_iso(),
        "ticket_id": ticket_id,
        "skill": skill,
        "agent_role": role,
        "instance": instance,
        "scope_level": ticket_obj.scope_level,
        "copies": copied,
        "post_copy": post_copy_results,
        "complete": [complete1.get("action"), complete2.get("action")],
    }
    append_metrics_log(workspace, event)
    return event


def find_in_progress_claim(workspace: Path, role: str) -> tuple[str, str] | None:
    board = load_board(workspace)
    config_name = board.get("stage_configuration") or board.get("system_of_work", "")
    kb_map = load_kanban_board(workspace)
    kb = kb_map.get(config_name)
    if kb is None:
        return None
    active = [Ticket.from_dict(t) for t in board.get("active", [])]
    claims = kb.in_progress_claims_for_role(active, role)
    if not claims:
        return None
    ticket, skill = claims[0]
    return ticket.ticket_id, skill
