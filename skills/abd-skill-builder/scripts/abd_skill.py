"""
AbdSkill — skill with Engine injected; operation_sections; instructions property.
"""
import json
from pathlib import Path
from typing import TYPE_CHECKING

from instructions import Instructions
from rule_set import RuleSet

if TYPE_CHECKING:
    from engine import AgileContextEngine


class AbdSkill:
    """Abd-skill. Receives Engine at construction."""

    def __init__(self, path: str | Path, engine: "AgileContextEngine"):
        self.path = Path(path).resolve()
        self.engine = engine
        self.rule_set = RuleSet(self.path)
        self.rule_set.load()
        self._skill_config = self._load_skill_config()
        self._operation_sections: dict[str, list[str]] = self._skill_config.get("operation_sections", {})
        self._instructions: Instructions | None = None

    def _load_skill_config(self) -> dict:
        skill_config_path = self.path / "skill-config.json"
        if not skill_config_path.exists():
            return {}
        return json.loads(skill_config_path.read_text(encoding="utf-8"))

    @property
    def operation_sections(self) -> dict[str, list[str]]:
        return self._operation_sections

    @property
    def skill_config(self) -> dict:
        return self._skill_config

    @property
    def instructions(self) -> Instructions:
        if self._instructions is None:
            self._instructions = Instructions(
                operation_sections=self._operation_sections,
                skill_path=self.path,
                engine=self.engine,
                skill_config=self._skill_config,
            )
        return self._instructions
