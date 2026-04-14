#!/usr/bin/env python3
"""Batch-merge ``content/parts/`` into ``AGENTS.md`` (and optional ``phases/built/``, ``content/built/``).

This is the **agent / IDE assembly** step: use it when the repo **ships** merged context or
``static_built`` slices. Authors edit **`content/parts/`**, **`SKILL.md`**, and **`rules/`**; run this to
refresh **`AGENTS.md`** and run configured scanners. See ``content/parts/library/base/skill-structure-and-concepts.md`` (§3). **Agent** stages/phases across skills:
``content/parts/library/base/process-phases.md``.

Merge order and delivery policy: skill root ``README.md`` — Delivery & merge order.

After merge, runs post-merge steps: explicit ``build.build_pipeline`` when set; otherwise the same
merged scanner list as **execute_rules** ``run_scanners.py`` (``scanner:`` in ``rules/*.md`` + ``scripts/scanners/*.py``).
Scanner resolution is inlined here so scaffolded skills stay self-contained; canonical module:
``skills/execute_rules/scripts/scanner_paths.py``.
Same base pattern as ``abd-maps-models-specs``.
See ``parts/library/rules-and-scanners.md``.

Shared helpers live under ``scripts/base/`` (``instructions``, ``skill``, …). Run from skill root:
``python scripts/base/build.py``.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

# This file always lives at ``scripts/base/build.py``; shared modules are alongside it.
_BASE_DIR = Path(__file__).resolve().parent
if str(_BASE_DIR) not in sys.path:
    sys.path.insert(0, str(_BASE_DIR))

from skill_root import SKILL_ROOT as ROOT

from instructions import PREFIX, Instructions, _parts_dir


# --- Scanner paths (same behavior as ``skills/execute_rules/scripts/scanner_paths.py``) ---


def _skill_build_cfg(cfg: dict[str, Any]) -> dict[str, Any]:
    b = cfg.get("build")
    return b if isinstance(b, dict) else {}


def _parse_frontmatter_scanner(content: str) -> str | None:
    match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    for line in match.group(1).split("\n"):
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        if k.strip().lower() == "scanner":
            return v.strip().strip('"').strip("'") or None
    return None


def _resolve_scanner_value(skill_root: Path, raw: str) -> str | None:
    v = raw.strip().strip('"').strip("'")
    if not v or "/" in v or "\\" in v or ".." in v:
        return None
    name = Path(v).name
    if name != v:
        return None
    if name.endswith(".py"):
        filename = name
    elif name.endswith("-scanner"):
        filename = f"{name}.py"
    else:
        filename = f"{name}-scanner.py"
    candidate = skill_root / "scripts" / "scanners" / filename
    if candidate.is_file():
        return f"scripts/scanners/{filename}"
    return None


def _scanners_from_rule_frontmatter(skill_root: Path) -> list[str]:
    rules_dir = skill_root / "rules"
    if not rules_dir.is_dir():
        return []
    out: list[str] = []
    seen: set[str] = set()
    for md in sorted(rules_dir.glob("*.md")):
        if md.name == "README.md":
            continue
        spec = _parse_frontmatter_scanner(md.read_text(encoding="utf-8"))
        if not spec:
            continue
        rel = _resolve_scanner_value(skill_root, spec)
        if rel and rel not in seen:
            seen.add(rel)
            out.append(rel)
    return out


def _discover_scanner_scripts(skill_root: Path) -> list[str]:
    d = skill_root / "scripts" / "scanners"
    if not d.is_dir():
        return []
    out: list[str] = []
    for p in sorted(d.glob("*.py")):
        if not p.is_file() or p.name == "__init__.py":
            continue
        out.append(str(p.relative_to(skill_root)).replace("\\", "/"))
    return out


def _list_scanner_scripts(skill_root: Path, cfg: dict[str, Any]) -> list[str]:
    del cfg
    seen: set[str] = set()
    ordered: list[str] = []

    def add(rel: str | None) -> None:
        if not rel:
            return
        s = str(rel).replace("\\", "/")
        if s not in seen:
            seen.add(s)
            ordered.append(s)

    for rel in _scanners_from_rule_frontmatter(skill_root):
        add(rel)
    for rel in _discover_scanner_scripts(skill_root):
        add(rel)
    return ordered


def resolve_build_pipeline(skill_root: Path, cfg: dict[str, Any]) -> list[str]:
    build_cfg = _skill_build_cfg(cfg)
    raw = build_cfg.get("build_pipeline")
    if raw:
        return [str(x).replace("\\", "/") for x in raw]
    return _list_scanner_scripts(skill_root, cfg)

# Purpose + outline: ``content/purpose.md`` and ``content/outline.md`` (see ``instructions._resolve_library_md``).
_DEFAULT_AGENTS_PREAMBLE: tuple[str, ...] = (
    f"{PREFIX}bundle.purpose",
    f"{PREFIX}bundle.outline",
    f"{PREFIX}bundle.role",
)
from skill import _BuildTimeContext

BUILT_DIR = ROOT / "content" / "built"

BUILT_README = """# content/built/ — static_built outputs

This directory holds **pre-merged** agent instructions for **`static_built`** delivery.

| File | Role |
| --- | --- |
| **`AGENTS.md`** | Byte-for-byte same merge as repo root **`AGENTS.md`** produced by **`scripts/base/build.py`**. |

Sources and merge order: **`README.md`** (Delivery & merge order). Regenerate with:

```bash
python scripts/base/build.py
```
"""

PHASES_BUILT_README = """# parts/phases/built/ — derived per-phase prompts

Files here are **generated** by **`scripts/base/build.py`**. Sources of truth: **`skill-config.json`**
(`library_files`, `phase_library`, `phase_rules`, `every_phase_rules`, `phase_bundle`, …) and **`parts/`** / **`rules/`**.

Regenerate:

```bash
python scripts/base/build.py
```

**Consumers:** merged **`AGENTS.md`** and tooling read these files when present; otherwise **`build.py`** assembles from **`content/parts/`** sources.
"""


def load_skill_config(skill_root: Path) -> dict[str, Any]:
    p = skill_root / "skill-config.json"
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _process_md_for_agents(process_text: str) -> str:
    return (
        process_text.replace("](../templates/", "](templates/")
        .replace("](../scripts/", "](scripts/")
        .replace("](../docs/", "](docs/")
    )


class ContentAssembler:
    """Single place for merge order: AGENTS + phases/built/*.md."""

    def __init__(self, skill_root: Path, skill_config: dict[str, Any]):
        self.root = Path(skill_root).resolve()
        self.config = skill_config
        self.parts = _parts_dir(self.root)
        self.phase_files: tuple[str, ...] = tuple(
            skill_config.get(
                "phase_files",
                [
                    "workspace-and-config",
                    "plan-script-build",
                    "plan-migrate",
                    "scaffold",
                    "migrate",
                    "fill-scaffold-parts",
                ],
            )
        )
        self.phase_section_headings: dict[str, str] = skill_config.get(
            "phase_section_headings",
            {"workspace-and-config": "Workspace and config"},
        )
        self.skill_name = skill_config.get("name", "abd-skill")

    def _make_instructions(self) -> Instructions:
        op = self.config.get("operation_sections", {})
        return Instructions(op, self.root, _BuildTimeContext(), self.config)

    def build_agents_text(self) -> str:
        """AGENTS.md = optional preamble (Outline, Role) + Process + optional ``agents_front`` + one assembly per phase."""
        inst = self._make_instructions()
        chunks: list[str] = [f"# AGENTS — {self.skill_name}\n\n"]

        preamble = self.config.get("agents_preamble")
        if preamble is None:
            preamble_ids = list(_DEFAULT_AGENTS_PREAMBLE)
        else:
            preamble_ids = [str(x) for x in preamble]
        if preamble_ids:
            preamble_text = inst.render_section_ids(preamble_ids)
            if preamble_text.strip():
                chunks.append(preamble_text)
                chunks.append("\n")

        process = _process_md_for_agents((self.parts / "process.md").read_text(encoding="utf-8"))
        chunks.append("## Process\n\n")
        chunks.append(process)
        chunks.append("\n")

        front_ids: list[str] = list(self.config.get("agents_front", []))
        front_heading = self.config.get("agents_front_heading", "## Front matter")
        if front_ids:
            if front_heading:
                chunks.append(f"{front_heading}\n\n")
            chunks.append(inst.render_section_ids(front_ids))
            chunks.append("\n")

        for slug in self.phase_files:
            section_title = self.phase_section_headings.get(slug, f"Phase: {slug}")
            chunks.append(f"\n## {section_title}\n\n")
            chunks.append(inst.assemble_prompt(slug, include_context=False))

        return "".join(chunks)

    def build_phase_text(self, slug: str) -> str:
        return self._make_instructions().assemble_prompt(slug, include_context=False)

    def write_built_phases(self, out_dir: Path | None = None) -> list[Path]:
        base = out_dir or (self.parts / "phases" / "built")
        base.mkdir(parents=True, exist_ok=True)
        written: list[Path] = []
        for slug in self.phase_files:
            text = self.build_phase_text(slug)
            path = base / f"{slug}.md"
            path.write_text(text, encoding="utf-8")
            written.append(path)
        return written


def _run_script_relative_to_root(skill_root: Path, rel: str) -> None:
    r = rel.replace("\\", "/").strip()
    path = skill_root / r
    print(f"--- {r} ---", flush=True)
    subprocess.run([sys.executable, str(path)], cwd=str(skill_root), check=True)


def main() -> None:
    cfg = load_skill_config(ROOT)
    asm = ContentAssembler(ROOT, cfg)
    text = asm.build_agents_text()
    out = ROOT / "AGENTS.md"
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")

    BUILT_DIR.mkdir(parents=True, exist_ok=True)
    built_agents = BUILT_DIR / "AGENTS.md"
    built_agents.write_text(text, encoding="utf-8")
    print(f"Wrote {built_agents.relative_to(ROOT)}")

    built_readme = BUILT_DIR / "README.md"
    built_readme.write_text(BUILT_README, encoding="utf-8")
    print(f"Wrote {built_readme.relative_to(ROOT)}")

    parts = asm.parts
    built_phase_dir = parts / "phases" / "built"
    built_phase_dir.mkdir(parents=True, exist_ok=True)
    for p in asm.write_built_phases(built_phase_dir):
        print(f"Wrote {p.relative_to(ROOT)}")
    (built_phase_dir / "README.md").write_text(PHASES_BUILT_README, encoding="utf-8")
    print(f"Wrote {(built_phase_dir / 'README.md').relative_to(ROOT)}")

    pipeline: list[str] = resolve_build_pipeline(ROOT, cfg)
    for step in pipeline:
        _run_script_relative_to_root(ROOT, step)
    if pipeline:
        print("build.py: build_pipeline complete", flush=True)


if __name__ == "__main__":
    main()
