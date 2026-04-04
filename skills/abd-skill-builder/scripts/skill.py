"""
skill — Skill runtime: load conf/abd-config.json, resolve workspace, assemble prompts.

Public API:
    Skill.load()               → Skill (reads conf/abd-config.json relative to scripts/)
    Skill(path, engine=None)   → attach a skill path to an optional parent engine context
    skill.prompt(slug, form)   → str
    skill.instructions         → Instructions
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from config import AbdConfig
from rules import RuleSet


def _default_skill_root() -> Path:
    """Skill root = parent of the scripts/ folder that contains this file."""
    return Path(__file__).resolve().parent.parent


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

    def _skill_space_from_path(self, skill_path: Path) -> Path:
        p = skill_path.resolve()
        if p.parent.name == "skills" and p.parent.parent.name == ".agents":
            return p.parent.parent.parent
        if p.parent.name == "skills":
            return p.parent.parent
        return p.parent

    def _load_context_paths(self, workspace_path: Path) -> None:
        ss_config = workspace_path / "conf" / "abd-config.json"
        if not ss_config.exists():
            return
        try:
            data = json.loads(ss_config.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
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
        """Assemble prompt for *slug*. static reads phases/built/<slug>.md when present."""
        built = _resolve_parts_dir(self.path) / "phases" / "built" / f"{slug}.md"
        if form == "static" and built.is_file():
            return built.read_text(encoding="utf-8")
        return self.instructions.assemble_prompt(slug)

    # ------------------------------------------------------------------
    # Factory: load from conf/abd-config.json
    # ------------------------------------------------------------------

    @classmethod
    def load(cls, skill_root: str | Path | None = None) -> "Skill":
        """Load skill from ``conf/abd-config.json`` in *skill_root* (default: skill package root)."""
        root = Path(skill_root).resolve() if skill_root else _default_skill_root()
        config_path = root / "conf" / "abd-config.json"
        if not config_path.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")
        data = json.loads(config_path.read_text(encoding="utf-8"))
        if not data.get("skills"):
            data["skills"] = ["."]
        if not data.get("skills_config"):
            data["skills_config"] = {"order": data["skills"]}
        cfg = AbdConfig.model_validate(data)

        ctx = _EngineContext()
        order = (cfg.skills_config or {}).get("order", cfg.skills)
        skill_path: Path | None = None
        for rel_path in order:
            p = Path(rel_path)
            candidate = p.resolve() if p.is_absolute() else (root / p).resolve()
            if candidate.exists():
                skill_path = candidate
                break

        if skill_path is None:
            raise RuntimeError(f"No valid skill path found in {config_path}")

        # Resolve workspace
        wr = cfg.workspace_root
        if wr:
            wp = Path(wr)
            ctx.workspace_path = wp.resolve() if wp.is_absolute() else (Path.cwd() / wp).resolve()
        else:
            ctx.workspace_path = ctx._skill_space_from_path(skill_path)
        if ctx.workspace_path:
            ctx._load_context_paths(ctx.workspace_path)

        return cls(skill_path, context=ctx)
