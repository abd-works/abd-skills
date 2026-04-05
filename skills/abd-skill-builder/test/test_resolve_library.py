"""Library path resolution: skill root overrides required, then base."""

from __future__ import annotations

from pathlib import Path

import pytest

# scripts/base/build.py adds scripts/base to path; tests import from there via conftest or path hack
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "base"))

from instructions import _resolve_library_md  # noqa: E402


@pytest.fixture
def parts_dir(tmp_path: Path) -> Path:
    lib = tmp_path / "library"
    (lib / "base").mkdir(parents=True)
    (lib / "required").mkdir(parents=True)
    return tmp_path


def test_prefers_root_over_base_and_required(parts_dir: Path) -> None:
    (parts_dir / "library" / "foo.md").write_text("root", encoding="utf-8")
    (parts_dir / "library" / "required" / "foo.md").write_text("required", encoding="utf-8")
    (parts_dir / "library" / "base" / "foo.md").write_text("base", encoding="utf-8")
    p = _resolve_library_md(parts_dir, "foo.md")
    assert p is not None
    assert p.read_text(encoding="utf-8") == "root"


def test_prefers_required_over_base(parts_dir: Path) -> None:
    (parts_dir / "library" / "required" / "foo.md").write_text("required", encoding="utf-8")
    (parts_dir / "library" / "base" / "foo.md").write_text("base", encoding="utf-8")
    p = _resolve_library_md(parts_dir, "foo.md")
    assert p is not None
    assert p.read_text(encoding="utf-8") == "required"


def test_falls_back_to_base_when_only_base_exists(parts_dir: Path) -> None:
    (parts_dir / "library" / "base" / "foo.md").write_text("base", encoding="utf-8")
    p = _resolve_library_md(parts_dir, "foo.md")
    assert p is not None
    assert p.read_text(encoding="utf-8") == "base"


def test_falls_back_to_library_root_when_only_root_exists(parts_dir: Path) -> None:
    (parts_dir / "library" / "outline.md").write_text("only root", encoding="utf-8")
    p = _resolve_library_md(parts_dir, "outline.md")
    assert p is not None
    assert p.read_text(encoding="utf-8") == "only root"


def test_skill_structure_legacy_prefers_root_over_base(parts_dir: Path) -> None:
    (parts_dir / "library" / "skill-structure-and-concepts.md").write_text("root", encoding="utf-8")
    (parts_dir / "library" / "base" / "skill-structure-and-concepts.md").write_text("base", encoding="utf-8")
    p = _resolve_library_md(parts_dir, "Skill structure and concepts.md")
    assert p is not None
    assert p.read_text(encoding="utf-8") == "root"


def test_skill_structure_legacy_falls_back_to_base(parts_dir: Path) -> None:
    (parts_dir / "library" / "base" / "skill-structure-and-concepts.md").write_text("base", encoding="utf-8")
    p = _resolve_library_md(parts_dir, "Skill structure and concepts.md")
    assert p is not None
    assert p.read_text(encoding="utf-8") == "base"
