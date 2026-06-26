#!/usr/bin/env python3
"""Print workspace.active_skill_workspace from the agent root skill-config.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from _agent_root import find_agent_root

AGENT_ROOT = find_agent_root(Path(__file__).resolve().parent)
CONFIG = None if AGENT_ROOT is None else AGENT_ROOT / "skill-config.json"


def main() -> int:
    if CONFIG is None or not CONFIG.is_file():
        print("(no skill-config.json at agent root)", file=sys.stderr)
        return 1
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    ws = data.get("workspace") if isinstance(data.get("workspace"), dict) else {}
    print(ws.get("active_skill_workspace", "(not set)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
