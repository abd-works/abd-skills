#!/usr/bin/env python3
"""Deploy a family capability package into an engagement workspace.

Each family package at the agilebydesign-skills repo root follows the same layout::

    <family>/
        agents/           optional orchestrators
        skills/           one folder per practice skill (SKILL.md)
        content/          shared prose (merged into .cursor/content/)
        lib/              shared Python packages (e.g. diagram_story_sync)
        instructions/     .mdc and .instructions.md → rules / instructions
        prompts/          .prompt.md → commands / prompts

Usage::

    python scripts/deploy_family_package.py --package delivery --to C:\\dev\\abd-pet-store-demo
    python scripts/deploy_family_package.py --package story-driven-delivery --to C:\\dev\\abd-pet-store-demo
"""
from __future__ import annotations

import argparse
import os
import shutil
import stat
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

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

_AGENT_SKILL_REF_REWRITES = (
    ("../../skills/", "../skills/"),
)

_LEGACY_ROOT_DIRS = ("agents", "skills")

_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache")


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
    shutil.rmtree(path, ignore_errors=False)


def _is_reparse_point(path: Path) -> bool:
    try:
        st = os.lstat(path)
    except OSError:
        return False
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    attrs = getattr(st, "st_file_attributes", 0)
    return bool(attrs & reparse) or stat.S_ISLNK(st.st_mode)


def _clear_skill_junctions(skills_root: Path) -> None:
    """Remove junction/symlink skill folders so family copy deploy can replace them."""
    if not skills_root.is_dir():
        return
    for child in sorted(skills_root.iterdir()):
        if _is_reparse_point(child) or child.is_symlink():
            print(f"  remove junction {child.name}")
            _force_remove(child)


def _force_remove(path: Path) -> None:
    """Remove a file, directory, or junction/symlink at ``path``."""
    if not path.exists() and not path.is_symlink() and not _is_reparse_point(path):
        return
    if _is_reparse_point(path) or path.is_symlink() or path.is_dir():
        import subprocess
        subprocess.run(
            ["cmd", "/c", "rmdir", str(path)],
            check=False,
            capture_output=True,
        )
        if path.exists() or _is_reparse_point(path):
            subprocess.run(
                ["cmd", "/c", "rmdir", "/s", "/q", str(path)],
                check=False,
                capture_output=True,
            )
        if path.exists() or _is_reparse_point(path):
            _rmtree(path)
        return
    try:
        os.chmod(path, stat.S_IWUSR)
    except OSError:
        pass
    path.unlink(missing_ok=True)


def _replace_tree(src: Path, dst: Path) -> None:
    if not src.is_dir():
        print(f"  skip missing {src}", file=sys.stderr)
        return
    if dst.exists() or dst.is_symlink() or _is_reparse_point(dst):
        try:
            _force_remove(dst)
        except OSError as exc:
            print(f"  warning: could not remove {dst} ({exc}); syncing in place", file=sys.stderr)
            _sync_tree(src, dst)
            print(f"  {src} -> {dst}")
            return
    try:
        shutil.copytree(src, dst, ignore=_IGNORE)
    except OSError as exc:
        print(f"  warning: replace {dst} failed ({exc}); syncing in place", file=sys.stderr)
        _sync_tree(src, dst)
    print(f"  {src} -> {dst}")


def _sync_tree(src: Path, dst: Path) -> None:
    if not src.is_dir():
        print(f"  skip missing {src}", file=sys.stderr)
        return
    for item in src.rglob("*"):
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            if (target.exists() or _is_reparse_point(target)) and not target.is_dir() and not _is_reparse_point(target):
                _force_remove(target)
            target.mkdir(parents=True, exist_ok=True)
        else:
            if target.exists() or _is_reparse_point(target):
                _force_remove(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
    print(f"  {src} -> {dst}")


def _rewrite_agent_skill_refs(agent_dir: Path) -> None:
    for name in ("AGENT.md", "AGENTS.md"):
        agent_md = agent_dir / name
        if not agent_md.is_file():
            continue
        text = agent_md.read_text(encoding="utf-8")
        for old, new in _AGENT_SKILL_REF_REWRITES:
            text = text.replace(old, new)
        agent_md.write_text(text, encoding="utf-8")


def _copy_glob_files(src_dir: Path, dst_dir: Path, pattern: str, label: str) -> None:
    if not src_dir.is_dir():
        return
    dst_dir.mkdir(parents=True, exist_ok=True)
    for f in sorted(src_dir.glob(pattern)):
        if f.is_file():
            shutil.copy2(f, dst_dir / f.name)
            print(f"  {f.name} -> {label}/")


def _sync_local_content(content_src: Path, ide_root: Path) -> None:
    if not content_src.is_dir():
        return
    _sync_tree(content_src, ide_root / "content")


def _deploy_agents(agents_root: Path, source: Path) -> None:
    agents_src = source / "agents"
    if not agents_src.is_dir():
        return
    agents_root.mkdir(parents=True, exist_ok=True)
    stale_content = agents_root / "content"
    if stale_content.is_dir():
        print(f"  remove stale {stale_content}")
        try:
            _rmtree(stale_content)
        except OSError as exc:
            print(f"  warning: could not remove {stale_content}: {exc}", file=sys.stderr)
    for agent_dir in sorted(agents_src.iterdir()):
        if not agent_dir.is_dir():
            continue
        if (agent_dir / "AGENT.md").is_file() or (agent_dir / "AGENTS.md").is_file():
            _replace_tree(agent_dir, agents_root / agent_dir.name)
            _rewrite_agent_skill_refs(agents_root / agent_dir.name)


def _deploy_skills(skills_root: Path, source: Path) -> None:
    skills_src = source / "skills"
    if not skills_src.is_dir():
        return
    skills_root.mkdir(parents=True, exist_ok=True)
    stale_content = skills_root / "content"
    if stale_content.is_dir():
        print(f"  remove stale {stale_content}")
        try:
            _rmtree(stale_content)
        except OSError as exc:
            print(f"  warning: could not remove {stale_content}: {exc}", file=sys.stderr)
    for skill_dir in sorted(skills_src.iterdir()):
        if skill_dir.is_dir() and skill_dir.name != "content" and (skill_dir / "SKILL.md").is_file():
            _replace_tree(skill_dir, skills_root / skill_dir.name)


def _deploy_lib(lib_root: Path, source: Path) -> None:
    lib_src = source / "lib"
    if not lib_src.is_dir():
        return
    lib_root.mkdir(parents=True, exist_ok=True)
    for item in sorted(lib_src.iterdir()):
        if item.is_dir():
            _replace_tree(item, lib_root / item.name)


def _deploy_ide_tree(ide_root: Path, source: Path, *, vscode: bool) -> None:
    instructions = source / "instructions"
    prompts = source / "prompts"
    label = ide_root.name

    print(f"{label}/agents/")
    _deploy_agents(ide_root / "agents", source)

    print(f"{label}/skills/")
    _deploy_skills(ide_root / "skills", source)

    print(f"{label}/lib/")
    _deploy_lib(ide_root / "lib", source)

    if vscode:
        _copy_glob_files(instructions, ide_root / "instructions", "*.mdc", f"{label}/instructions")
        _copy_glob_files(instructions, ide_root, "*.instructions.md", label)
        _copy_glob_files(prompts, ide_root / "prompts", "*.prompt.md", f"{label}/prompts")
    else:
        _copy_glob_files(instructions, ide_root / "rules", "*.mdc", f"{label}/rules")
        _copy_glob_files(prompts, ide_root / "commands", "*.prompt.md", f"{label}/commands")

    _sync_local_content(source / "content", ide_root)


def _normalize_ide(ide: str) -> str:
    if ide == "github":
        return "vscode"
    return ide


def _remove_legacy_root_deploy(workspace: Path) -> None:
    for name in _LEGACY_ROOT_DIRS:
        path = workspace / name
        if not path.is_dir():
            continue
        try:
            print(f"remove legacy {path}")
            _rmtree(path)
        except OSError as exc:
            print(f"  warning: could not remove {path}: {exc}", file=sys.stderr)


def deploy_family_package(
    workspace: Path,
    source: Path,
    *,
    ide: str = "cursor",
    skip_ide: bool = False,
    remove_legacy: bool = False,
) -> int:
    workspace = workspace.resolve()
    source = source.resolve()

    if not source.is_dir():
        print(f"error: package not found at {source}", file=sys.stderr)
        return 1

    ide = _normalize_ide(ide)
    if ide not in ("cursor", "vscode", "both"):
        print(f"error: unknown --ide {ide!r}", file=sys.stderr)
        return 1

    print(f"deploy {source.name} ({source}) -> {workspace} (ide={ide})")
    if remove_legacy:
        _remove_legacy_root_deploy(workspace)

    if not skip_ide:
        if ide in ("cursor", "both"):
            _deploy_ide_tree(workspace / ".cursor", source, vscode=False)
        if ide in ("vscode", "both"):
            _deploy_ide_tree(workspace / ".github", source, vscode=True)

    return 0


def deploy_all_family_packages(
    workspace: Path,
    repo_root: Path | None = None,
    *,
    ide: str = "cursor",
    packages: tuple[str, ...] | None = None,
) -> int:
    repo_root = (repo_root or REPO_ROOT).resolve()
    workspace = workspace.resolve()
    packages = packages or FAMILY_PACKAGES
    ide = _normalize_ide(ide)

    print(f"deploy family packages -> {workspace} (ide={ide})")
    _remove_legacy_root_deploy(workspace)

    if ide in ("cursor", "both"):
        _clear_skill_junctions(workspace / ".cursor" / "skills")
    if ide in ("vscode", "both"):
        _clear_skill_junctions(workspace / ".github" / "skills")

    rc = 0
    for name in packages:
        source = repo_root / name
        if not source.is_dir():
            print(f"  skip missing package {source}", file=sys.stderr)
            continue
        if deploy_family_package(workspace, source, ide=ide, remove_legacy=False) != 0:
            rc = 1
    print("done")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--to", required=True, type=Path, dest="workspace",
                    help="Engagement workspace repo root")
    ap.add_argument(
        "--package",
        choices=("all",) + FAMILY_PACKAGES,
        default="all",
        help="Family package to deploy (default: all)",
    )
    ap.add_argument("--source", type=Path, default=None,
                    help="Override package path (requires --package other than all)")
    ap.add_argument("--skip-ide", action="store_true",
                    help="Skip deploy")
    ap.add_argument(
        "--ide",
        choices=("cursor", "vscode", "github", "both"),
        default="cursor",
    )
    ns = ap.parse_args()

    if ns.package == "all":
        return deploy_all_family_packages(ns.workspace, ide=_normalize_ide(ns.ide))

    source = ns.source or (REPO_ROOT / ns.package)
    return deploy_family_package(
        ns.workspace,
        source,
        ide=_normalize_ide(ns.ide),
        skip_ide=ns.skip_ide,
        remove_legacy=True,
    )


if __name__ == "__main__":
    raise SystemExit(main())
