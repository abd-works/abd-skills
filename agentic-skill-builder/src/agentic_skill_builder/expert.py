"""Expert critique: LLM + rubric (plan §4.3)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from agentic_skill_builder.slack_notify import REPO_ROOT, merged_config

_RUBRIC = REPO_ROOT / "conf" / "expert_rubric.yaml"

try:
    from openai import APIError, AuthenticationError, OpenAI
except ImportError:  # pragma: no cover
    APIError = Exception  # type: ignore[misc, assignment]
    AuthenticationError = Exception  # type: ignore[misc, assignment]
    OpenAI = None  # type: ignore[misc, assignment]


def _read_rubric_text() -> str:
    if not _RUBRIC.is_file():
        return "dimensions: []\n"
    return _RUBRIC.read_text(encoding="utf-8")


def _snippet(path: Path, max_chars: int) -> str:
    if not path.is_file():
        return ""
    t = path.read_text(encoding="utf-8")
    if len(t) <= max_chars:
        return t
    return t[: max_chars - 20] + "\n… [truncated]\n"


def run_expert(
    *,
    skill_id: str,
    skill_path: str | Path,
    operator_report: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Call OpenAI with rubric + SKILL/AGENTS excerpts. Without API key, returns skipped report.
    """
    root = Path(skill_path).resolve()
    cfg = merged_config()
    key = cfg.get("OPENAI_API_KEY", "").strip() or os.environ.get("OPENAI_API_KEY", "").strip()

    if not key or OpenAI is None:
        return {
            "ok": True,
            "skipped": True,
            "reason": "OPENAI_API_KEY unset or openai package not installed",
            "skill_id": skill_id,
            "public": [
                "Expert skipped: set OPENAI_API_KEY in conf/.secrets or environment "
                "for LLM rubric critique."
            ],
            "scores": {},
        }

    rubric = _read_rubric_text()
    skill_md = _snippet(root / "SKILL.md", 12000)
    agents_md = _snippet(root / "AGENTS.md", 12000)
    op_summary = json.dumps(operator_report or {}, indent=2)[:8000]

    system = (
        "You are a careful skill authoring critic. "
        "Respond ONLY with valid JSON matching the rubric output_schema. "
        "Public bullets must be safe to show the skill author — no hidden gold examples."
    )
    user = (
        f"skill_id: {skill_id}\n\n"
        f"## Rubric (YAML)\n{rubric}\n\n"
        f"## Operator report (JSON)\n{op_summary}\n\n"
        f"## SKILL.md\n{skill_md}\n\n"
        f"## AGENTS.md\n{agents_md}\n"
    )

    model = os.environ.get("AGENTIC_SKILL_BUILDER_EXPERT_MODEL", "gpt-4o-mini")
    client = OpenAI(api_key=key)
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
    except (AuthenticationError, APIError) as exc:
        return {
            "ok": False,
            "skipped": True,
            "reason": f"openai api: {exc}",
            "skill_id": skill_id,
            "public": [
                "Expert skipped: OpenAI request failed (check OPENAI_API_KEY). "
                f"Details: {exc}"
            ],
            "scores": {},
        }

    raw = resp.choices[0].message.content or "{}"
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = {"raw": raw, "parse_error": True}

    public = parsed.get("public")
    if isinstance(public, str):
        public = [public]
    elif not isinstance(public, list):
        public = [str(parsed.get("summary", "expert completed"))]

    scores = parsed.get("scores") if isinstance(parsed.get("scores"), dict) else {}

    return {
        "ok": True,
        "skipped": False,
        "skill_id": skill_id,
        "model": model,
        "public": public,
        "scores": scores,
        "summary": parsed.get("summary"),
        "raw_keys": list(parsed.keys()) if isinstance(parsed, dict) else [],
    }
