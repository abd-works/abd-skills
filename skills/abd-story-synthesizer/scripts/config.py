"""
Engine config — abd-config.json schema. Uses pydantic if available, else plain dict.
"""
from typing import Any

try:
    from pydantic import BaseModel

    class AbdConfig(BaseModel):
        """Engine config. **active_skill_workspace** is canonical; **solution_workspace** / **skill_space_path** are deprecated aliases."""

        skills: list[str]
        skills_config: dict | None = None
        constraints: list[dict] = []
        context_paths: list[str] = []
        active_skill_workspace: str | None = None
        solution_workspace: str | None = None
        skill_space_path: str | None = None

        class Config:
            extra = "ignore"

        @classmethod
        def model_validate(cls, data: Any, **kwargs: Any) -> "AbdConfig":
            if isinstance(data, dict):
                data = dict(data)
                if not data.get("solution_workspace"):
                    if data.get("active_skill_workspace"):
                        data["solution_workspace"] = str(data["active_skill_workspace"]).strip()
                    elif data.get("skill_space_path"):
                        data["solution_workspace"] = data["skill_space_path"]
            return super().model_validate(data, **kwargs)

        @property
        def workspace_root(self) -> str | None:
            return self.active_skill_workspace or self.solution_workspace or self.skill_space_path

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
            solution_workspace: str | None = None,
            skill_space_path: str | None = None,
            **_: Any,
        ):
            self.skills = skills or []
            self.skills_config = skills_config
            self.constraints = constraints or []
            self.context_paths = context_paths or []
            self.active_skill_workspace = active_skill_workspace
            self.skill_space_path = skill_space_path
            self.solution_workspace = (
                solution_workspace
                or active_skill_workspace
                or skill_space_path
            )

        @property
        def workspace_root(self) -> str | None:
            return self.active_skill_workspace or self.solution_workspace or self.skill_space_path

        @classmethod
        def model_validate(cls, data: dict[str, Any]) -> "AbdConfig":
            aw = data.get("active_skill_workspace")
            sw = data.get("solution_workspace") or data.get("skill_space_path")
            if not sw and aw:
                sw = str(aw).strip() or None
            elif not sw:
                sw = data.get("skill_space_path")
            return cls(
                skills=data.get("skills", []),
                skills_config=data.get("skills_config"),
                constraints=data.get("constraints", []),
                context_paths=data.get("context_paths", []),
                active_skill_workspace=str(aw).strip() if aw else None,
                solution_workspace=sw,
                skill_space_path=data.get("skill_space_path"),
            )
