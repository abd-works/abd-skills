"""
Engine config — **skill-config.json** → **`workspace`** object.
Uses pydantic if available, else plain dict. Ported from abd-story-synthesizer (same contract).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_engine_config_dict(skill_root: Path) -> dict[str, Any]:
    """Load flat dict for **AbdConfig** from ``skill-config.json`` → ``workspace``."""
    skill_cfg = skill_root / "skill-config.json"
    if skill_cfg.is_file():
        full = json.loads(skill_cfg.read_text(encoding="utf-8"))
        ws = full.get("workspace")
        if isinstance(ws, dict) and ws:
            return dict(ws)
    raise FileNotFoundError(
        f"No `workspace` object in skill-config.json under {skill_root}"
    )


try:
    from pydantic import BaseModel

    class AbdConfig(BaseModel):
        """Engine config. **active_skill_workspace** is the only workspace root pointer (no fallback)."""

        constraints: list[dict] = []
        context_paths: list[str] = []
        active_skill_workspace: str | None = None

        class Config:
            extra = "ignore"

        @property
        def workspace_root(self) -> str | None:
            return self.active_skill_workspace

except ImportError:

    class AbdConfig:
        """Plain-dict fallback when pydantic not installed."""

        def __init__(
            self,
            constraints: list[dict] | None = None,
            context_paths: list[str] | None = None,
            active_skill_workspace: str | None = None,
            **_: Any,
        ):
            self.constraints = constraints or []
            self.context_paths = context_paths or []
            self.active_skill_workspace = active_skill_workspace

        @property
        def workspace_root(self) -> str | None:
            return self.active_skill_workspace

        @classmethod
        def model_validate(cls, data: dict[str, Any]) -> "AbdConfig":
            aw = data.get("active_skill_workspace")
            return cls(
                constraints=data.get("constraints", []),
                context_paths=data.get("context_paths", []),
                active_skill_workspace=str(aw).strip() if aw else None,
            )
