#!/usr/bin/env python3
"""Run every scanner script configured for a skill (execute_rules — canonical driver)."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# Same directory as this file (…/execute_using_rules/scripts)
_SCRIPT_DIR = Path(__file__).resolve().parent
_STORY_GRAPH_OPS_SCRIPTS = _SCRIPT_DIR.parent.parent / "story-graph-ops" / "scripts"
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
if _STORY_GRAPH_OPS_SCRIPTS.is_dir() and str(_STORY_GRAPH_OPS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_STORY_GRAPH_OPS_SCRIPTS))

from scanner_paths import list_scanner_scripts  # noqa: E402


def _load_cfg(skill_root: Path) -> dict:
    p = skill_root / "skill-config.json"
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="execute_rules: run scanners for --skill-root")
    parser.add_argument(
        "--skill-root",
        type=Path,
        default=Path.cwd(),
        help="Skill root (directory with SKILL.md, rules/, scanners/*-scanner.py, …). Default: cwd.",
    )
    parser.add_argument(
        "--workspace",
        default=None,
        help="Path passed to each scanner as --workspace (default: --skill-root).",
    )
    args = parser.parse_args(argv)
    root = args.skill_root.resolve()
    workspace = args.workspace if args.workspace is not None else str(root)

    cfg = _load_cfg(root)
    scanners = list_scanner_scripts(root, cfg)
    if not scanners:
        print("[INFO] No scanners (no scanner: in rules frontmatter and no scanners/*-scanner.py)")
        return 0

    results: dict[str, int] = {}
    for scanner_path in scanners:
        script = root.joinpath(*scanner_path.split("/"))
        if not script.is_file():
            print(f"[MISSING] {scanner_path}")
            results[scanner_path] = 2
            continue
        env = os.environ.copy()
        parts: list[str] = []
        if _STORY_GRAPH_OPS_SCRIPTS.is_dir():
            parts.append(str(_STORY_GRAPH_OPS_SCRIPTS))
        parts.append(str(_SCRIPT_DIR))
        skill_scripts = root / "scripts"
        if skill_scripts.is_dir():
            parts.append(str(skill_scripts))
        skill_scanners = root / "scanners"
        if skill_scanners.is_dir():
            parts.append(str(skill_scanners))
        prev = env.get("PYTHONPATH", "")
        if prev:
            parts.append(prev)
        env["PYTHONPATH"] = os.pathsep.join(parts)

        result = subprocess.run(
            [sys.executable, str(script), "--workspace", workspace],
            cwd=str(root),
            capture_output=False,
            env=env,
        )
        results[scanner_path] = result.returncode

    print("\n--- Scanner summary ---")
    failed: list[str] = []
    for path, code in results.items():
        status = "[PASS]" if code == 0 else "[FAIL]" if code == 1 else "[MISSING]"
        print(f"  {status} {path}")
        if code != 0:
            failed.append(path)

    if failed:
        print(f"\n{len(failed)} scanner(s) failed.")
        return 1

    print(f"\nAll {len(results)} scanner(s) passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
