"""Which scanner scripts apply to a skill (rules frontmatter + ``scanners/*-scanner.py``).

Used by **execute_rules** ``run_scanners.py``, ``rule_inventory.py --list-scanners``, and **build_skill**
``build_pipeline_plan.py``. ``scripts/base/build.py`` inlines the same logic so scaffolded skill packages
stay self-contained without a separate ``scanner_paths`` module under ``scripts/base/``.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def skill_build_cfg(cfg: dict[str, Any]) -> dict[str, Any]:
    """Return the ``build`` block from ``skill-config.json`` (empty dict if missing)."""
    b = cfg.get("build")
    return b if isinstance(b, dict) else {}


def _parse_frontmatter_scanner(content: str) -> str | None:
    match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    for line in match.group(1).split("\n"):
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        if k.strip().lower() == "scanner":
            return v.strip().strip('"').strip("'") or None
    return None


def _resolve_scanner_value(skill_root: Path, raw: str) -> str | None:
    """Map ``scanner:`` to ``<skill-root>/scanners/<stem>-scanner.py`` — basename only."""
    v = raw.strip().strip('"').strip("'")
    if not v or "/" in v or "\\" in v or ".." in v:
        return None
    name = Path(v).name
    if name != v:
        return None
    if name.endswith(".py"):
        filename = name
    elif name.endswith("-scanner"):
        filename = f"{name}.py"
    else:
        filename = f"{name}-scanner.py"
    candidate = skill_root / "scanners" / filename
    if candidate.is_file():
        return f"scanners/{filename}"
    return None


def scanners_from_rule_frontmatter(skill_root: Path) -> list[str]:
    """Paths under ``scanners/`` from ``scanner:`` in each ``rules/*.md`` (sorted by filename)."""
    rules_dir = skill_root / "rules"
    if not rules_dir.is_dir():
        return []
    out: list[str] = []
    seen: set[str] = set()
    for md in sorted(rules_dir.glob("*.md")):
        if md.name == "README.md":
            continue
        spec = _parse_frontmatter_scanner(md.read_text(encoding="utf-8"))
        if not spec:
            continue
        rel = _resolve_scanner_value(skill_root, spec)
        if rel and rel not in seen:
            seen.add(rel)
            out.append(rel)
    return out


def discover_scanner_scripts(skill_root: Path) -> list[str]:
    """Sorted relative POSIX paths for ``scanners/*-scanner.py`` (CLI entrypoints only).

    Modules like ``verb_noun_scanner.py`` are excluded — only files ending in ``-scanner.py``.
    """
    d = skill_root / "scanners"
    if not d.is_dir():
        return []
    out: list[str] = []
    for p in sorted(d.glob("*-scanner.py")):
        if not p.is_file():
            continue
        out.append(str(p.relative_to(skill_root)).replace("\\", "/"))
    return out


def list_scanner_scripts(skill_root: Path, cfg: dict[str, Any]) -> list[str]:
    """Return scanner script paths to run: rule ``scanner:`` first, then any other ``scanners/*-scanner.py``.

    ``cfg`` is reserved for API compatibility; scanner lists are not read from ``skill-config.json``.
    """
    del cfg  # API compatibility only
    seen: set[str] = set()
    ordered: list[str] = []

    def add(rel: str | None) -> None:
        if not rel:
            return
        s = str(rel).replace("\\", "/")
        if s not in seen:
            seen.add(s)
            ordered.append(s)

    for rel in scanners_from_rule_frontmatter(skill_root):
        add(rel)

    for rel in discover_scanner_scripts(skill_root):
        add(rel)

    return ordered


# Backward-compatible name for older call sites
merge_scanner_paths = list_scanner_scripts


def resolve_build_pipeline(skill_root: Path, cfg: dict[str, Any]) -> list[str]:
    """If ``build.build_pipeline`` is non-empty, return that; else :func:`list_scanner_scripts`."""
    build_cfg = skill_build_cfg(cfg)
    raw = build_cfg.get("build_pipeline")
    if raw:
        return [str(x).replace("\\", "/") for x in raw]
    return list_scanner_scripts(skill_root, cfg)
