#!/usr/bin/env python3
"""Scaffold a multi-skill agent: asks what goes in it, then writes the tree.

Contract (abd-skill-builder):
  content/outline.md, principles.md, purpose.md, role.md
  scripts/build.py  → merges those into AGENTS.md
  skills/workspace/ → SKILL.md + get/set workspace scripts
  skill-config.json → agents_md.sections + workspace

Interactive by default. Non-interactive:  --batch --name X --out PARENT (stub text).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_TEMPLATES = _HERE.parent / "templates"
_BUILD_PY = _TEMPLATES / "build.py"
_WORKSPACE_SKILL = _TEMPLATES / "workspace_skill"

_SECTIONS: list[dict[str, str]] = [
    {"heading": "Outline", "file": "outline.md"},
    {"heading": "Principles", "file": "principles.md"},
    {"heading": "Purpose", "file": "purpose.md"},
    {"heading": "Role", "file": "role.md"},
]


def _ask(prompt: str, default: str = "") -> str:
    if default:
        line = input(f"{prompt} [{default}]: ").strip()
        return line if line else default
    line = input(f"{prompt}: ").strip()
    return line


def _gather_interactive(default_name: str = "", default_out: str = "") -> dict[str, str]:
    print("New multi-skill agent — answer each prompt (Enter keeps [default]).\n", flush=True)
    name = _ask("Agent folder name (directory will be <parent>/<name>)", default_name)
    if not name:
        raise SystemExit("Agent name is required.")
    out = _ask("Parent directory (must exist)", default_out)
    if not out:
        raise SystemExit("Parent directory is required.")
    title = _ask("Title for AGENTS.md heading", name)
    desc = _ask("One-line SKILL.md description", f"Orchestrator — see AGENTS.md ({name}).")

    print("\n--- Content for content/*.md (orchestration narrative) ---\n", flush=True)
    outline = _ask("Outline: stages / flow / hand-offs between skills", "(Edit outline.md after scaffold.)")
    principles = _ask("Principles: non-negotiables for this agent", "(Edit principles.md after scaffold.)")
    purpose = _ask("Purpose: why this agent exists", "(Edit purpose.md after scaffold.)")
    role = _ask("Role: who the orchestrator is and what it delegates", "(Edit role.md after scaffold.)")

    print("\n--- Workspace ---\n", flush=True)
    ws = _ask("Initial active_skill_workspace (engagement root, or . for agent dir)", ".")

    return {
        "name": name,
        "out": out,
        "title": title,
        "desc": desc,
        "outline": outline,
        "principles": principles,
        "purpose": purpose,
        "role": role,
        "workspace": ws,
    }


def _gather_batch(name: str, out: str) -> dict[str, str]:
    return {
        "name": name,
        "out": out,
        "title": name,
        "desc": f"Orchestrator — see AGENTS.md ({name}).",
        "outline": "Edit **content/outline.md**: list stages and which skill handles each.",
        "principles": "Edit **content/principles.md**.",
        "purpose": "Edit **content/purpose.md**.",
        "role": "Edit **content/role.md**.",
        "workspace": ".",
    }


def _md_body(title: str, text: str) -> str:
    return f"# {title}\n\n{text}\n"


def main() -> int:
    p = argparse.ArgumentParser(description="Scaffold agent: content/*.md + workspace skill + build.py")
    p.add_argument("--batch", action="store_true", help="Non-interactive; requires --name and --out")
    p.add_argument("--name", help="Agent folder name")
    p.add_argument("--out", type=Path, help="Parent directory")
    args = p.parse_args()

    if args.batch:
        if not args.name or not args.out:
            print("--batch requires --name and --out", file=sys.stderr)
            return 1
        data = _gather_batch(args.name, str(args.out))
    else:
        dn = args.name or ""
        dout = str(args.out) if args.out else ""
        data = _gather_interactive(default_name=dn, default_out=dout)

    root = (Path(data["out"]).expanduser().resolve() / data["name"]).resolve()
    if not Path(data["out"]).expanduser().resolve().is_dir():
        print(f"Parent directory does not exist: {data['out']}", file=sys.stderr)
        return 1
    if root.exists():
        print(f"Refusing to overwrite: {root}", file=sys.stderr)
        return 1
    if not _BUILD_PY.is_file() or not _WORKSPACE_SKILL.is_dir():
        print(f"Missing templates under {_TEMPLATES}", file=sys.stderr)
        return 1

    body_by_file = {
        "outline.md": data["outline"],
        "principles.md": data["principles"],
        "purpose.md": data["purpose"],
        "role.md": data["role"],
    }

    (root / "content").mkdir(parents=True)
    (root / "scripts").mkdir(parents=True)
    (root / "skills").mkdir(parents=True)

    for spec in _SECTIONS:
        fn = spec["file"]
        title = spec["heading"]
        text = body_by_file[fn]
        (root / "content" / fn).write_text(_md_body(title, text), encoding="utf-8")

    cfg = {
        "name": data["name"],
        "version": "0.1.0",
        "workspace": {
            "active_skill_workspace": data["workspace"],
            "known_skill_workspaces": [],
            "context_paths": [],
        },
        "agents_md": {
            "title": data["title"],
            "sections": _SECTIONS,
        },
        "build": {"script": "scripts/build.py", "output": "AGENTS.md"},
    }
    (root / "skill-config.json").write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(_BUILD_PY, root / "scripts" / "build.py")
    shutil.copytree(_WORKSPACE_SKILL, root / "skills" / "workspace")

    (root / "SKILL.md").write_text(
        f"---\nname: {data['name']}\ndescription: {data['desc']}\n---\n\n"
        f"# {data['title']}\n\n"
        "Discovery only. **AGENTS.md** is built from **content/** — run `python scripts/build.py`. "
        "Workspace: **skills/workspace/**.\n",
        encoding="utf-8",
    )

    r = subprocess.run(
        [sys.executable, str(root / "scripts" / "build.py")],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        print(r.stderr or r.stdout, file=sys.stderr)
        print(f"Created {root} but initial build failed — run: python scripts/build.py", flush=True)
        return r.returncode

    print(f"Created {root}", flush=True)
    print("  content/: outline.md, principles.md, purpose.md, role.md", flush=True)
    print("  skills/workspace/: get_workspace.py, set_workspace.py", flush=True)
    print("  Run again after edits: python scripts/build.py", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
