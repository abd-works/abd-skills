"""CLI to read or set solution_workspace in skill-config.json → workspace.

Usage:
    python workspace.py              # print current workspace
    python workspace.py <path>       # set solution_workspace to <path>
"""
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_CONFIG_PATH = SKILL_DIR / "skill-config.json"


def load_skill_config() -> dict:
    if SKILL_CONFIG_PATH.exists():
        return json.loads(SKILL_CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def save_skill_config(cfg: dict) -> None:
    SKILL_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    SKILL_CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    if len(sys.argv) == 1:
        cfg = load_skill_config()
        ws_block = cfg.get("workspace") if isinstance(cfg.get("workspace"), dict) else {}
        workspace = ws_block.get("solution_workspace")
        if workspace:
            print(workspace)
        else:
            print("(not set)")
    elif len(sys.argv) == 2:
        path = Path(sys.argv[1]).resolve()
        cfg = load_skill_config()
        if "workspace" not in cfg or not isinstance(cfg.get("workspace"), dict):
            cfg["workspace"] = {}
        cfg["workspace"]["solution_workspace"] = str(path)
        save_skill_config(cfg)
        print(f"solution_workspace set to: {path}")
    else:
        print("Usage: workspace.py [path]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
