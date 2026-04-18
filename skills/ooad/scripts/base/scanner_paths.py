"""Discover and merge scanner script paths for build.py and run_scanners.

Convention: every ``*.py`` directly under ``scripts/scanners/`` is a scanner (except ``__init__.py``).
Explicit lists in ``skill-config.json`` / ``rules/scanners.json`` are optional — they add paths;
discovered scripts are merged so you do not have to list every file.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_SCANNERS_JSON = Path("rules") / "scanners.json"


def skill_build_cfg(cfg: dict[str, Any]) -> dict[str, Any]:
    """Return the ``build`` block from ``skill-config.json`` (empty dict if missing)."""
    b = cfg.get("build")
    return b if isinstance(b, dict) else {}


def discover_scanner_scripts(skill_root: Path) -> list[str]:
    """Sorted relative POSIX paths for ``scripts/scanners/*.py`` (excludes ``__init__.py``)."""
    d = skill_root / "scripts" / "scanners"
    if not d.is_dir():
        return []
    out: list[str] = []
    for p in sorted(d.glob("*.py")):
        if not p.is_file() or p.name == "__init__.py":
            continue
        out.append(str(p.relative_to(skill_root)).replace("\\", "/"))
    return out


def merge_scanner_paths(skill_root: Path, cfg: dict[str, Any]) -> list[str]:
    """Union of optional explicit lists and :func:`discover_scanner_scripts`. Preserves order; dedupes.

    Order: ``workspace.scanners`` → ``build.scanners`` → ``rules/scanners.json`` → discovered ``*.py``.
    """
    seen: set[str] = set()
    ordered: list[str] = []

    def add(rel: str | None) -> None:
        if not rel:
            return
        s = str(rel).replace("\\", "/")
        if s not in seen:
            seen.add(s)
            ordered.append(s)

    ws = cfg.get("workspace")
    if isinstance(ws, dict):
        for rel in ws.get("scanners") or []:
            add(rel)

    build_cfg = skill_build_cfg(cfg)
    for rel in build_cfg.get("scanners") or []:
        add(rel)

    sj = skill_root / _SCANNERS_JSON
    if sj.is_file():
        data = json.loads(sj.read_text(encoding="utf-8"))
        for b in data.get("rule_scanner_bindings") or []:
            add(b.get("scanner"))
        for rel in data.get("scanners") or []:
            add(rel)

    for rel in discover_scanner_scripts(skill_root):
        add(rel)

    return ordered


def resolve_build_pipeline(skill_root: Path, cfg: dict[str, Any]) -> list[str]:
    """Run explicit ``build.build_pipeline`` when non-empty.

    When missing or empty, run the merged scanner set from :func:`merge_scanner_paths`.
    """
    build_cfg = skill_build_cfg(cfg)
    raw = build_cfg.get("build_pipeline")
    if raw:
        return [str(x).replace("\\", "/") for x in raw]
    return merge_scanner_paths(skill_root, cfg)
