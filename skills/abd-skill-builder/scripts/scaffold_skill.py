#!/usr/bin/env python3
"""
Emit a new skill directory from packaged templates (standards: skill-repo-standards.md).

Does not invoke agentic-skill-builder; run Operator separately:

  agentic-skill-builder run --skill-path <out>
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"


def _load(name: str) -> str:
    return (TEMPLATES / name).read_text(encoding="utf-8")


def _apply(s: str, ctx: dict[str, str]) -> str:
    out = s
    for k, v in ctx.items():
        out = out.replace("{{" + k + "}}", v)
    return out


def scaffold(out: Path, *, name: str, description: str, purpose: str) -> None:
    if out.exists() and any(out.iterdir()):
        raise ValueError(f"refuse: {out} exists and is not empty")
    out.mkdir(parents=True, exist_ok=True)

    title = name.replace("-", " ").title()
    ctx = {
        "skill_name": name,
        "skill_title": title,
        "skill_description": description,
        "skill_summary": f"**{title}** — scaffolded skill. Replace this summary in SKILL.md.",
        "skill_purpose": purpose,
    }

    (out / "SKILL.md").write_text(_apply(_load("SKILL.md.template"), ctx), encoding="utf-8")
    (out / "skill-config.json").write_text(_apply(_load("skill-config.json.template"), ctx), encoding="utf-8")
    conf = out / "conf"
    conf.mkdir(parents=True, exist_ok=True)
    (conf / "build-strategy.json").write_text(_apply(_load("build-strategy.json.template"), ctx), encoding="utf-8")
    (conf / "abd-config.json").write_text(_apply(_load("abd-config.json.template"), ctx), encoding="utf-8")
    (conf / "README.md").write_text(_apply(_load("conf_README.md.template"), ctx), encoding="utf-8")

    parts = out / "content" / "parts"
    phases = parts / "phases"
    phases.mkdir(parents=True, exist_ok=True)
    built = phases / "built"
    built.mkdir(parents=True, exist_ok=True)
    (built / "README.md").write_text(_load("phases_built_README.md.template"), encoding="utf-8")
    (parts / "process.md").write_text(_apply(_load("process.md.template"), ctx), encoding="utf-8")
    (phases / "author.md").write_text(_apply(_load("phase_author.md.template"), ctx), encoding="utf-8")

    scripts = out / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    (scripts / "build.py").write_text(_apply(_load("child_build.py.template"), ctx), encoding="utf-8")
    (scripts / "generate_prompt.py").write_text(_apply(_load("generate_prompt.py.template"), ctx), encoding="utf-8")
    (scripts / "scanner_smoke.py").write_text(_apply(_load("child_scanner_smoke.py.template"), ctx), encoding="utf-8")

    rules = out / "rules"
    rules.mkdir(parents=True, exist_ok=True)
    (rules / "README.md").write_text(_apply(_load("rules_README.md.template"), ctx), encoding="utf-8")
    (rules / "scanners.json").write_text(_apply(_load("scanners.json.template"), ctx), encoding="utf-8")

    test_dir = out / "test"
    test_dir.mkdir(parents=True, exist_ok=True)
    (test_dir / "README.md").write_text(_apply(_load("test_README.md.template"), ctx), encoding="utf-8")

    docs_dir = out / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    checklist_src = ROOT / "content" / "parts" / "library" / "authoring-checklist.md"
    if checklist_src.is_file():
        shutil.copyfile(checklist_src, docs_dir / "authoring-checklist.md")
    else:
        print("Warning: skill-authoring-checklist.md not found; skip docs/authoring-checklist.md", file=sys.stderr)

    print(f"Scaffolded skill at {out.resolve()}")
    print("docs/authoring-checklist.md — track progress with - [ ] / - [x]; resume from first unchecked box.")
    print("conf/abd-config.json must set active_skill_workspace (mandatory). Edit it, then: python scripts/build.py")


def main() -> int:
    p = argparse.ArgumentParser(description="Create a skill skeleton from abd-skill-builder templates.")
    p.add_argument("--name", required=True, help="Skill id / directory name (e.g. my-new-skill)")
    p.add_argument("--out", type=Path, required=True, help="Output directory (e.g. ../my-new-skill)")
    p.add_argument("--description", default="Scaffolded Open Agent Skill package.")
    p.add_argument(
        "--purpose",
        default="Replace with one sentence: what this skill helps users accomplish end-to-end.",
    )
    ns = p.parse_args()
    try:
        scaffold(ns.out.resolve(), name=ns.name, description=ns.description, purpose=ns.purpose)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
