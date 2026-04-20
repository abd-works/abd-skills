"""Test helpers for running scanners with the same **PYTHONPATH** as **run_scanners.py**.

Use from pytest under ``skills/*/tests``: call :func:`prepend_scanner_pythonpath` before
importing ``scanner_runner``, ``story_map``, or a skill-local ``*-scanner.py`` module.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence


def execute_using_rules_scripts() -> Path:
    """Directory containing ``run_scanners.py``, ``scanner_runner.py``, ``scanner_bases/``."""
    return Path(__file__).resolve().parent


def story_graph_ops_scripts() -> Path:
    """Sibling ``story-graph-ops/scripts`` (same layout as **run_scanners.py**)."""
    return execute_using_rules_scripts().parent.parent / "story-graph-ops" / "scripts"


def skill_scripts(skill_root: Path) -> Path:
    """``scripts/`` under a skill root, if present."""
    return Path(skill_root) / "scripts"


def skill_scanners(skill_root: Path, language: str | None = None) -> Path | None:
    """``scanners/`` or ``scanners/<language>/`` under *skill_root* when it exists."""
    root = Path(skill_root)
    if language:
        p = root / "scanners" / language
        return p if p.is_dir() else None
    p = root / "scanners"
    return p if p.is_dir() else None


def _scanner_pythonpath_parts(
    skill_root: Path | None = None,
    *,
    language: str | None = None,
    extra_pythonpath: Iterable[str | Path] | None = None,
) -> list[str]:
    """Path list in the same order as **run_scanners.py** ``env["PYTHONPATH"]`` (before prior env)."""
    parts: list[str] = []
    ops = story_graph_ops_scripts()
    er = execute_using_rules_scripts()
    if ops.is_dir():
        parts.append(str(ops.resolve()))
    parts.append(str(er.resolve()))
    if skill_root is not None:
        root = Path(skill_root)
        ss = root / "scripts"
        if ss.is_dir():
            parts.append(str(ss.resolve()))
        sc = root / "scanners"
        if sc.is_dir():
            parts.append(str(sc.resolve()))
        if language:
            sl = root / "scanners" / language
            if sl.is_dir():
                parts.append(str(sl.resolve()))
    if extra_pythonpath:
        for e in extra_pythonpath:
            p = Path(e)
            if p.is_dir():
                parts.append(str(p.resolve()))
    return parts


def prepend_scanner_pythonpath(
    skill_root: Path | None = None,
    *,
    language: str | None = None,
    extra: Sequence[str | Path] | None = None,
) -> list[str]:
    """Insert scanner paths on ``sys.path`` and set ``PYTHONPATH`` like **run_scanners**.

    Inserts in reverse order so the first entry in the canonical list (story-graph-ops)
    ends up at ``sys.path[0]``, matching **run_scanners.py** in-process inserts.

    Returns the ordered path strings (ops, er, …) used for ``PYTHONPATH``.
    """
    parts = _scanner_pythonpath_parts(
        skill_root,
        language=language,
        extra_pythonpath=extra,
    )
    for s in reversed(parts):
        if s not in sys.path:
            sys.path.insert(0, s)

    prev = os.environ.get("PYTHONPATH", "")
    tail = [prev] if prev else []
    joined = os.pathsep.join(parts + tail)
    if joined:
        os.environ["PYTHONPATH"] = joined
    return parts


def build_scanner_env(
    skill_root: Path | None = None,
    *,
    language: str | None = None,
    extra_pythonpath: Iterable[str | Path] | None = None,
) -> dict[str, str]:
    """Return ``environ`` with **PYTHONPATH** set like **run_scanners.py** (for subprocess tests)."""
    env = os.environ.copy()
    parts = _scanner_pythonpath_parts(
        skill_root,
        language=language,
        extra_pythonpath=extra_pythonpath,
    )
    prev = env.get("PYTHONPATH", "")
    if prev:
        parts = parts + [prev]
    env["PYTHONPATH"] = os.pathsep.join(parts)
    return env


def run_scanner_script(
    scanner_script: Path,
    workspace: Path,
    *,
    skill_root: Path | None = None,
    language: str | None = None,
    capture_output: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run ``python <scanner_script> --workspace <workspace>`` with scanner **PYTHONPATH**."""
    env = build_scanner_env(skill_root=skill_root, language=language)
    cwd = str(skill_root) if skill_root is not None else str(scanner_script.parent)
    return subprocess.run(
        [sys.executable, str(scanner_script), "--workspace", str(workspace)],
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        text=True,
    )


def run_scanner_script_with_cwd(
    scanner_script: Path,
    workspace: Path,
    cwd: Path,
    *,
    skill_root: Path | None = None,
    language: str | None = None,
    capture_output: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Like :func:`run_scanner_script` but explicit *cwd* (matches **run_scanners** ``cwd=str(root)``)."""
    env = build_scanner_env(skill_root=skill_root, language=language)
    return subprocess.run(
        [sys.executable, str(scanner_script), "--workspace", str(workspace)],
        cwd=str(cwd),
        env=env,
        capture_output=capture_output,
        text=True,
    )
