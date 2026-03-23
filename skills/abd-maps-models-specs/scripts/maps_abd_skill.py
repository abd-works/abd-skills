"""
MapsAbdSkill — AbdSkill with MapsInstructions for phase bundle assembly.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from abd_skill import AbdSkill
from maps_instructions import MapsInstructions

if TYPE_CHECKING:
    from engine import AgileContextEngine


class MapsAbdSkill(AbdSkill):
    """Same as AbdSkill; ``instructions`` returns MapsInstructions."""

    def __init__(self, path: str | Path, engine: "AgileContextEngine"):
        super().__init__(path, engine)

    @property
    def instructions(self) -> MapsInstructions:
        if self._instructions is None:
            self._instructions = MapsInstructions(
                self._operation_sections,
                self.path,
                self.engine,
                self._skill_config,
            )
        return self._instructions
