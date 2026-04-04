#!/usr/bin/env python3
"""Emit instruction text for a phase or operation slug.

Usage:
    python scripts/generate.py --phase <slug> [--mode static|dynamic]

--mode static   reads phases/built/<slug>.md when present; else assembles from sources.
--mode dynamic  always assembles from sources (default).

See parts/library/process-approach.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from skill import Skill


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    p = argparse.ArgumentParser(
        description="Generate prompt instructions for a phase or operation slug."
    )
    p.add_argument(
        "--phase",
        required=True,
        dest="slug",
        help="Phase or operation slug (filename without .md for phases; operation name from skill-config)",
    )
    p.add_argument(
        "--mode",
        choices=("static", "dynamic"),
        default="dynamic",
        help="static = use phases/built/<slug>.md when present; else assemble from sources. dynamic = always assemble.",
    )
    ns = p.parse_args()
    try:
        skill = Skill.load()
        form = "static" if ns.mode == "static" else "dynamic"
        text = skill.prompt(ns.slug, form=form)
    except (FileNotFoundError, KeyError, RuntimeError) as e:
        print(e, file=sys.stderr)
        return 1
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
