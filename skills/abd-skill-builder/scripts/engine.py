"""
Agile Context Engine — single-skill runtime for abd-skill-builder (and scaffolded skills).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from config import AbdConfig

if TYPE_CHECKING:
    from abd_skill import AbdSkill  # noqa: F401


def _default_engine_root() -> Path:
    return Path(__file__).resolve().parent.parent


class AgileContextEngine:
    """Engine: load conf/abd-config.json, attach one AbdSkill at skill root."""

    def __init__(self, engine_root: str | Path | None = None):
        self.engine_root = Path(engine_root).resolve() if engine_root else _default_engine_root()
        self.config_path = self.engine_root / "conf" / "abd-config.json"
        self.workspace_path: Path | None = None
        self.context_paths: list[Path] = []
        self.skills: list[AbdSkill] = []
        self._config: AbdConfig | None = None

    def load(self) -> AgileContextEngine:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        if not data.get("skills"):
            data["skills"] = ["."]
        if not data.get("skills_config"):
            data["skills_config"] = {"order": data["skills"]}
        self._config = AbdConfig.model_validate(data)

        from abd_skill import AbdSkill

        order = (self._config.skills_config or {}).get("order", self._config.skills)
        self.skills = []
        for rel_path in order:
            path = Path(rel_path)
            skill_path = path.resolve() if path.is_absolute() else (self.engine_root / path).resolve()
            if skill_path.exists():
                self.skills.append(AbdSkill(skill_path, engine=self))

        if self.skills:
            wr = self._config.workspace_root
            if wr:
                wp = Path(wr)
                self.workspace_path = wp.resolve() if wp.is_absolute() else (Path.cwd() / wp).resolve()
            else:
                self.workspace_path = self._skill_space_from_path(self.skills[0].path)
            self._load_skill_space_context_paths()

        return self

    def _skill_space_from_path(self, skill_path: Path) -> Path:
        p = skill_path.resolve()
        if p.parent.name == "skills" and p.parent.parent.name == ".agents":
            return p.parent.parent.parent
        if p.parent.name == "skills":
            return p.parent.parent
        return p.parent

    def _load_skill_space_context_paths(self) -> None:
        if not self.workspace_path:
            return
        ss_config_path = self.workspace_path / "conf" / "abd-config.json"
        if not ss_config_path.exists():
            return
        try:
            ss_data = json.loads(ss_config_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        for p in ss_data.get("context_paths", []):
            path = Path(p)
            resolved = path.resolve() if path.is_absolute() else (self.workspace_path / p).resolve()
            if resolved not in self.context_paths:
                self.context_paths.append(resolved)

    def get_skill(self, name: str) -> AbdSkill | None:
        for s in self.skills:
            if s.path.name == name or name in str(s.path):
                return s
        return None

    def prompt(self, slug: str, form: Literal["dynamic", "static"] = "dynamic") -> str:
        """Assemble prompt for phase or operation *slug*; static reads derived built file if present."""
        if not self.skills:
            raise RuntimeError("Engine has no skills; call load() after fixing conf/abd-config.json")
        skill = self.skills[0]
        parts_dir = _resolve_parts_dir(skill.path)
        built = parts_dir / "phases" / "built" / f"{slug}.md"
        if form == "static" and built.is_file():
            return built.read_text(encoding="utf-8")
        # static with missing/stale built file → assemble from sources
        return skill.instructions.assemble_prompt(slug)


def _resolve_parts_dir(skill_path: Path) -> Path:
    p = skill_path / "content" / "parts"
    if (p / "process.md").is_file():
        return p
    return skill_path / "parts"
