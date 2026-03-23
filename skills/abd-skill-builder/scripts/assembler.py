"""
ContentAssembler — build AGENTS.md and per-phase built files from skill-config.json + parts/.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from instructions import Instructions, _parts_dir


class _BuildTimeEngine:
    """Minimal engine surface for Instructions when writing derived built files (no workspace context)."""

    workspace_path = None
    context_paths: list = []


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
        .replace("](../conf/", "](conf/")
        .replace("](../../conf/", "](conf/")
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

    def build_agents_text(self) -> str:
        """AGENTS.md = Process + optional ``agents_front`` section IDs + one real-time assembly per phase.

        Each phase block is **identical** to ``assemble_prompt(phase, include_context=False)`` (same as
        ``phases/built/<phase>.md``), so the full bundle matches chaining what you would generate at runtime
        for every phase, with process and configurable front matter first.
        """
        op = self.config.get("operation_sections", {})
        inst = Instructions(op, self.root, _BuildTimeEngine(), self.config)

        chunks: list[str] = [f"# AGENTS — {self.skill_name}\n\n"]

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
        """Assemble one phase/operation prompt from sources (no runtime context block)."""
        op = self.config.get("operation_sections", {})
        inst = Instructions(op, self.root, _BuildTimeEngine(), self.config)
        return inst.assemble_prompt(slug, include_context=False)

    def write_built_phases(self, out_dir: Path | None = None) -> list[Path]:
        """Write ``phases/built/<slug>.md`` for each phase in *phase_files*."""
        base = out_dir or (self.parts / "phases" / "built")
        base.mkdir(parents=True, exist_ok=True)
        written: list[Path] = []
        for slug in self.phase_files:
            text = self.build_phase_text(slug)
            path = base / f"{slug}.md"
            path.write_text(text, encoding="utf-8")
            written.append(path)
        return written
