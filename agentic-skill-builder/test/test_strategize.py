"""Build strategy loading (conf/build-strategy.json, --strategy-file)."""

import json
from pathlib import Path

from agentic_skill_builder.strategize import (
    load_build_strategy,
    strategy_filled_enough,
)


def test_load_from_skill_conf(tmp_path):
    conf = tmp_path / "conf"
    conf.mkdir()
    data = {"version": 1, "skill_purpose": "Test purpose"}
    (conf / "build-strategy.json").write_text(json.dumps(data), encoding="utf-8")
    strat, extra, src = load_build_strategy(tmp_path, None)
    assert src == "skill_conf"
    assert strat["skill_purpose"] == "Test purpose"
    assert strategy_filled_enough(strat) is True
    assert any("loaded" in x for x in extra)


def test_load_from_strategy_file_override(tmp_path):
    f = tmp_path / "custom.json"
    f.write_text(json.dumps({"skill_purpose": "From file arg"}), encoding="utf-8")
    strat, extra, src = load_build_strategy(tmp_path, str(f))
    assert "file:" in src
    assert strat["skill_purpose"] == "From file arg"


def test_empty_when_missing():
    strat, extra, src = load_build_strategy(Path("/nonexistent/path/000"), None)
    assert src == "empty"
    assert strat == {}
    assert strategy_filled_enough(strat) is False
    assert any("questionnaire" in x or "skill_purpose" in x for x in extra)


def test_missing_override_file_errors(tmp_path):
    strat, extra, src = load_build_strategy(tmp_path, str(tmp_path / "nope.json"))
    assert src == "error"
    assert strat == {}
