"""
Instructions — assemble prompt text for a phase or operation slug (section IDs from skill-config.json).
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from section_markers import filter_library_for_phase

if TYPE_CHECKING:
    from engine import AgileContextEngine

PREFIX = "abd_skill_builder."

_DEFAULT_LIBRARY_FILES = (
    "documentation-standards.md",
    "process-table-standards.md",
    "delivery-modes.md",
    "process-approach.md",
    "authoring-checklist.md",
    "skill-repo-standards.md",
    "skill-standards-section-3.md",
    "builder-vs-operator.md",
)

_DEFAULT_PHASE_FILES = (
    "workspace-and-config",
    "plan-script-build",
    "plan-migrate",
    "scaffold",
    "migrate",
    "fill-scaffold-parts",
)


def _parts_dir(skill_path: Path) -> Path:
    p = skill_path / "content" / "parts"
    if (p / "process.md").is_file():
        return p
    return skill_path / "parts"


class Instructions:
    """Resolves section IDs and assembles markdown for a slug."""

    def __init__(
        self,
        operation_sections: dict[str, list[str]],
        skill_path: Path,
        engine: AgileContextEngine,
        skill_config: dict,
    ):
        self.operation_sections = operation_sections
        self.skill_path = Path(skill_path).resolve()
        self.engine = engine
        self._skill_config = skill_config
        self._library_files: tuple[str, ...] = tuple(
            skill_config.get("library_files", list(_DEFAULT_LIBRARY_FILES))
        )
        self._phase_files: tuple[str, ...] = tuple(skill_config.get("phase_files", list(_DEFAULT_PHASE_FILES)))
        self._phase_library_slices: dict[str, list[str]] = skill_config.get("PHASE_LIBRARY_SLICES", {})
        self._phase_rules: dict[str, list[str]] = skill_config.get("phase_rules", {})

    def render_section_ids(self, section_ids: list[str]) -> str:
        """Join section IDs the same way as a prompt body (no context block). Used for ``agents_front``."""
        if not section_ids:
            return ""
        parts: list[str] = []
        for sid in section_ids:
            text = self._get_section_content(sid, phase_slug=None)
            if text:
                parts.append(text)
                parts.append("\n\n---\n\n")
        return "".join(parts).rstrip() + "\n"

    def assemble_prompt(self, slug: str, *, include_context: bool = True) -> str:
        section_ids = self._section_ids_for_slug(slug)
        if not section_ids:
            raise KeyError(f"Empty or missing section list for slug: {slug}")

        parts: list[str] = []
        if include_context:
            ctx = self._build_context_block()
            if ctx:
                parts.append(ctx)
                parts.append("\n\n---\n\n")

        for sid in section_ids:
            text = self._get_section_content(sid, phase_slug=slug)
            if text:
                parts.append(text)
                parts.append("\n\n---\n\n")

        return "".join(parts).rstrip() + "\n"

    def _section_ids_for_slug(self, slug: str) -> list[str]:
        if slug in self.operation_sections:
            return list(self.operation_sections[slug])
        if slug in self._phase_files:
            return self._default_phase_section_ids(slug)
        raise KeyError(f"Unknown slug (not in phase_files or operation_sections): {slug}")

    def _default_phase_section_ids(self, slug: str) -> list[str]:
        libs = self._phase_library_slices.get(slug, list(self._library_files))
        ids: list[str] = []
        for fname in libs:
            stem = Path(fname).stem
            ids.append(f"{PREFIX}library.{stem}")
        ids.append(f"{PREFIX}phase.{slug}")
        for stem in self._phase_rules.get(slug, []):
            ids.append(f"{PREFIX}rules.{stem}")
        return ids

    def _read_library_raw(self, stem: str) -> str:
        pd = _parts_dir(self.skill_path)
        for name in self._library_files:
            if Path(name).stem == stem:
                p = pd / "library" / name
                return p.read_text(encoding="utf-8") if p.is_file() else ""
        p = pd / "library" / f"{stem}.md"
        return p.read_text(encoding="utf-8") if p.is_file() else ""

    def _get_section_content(self, section_id: str, *, phase_slug: str | None = None) -> str:
        if section_id.endswith(".rules") or "validation.rules" in section_id:
            return self._all_rules_text()

        if section_id.startswith(f"{PREFIX}rules."):
            stem = section_id[len(f"{PREFIX}rules.") :]
            return self._single_rule_text(stem)

        pd = _parts_dir(self.skill_path)

        if section_id == f"{PREFIX}process":
            proc = pd / "process.md"
            return proc.read_text(encoding="utf-8") if proc.is_file() else ""

        if section_id.startswith(f"{PREFIX}library."):
            stem = section_id[len(f"{PREFIX}library.") :]
            raw = self._read_library_raw(stem)
            return filter_library_for_phase(raw, phase_slug)

        if section_id.startswith(f"{PREFIX}phase."):
            slug = section_id[len(f"{PREFIX}phase.") :]
            p = pd / "phases" / f"{slug}.md"
            return p.read_text(encoding="utf-8") if p.is_file() else ""

        return ""

    def _all_rules_text(self) -> str:
        rules_dir = self.skill_path / "rules"
        if not rules_dir.is_dir():
            return ""
        parts: list[str] = []
        for md in sorted(rules_dir.glob("*.md")):
            if md.name == "README.md":
                continue
            parts.append(md.read_text(encoding="utf-8").strip())
            parts.append("\n\n---\n\n")
        return "".join(parts).rstrip()

    def _single_rule_text(self, stem: str) -> str:
        p = self.skill_path / "rules" / f"{stem}.md"
        return p.read_text(encoding="utf-8").strip() if p.is_file() else ""

    def _build_context_block(self) -> str:
        lines: list[str] = [
            "**Execute these instructions.** You are the AI. Proceed directly to the task. Do not ask the user to paste, copy, or repeat these instructions elsewhere.",
            "",
        ]
        if self.engine.workspace_path:
            lines.append(f"**Workspace:** `{self.engine.workspace_path}`")
        if self.engine.context_paths:
            lines.append("**Context paths:**")
            for path in self.engine.context_paths:
                lines.append(f"- `{path}`")
        if len(lines) <= 2:
            return ""
        return "## Context\n\n" + "\n".join(lines)
