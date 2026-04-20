"""Smoke: CLI renders outline DrawIO using only this skill + story-graph-ops."""
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

pytestmark = pytest.mark.skipif(
    not _OPS_SCRIPTS.is_dir(),
    reason="story-graph-ops skill not present as sibling (skills/story-graph-ops/scripts)",
)


_MINIMAL_GRAPH = {
    "epics": [
        {
            "name": "Epic A",
            "sequential_order": 1.0,
            "sub_epics": [
                {
                    "name": "Sub A",
                    "sequential_order": 1.0,
                    "sub_epics": [],
                    "story_groups": [
                        {
                            "name": None,
                            "type": "and",
                            "connector": None,
                            "stories": [
                                {
                                    "name": "Story One",
                                    "sequential_order": 1.0,
                                    "story_type": "user",
                                    "users": [],
                                    "acceptance_criteria": [],
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    ],
    "increments": [],
}


def test_cli_render_outline_smoke(tmp_path: Path) -> None:
    graph = tmp_path / "story-graph.json"
    graph.write_text(json.dumps(_MINIMAL_GRAPH), encoding="utf-8")
    out = tmp_path / "smoke.drawio"
    env = os.environ.copy()
    parts = [str(_SCRIPTS.resolve()), str(_OPS_SCRIPTS.resolve())]
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
