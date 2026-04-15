"""CLI to read or set active_skill_workspace in skill-config.json → workspace.

The skill package stores **one** value: which project directory (absolute path) contains
`solution.conf`. There is no fallback or inference.

Usage:
    python scripts/set_workspace.py              # print configured workspace (exit 1 if unset)
    python scripts/set_workspace.py <path>       # set workspace (directory must exist; stored absolute)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_CONFIG_PATH = SKILL_ROOT / "skill-config.json"

_LEGACY_KEYS = ("solution_workspace", "skill_space_path")


def load_skill_config() -> dict:
    if SKILL_CONFIG_PATH.exists():
        return json.loads(SKILL_CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def save_skill_config(cfg: dict) -> None:
    SKILL_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    SKILL_CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")


def _active_skill_workspace(data: dict) -> str | None:
    v = data.get("active_skill_workspace")
    if v is None:
        return None
    s = str(v).strip()
    return s if s else None


def main() -> None:
    if len(sys.argv) == 1:
        cfg = load_skill_config()
        ws_block = cfg.get("workspace") if isinstance(cfg.get("workspace"), dict) else {}
        ws = _active_skill_workspace(ws_block)
        if not ws:
            print(
                "abd-maps-models-specs: active_skill_workspace is not set in skill-config.json → workspace",
                file=sys.stderr,
            )
            print("Set it with: python scripts/set_workspace.py <path>", file=sys.stderr)
            sys.exit(1)
        print(ws)
    elif len(sys.argv) == 2:
        raw = Path(sys.argv[1])
        target = raw if raw.is_absolute() else (Path.cwd() / raw)
        target = target.resolve()
        if not target.is_dir():
            print(f"abd-maps-models-specs: not a directory: {target}", file=sys.stderr)
            sys.exit(1)
        stored = str(target)
        cfg = load_skill_config()
        if "workspace" not in cfg or not isinstance(cfg.get("workspace"), dict):
            cfg["workspace"] = {}
        w = cfg["workspace"]
        for k in _LEGACY_KEYS:
            w.pop(k, None)
        if not w.get("skills"):
            w["skills"] = ["."]
        if not w.get("skills_config"):
            w["skills_config"] = {"order": w["skills"]}
        w["active_skill_workspace"] = stored
        save_skill_config(cfg)
        print(f"active_skill_workspace set to: {stored}")
    else:
        print("Usage: set_workspace.py [path]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
