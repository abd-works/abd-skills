#!/usr/bin/env python3
"""Set workspace.active_skill_workspace in the agent root skill-config.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

AGENT_ROOT = Path(__file__).resolve().parents[3]
CONFIG = AGENT_ROOT / "skill-config.json"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: set_workspace.py <path>", file=sys.stderr)
        return 1
    path = str(Path(sys.argv[1]).resolve())
    if not CONFIG.is_file():
        print(f"Missing {CONFIG}", file=sys.stderr)
        return 1
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    if "workspace" not in data or not isinstance(data["workspace"], dict):
        data["workspace"] = {}
    data["workspace"]["active_skill_workspace"] = path
    data["workspace"].setdefault("known_skill_workspaces", [])
    data["workspace"].setdefault("context_paths", [])
    CONFIG.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
