"""
Engine config — skill-config.json → workspace schema. Uses pydantic if available, else plain dict.
Ported from abd-story-synthesizer (same contract).

Workspace: only **active_skill_workspace** is used (absolute path). No deprecated aliases.
"""
from typing import Any

try:
    from pydantic import BaseModel

    class AbdConfig(BaseModel):
        """Engine config. Project workspace is **active_skill_workspace** only."""

        skills: list[str]
        skills_config: dict | None = None
        constraints: list[dict] = []
        context_paths: list[str] = []
        active_skill_workspace: str | None = None

        class Config:
            extra = "ignore"

        @property
        def workspace_root(self) -> str | None:
            if not self.active_skill_workspace:
                return None
            s = str(self.active_skill_workspace).strip()
            return s if s else None

except ImportError:

    class AbdConfig:
        """Plain-dict fallback when pydantic not installed."""

        def __init__(
            self,
            skills: list[str],
            skills_config: dict | None = None,
            constraints: list[dict] | None = None,
            context_paths: list[str] | None = None,
            active_skill_workspace: str | None = None,
            **_: Any,
        ):
            self.skills = skills or []
            self.skills_config = skills_config
            self.constraints = constraints or []
            self.context_paths = context_paths or []
            self.active_skill_workspace = active_skill_workspace

        @property
        def workspace_root(self) -> str | None:
            if not self.active_skill_workspace:
                return None
            s = str(self.active_skill_workspace).strip()
            return s if s else None

        @classmethod
        def model_validate(cls, data: dict[str, Any]) -> "AbdConfig":
            aw = data.get("active_skill_workspace")
            return cls(
                skills=data.get("skills", []),
                skills_config=data.get("skills_config"),
                constraints=data.get("constraints", []),
                context_paths=data.get("context_paths", []),
                active_skill_workspace=str(aw).strip() if aw else None,
            )
