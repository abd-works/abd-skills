#!/usr/bin/env python3
"""One-time restructure: skills/<family>/ → <family>/ at repo root."""
from __future__ import annotations

import os
import shutil
import stat
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


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


def restructure_story_driven() -> None:
    src = REPO / "skills" / "story-driven-delivery"
    dst = REPO / "story-driven-delivery"
    if dst.exists():
        print("story-driven-delivery already at root")
        return
    if not src.exists():
        print("source missing", src)
        return
    shutil.move(str(src), str(dst))
    skills_dir = dst / "skills"
    skills_dir.mkdir(exist_ok=True)
    skip = {
        "skills", "lib", "content", "agents", "prompts", "instructions",
        "scripts", "common", "README.md",
    }
    for item in list(dst.iterdir()):
        if item.name in skip:
            continue
        if item.is_dir() and (item / "SKILL.md").exists():
            shutil.move(str(item), str(skills_dir / item.name))
    lib_dir = dst / "lib"
    lib_dir.mkdir(exist_ok=True)
    common_pkg = dst / "common" / "diagram_story_sync"
    if common_pkg.is_dir():
        shutil.move(str(common_pkg), str(lib_dir / "diagram_story_sync"))
    _rmtree(dst / "scripts")
    _rmtree(dst / "common")
    for sub in ("agents", "prompts", "content", "instructions"):
        (dst / sub).mkdir(exist_ok=True)
    (dst / "content").mkdir(parents=True, exist_ok=True)
    instr = dst / "instructions"
    for skill in (skills_dir / "drawio-story-sync", skills_dir / "story-graph-ops"):
        ide = skill / "ide-files"
        if ide.is_dir():
            for f in ide.glob("*"):
                if f.is_file():
                    target = instr / f.name
                    if not target.exists():
                        shutil.copy2(f, target)
    guidance = skills_dir / "drawio-story-sync" / "guidance"
    if guidance.is_dir():
        for f in guidance.glob("*.mdc"):
            target = instr / f.name
            if not target.exists():
                shutil.copy2(f, target)
    readme = dst / "lib" / "README.md"
    if not readme.exists():
        readme.write_text(
            "# lib\n\n"
            "Shared Python for story-driven-delivery diagram backends.\n\n"
            "## diagram_story_sync/\n\n"
            "Used by drawio-story-sync and miro-story-sync.\n",
            encoding="utf-8",
        )
    pkg_readme = dst / "README.md"
    if not pkg_readme.exists():
        pkg_readme.write_text(
            "# Story-driven delivery package\n\n"
            "Deploy: `python scripts/deploy_family_package.py "
            "--package story-driven-delivery --to <workspace>`\n",
            encoding="utf-8",
        )
    print("story-driven-delivery restructured")


def restructure_with_source(family: str, source_name: str | None = None) -> None:
    """Move skills/<source_name>/ to <family>/ at repo root."""
    src_name = source_name or family
    src = REPO / "skills" / src_name
    dst = REPO / family
    if dst.exists():
        print(f"{family} already at root")
        return
    if not src.exists():
        print(f"source missing {src}")
        return
    shutil.move(str(src), str(dst))
    skills_dir = dst / "skills"
    skills_dir.mkdir(exist_ok=True)
    skip = {"skills", "lib", "content", "agents", "prompts", "instructions", "scripts", "common"}
    for item in list(dst.iterdir()):
        if item.name in skip:
            continue
        if item.is_dir() and (item / "SKILL.md").exists():
            shutil.move(str(item), str(skills_dir / item.name))
        elif item.is_file() and item.suffix in {".md", ".json"}:
            content_dir = dst / "content"
            content_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(content_dir / item.name))
    common_dir = dst / "common"
    if common_dir.is_dir():
        content_dir = dst / "content"
        content_dir.mkdir(parents=True, exist_ok=True)
        for f in common_dir.rglob("*"):
            if f.is_file():
                rel = f.relative_to(common_dir)
                target = content_dir / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists():
                    shutil.move(str(f), str(target))
        _rmtree(common_dir)
    for sub in ("agents", "prompts", "instructions", "lib"):
        (dst / sub).mkdir(exist_ok=True)
    (dst / "content").mkdir(parents=True, exist_ok=True)
    instr = dst / "instructions"
    for skill in skills_dir.iterdir():
        if not skill.is_dir():
            continue
        ide = skill / "ide-files"
        if ide.is_dir():
            for f in ide.iterdir():
                if f.is_file():
                    target = instr / f.name
                    if not target.exists():
                        shutil.copy2(f, target)
        guidance = skill / "guidance"
        if guidance.is_dir():
            for f in guidance.glob("*.mdc"):
                target = instr / f.name
                if not target.exists():
                    shutil.copy2(f, target)
    readme = dst / "README.md"
    if not readme.exists():
        if family == "context-to-memory":
            blurb = "Convert, chunk, embed, and search document corpora for agent memory.\n\n"
        elif family == "idea-shaping":
            blurb = "Opportunity framing, impact mapping, cost of delay, and validated learning.\n\n"
        else:
            blurb = ""
        readme.write_text(
            f"# {family} package\n\n"
            f"{blurb}"
            f"Deploy: `python scripts/deploy_family_package.py "
            f"--package {family} --to <workspace>`\n",
            encoding="utf-8",
        )
    print(f"{family} restructured")


def restructure_simple(family: str) -> None:
    restructure_with_source(family)


def finish_package(family: str) -> None:
    """Ensure instructions/content exist for an already-moved package."""
    dst = REPO / family
    if not dst.is_dir():
        return
    skills_dir = dst / "skills"
    if not skills_dir.is_dir():
        return
    for sub in ("agents", "prompts", "instructions", "lib"):
        (dst / sub).mkdir(exist_ok=True)
    (dst / "content").mkdir(parents=True, exist_ok=True)
    instr = dst / "instructions"
    for skill in skills_dir.iterdir():
        if not skill.is_dir():
            continue
        ide = skill / "ide-files"
        if ide.is_dir():
            for f in ide.iterdir():
                if f.is_file():
                    target = instr / f.name
                    if not target.exists():
                        shutil.copy2(f, target)
        guidance = skill / "guidance"
        if guidance.is_dir():
            for f in guidance.glob("*.mdc"):
                target = instr / f.name
                if not target.exists():
                    shutil.copy2(f, target)
    _rmtree(dst / "common")
    scripts = dst / "scripts"
    if scripts.is_dir() and not any(scripts.rglob("*.*")):
        _rmtree(scripts)
    readme = dst / "README.md"
    if not readme.exists():
        readme.write_text(
            f"# {family} package\n\n"
            f"Deploy: `python scripts/deploy_family_package.py "
            f"--package {family} --to <workspace>`\n",
            encoding="utf-8",
        )


def restructure_utilities() -> None:
    """Move utilities/skills/ to utilities/; flatten ai-research-assistant skills; move agent."""
    src = REPO / "skills" / "utilities"
    dst = REPO / "utilities"
    if dst.exists() and (dst / "skills").is_dir() and any((dst / "skills").iterdir()):
        print("utilities already at root")
        return
    if not src.is_dir():
        print("source missing skills/utilities")
        return
    for sub in ("agents", "skills", "content", "instructions", "prompts", "lib", "scripts"):
        (dst / sub).mkdir(parents=True, exist_ok=True)
    for item in sorted(src.iterdir()):
        if not item.is_dir():
            continue
        if item.name == "abd-proposal-respond" and (item / "SKILL.md").is_file():
            target = dst / "skills" / item.name
            if target.exists():
                continue
            shutil.move(str(item), str(target))
        elif item.name == "ai-research-assistant":
            for child in sorted(item.iterdir()):
                if child.is_dir() and (child / "SKILL.md").is_file():
                    target = dst / "skills" / child.name
                    if not target.exists():
                        shutil.move(str(child), str(target))
    agent_src = REPO / "agents" / "ai-research-assistant"
    agent_dst = dst / "agents" / "ai-research-assistant"
    if agent_src.is_dir() and not agent_dst.exists():
        shutil.move(str(agent_src), str(agent_dst))
    _rmtree(src)
    readme = dst / "README.md"
    if not readme.exists():
        readme.write_text(
            "# utilities package\n\n"
            "Proposal response, AI research assistant skills, and related utilities.\n\n"
            "Deploy: `python scripts/deploy_family_package.py "
            "--package utilities --to <workspace>`\n",
            encoding="utf-8",
        )
    print("utilities restructured")


def move_agent_to_family(agent_name: str, family: str) -> None:
    """Move agents/<agent_name>/ into <family>/agents/ when still at repo root."""
    src = REPO / "agents" / agent_name
    dst = REPO / family / "agents" / agent_name
    if not src.is_dir():
        return
    if dst.exists():
        print(f"  {agent_name} already in {family}/agents/")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    print(f"  moved agents/{agent_name} -> {family}/agents/{agent_name}")


def move_orphan_agents() -> None:
    """Place remaining repo-root agents into their family packages."""
    print("\norphan agents")
    move_agent_to_family("abd-context-to-memory", "context-to-memory")
    ddd_stub = REPO / "agents" / "abd-domain-driven-design"
    if ddd_stub.is_dir() and not (REPO / "domain-driven-design" / "agents" / "abd-domain-driven-design").exists():
        move_agent_to_family("abd-domain-driven-design", "domain-driven-design")


def main() -> None:
    restructure_story_driven()
    for family in (
        "domain-driven-design",
        "architecture-centric-engineering",
        "user-experience-design",
    ):
        restructure_simple(family)
        finish_package(family)
    restructure_with_source("context-to-memory")
    finish_package("context-to-memory")
    restructure_with_source("idea-shaping", source_name="idea shaping")
    finish_package("idea-shaping")
    restructure_with_source("skill-builder")
    finish_package("skill-builder")
    restructure_with_source("skill-helpers")
    finish_package("skill-helpers")
    restructure_utilities()
    finish_package("utilities")
    move_orphan_agents()
    for family in FAMILY_PACKAGES_ALL:
        finish_package(family)
    finish_package("story-driven-delivery")
    print("done")


FAMILY_PACKAGES_ALL = (
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


if __name__ == "__main__":
    main()
