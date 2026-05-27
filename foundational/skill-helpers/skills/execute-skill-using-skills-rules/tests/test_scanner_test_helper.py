"""Tests for :mod:`scanner_test_helper` alignment with **run_scanners.py**."""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from scanner_test_helper import (
    build_scanner_env,
    execute_skill_using_skills_rules_scripts,
    prepend_scanner_pythonpath,
    story_graph_ops_scripts,
)


def test_paths_exist() -> None:
    assert execute_skill_using_skills_rules_scripts().is_dir()
    assert (execute_skill_using_skills_rules_scripts() / "run_scanners.py").is_file()
    assert story_graph_ops_scripts().is_dir()
    assert (story_graph_ops_scripts() / "story_map.py").is_file()


def test_build_scanner_env_pythonpath_order_matches_run_scanners() -> None:
    env = build_scanner_env()
    parts = env["PYTHONPATH"].split(os.pathsep)
    ops = str(story_graph_ops_scripts().resolve())
    er = str(execute_skill_using_skills_rules_scripts().resolve())
    assert ops in parts
    assert er in parts
    assert parts.index(ops) < parts.index(er)


def test_prepend_imports_story_map() -> None:
    prepend_scanner_pythonpath()
    import story_map  # noqa: PLC0415

    assert hasattr(story_map, "StoryMap")


@pytest.mark.parametrize("skill_name", ["story-graph-ops", "drawio-story-sync"])
def test_build_scanner_env_with_skill_root(skill_name: str) -> None:
    repo_skills = Path(__file__).resolve().parents[2]
    root = repo_skills / skill_name
    if not root.is_dir():
        pytest.skip(f"missing {root}")
    env = build_scanner_env(root)
    scripts = str((root / "scripts").resolve())
    if (root / "scripts").is_dir():
        assert scripts in env["PYTHONPATH"]
