#!/usr/bin/env python3
"""Merge library + process + phases into AGENTS.md; write content/built/phases/*.md (derived).

Merge order and delivery policy: skill root ``README.md`` — Delivery & merge order.

After merge, runs post-merge steps: explicit ``build.build_pipeline`` when set; otherwise the same
merged scanner set as ``run_scanners`` (``build.scanners`` + ``rules/scanners.json`` + ``scripts/scanners/*.py``).
See ``scripts/base/scanner_paths.py``.
Same base pattern as ``abd-maps-models-specs``.
See ``parts/library/rules-and-scanners.md``.

Shared helpers live under ``scripts/base/`` (``instructions``, ``skill``, …). Run from skill root:
``python scripts/base/build.py``.
"""

from __future__ import annotations

import json
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
from scanner_paths import resolve_build_pipeline

# Purpose + outline: fixed library files ``content/parts/library/purpose.md`` and ``outline.md`` (see ``instructions.py``).
_DEFAULT_AGENTS_PREAMBLE: tuple[str, ...] = (
    f"{PREFIX}bundle.purpose",
    f"{PREFIX}bundle.outline",
    f"{PREFIX}bundle.role",
)
from skill import _BuildTimeContext

BUILT_DIR = ROOT / "content" / "built"
PHASES_BUILT_DIR = BUILT_DIR / "phases"

# Phase sources use ``../library/…`` (relative to ``content/parts/phases/``). That path is wrong for
# merged outputs: rewrite when writing **skill-root AGENTS.md** and **content/built/phases/*.md**.
_LINK_FROM_PHASE_TO_LIBRARY = "](../library/"
_LINK_AGENTS_ROOT_LIBRARY = "](content/parts/library/"
_LINK_BUILT_PHASE_LIBRARY = "](../../parts/library/"


def _rewrite_phase_links_for_agents_root(text: str) -> str:
    """``AGENTS.md`` lives at skill root; library markdown is under ``content/parts/library/``."""
    return text.replace(_LINK_FROM_PHASE_TO_LIBRARY, _LINK_AGENTS_ROOT_LIBRARY)


def _rewrite_phase_links_for_built_phase_file(text: str) -> str:
    """Built phase files live at ``content/built/phases/<slug>.md``."""
    return text.replace(_LINK_FROM_PHASE_TO_LIBRARY, _LINK_BUILT_PHASE_LIBRARY)


BUILT_README = """# content/built/ — static_built outputs

This directory holds **pre-merged** agent instructions for **`static_built`** delivery.

| Path | Role |
| --- | --- |
| **`AGENTS.md`** | Byte-for-byte same merge as repo root **`AGENTS.md`** produced by **`scripts/base/build.py`**. |
| **`phases/<slug>.md`** | Per-phase snapshots for **`--mode static`** (see **`phases/README.md`**). |

Sources and merge order: **`README.md`** (Delivery & merge order). Regenerate with:

```bash
python scripts/base/build.py
```
"""

PHASES_BUILT_README = """# content/built/phases/ — derived per-phase prompts

Files here are **generated** by **`scripts/base/build.py`**. Sources of truth: **`skill-config.json`**
(`library_files`, `phase_library`, `phase_rules`, `every_phase_rules`, `phase_bundle`, …) and **`parts/`** / **`rules/`**.

Phase bodies under **`parts/phases/`** may link to library shards with ``../library/…``; the build rewrites those to
``../../parts/library/…`` in this folder so links resolve from **`content/built/phases/<slug>.md`**.

Regenerate:

```bash
python scripts/base/build.py
```

**Runtime:** `python scripts/base/generate.py --phase <slug> --mode static` reads these files when present; otherwise assembles from sources (`dynamic`).
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
    """Single place for merge order: AGENTS + content/built/phases/*.md."""

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
            phase_body = inst.assemble_prompt(slug, include_context=False)
            chunks.append(_rewrite_phase_links_for_agents_root(phase_body))

        return "".join(chunks)

    def build_phase_text(self, slug: str) -> str:
        return self._make_instructions().assemble_prompt(slug, include_context=False)

    def write_built_phases(self, out_dir: Path | None = None) -> list[Path]:
        base = out_dir or PHASES_BUILT_DIR
        base.mkdir(parents=True, exist_ok=True)
        written: list[Path] = []
        for slug in self.phase_files:
            text = _rewrite_phase_links_for_built_phase_file(self.build_phase_text(slug))
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

    built_phase_dir = PHASES_BUILT_DIR
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
