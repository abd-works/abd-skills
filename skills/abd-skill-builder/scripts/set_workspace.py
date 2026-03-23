"""CLI to read or set active_skill_workspace in conf/abd-config.json.

Same behavior as **abd-maps-models-specs** `scripts/set_workspace.py` (and the same
idea as **abd-solution-modeler** `scripts/workspace.py`). Canonical install key is
**active_skill_workspace**; deprecated **solution_workspace** / **skill_space_path**
are still honored when reading.

Usage:
    python scripts/set_workspace.py              # print configured workspace path
    python scripts/set_workspace.py <path>       # set workspace (directory must exist)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = SKILL_ROOT / "conf" / "abd-config.json"


def read_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def write_config(cfg: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")


def _workspace_path_string(data: dict) -> str | None:
    for key in ("active_skill_workspace", "solution_workspace", "skill_space_path"):
        v = data.get(key)
        if v is None:
            continue
        s = str(v).strip()
        if s:
            return s
    return None


def _path_for_json(path: Path) -> str:
    """Prefer repo-relative path when under the skill package root."""
    resolved = path.resolve()
    try:
        rel = resolved.relative_to(SKILL_ROOT.resolve())
        return rel.as_posix()
    except ValueError:
        return str(resolved)


def main() -> None:
    if len(sys.argv) == 1:
        cfg = read_config()
        ws = _workspace_path_string(cfg)
        print(ws if ws else "(not set)")
    elif len(sys.argv) == 2:
        raw = Path(sys.argv[1])
        target = raw if raw.is_absolute() else (Path.cwd() / raw)
        target = target.resolve()
        if not target.is_dir():
            print(f"set_workspace: not a directory: {target}", file=sys.stderr)
            sys.exit(1)
        stored = _path_for_json(target)
        cfg = read_config()
        cfg["active_skill_workspace"] = stored
        cfg["solution_workspace"] = stored
        write_config(cfg)
        print(f"active_skill_workspace set to: {stored}")
    else:
        print("Usage: set_workspace.py [path]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
