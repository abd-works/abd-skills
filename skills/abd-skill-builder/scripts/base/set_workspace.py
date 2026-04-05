#!/usr/bin/env python3
"""Read or write **active_skill_workspace** in **skill-config.json** → **workspace**.

Imports ``skill_root`` from ``scripts/base/``; this file is the entry point (no subprocess hop).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_BASE_DIR = Path(__file__).resolve().parent
if str(_BASE_DIR) not in sys.path:
    sys.path.insert(0, str(_BASE_DIR))

from skill_root import SKILL_ROOT

SKILL_CONFIG_PATH = SKILL_ROOT / "skill-config.json"


def load() -> dict:
    if SKILL_CONFIG_PATH.exists():
        return json.loads(SKILL_CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def save(cfg: dict) -> None:
    SKILL_CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    cfg = load()
    if len(sys.argv) == 1:
        ws = cfg.get("workspace") if isinstance(cfg.get("workspace"), dict) else {}
        print(ws.get("active_skill_workspace", "(not set)"))
    else:
        path = str(Path(sys.argv[1]).resolve())
        if "workspace" not in cfg or not isinstance(cfg.get("workspace"), dict):
            cfg["workspace"] = {}
        w = cfg["workspace"]
        w["active_skill_workspace"] = path
        save(cfg)
        print(f"active_skill_workspace → {path}")


if __name__ == "__main__":
    main()
