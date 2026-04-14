"""Parse --skill-root and subprocess a script from the target skill's scripts/base/ (build_skill wrappers)."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def skill_root_and_rest(description: str) -> tuple[Path, list[str]]:
    p = argparse.ArgumentParser(description=description)
    p.add_argument(
        "--skill-root",
        type=Path,
        default=Path.cwd(),
        help="Skill repo root (directory with skill-config.json). Default: cwd.",
    )
    args, rest = p.parse_known_args()
    return args.skill_root.resolve(), rest


def run_base(base_script: str, skill_root: Path, extra_argv: list[str]) -> int:
    script = skill_root / "scripts" / "base" / base_script
    if not script.is_file():
        print(f"[build-skill] Missing {script}", file=sys.stderr)
        print(
            "[build-skill] Target skill must ship scripts/base/ (vendor or copy from abd-skill-builder).",
            file=sys.stderr,
        )
        return 2
    return subprocess.run([sys.executable, str(script)] + extra_argv, cwd=str(skill_root)).returncode
