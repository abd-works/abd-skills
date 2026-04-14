#!/usr/bin/env python3
"""Run the target skill's own scripts/base/set_workspace.py (--skill-root, default cwd)."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _skill_root_and_rest(description: str) -> tuple[Path, list[str]]:
    p = argparse.ArgumentParser(description=description)
    p.add_argument(
        "--skill-root",
        type=Path,
        default=Path.cwd(),
        help="Skill repo root (directory with SKILL.md; skill-config.json when present). Default: cwd.",
    )
    args, rest = p.parse_known_args()
    return args.skill_root.resolve(), rest


def main() -> int:
    root, rest = _skill_root_and_rest("build-skill: active_skill_workspace (delegates to skill scripts/base/)")
    script = root / "scripts" / "base" / "set_workspace.py"
    if not script.is_file():
        print(f"[build-skill] Missing {script}", file=sys.stderr)
        print(
            "[build-skill] Scaffold the skill with scripts/base/ (e.g. build_skill template) or run "
            f"python {script} from a repo that vendors scripts/base/.",
            file=sys.stderr,
        )
        return 2
    return subprocess.run([sys.executable, str(script)] + rest, cwd=str(root)).returncode


if __name__ == "__main__":
    sys.exit(main())
