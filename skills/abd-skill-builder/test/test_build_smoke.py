"""Smoke tests: build.py emits root + content/built AGENTS in sync."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_build_py_exits_zero() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr


def test_root_and_built_agents_match() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build.py")],
        cwd=ROOT,
        check=True,
    )
    root_agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    built_agents = (ROOT / "content" / "built" / "AGENTS.md").read_text(encoding="utf-8")
    assert root_agents == built_agents
    assert root_agents.startswith("# AGENTS — abd-skill-builder")


def test_content_built_readme_exists_after_build() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build.py")],
        cwd=ROOT,
        check=True,
    )
    readme = ROOT / "content" / "built" / "README.md"
    assert readme.is_file()
    body = readme.read_text(encoding="utf-8")
    assert "static_built" in body
    assert "AGENTS.md" in body
