#!/usr/bin/env python3
"""
Emit a new skill package from ``skills/build_skill/templates/skill-scaffold/``
(see ``content/parts/library/skill-structure-and-concepts.md``).

Copies the template with ``{{…}}`` substitution, then ``library/base/``,
``process-phases.md``, and ``scripts/base/`` from this repo.

Run: ``python skills/build_skill/scripts/build_skill.py --name … --out …``
(from **abd-skill-builder** root). Then in the new skill: ``python scripts/base/build.py``.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# skills/build_skill/scripts/build_skill.py -> abd-skill-builder root
ROOT = Path(__file__).resolve().parents[3]
BUILDER_BASE_SCRIPTS = ROOT / "scripts" / "base"
BUILDER_LIBRARY_BASE = ROOT / "content" / "parts" / "library" / "base"
SCAFFOLD = ROOT / "skills" / "build_skill" / "templates" / "skill-scaffold"

_DEFAULT_PLACEHOLDERS: dict[str, str] = {
    "phase_name": "Author",
    "phase_slug": "author",
    "phase_description": "Write and refine skill content (library, phases, rules).",
    "phase_input": "Prior plan and workspace",
    "phase_output": "Draft content under content/parts/",
    "code_phase_name": "Plan script and build",
    "code_phase_slug": "plan-script-build",
    "code_phase_description": "Plan automation and wire scripts under scripts/<skill>.",
    "code_phase_input": "Author phase output",
    "code_phase_output": "Runnable scripts and build wiring",
    "code_phase_script": "plan_build.py",
    "description": "Describe what this script does after you add it.",
    "rule_id": "example-rule",
}


def _apply(s: str, ctx: dict[str, str]) -> str:
    out = s
    for k, v in ctx.items():
        out = out.replace("{{" + k + "}}", v)
    return out


def _copy_template_tree(out: Path, ctx: dict[str, str]) -> None:
    if not SCAFFOLD.is_dir():
        raise ValueError(f"missing skill template directory: {SCAFFOLD}")

    skill_name = ctx["skill_name"]
    rule_id = ctx["rule_id"]

    for src in sorted(SCAFFOLD.rglob("*")):
        if src.is_dir():
            continue
        rel = src.relative_to(SCAFFOLD)

        parts: list[str] = []
        for p in rel.parts:
            if p == "{{skill_name}}":
                p = skill_name
            if "{{rule_id}}" in p:
                p = p.replace("{{rule_id}}", rule_id)
            parts.append(p)
        dst = out.joinpath(*parts)
        dst.parent.mkdir(parents=True, exist_ok=True)

        raw = src.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            dst.write_bytes(raw)
            continue

        text = _apply(text, ctx)
        if "my-skill" in text:
            text = text.replace("my-skill", skill_name)
        dst.write_text(text, encoding="utf-8")

    phases = out / "content" / "parts" / "phases"
    pt = phases / "phase-template.md"
    if pt.is_file():
        (phases / "author.md").write_text(pt.read_text(encoding="utf-8"), encoding="utf-8")
    ct = phases / "code-phase-template.md"
    if ct.is_file():
        (phases / "plan-script-build.md").write_text(ct.read_text(encoding="utf-8"), encoding="utf-8")


def _copy_builder_library_base(out: Path) -> None:
    if not BUILDER_LIBRARY_BASE.is_dir():
        raise ValueError(f"missing builder library/base: {BUILDER_LIBRARY_BASE}")
    dst = out / "content" / "parts" / "library" / "base"
    dst.mkdir(parents=True, exist_ok=True)
    for src in sorted(BUILDER_LIBRARY_BASE.iterdir()):
        if src.is_file():
            shutil.copy2(src, dst / src.name)


def _copy_builder_process_phases_norm(out: Path) -> None:
    src = ROOT / "content" / "parts" / "library" / "process-phases.md"
    if not src.is_file():
        raise ValueError(f"missing builder library process-phases.md: {src}")
    dst_lib = out / "content" / "parts" / "library"
    dst_lib.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst_lib / "process-phases.md")


def _copy_canonical_base_scripts(out: Path) -> None:
    if not BUILDER_BASE_SCRIPTS.is_dir():
        raise ValueError(f"missing builder scripts/base: {BUILDER_BASE_SCRIPTS}")
    dst = out / "scripts" / "base"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(BUILDER_BASE_SCRIPTS, dst)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Emit a new skill package from skills/build_skill/templates/skill-scaffold/.",
    )
    p.add_argument("--name", required=True, help="Skill id / directory name (e.g. my-new-skill)")
    p.add_argument("--out", type=Path, required=True, help="Output directory (e.g. ../my-new-skill)")
    p.add_argument("--description", default="Open Agent Skill package (build_skill).")
    p.add_argument(
        "--purpose",
        default="Replace with one sentence: what this skill helps users accomplish end-to-end.",
    )
    ns = p.parse_args()
    out = ns.out.resolve()
    try:
        if out.exists() and any(out.iterdir()):
            raise ValueError(f"refuse: {out} exists and is not empty")

        out.mkdir(parents=True, exist_ok=True)
        title = ns.name.replace("-", " ").title()
        ctx: dict[str, str] = {
            **_DEFAULT_PLACEHOLDERS,
            "skill_name": ns.name,
            "skill_title": title,
            "skill_description": ns.description,
            "skill_summary": f"**{title}** — new skill package. Replace this summary in SKILL.md.",
            "skill_purpose": ns.purpose,
        }

        _copy_template_tree(out, ctx)
        _copy_builder_library_base(out)
        _copy_builder_process_phases_norm(out)
        _copy_canonical_base_scripts(out)

        print(f"Built skill package at {out.resolve()}")
        print(
            "Shared library/base/ (including checklist.md): content/parts/library/base/ copied from "
            "abd-skill-builder; refresh when standards change. See skill-structure-and-concepts.md "
            "(## Authoring checklist — injector body)."
        )
        print(
            "Progress checklists under <active_skill_workspace>/<skill_name>/progress/: "
            "see content/parts/library/base/checklist.md and scripts/base/workspace_checklists.py."
        )
        print(
            "skill-config.json → workspace.active_skill_workspace must be set for runtime. "
            "Use: python scripts/base/set_workspace.py <path> — then: python scripts/base/build.py"
        )
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
