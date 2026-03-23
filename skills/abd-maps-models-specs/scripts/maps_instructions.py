"""
MapsInstructions — phase bundles: solution role + YAML-filtered rules + library slice + phase body + critical quality.

Extends Instructions (abd-skill-builder shape) with maps-specific section IDs (``maps.*``).
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from build_support import (
    demote_all_headings,
    load_rule_files_for_phase,
    slug_to_phase_fname,
    strip_solution_role_block_for_agents,
)
from instructions import Instructions, _parts_dir
from section_markers import filter_library_for_phase

if TYPE_CHECKING:
    from engine import AgileContextEngine

MAPS_PREFIX = "maps."


class MapsInstructions(Instructions):
    """Assemble one phase prompt: solution role, rules (frontmatter-filtered), library, phase steps, critical quality."""

    def assemble_prompt(self, slug: str, *, include_context: bool = True) -> str:
        section_ids = self._section_ids_for_slug(slug)
        if not section_ids:
            raise KeyError(f"Empty or missing section list for slug: {slug}")

        parts: list[str] = []
        if include_context:
            ctx = self._build_context_block()
            if ctx:
                parts.append(ctx)

        for sid in section_ids:
            text = self._get_section_content(sid, phase_slug=slug)
            if text:
                parts.append(text)

        return "\n\n".join(parts).rstrip() + "\n"

    def _section_ids_for_slug(self, slug: str) -> list[str]:
        if slug in self.operation_sections:
            return list(self.operation_sections[slug])
        if slug in self._phase_files:
            return [
                f"{MAPS_PREFIX}solution",
                f"{MAPS_PREFIX}rules",
                f"{MAPS_PREFIX}library",
                f"{MAPS_PREFIX}phase.{slug}",
                f"{MAPS_PREFIX}critical_quality",
            ]
        raise KeyError(f"Unknown slug (not in phase_files or operation_sections): {slug}")

    def _get_section_content(self, section_id: str, *, phase_slug: str | None = None) -> str:
        if section_id.startswith(MAPS_PREFIX):
            return self._maps_get_section(section_id, phase_slug)
        return super()._get_section_content(section_id, phase_slug=phase_slug)

    def _maps_get_section(self, section_id: str, phase_slug: str | None) -> str:
        if phase_slug is None:
            return ""

        pd = _parts_dir(self.skill_path)
        rules_dir = self.skill_path / "rules"
        phase_fname = slug_to_phase_fname(phase_slug)
        cq_lib = self._skill_config.get("critical_quality_library", "critical-quality-steps.md")
        cq_notes: dict[str, str] = self._skill_config.get("phase_critical_quality_notes", {})

        if section_id == f"{MAPS_PREFIX}solution":
            op_path = pd / "solution-analyst-role.md"
            if not op_path.is_file():
                return ""
            op = demote_all_headings(op_path.read_text(encoding="utf-8"), 2)
            return "## Solution analyst role\n\n" + op

        if section_id == f"{MAPS_PREFIX}rules":
            rules = load_rule_files_for_phase(rules_dir, phase_fname)
            if rules:
                inner = "\n\n".join(
                    f"### `{name}`\n\n{demote_all_headings(text, 2)}" for name, text in rules
                )
            else:
                inner = (
                    "*No rules mapped to this phase in `rules/*.md`. "
                    "Each rule file must declare `phase_files:` (or `every_phase: true`) in YAML frontmatter — see `rules/README.md`.*"
                )
            return "## Rules\n\n" + inner

        if section_id == f"{MAPS_PREFIX}library":
            libs = self._phase_library_slices.get(phase_slug, [])
            if not libs:
                return (
                    "## Library\n\n"
                    "*No library files listed for this phase in `PHASE_LIBRARY_SLICES` (see `skill-config.json`).*"
                )
            chunks: list[str] = []
            for lib in libs:
                lp = pd / "library" / lib
                if not lp.is_file():
                    raise FileNotFoundError(f"Missing library file for phase {phase_slug}: {lp}")
                raw = lp.read_text(encoding="utf-8")
                raw = filter_library_for_phase(raw, phase_slug)
                lib_text = demote_all_headings(raw, 2)
                chunks.append(f"### `{lib}`\n\n{lib_text}")
            return "## Library\n\n" + "\n\n".join(chunks)

        if section_id.startswith(f"{MAPS_PREFIX}phase."):
            p = pd / "phases" / phase_fname
            if not p.is_file():
                return ""
            body = strip_solution_role_block_for_agents(p.read_text(encoding="utf-8"))
            body = demote_all_headings(body.strip() + "\n", 2)
            return "## Phase steps (normative)\n\n" + body

        if section_id == f"{MAPS_PREFIX}critical_quality":
            cq_path = pd / "library" / cq_lib
            if not cq_path.is_file():
                raise FileNotFoundError(f"Missing {cq_path}")
            cq = demote_all_headings(cq_path.read_text(encoding="utf-8"), 2)
            note = (cq_notes.get(phase_slug) or "").strip()
            block = cq.rstrip() + "\n"
            if note:
                block = block + "\n" + note + "\n"
            return "## Critical quality steps\n\n" + block

        return ""
