"""
Instructions — assemble prompt text for a phase or operation slug.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from rules import read_rule_body, stems_for_phase_rules
from markers import filter_library_for_phase

if TYPE_CHECKING:
    from skill import _EngineContext

PREFIX = "abd_skill_builder."

# AGENTS preamble sections — purpose/outline/role resolve via ``_resolve_library_md`` (``content/*.md``, …).
DEFAULT_PURPOSE_LIBRARY_NAME = "purpose.md"
DEFAULT_OUTLINE_LIBRARY_NAME = "outline.md"
DEFAULT_OUTLINE_HEADING = "## Outline"

_DEFAULT_LIBRARY_FILES = (
    "skill-structure-and-concepts.md",
    "critical-quality-steps.md",
    "delivery-modes.md",
    "process-phases.md",
    "rules-and-scanners.md",
)

_DEFAULT_PHASE_FILES = (
    "workspace-and-config",
    "plan-script-build",
    "plan-migrate",
    "scaffold",
    "migrate",
    "fill-scaffold-parts",
)

# Default assembly order for AI-chat phase prompts.
# Skills override or extend via ``skill-config.json`` → ``phase_bundle``.
_DEFAULT_PHASE_BUNDLE: dict = {
    # Role first in every assembled phase (built slice and AGENTS per-phase sections).
    "order": ["role", "principles", "phase", "library", "rules"],
    "role_file": "role.md",
    "principles_file": "principles.md",
    "role_heading": "## Role",
    "phase_heading": "## Phase",
    "library_heading": "## Library",
    "rules_heading": "## Rules",
    "principles_heading": "## Principles",
}


def _parts_dir(skill_path: Path) -> Path:
    p = skill_path / "content" / "parts"
    if (p / "process.md").is_file():
        return p
    return skill_path / "parts"


def _skill_content_dir(parts_dir: Path) -> Path | None:
    """``skill_root/content`` when ``parts_dir`` is ``.../content/parts``; else ``None``."""
    if parts_dir.name == "parts" and parts_dir.parent.name == "content":
        return parts_dir.parent
    return None


def _resolve_library_md(parts_dir: Path, filename: str) -> Path | None:
    """Resolve a library shard path.

    **Precedence:** ``library/<filename>`` (skill override) → ``content/<filename>`` (per-skill
    narrative next to ``content/parts/``) → ``library/required/<filename>`` (legacy) →
    ``library/base/<filename>`` (frozen norms from abd-skill-builder).

    Use a **different** filename in ``library_files`` only when you need an extra shard that does
    not share a name with base or required.
    """
    lib = parts_dir / "library"
    direct = lib / filename
    if direct.is_file():
        return direct
    content_dir = _skill_content_dir(parts_dir)
    if content_dir is not None:
        under_content = content_dir / filename
        if under_content.is_file():
            return under_content
    under_req = lib / "required" / filename
    if under_req.is_file():
        return under_req
    under_base = lib / "base" / filename
    if under_base.is_file():
        return under_base
    # Legacy spaced filename → kebab-case on disk (abd-skill-builder library).
    if filename == "Skill structure and concepts.md":
        for candidate in (
            lib / "skill-structure-and-concepts.md",
            (content_dir / "skill-structure-and-concepts.md") if content_dir else None,
            lib / "required" / "skill-structure-and-concepts.md",
            lib / "base" / "skill-structure-and-concepts.md",
        ):
            if candidate is not None and candidate.is_file():
                return candidate
    return None


def _merge_phase_library_config(skill_config: dict) -> dict[str, list[str]]:
    """Per-phase extra library filenames (merged after ``library_files``), like ``phase_rules``."""
    raw = skill_config.get("phase_library")
    if isinstance(raw, dict):
        return _normalize_phase_string_lists(raw)
    return {}


def _normalize_phase_string_lists(d: dict) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for k, v in d.items():
        slug = str(k).strip()
        if not slug:
            continue
        if isinstance(v, (list, tuple)):
            out[slug] = [str(x).strip() for x in v if str(x).strip()]
        else:
            out[slug] = []
    return out


def _strip_optional_h1(md: str) -> str:
    """Drop a single leading ``# Title`` line so purpose/outline files may use optional H1."""
    lines = md.strip().splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines.pop(0)
        return "\n".join(lines).strip()
    return md.strip()


class Instructions:
    """Resolves section IDs and assembles markdown for a slug."""

    def __init__(
        self,
        operation_sections: dict[str, list[str]],
        skill_path: Path,
        context: "_EngineContext",
        skill_config: dict,
    ):
        self.operation_sections = operation_sections
        self.skill_path = Path(skill_path).resolve()
        self.context = context
        self._skill_config = skill_config
        self._library_files: tuple[str, ...] = tuple(
            skill_config.get("library_files", list(_DEFAULT_LIBRARY_FILES))
        )
        self._phase_files: tuple[str, ...] = tuple(skill_config.get("phase_files", list(_DEFAULT_PHASE_FILES)))
        self._phase_library_extra: dict[str, list[str]] = _merge_phase_library_config(skill_config)
        self._phase_rules: dict[str, list[str]] = dict(skill_config.get("phase_rules") or {})
        self._phase_bundle: dict = dict(_DEFAULT_PHASE_BUNDLE)
        raw_pb = skill_config.get("phase_bundle")
        if isinstance(raw_pb, dict):
            self._phase_bundle.update(raw_pb)

    def _purpose_body(self) -> str:
        pd = _parts_dir(self.skill_path)
        p = _resolve_library_md(pd, DEFAULT_PURPOSE_LIBRARY_NAME)
        if not p:
            return ""
        raw = p.read_text(encoding="utf-8").strip()
        return _strip_optional_h1(raw) if raw else ""

    def _outline_body(self) -> str:
        pd = _parts_dir(self.skill_path)
        p = _resolve_library_md(pd, DEFAULT_OUTLINE_LIBRARY_NAME)
        if not p:
            return ""
        raw = p.read_text(encoding="utf-8").strip()
        return _strip_optional_h1(raw) if raw else ""

    def _outline_section_markdown(self) -> str:
        body = self._outline_body()
        if not body:
            return ""
        return f"{DEFAULT_OUTLINE_HEADING}\n\n{body}\n"

    def render_section_ids(self, section_ids: list[str]) -> str:
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
        order = self._phase_bundle.get("order")
        if not isinstance(order, list) or not order:
            order = list(_DEFAULT_PHASE_BUNDLE["order"])

        libs = self._merged_library_filenames(slug)
        rule_stems = stems_for_phase_rules(self._skill_config, slug)

        ids: list[str] = []
        for token in order:
            t = str(token).strip().lower()
            if t == "outline":
                ids.append(f"{PREFIX}bundle.outline")
            elif t == "role":
                ids.append(f"{PREFIX}bundle.role")
            elif t == "phase":
                ids.append(f"{PREFIX}phase.{slug}")
            elif t == "library":
                if libs:
                    ids.append(f"{PREFIX}bundle.library_header")
                    for fname in libs:
                        ids.append(f"{PREFIX}library.{Path(fname).stem}")
                else:
                    ids.append(f"{PREFIX}bundle.library_empty")
            elif t == "rules":
                if rule_stems:
                    ids.append(f"{PREFIX}bundle.rules_header")
                    for stem in rule_stems:
                        ids.append(f"{PREFIX}rules.{stem}")
                else:
                    ids.append(f"{PREFIX}bundle.rules_empty")
            elif t == "principles":
                ids.append(f"{PREFIX}bundle.principles")
        return ids

    def _merged_library_filenames(self, slug: str) -> list[str]:
        """``library_files`` for every phase, then ``phase_library[slug]`` extras (deduped, order preserved)."""
        base = list(self._library_files)
        extra = list(self._phase_library_extra.get(slug) or [])
        seen: set[str] = set()
        out: list[str] = []
        for name in base + extra:
            n = str(name).strip()
            if not n or n in seen:
                continue
            seen.add(n)
            out.append(n)
        return out

    def _read_library_raw(self, stem: str) -> str:
        pd = _parts_dir(self.skill_path)
        for name in self._library_files:
            if Path(name).stem == stem:
                p = _resolve_library_md(pd, name)
                return p.read_text(encoding="utf-8") if p else ""
        p = _resolve_library_md(pd, f"{stem}.md")
        return p.read_text(encoding="utf-8") if p else ""

    def _get_section_content(self, section_id: str, *, phase_slug: str | None = None) -> str:
        if section_id.endswith(".rules") or "validation.rules" in section_id:
            return self._all_rules_text()

        if section_id.startswith(f"{PREFIX}rules."):
            stem = section_id[len(f"{PREFIX}rules."):]
            body = self._single_rule_text(stem)
            if not body.strip():
                return ""
            return f"### `{stem}.md`\n\n{body.strip()}\n"

        pd = _parts_dir(self.skill_path)

        if section_id == f"{PREFIX}process":
            proc = pd / "process.md"
            return proc.read_text(encoding="utf-8") if proc.is_file() else ""

        if section_id.startswith(f"{PREFIX}library."):
            stem = section_id[len(f"{PREFIX}library."):]
            raw = self._read_library_raw(stem)
            body = filter_library_for_phase(raw, phase_slug)
            if not (body or "").strip():
                return ""
            return f"### `{stem}.md`\n\n{body.strip()}\n"

        if section_id.startswith(f"{PREFIX}phase."):
            slug = section_id[len(f"{PREFIX}phase."):]
            p = pd / "phases" / f"{slug}.md"
            if not p.is_file():
                return ""
            body = p.read_text(encoding="utf-8").strip()
            heading = (self._phase_bundle.get("phase_heading") or "").strip()
            if heading and body:
                return f"{heading}\n\n{body}\n"
            return body + "\n" if body else ""

        if section_id in (f"{PREFIX}bundle.purpose", f"{PREFIX}build_strategy.purpose"):
            body = self._purpose_body()
            if not body:
                return ""
            return f"## Purpose\n\n{body}\n"

        if section_id in (f"{PREFIX}bundle.outline", f"{PREFIX}build_strategy.outline"):
            return self._outline_section_markdown()

        if section_id == f"{PREFIX}bundle.role":
            name = str(self._phase_bundle.get("role_file") or "role.md").strip()
            if not name:
                return ""
            role_path = _resolve_library_md(pd, name)
            if not role_path or not role_path.is_file():
                return ""
            body = role_path.read_text(encoding="utf-8").strip()
            if not body:
                return ""
            heading = (self._phase_bundle.get("role_heading") or "## Role").strip()
            return f"{heading}\n\n{body}\n"

        if section_id == f"{PREFIX}bundle.principles":
            name = str(self._phase_bundle.get("principles_file") or "principles.md").strip()
            if not name:
                return ""
            pr_path = _resolve_library_md(pd, name)
            if not pr_path:
                return ""
            body = pr_path.read_text(encoding="utf-8").strip()
            if not body:
                return ""
            heading = (self._phase_bundle.get("principles_heading") or "## Principles").strip()
            return f"{heading}\n\n{body}\n"

        if section_id == f"{PREFIX}bundle.library_header":
            lib_h = (self._phase_bundle.get("library_heading") or "## Library").strip()
            return f"{lib_h}\n\n" if lib_h else ""

        if section_id == f"{PREFIX}bundle.library_empty":
            lib_h = (self._phase_bundle.get("library_heading") or "## Library").strip()
            return (
                f"{lib_h}\n\n"
                "*No library shards for this phase — set `library_files` and/or "
                "`phase_library` in `skill-config.json`.*\n"
            )

        if section_id == f"{PREFIX}bundle.rules_header":
            rules_h = (self._phase_bundle.get("rules_heading") or "## Rules").strip()
            return f"{rules_h}\n\n" if rules_h else ""

        if section_id == f"{PREFIX}bundle.rules_empty":
            rules_h = (self._phase_bundle.get("rules_heading") or "## Rules").strip()
            return (
                f"{rules_h}\n\n"
                "*No rules for this phase. List rule stems (filename without `.md`) under "
                "`skill-config.json` → `phase_rules` for this phase slug, and optionally "
                "`every_phase_rules` for rules that apply to every phase. See "
                "`parts/library/skill-structure-and-concepts.md` §3.1 (Config row) and "
                "`parts/library/rules-and-scanners.md`.*\n"
            )

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
        return read_rule_body(self.skill_path / "rules", stem)

    def _build_context_block(self) -> str:
        lines: list[str] = [
            "**Execute these instructions.** You are the AI. Proceed directly to the task. Do not ask the user to paste, copy, or repeat these instructions elsewhere.",
            "",
        ]
        if self.context.workspace_path:
            lines.append(f"**Workspace:** `{self.context.workspace_path}`")
        if self.context.context_paths:
            lines.append("**Context paths:**")
            for path in self.context.context_paths:
                lines.append(f"- `{path}`")
        if len(lines) <= 2:
            return ""
        return "## Context\n\n" + "\n".join(lines)
