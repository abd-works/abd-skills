#!/usr/bin/env python3
"""Print workspace.active_skill_workspace from the agent root skill-config.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

# skills/workspace/scripts -> agent root is three levels up
AGENT_ROOT = Path(__file__).resolve().parents[3]
CONFIG = AGENT_ROOT / "skill-config.json"


def main() -> int:
    if not CONFIG.is_file():
        print("(no skill-config.json at agent root)", file=sys.stderr)
        return 1
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    ws = data.get("workspace") if isinstance(data.get("workspace"), dict) else {}
    print(ws.get("active_skill_workspace", "(not set)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
