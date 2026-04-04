"""
set_workspace.py — read or write active_skill_workspace in conf/abd-config.json

Usage:
    python scripts/base/set_workspace.py              # print current workspace
    python scripts/base/set_workspace.py <path>       # set workspace to <path>
"""
import sys
import json
from pathlib import Path
from skill_root import SKILL_ROOT

CONFIG_PATH = SKILL_ROOT / "conf" / "abd-config.json"


def load() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def save(cfg: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    cfg = load()
    if len(sys.argv) == 1:
        print(cfg.get("active_skill_workspace", "(not set)"))
    else:
        path = str(Path(sys.argv[1]).resolve())
        cfg["active_skill_workspace"] = path
        save(cfg)
        print(f"active_skill_workspace → {path}")


if __name__ == "__main__":
    main()
