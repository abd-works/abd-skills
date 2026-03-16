"""CLI to read or set solution_workspace in conf/abd-config.json.

Usage:
    python workspace.py              # print current workspace
    python workspace.py <path>       # set solution_workspace to <path>
"""
import json
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "conf" / "abd-config.json"


def read_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def write_config(cfg: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    if len(sys.argv) == 1:
        cfg = read_config()
        workspace = cfg.get("solution_workspace")
        if workspace:
            print(workspace)
        else:
            print("(not set)")
    elif len(sys.argv) == 2:
        path = Path(sys.argv[1]).resolve()
        cfg = read_config()
        cfg["solution_workspace"] = str(path)
        write_config(cfg)
        print(f"solution_workspace set to: {path}")
    else:
        print("Usage: workspace.py [path]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
