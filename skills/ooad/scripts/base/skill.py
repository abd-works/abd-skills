"""
skill — Skill runtime: load **skill-config.json** → **workspace**, resolve workspace, assemble prompts.

Public API:
    Skill.load()               → Skill (skill root = folder with skill-config.json; workspace = workspace.active_skill_workspace only, else None)
    Skill(path, engine=None)   → attach a skill path to an optional parent engine context
    skill.prompt(slug, form)   → str
    skill.instructions         → Instructions
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from config import AbdConfig, load_engine_config_dict
from rules import RuleSet


def _default_skill_root() -> Path:
    """Skill root = grandparent of ``scripts/base/`` (base/ → scripts/ → skill root)."""
    return Path(__file__).resolve().parents[2]


def _resolve_parts_dir(skill_path: Path) -> Path:
    p = skill_path / "content" / "parts"
    if (p / "process.md").is_file():
        return p
    return skill_path / "parts"


# ---------------------------------------------------------------------------
# _EngineContext — workspace and context_paths (passed into Instructions)
# ---------------------------------------------------------------------------

class _EngineContext:
    """Lightweight runtime context: workspace + context file paths."""

    def __init__(self) -> None:
        self.workspace_path: Path | None = None
        self.context_paths: list[Path] = []

    def _load_context_paths(self, workspace_path: Path) -> None:
        data: dict | None = None
        candidate = workspace_path / "skill-config.json"
        if candidate.is_file():
            try:
                raw = json.loads(candidate.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                raw = None
            if isinstance(raw, dict):
                inner = raw.get("workspace", raw)
                if isinstance(inner, dict) and inner.get("context_paths"):
                    data = inner
        if data is None:
            return
        for p in data.get("context_paths", []):
            path = Path(p)
            resolved = path.resolve() if path.is_absolute() else (workspace_path / p).resolve()
            if resolved not in self.context_paths:
                self.context_paths.append(resolved)


# ---------------------------------------------------------------------------
# _BuildTimeContext — no workspace, used by build.py
# ---------------------------------------------------------------------------

class _BuildTimeContext(_EngineContext):
    """Minimal engine surface when generating derived built files (no workspace context)."""

    workspace_path = None
    context_paths: list = []


# ---------------------------------------------------------------------------
# Skill — single skill object
# ---------------------------------------------------------------------------

class Skill:
    """Represents one abd-skill.  Holds its path, config, and instruction assembler."""

    def __init__(self, path: str | Path, context: _EngineContext | None = None):
        self.path = Path(path).resolve()
        self._context: _EngineContext = context or _BuildTimeContext()
        self.rule_set = RuleSet(self.path)
        self.rule_set.load()
        self._skill_config = self._load_skill_config()
        self._operation_sections: dict[str, list[str]] = self._skill_config.get("operation_sections", {})
        self._instructions = None

    def _load_skill_config(self) -> dict:
        p = self.path / "skill-config.json"
        if not p.is_file():
            return {}
        return json.loads(p.read_text(encoding="utf-8"))

    @property
    def skill_config(self) -> dict:
        return self._skill_config

    @property
    def operation_sections(self) -> dict[str, list[str]]:
        return self._operation_sections

    @property
    def instructions(self) -> "Instructions":  # type: ignore[name-defined]
        if self._instructions is None:
            from instructions import Instructions

            self._instructions = Instructions(
                operation_sections=self._operation_sections,
                skill_path=self.path,
                context=self._context,
                skill_config=self._skill_config,
            )
        return self._instructions

    def prompt(self, slug: str, form: Literal["dynamic", "static"] = "dynamic") -> str:
        """Assemble prompt for *slug*. static reads content/built/phases/<slug>.md when present."""
        built = self.path / "content" / "built" / "phases" / f"{slug}.md"
        if form == "static" and built.is_file():
            return built.read_text(encoding="utf-8")
        return self.instructions.assemble_prompt(slug)

    # ------------------------------------------------------------------
    # Factory: load from skill-config.json → workspace
    # ------------------------------------------------------------------

    @classmethod
    def load(cls, skill_root: str | Path | None = None) -> "Skill":
        """Load skill from ``skill-config.json`` → ``workspace`` in *skill_root* (default: skill package root)."""
        root = Path(skill_root).resolve() if skill_root else _default_skill_root()
        data = load_engine_config_dict(root)
        cfg = AbdConfig.model_validate(data)

        ctx = _EngineContext()
        # Skill package root is always the directory that contains skill-config.json / scripts/
        skill_path = root.resolve()

        # Workspace: only active_skill_workspace — no inference from skill path
        wr = cfg.workspace_root
        if wr and str(wr).strip():
            wp = Path(wr)
            ctx.workspace_path = wp.resolve() if wp.is_absolute() else (Path.cwd() / wp).resolve()
        else:
            ctx.workspace_path = None
        if ctx.workspace_path:
            ctx._load_context_paths(ctx.workspace_path)

        return cls(skill_path, context=ctx)
