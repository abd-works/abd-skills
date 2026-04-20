"""Smoke: CLI renders outline DrawIO when **agile_bots** ``src`` and a graph file exist."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

_SKILL_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = _SKILL_ROOT / "scripts"
_OPS_SCRIPTS = _SKILL_ROOT.parent / "story-graph-ops" / "scripts"


def _agile_bots_src() -> Path | None:
    env = os.environ.get("AGILE_BOTS_SRC", "").strip()
    if env:
        p = Path(env)
        return p if p.is_dir() else None
    candidate = _SKILL_ROOT.parent.parent.parent / "agile_bots" / "src"
    return candidate if candidate.is_dir() else None


AGILE_BOTS_SRC = _agile_bots_src()

pytestmark = pytest.mark.skipif(
    AGILE_BOTS_SRC is None,
    reason="Set AGILE_BOTS_SRC or place agile_bots next to agilebydesign-skills",
)


def _default_graph() -> Path | None:
    g = _SKILL_ROOT.parent.parent.parent / "agile_bots" / "docs" / "story" / "story-graph.json"
    return g if g.is_file() else None


def test_cli_render_outline_smoke(tmp_path: Path) -> None:
    graph = _default_graph()
    if graph is None:
        pytest.skip("No agile_bots docs/story/story-graph.json at sibling path")
    out = tmp_path / "smoke.drawio"
    env = os.environ.copy()
    parts = [
        str(_SCRIPTS.resolve()),
        str(_OPS_SCRIPTS.resolve()),
        str(AGILE_BOTS_SRC.resolve()),
    ]
    prev = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join(parts + ([prev] if prev else []))
    cli = _SCRIPTS / "drawio_story_sync_cli.py"
    r = subprocess.run(
        [
            sys.executable,
            str(cli),
            "render",
            "--mode",
            "outline",
            "--graph",
            str(graph),
            "--out",
            str(out),
        ],
        env=env,
        capture_output=True,
        text=True,
        cwd=str(_SCRIPTS),
    )
    assert r.returncode == 0, r.stderr + r.stdout
    assert out.is_file() and out.stat().st_size > 100
    line = r.stdout.strip().splitlines()[-1]
    payload = json.loads(line)
    assert payload.get("status") == "ok"
