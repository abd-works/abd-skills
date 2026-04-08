#!/usr/bin/env python3
"""Emit instruction text for a phase or operation slug, or a full stage.

Usage:
    python scripts/base/generate.py --phase <phase-id> [--mode static|dynamic] [--no-ensure-checklists]
    python scripts/base/generate.py --stage <A|B|C|D|E|F> [--mode static|dynamic] [--no-ensure-checklists]
    python scripts/base/generate.py --list-phases
    python scripts/base/generate.py --list-stages

--mode static   reads content/built/phases/<slug>.md when present; else assembles from sources.
--mode dynamic  always assembles from sources (default).

Unless ``--no-ensure-checklists`` is passed, creates missing live checklists under
``active_skill_workspace/<skill_name>/progress/`` (see workspace_checklists.py):
``process-checklist.md``, ``<phase>-checklist.md``, and optionally ``strategy-run-checklist.md``
(from ``templates/strategy-run-checklist.md`` when the skill provides it).

``--stage`` runs each phase-id in that stage in **process_stages** order (see ``skill-config.json``),
concatenating prompts with clear separators.

Run from skill root: ``python scripts/base/generate.py``.

See parts/library/process.md
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


def _phase_ids(skill) -> list[str]:
    return list(skill.skill_config.get("phase_files") or [])


def _stages_map(skill) -> dict[str, list[str]]:
    raw = skill.skill_config.get("process_stages") or {}
    out: dict[str, list[str]] = {}
    if isinstance(raw, dict):
        for k, v in raw.items():
            if isinstance(v, list):
                out[str(k).upper()] = [str(x) for x in v]
    return out


def _emit_list_phases(skill: Skill) -> None:
    for pid in _phase_ids(skill):
        sys.stdout.write(pid + "\n")


def _emit_list_stages(skill: Skill) -> None:
    sm = _stages_map(skill)
    for letter in sorted(sm.keys()):
        ids = sm[letter]
        sys.stdout.write(f"{letter}: {' '.join(ids)}\n")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    p = argparse.ArgumentParser(
        description="Generate prompt instructions for a phase-id, a stage (A–F), or list phases/stages."
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument(
        "--phase",
        dest="slug",
        metavar="PHASE_ID",
        help="Single phase-id (same as phase filename without .md).",
    )
    g.add_argument(
        "--stage",
        metavar="LETTER",
        help="Run all phase-ids for stage A–F (see skill-config process_stages), in order.",
    )
    g.add_argument(
        "--list-phases",
        action="store_true",
        help="Print all phase_ids from skill-config phase_files, one per line.",
    )
    g.add_argument(
        "--list-stages",
        action="store_true",
        help="Print each stage letter and its ordered phase-ids (from process_stages).",
    )
    p.add_argument(
        "--mode",
        choices=("static", "dynamic"),
        default="dynamic",
        help="static = use content/built/phases/<slug>.md when present; else assemble. dynamic = always assemble.",
    )
    p.add_argument(
        "--no-ensure-checklists",
        action="store_true",
        help="Do not create missing progress checklists under active_skill_workspace (see workspace_checklists.py).",
    )
    ns = p.parse_args()
    try:
        skill = Skill.load()
        if ns.list_phases:
            _emit_list_phases(skill)
            return 0
        if ns.list_stages:
            _emit_list_stages(skill)
            return 0

        form = "static" if ns.mode == "static" else "dynamic"

        if ns.slug:
            if not ns.no_ensure_checklists:
                ensure_workspace_checklists(skill, ns.slug)
            text = skill.prompt(ns.slug, form=form)
            sys.stdout.write(text)
            if not text.endswith("\n"):
                sys.stdout.write("\n")
            return 0

        # --stage
        letter = (ns.stage or "").strip().upper()
        sm = _stages_map(skill)
        if letter not in sm:
            print(
                f"Unknown stage {letter!r}. Configure skill-config.json → process_stages. "
                f"Known: {', '.join(sorted(sm.keys()))}",
                file=sys.stderr,
            )
            return 1
        ids = sm[letter]
        all_ids = set(_phase_ids(skill))
        chunks: list[str] = []
        for i, slug in enumerate(ids):
            if slug not in all_ids:
                print(
                    f"Stage {letter} lists unknown phase-id {slug!r} (not in phase_files).",
                    file=sys.stderr,
                )
                return 1
            if not ns.no_ensure_checklists:
                ensure_workspace_checklists(skill, slug)
            body = skill.prompt(slug, form=form)
            header = (
                f"\n\n---\n\n## Stage {letter} — `{slug}`\n\n"
                if i > 0
                else f"## Stage {letter} — `{slug}`\n\n"
            )
            chunks.append(header + body)
        out = "".join(chunks)
        sys.stdout.write(out)
        if not out.endswith("\n"):
            sys.stdout.write("\n")
        return 0
    except (FileNotFoundError, KeyError, RuntimeError) as e:
        print(e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
