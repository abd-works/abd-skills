#!/usr/bin/env python3
"""Print <active_skill_workspace>/<skill_name>/progress for checkbox tracking."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# skill-helpers/skills/track_task/scripts -> repo root is four levels up
AGENT_ROOT = Path(__file__).resolve().parents[4]
CONFIG = AGENT_ROOT / "skill-config.json"


def _load_workspace() -> Path | None:
    if not CONFIG.is_file():
        return None
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    ws = data.get("workspace") if isinstance(data.get("workspace"), dict) else {}
    raw = ws.get("active_skill_workspace")
    if not raw or not isinstance(raw, str):
        return None
    p = Path(raw).expanduser()
    if not p.is_absolute():
        p = (AGENT_ROOT / p).resolve()
    return p


def _skill_name(explicit: str | None) -> str:
    if explicit:
        return explicit
    if CONFIG.is_file():
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
        name = data.get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return "track_task"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--skill",
        default=None,
        help="Skill name segment under workspace (default: skill-config.json name, else track_task)",
    )
    ns = p.parse_args()
    root = _load_workspace()
    if root is None:
        print("(set workspace.active_skill_workspace in skill-config.json first)", file=sys.stderr)
        return 1
    skill = _skill_name(ns.skill)
    out = root / skill / "progress"
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
