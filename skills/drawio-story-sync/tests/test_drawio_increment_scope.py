"""DrawIOSynchronizer: increment scope skips when increment name is missing from graph."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from drawio_story_sync.story_io_synchronizer import DrawIOSynchronizer

pytestmark = pytest.mark.skipif(
    not Path(__file__).resolve().parents[1].parent.joinpath("story-graph-ops", "scripts").is_dir(),
    reason="story-graph-ops sibling required for drawio_story_sync imports",
)


def test_increment_scope_skips_when_increment_missing(tmp_path: Path) -> None:
    sg = tmp_path / "story-graph.json"
    sg.write_text(json.dumps({"epics": [], "increments": []}), encoding="utf-8")
    out = tmp_path / "out.drawio"
    sync = DrawIOSynchronizer()
    result = sync.render(
        sg,
        out,
        renderer_command="render-exploration",
        scope="increment:Bring Heroes to the Table",
    )
    assert result.get("skipped") is True
    assert "Bring Heroes" in result.get("skip_reason", "")
    assert not out.exists()
