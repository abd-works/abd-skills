#!/usr/bin/env python3
"""Normalize family packages to the standard layout (like domain-driven-design).

Standard slots at ``<family>/``:

    agents/        orchestrators (may be empty)
    skills/        one folder per practice skill
    content/       shared prose — flat files or semantic subfolders (stages/, roles/)
    instructions/  .mdc / .instructions.md for deploy → rules
    prompts/       .prompt.md for deploy → commands
    lib/           shared Python only when needed (e.g. story-driven-delivery)
    scripts/       package-level scripts only when needed (e.g. delivery)
    README.md

Removes ``common/``, hoists ``content/reference/`` and ``content/catalog/`` into ``content/``.
"""
from __future__ import annotations

import os
import shutil
import stat
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

FAMILY_PACKAGES = (
    "delivery",
    "story-driven-delivery",
    "domain-driven-design",
    "architecture-centric-engineering",
    "user-experience-design",
    "context-to-memory",
    "idea-shaping",
    "skill-builder",
    "skill-helpers",
    "utilities",
)

STANDARD_DIRS = ("agents", "skills", "content", "instructions", "prompts", "lib", "scripts")
CONTENT_HOIST_DIRS = ("reference", "catalog")
ROOT_CONTENT_SUFFIXES = {".md", ".json", ".txt", ".pptx", ".docx", ".pdf"}


def _rmtree(path: Path) -> None:
    if not path.exists():
        return
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            fp = os.path.join(root, name)
            try:
                os.chmod(fp, stat.S_IWUSR)
            except OSError:
                pass
        for name in dirs:
            dp = os.path.join(root, name)
            try:
                os.chmod(dp, stat.S_IWUSR)
            except OSError:
                pass
    shutil.rmtree(path, ignore_errors=True)
    if path.exists():
        import subprocess
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(path)], check=False)


def _hoist_content_subdir(content: Path, sub: str) -> None:
    src = content / sub
    if not src.is_dir():
        return
    for item in src.rglob("*"):
        if item.is_file():
            rel = item.relative_to(src)
            target = content / rel
            if target.exists():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(target))
    _rmtree(src)
    print(f"  hoisted content/{sub}/ -> content/")


def _move_root_strays(package: Path) -> None:
    content = package / "content"
    content.mkdir(parents=True, exist_ok=True)
    skip = set(STANDARD_DIRS) | {"README.md"}
    for item in list(package.iterdir()):
        if item.name in skip:
            continue
        if item.is_file() and item.suffix.lower() in ROOT_CONTENT_SUFFIXES:
            target = content / item.name
            if not target.exists():
                shutil.move(str(item), str(target))
                print(f"  moved stray {item.name} -> content/")


def _remove_empty_dir(path: Path) -> None:
    if path.is_dir() and not any(path.rglob("*")):
        _rmtree(path)
        if not path.exists():
            print(f"  removed empty {path.relative_to(path.parents[1])}/")


def normalize_package(family: str) -> None:
    package = REPO / family
    if not package.is_dir():
        print(f"skip missing {family}")
        return
    print(f"\n{family}/")
    for sub in STANDARD_DIRS:
        (package / sub).mkdir(exist_ok=True)

    content = package / "content"
    for sub in CONTENT_HOIST_DIRS:
        _hoist_content_subdir(content, sub)

    if (package / "common").exists():
        common = package / "common"
        for f in common.rglob("*"):
            if f.is_file():
                rel = f.relative_to(common)
                target = content / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists():
                    shutil.move(str(f), str(target))
        _rmtree(common)
        print("  removed common/ (files -> content/)")

    _move_root_strays(package)

    # Remove empty scripts/ unless delivery keeps copy_delivery.py
    scripts = package / "scripts"
    if scripts.is_dir():
        has_files = any(scripts.rglob("*.*"))
        if not has_files:
            _remove_empty_dir(scripts)

    # Remove lib/ only when completely empty (story-driven keeps diagram_story_sync)
    lib = package / "lib"
    if lib.is_dir() and not any(lib.iterdir()):
        pass  # keep empty lib/ as standard slot (matches domain-driven-design)

    _rmtree(package / "common")


def main() -> None:
    for family in FAMILY_PACKAGES:
        normalize_package(family)
    print("\ndone")


if __name__ == "__main__":
    main()
