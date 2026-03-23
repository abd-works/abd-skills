#!/usr/bin/env python3
"""Emit instruction text for a phase or operation slug (abd-skill-builder contract).

Resolves the same slug namespace as ``skill-config.json`` ``phase_files`` and ``operation_sections``.

**Assembly mode** (static vs dynamic) comes from ``skill-config.json`` — see ``generate_prompt.assembly_mode``
or, if absent, ``delivery.mode`` (``static_built`` → static; ``runtime_injection`` → dynamic). Default is
**static**: use ``content/built/phases/<slug>.md`` when present; otherwise assemble via ``MapsInstructions``.

See ``content/parts/library/`` cross-links in abd-skill-builder ``process-approach.md``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Literal

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from engine import AgileContextEngine

_SKILL_ROOT = _SCRIPTS.parent


def _assembly_form(skill_root: Path) -> Literal["static", "dynamic"]:
    cfg_path = skill_root / "skill-config.json"
    if not cfg_path.is_file():
        return "static"
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "static"

    gp = data.get("generate_prompt") or {}
    raw = (gp.get("assembly_mode") or "").strip().lower()
    if raw in ("static", "dynamic"):
        return raw  # type: ignore[return-value]

    delivery = data.get("delivery") or {}
    dm = (delivery.get("mode") or "static_built").strip().lower()
    if dm == "runtime_injection":
        return "dynamic"
    return "static"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    p = argparse.ArgumentParser(
        description="Generate prompt instructions for a phase or operation slug (see library/process-approach.md)."
    )
    p.add_argument(
        "--phase",
        required=True,
        dest="slug",
        help="Phase or operation slug (filename without .md for phases; operation name from skill-config)",
    )
    ns = p.parse_args()
    form = _assembly_form(_SKILL_ROOT)
    try:
        engine = AgileContextEngine().load()
        text = engine.prompt(ns.slug, form=form)
    except (FileNotFoundError, KeyError, RuntimeError) as e:
        print(e, file=sys.stderr)
        return 1
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
