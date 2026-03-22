#!/usr/bin/env python3
"""Emit instruction text for an AI-chat phase (abd-skill-builder contract).

This repo's phases live under content/parts/phases/ (scaffold, migrate). There is
no phases/built/ here unless you add a build step — use --mode dynamic.

See content/parts/library/process-approach.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "content" / "parts"
PHASES = PARTS / "phases"
BUILT = PHASES / "built"


def load_static(phase: str) -> str:
    path = BUILT / f"{phase}.md"
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing built phase: {path.relative_to(ROOT)} — run a build step that writes "
            "phases/built, or use --mode dynamic."
        )
    return path.read_text(encoding="utf-8")


def load_dynamic(phase: str) -> str:
    path = PHASES / f"{phase}.md"
    if not path.is_file():
        raise FileNotFoundError(f"Missing phase source: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    p = argparse.ArgumentParser(
        description="Generate prompt instructions for an AI-chat phase (see library/process-approach.md)."
    )
    p.add_argument("--phase", required=True, help="Phase slug (filename without .md)")
    p.add_argument(
        "--mode",
        choices=("static", "dynamic"),
        default="dynamic",
        help="static = read phases/built/<phase>.md; dynamic = read phases/<phase>.md",
    )
    ns = p.parse_args()
    try:
        text = load_static(ns.phase) if ns.mode == "static" else load_dynamic(ns.phase)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 1
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
