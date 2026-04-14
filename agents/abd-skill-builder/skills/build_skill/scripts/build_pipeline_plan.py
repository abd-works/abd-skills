#!/usr/bin/env python3
"""Diagnostic: what scripts/base/build.py would run after merge (build_pipeline vs merged scanners)."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

# skills/build_skill/scripts/build_pipeline_plan.py -> abd-skill-builder root
_BUILDER_ROOT = Path(__file__).resolve().parents[3]
_SCANNER_PATHS = _BUILDER_ROOT / "skills" / "execute_rules" / "scripts" / "scanner_paths.py"


def _load_scanner_paths():
    if not _SCANNER_PATHS.is_file():
        print(f"[build-skill] Missing {_SCANNER_PATHS}", file=sys.stderr)
        sys.exit(2)
    spec = importlib.util.spec_from_file_location(
        "execute_rules_scanner_paths",
        _SCANNER_PATHS,
    )
    if spec is None or spec.loader is None:
        print(f"[build-skill] Cannot load {_SCANNER_PATHS}", file=sys.stderr)
        sys.exit(2)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    p = argparse.ArgumentParser(description="build-skill: build.build_pipeline vs merged scanners")
    p.add_argument("--skill-root", type=Path, default=Path.cwd(), help="Skill repo root")
    args = p.parse_args()
    root = args.skill_root.resolve()
    cfg_path = root / "skill-config.json"
    if not cfg_path.is_file():
        print(f"[build-skill] Missing {cfg_path}", file=sys.stderr)
        return 2

    scanner_paths = _load_scanner_paths()
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    build_cfg = scanner_paths.skill_build_cfg(cfg)
    explicit = build_cfg.get("build_pipeline")
    steps = scanner_paths.resolve_build_pipeline(root, cfg)

    if explicit:
        print("Post-merge mode: build.build_pipeline (explicit)")
    else:
        print("Post-merge mode: merged scanner set (build_pipeline empty or missing)")

    for i, s in enumerate(steps, 1):
        print(f"  {i}. {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
