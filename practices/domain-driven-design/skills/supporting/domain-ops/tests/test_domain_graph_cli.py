"""Concurrency safeguards for domain_graph_cli.py write.

Mirrors story-graph-ops test_story_graph_cli_concurrency.py.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

_CLI = Path(__file__).resolve().parents[1] / "scripts" / "domain_graph_cli.py"


def _run(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(_CLI), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


def _minimal_json() -> str:
    return json.dumps(
        {
            "schema": "abd-domain-model/v1",
            "product": "T",
            "scope": "s",
            "modules": [
                {
                    "name": "M",
                    "relationships": [],
                    "key_abstractions": [
                        {
                            "name": "KA",
                            "definition": "d",
                            "relationships": [],
                            "classes": [
                                {
                                    "name": "Thing",
                                    "ka_anchor": True,
                                    "term": "thing",
                                    "extends": None,
                                    "constructor": {"parameter_types": []},
                                    "properties": [],
                                    "operations": [],
                                }
                            ],
                            "references": [],
                            "decisions": [],
                        }
                    ],
                    "boundary_domain": {
                        "relationships": [],
                        "classes": [],
                        "references": [],
                        "decisions": [],
                    },
                }
            ],
        }
    )


def _seed_graph(tmp_path: Path) -> Path:
    p = tmp_path / "domain-model.json"
    p.write_text(_minimal_json() + "\n", encoding="utf-8")
    return p


def test_normal_write_succeeds(tmp_path: Path) -> None:
    p = _seed_graph(tmp_path)
    payload = _minimal_json()
    r = _run("write", "--file", str(p), stdin=payload)
    assert r.returncode == 0, r.stderr


def test_lock_file_cleaned_up_after_successful_write(tmp_path: Path) -> None:
    p = _seed_graph(tmp_path)
    _run("write", "--file", str(p), stdin=_minimal_json())
    assert not p.with_name(p.name + ".lock").exists()


def test_live_lock_refuses_write(tmp_path: Path) -> None:
    p = _seed_graph(tmp_path)
    lock = p.with_name(p.name + ".lock")
    lock.write_text(
        json.dumps({"pid": 99999, "acquired_at": time.time(), "host": "other"}),
        encoding="utf-8",
    )
    try:
        r = _run("write", "--file", str(p), stdin=_minimal_json())
        assert r.returncode == 4, r.stderr
        assert "concurrent write refused" in r.stderr
    finally:
        if lock.exists():
            lock.unlink()


def test_expect_sha_mismatch_refuses_write(tmp_path: Path) -> None:
    p = _seed_graph(tmp_path)
    wrong = "0" * 64
    r = _run("write", "--file", str(p), "--expect-sha", wrong, stdin=_minimal_json())
    assert r.returncode == 3, r.stderr
    assert "expect-sha mismatch" in r.stderr


def test_read_validates_example_fixture(tmp_path: Path) -> None:
    from conftest import PRACTICE_REFERENCES

    example = PRACTICE_REFERENCES / "domain-model-example.json"
    r = _run("read", "--file", str(example), "--pretty")
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["product"] == "Check Resolution"


def test_names_lists_classes_from_example() -> None:
    from conftest import PRACTICE_REFERENCES

    example = PRACTICE_REFERENCES / "domain-model-example.json"
    r = _run("names", "--file", str(example))
    assert r.returncode == 0, r.stderr
    names = r.stdout.splitlines()
    assert "Check" in names
    assert "Trait" in names


def test_sha_matches_file_digest(tmp_path: Path) -> None:
    p = _seed_graph(tmp_path)
    expected = hashlib.sha256(p.read_bytes()).hexdigest()
    r = _run("sha", "--file", str(p))
    assert r.returncode == 0
    assert r.stdout.strip() == expected
