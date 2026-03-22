"""Load human-authored build strategy for a skill (purpose, scope, pipeline, operator expectations)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Keys we ask for explicitly — orchestrator / builder can branch on these later.
STRATEGY_KEYS_DOC = """
Expected JSON shape (all string/list fields optional unless you need them):

  skill_purpose     — What this skill helps the user accomplish.
  target_audience   — Who uses it (role, host tool, experience level).
  scope_in          — List of what is included.
  scope_out         — List of explicit non-goals / exclusions.
  pipeline_phases   — Ordered phases or steps the skill should follow.
  operator_expectations — What structural checks matter (compileall, build.py, scanners).
  rules_and_scanners — How rules ↔ scanners should behave for this skill.
  artifacts         — Files or dirs the skill must emit (e.g. SKILL.md, AGENTS.md).
  constraints       — Time, privacy, API keys, repo layout limits.
  notes             — Freeform.

See docs/templates/build-strategy.example.json in the agentic-skill-builder repo.
"""

CONF_NAME = "build-strategy.json"
CONF_DIR = "conf"


def _read_json(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"Strategy file must be a JSON object: {path}")
    return data


def load_build_strategy(
    skill_root: Path,
    strategy_path: str | None,
) -> tuple[dict[str, Any], list[str], str]:
    """
    Resolve and load build strategy.

    Resolution order:

    1. ``strategy_path`` if set (absolute or relative to process cwd).
    2. ``<skill_root>/conf/build-strategy.json`` if it exists.
    3. Empty dict with trace explaining how to author strategy.

    Returns ``(strategy_dict, extra_trace_lines, source)`` where ``source`` is
    ``file:<path>``, ``skill_conf``, or ``empty``.
    """
    extra: list[str] = []
    if strategy_path:
        p = Path(strategy_path).expanduser()
        if not p.is_absolute():
            p = Path.cwd() / p
        p = p.resolve()
        if p.is_file():
            try:
                data = _read_json(p)
            except (OSError, json.JSONDecodeError, ValueError) as e:
                extra.append(f"strategize: ERROR reading {p}: {e}")
                return {}, extra, "error"
            extra.append(f"strategize: loaded --strategy-file {p}")
            return data, extra, f"file:{p}"
        extra.append(f"strategize: --strategy-file not found: {p}")
        return {}, extra, "error"

    conf = skill_root / CONF_DIR / CONF_NAME
    if conf.is_file():
        try:
            data = _read_json(conf)
        except (OSError, json.JSONDecodeError, ValueError) as e:
            extra.append(f"strategize: ERROR reading {conf}: {e}")
            return {}, extra, "error"
        try:
            shown = str(conf.relative_to(skill_root))
        except ValueError:
            shown = str(conf)
        extra.append(f"strategize: loaded {shown}")
        return data, extra, "skill_conf"

    extra.append("strategize: no strategy file — using empty strategy (HITL: fill conf/build-strategy.json).")
    extra.extend(_empty_strategy_trace(skill_root))
    return {}, extra, "empty"


def _empty_strategy_trace(skill_root: Path) -> list[str]:
    conf_hint = skill_root / CONF_DIR / CONF_NAME
    out: list[str] = [
        "strategize: --- Build strategy questionnaire (author answers in JSON) ---",
    ]
    for line in STRATEGY_KEYS_DOC.strip().splitlines():
        s = line.strip()
        if s:
            out.append("strategize: " + s)
    out.append(
        f"strategize: Create {conf_hint} (copy from docs/templates/build-strategy.example.json) "
        "or re-run with --strategy-file PATH.",
    )
    return out


def strategy_filled_enough(strategy: dict[str, Any]) -> bool:
    """True if the author provided at least a non-empty skill_purpose."""
    v = strategy.get("skill_purpose")
    return isinstance(v, str) and bool(v.strip())
