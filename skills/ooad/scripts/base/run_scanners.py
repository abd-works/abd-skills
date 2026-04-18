"""
run_scanners.py — run the merged scanner set: optional **workspace.scanners** and
**build.scanners**, entries from **rules/scanners.json**, then every **scripts/scanners/*.py**.

Usage:
    python scripts/base/run_scanners.py [--workspace <path>]
"""
from __future__ import annotations

import sys
import json
import subprocess
from pathlib import Path
from skill_root import SKILL_ROOT
from scanner_paths import merge_scanner_paths

SKILL_CONFIG_PATH = SKILL_ROOT / "skill-config.json"


def load_scanners() -> list[str]:
    if not SKILL_CONFIG_PATH.exists():
        raise FileNotFoundError(f"skill-config.json not found: {SKILL_CONFIG_PATH}")
    cfg = json.loads(SKILL_CONFIG_PATH.read_text(encoding="utf-8"))
    return merge_scanner_paths(SKILL_ROOT, cfg)


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Run all configured scanners")
    parser.add_argument("--workspace", default=str(SKILL_ROOT), help="Path to skill workspace")
    args = parser.parse_args()

    scanners = load_scanners()
    if not scanners:
        print("[INFO] No scanners (empty merge: build.scanners, rules/scanners.json, scripts/scanners/)")
        return 0

    results: dict[str, int] = {}
    for scanner_path in scanners:
        script = SKILL_ROOT / scanner_path
        if not script.exists():
            print(f"[MISSING] {scanner_path}")
            results[scanner_path] = 2
            continue
        result = subprocess.run(
            [sys.executable, str(script), "--workspace", args.workspace],
            capture_output=False,
        )
        results[scanner_path] = result.returncode

    print("\n--- Scanner summary ---")
    failed = []
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
