#!/usr/bin/env python3
"""Emit instruction text for a phase or operation slug.

Usage:
    python scripts/base/generate.py --phase <slug> [--mode static|dynamic] [--no-ensure-checklists]

--mode static   reads content/built/phases/<slug>.md when present; else assembles from sources.
--mode dynamic  always assembles from sources (default).

Unless ``--no-ensure-checklists`` is passed, creates missing live checklists under
``active_skill_workspace/<skill_name>/progress/`` (see workspace_checklists.py):
``process-checklist.md``, ``<phase>-checklist.md``, and optionally ``strategy-run-checklist.md``
(from ``templates/strategy-run-checklist.md`` when the skill provides it).

Run from skill root: ``python scripts/base/generate.py``.

See parts/library/process-phases.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_BASE_DIR = Path(__file__).resolve().parent
if str(_BASE_DIR) not in sys.path:
    sys.path.insert(0, str(_BASE_DIR))

from skill import Skill
from workspace_checklists import ensure_workspace_checklists


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
        help="static = use content/built/phases/<slug>.md when present; else assemble from sources. dynamic = always assemble.",
    )
    p.add_argument(
        "--no-ensure-checklists",
        action="store_true",
        help="Do not create missing progress checklists under active_skill_workspace (see workspace_checklists.py).",
    )
    ns = p.parse_args()
    try:
        skill = Skill.load()
        if not ns.no_ensure_checklists:
            ensure_workspace_checklists(skill, ns.slug)
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
