"""Smoke: **run_scanners.py** exits 0 when a skill has no scanners."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def test_run_scanners_no_scanners_story_graph_ops() -> None:
    skills = Path(__file__).resolve().parents[2]
    root = skills / "story-graph-ops"
    if not root.is_dir():
        pytest.skip("story-graph-ops skill missing")
    r = subprocess.run(
        [sys.executable, str(_SCRIPTS / "run_scanners.py"), "--skill-root", str(root)],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
