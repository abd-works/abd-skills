#!/usr/bin/env python3
"""Light structural gate: SKILL.md and optional phased layout (no require build.py)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description="build-skill: layout smoke check")
    p.add_argument("--skill-root", type=Path, default=Path.cwd(), help="Skill repo root")
    args = p.parse_args()
    root = args.skill_root.resolve()
    errors = 0

    def ok(msg: str) -> None:
        print(f"  [OK] {msg}")

    def fail(msg: str) -> None:
        nonlocal errors
        print(f"  [FAIL] {msg}")
        errors += 1

    print(f"Skill root: {root}")

    data: dict = {}
    cfg_path = root / "skill-config.json"
    if cfg_path.is_file():
        ok("skill-config.json")
        try:
            raw = json.loads(cfg_path.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                data = raw
        except (json.JSONDecodeError, OSError) as e:
            fail(f"skill-config.json parse: {e}")
            print(f"\n{errors} issue(s).")
            return 1
    else:
        print("  [--] skill-config.json (optional for leaf skills)")

    pf = data.get("phase_files")
    if isinstance(pf, dict):
        for slug, files in pf.items():
            if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", str(slug)):
                fail(f"phase_files key not kebab-case: {slug!r}")
            if not isinstance(files, list):
                continue
            for rel in files:
                path = root / str(rel).replace("\\", "/")
                if not path.is_file():
                    fail(f"phase_files[{slug!r}] missing: {rel}")
                else:
                    ok(f"phase_files[{slug!r}] -> {rel}")

    if (root / "SKILL.md").is_file():
        ok("SKILL.md")
    else:
        fail("SKILL.md")

    parts = root / "content" / "parts"
    phased = bool(data.get("phase_files"))
    if parts.is_dir():
        ok("content/parts/")
        if (parts / "process.md").is_file():
            ok("content/parts/process.md")
        elif phased:
            fail("content/parts/process.md (expected when skill-config lists phases)")
    elif phased:
        fail("content/parts/ (missing but skill-config has phase_files)")
    else:
        print("  [--] content/parts/ (optional for leaf skills)")

    if (root / "rules").is_dir():
        ok("rules/")
    else:
        print("  [--] rules/ (optional)")

    base = root / "scripts" / "base"
    if (base / "build.py").is_file():
        print("  [--] scripts/base/build.py present (generic skill merge)")

    if errors:
        print(f"\n{errors} issue(s).")
        return 1
    print("\nLayout smoke check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
