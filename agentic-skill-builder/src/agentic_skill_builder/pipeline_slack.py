"""Stage-by-stage Slack logging for the delivery graph (best-effort; never raises)."""

from __future__ import annotations

import os
from typing import Any

from agentic_skill_builder.slack_notify import WEBHOOK_ENV_KEY, merged_config, notify_slack

_PIPELINE_LOG_ENV = "AGENTIC_SKILL_BUILDER_SLACK_PIPELINE_LOG"


def pipeline_slack_enabled() -> bool:
    """When webhook is configured, pipeline logs are on unless explicitly disabled."""
    cfg = merged_config()
    if not (cfg.get(WEBHOOK_ENV_KEY) or "").strip():
        return False
    raw = os.environ.get(_PIPELINE_LOG_ENV, "1").strip().lower()
    if raw in ("0", "false", "no", "off", ""):
        return False
    return True


def _truncate(text: str, max_len: int = 3200) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 24] + "\n… [truncated] …"


def log_pipeline_stage(
    stage: str,
    *,
    skill_id: str,
    skill_path: str,
    body_lines: list[str],
) -> list[str]:
    """
    Post a readable summary to Slack when pipeline logging is enabled.

    Returns trace lines to merge only when Slack failed (so the run still records why).
    """
    if not pipeline_slack_enabled():
        return []
    header = (
        f"*agentic-skill-builder* · *{stage}*\n"
        f"skill_id: `{skill_id}` · path: `{skill_path}`\n"
    )
    body = "\n".join(body_lines)
    text = _truncate(header + "\n" + body)
    ok, detail = notify_slack(text)
    if not ok:
        return [f"slack pipeline: not sent ({detail})"]
    return []


def lines_for_operator_report(report: dict[str, Any]) -> list[str]:
    ok = report.get("ok")
    lines = [f"*Operator:* structural pass = `{ok}`"]
    errs = report.get("errors") or []
    if errs:
        lines.append("*Errors:*")
        lines.extend(f"  • {e}" for e in errs[:12])
    checks = report.get("checks") or []
    for c in checks[:20]:
        step = c.get("step", "?")
        cok = c.get("ok")
        lines.append(f"  • {step}: {'OK' if cok else 'FAIL'}")
    return lines


def lines_for_expert_report(report: dict[str, Any]) -> list[str]:
    if report.get("skipped"):
        return [
            f"*Expert:* skipped — `{report.get('reason', 'n/a')}`",
        ]
    lines = [
        f"*Expert:* model `{report.get('model', '?')}` · ok `{report.get('ok')}`",
    ]
    scores = report.get("scores") or {}
    if scores:
        lines.append("*Scores:* " + ", ".join(f"{k}={v}" for k, v in scores.items()))
    summ = (report.get("summary") or "").strip()
    if summ:
        lines.append("*Summary:* " + summ)
    for b in (report.get("public") or [])[:8]:
        lines.append(f"  • {b}")
    return lines
