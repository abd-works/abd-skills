#!/usr/bin/env python3
"""Append an entry to `<workspace>/docs/planning/abd-kanban-lead/agile-delivery-plan.changelog.md`.

Called by abd-kanban-lead at Step 7 (run complete, revise plan) to record
what changed in the revised plan and why. Keeps strategy-shift rationale
auditable across long engagements instead of being silently overwritten.

Usage:

    python abd-kanban-planning/scripts/append_plan_revision.py \
        --workspace <workspace> \
        --summary "Re-ordered runs 3 and 4 after SSO spike found second auth path" \
        [--rationale "Second actor flow is higher risk than expected"] \
        [--strategy-shift "blended new-initiative-business-user-experience-risk"]

Resolution:

  - If --workspace is omitted, read skill-config.json -> workspace.active_skill_workspace
    from the agent root (parent of skills/), same as other track_task scripts.
  - If --plan is given, use it directly; its parent is treated as the workspace.

The changelog is append-only, ISO-8601 dated, and includes the sha of the
agile-delivery-plan.md at append time so a reader can correlate a changelog
entry with the plan file state it describes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_HERE = Path(__file__).resolve()
_SKILL_ROOT = _HERE.parent.parent
_REPO_ROOT = _HERE.parents[4]
_CONFIG = _REPO_ROOT / "skill-config.json"


def _load_workspace_from_config() -> Path | None:
    if not _CONFIG.is_file():
        return None
    try:
        data = json.loads(_CONFIG.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    ws = data.get("workspace") if isinstance(data.get("workspace"), dict) else {}
    raw = ws.get("active_skill_workspace")
    if not raw or not isinstance(raw, str):
        return None
    p = Path(raw).expanduser()
    if not p.is_absolute():
        p = (_AGENT_ROOT / p).resolve()
    return p


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _build_entry(
    *,
    when: str,
    summary: str,
    rationale: str | None,
    strategy_shift: str | None,
    plan_sha: str | None,
) -> str:
    lines: list[str] = []
    lines.append(f"## {when}")
    lines.append("")
    lines.append(f"**Summary:** {summary}")
    if rationale:
        lines.append(f"**Rationale:** {rationale}")
    if strategy_shift:
        lines.append(f"**Strategy shift:** {strategy_shift}")
    if plan_sha:
        lines.append(f"**Plan sha:** `{plan_sha}`")
    lines.append("")
    return "\n".join(lines) + "\n"


_HEADER = (
    "# Agile Delivery Plan — Changelog\n"
    "\n"
    "Append-only record of plan revisions. New entries go at the top, under the header.\n"
    "Written by `skills/abd-kanban-planning/scripts/append_plan_revision.py`.\n"
    "\n"
    "---\n"
    "\n"
)


def append_entry(
    *,
    changelog_path: Path,
    plan_path: Path | None,
    summary: str,
    rationale: str | None,
    strategy_shift: str | None,
    now_iso: str | None = None,
) -> Path:
    """Insert a new entry at the top of the changelog, under the fixed header.

    Returns the changelog path. Creates the file with a standard header if it
    did not exist.
    """
    when = now_iso or datetime.now(timezone.utc).isoformat(timespec="seconds")
    plan_sha = _sha256_file(plan_path) if (plan_path and plan_path.is_file()) else None
    entry = _build_entry(
        when=when,
        summary=summary,
        rationale=rationale,
        strategy_shift=strategy_shift,
        plan_sha=plan_sha,
    )

    if changelog_path.is_file():
        existing = changelog_path.read_text(encoding="utf-8")
        if existing.startswith(_HEADER):
            body = existing[len(_HEADER):]
            new = _HEADER + entry + body
        else:
            # Malformed or hand-edited header; prepend fresh header and keep old content below.
            new = _HEADER + entry + existing
    else:
        changelog_path.parent.mkdir(parents=True, exist_ok=True)
        new = _HEADER + entry

    changelog_path.write_text(new, encoding="utf-8")
    return changelog_path


PLANNING_DIR = Path("docs") / "planning"
DELIVERY_LEAD_DIR = PLANNING_DIR / "abd-kanban-lead"


def _resolve_plan_path(workspace: Path) -> Path:
    return workspace / DELIVERY_LEAD_DIR / "agile-delivery-plan.md"


def _resolve_changelog_path(workspace: Path) -> Path:
    return workspace / DELIVERY_LEAD_DIR / "agile-delivery-plan.changelog.md"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workspace", type=Path, default=None,
                    help="Engagement workspace root. Defaults to skill-config.json value.")
    ap.add_argument("--plan", type=Path, default=None,
                    help="Explicit path to agile-delivery-plan.md (overrides --workspace lookup).")
    ap.add_argument("--changelog", type=Path, default=None,
                    help="Explicit path to the changelog file (defaults to docs/planning/abd-kanban-lead/agile-delivery-plan.changelog.md).")
    ap.add_argument("--summary", required=True,
                    help="One-line summary of what changed in this revision.")
    ap.add_argument("--rationale", default=None,
                    help="Why this revision — what was learned, what forced the change.")
    ap.add_argument("--strategy-shift", dest="strategy_shift", default=None,
                    help="If the strategy changed, name the new strategy (file or slug).")
    ns = ap.parse_args(argv)

    if ns.plan:
        plan_path = ns.plan.resolve()
        workspace = plan_path.parent
    elif ns.workspace:
        workspace = ns.workspace.resolve()
        plan_path = _resolve_plan_path(workspace)
    else:
        ws = _load_workspace_from_config()
        if ws is None:
            print("error: provide --workspace or --plan, or set "
                  "workspace.active_skill_workspace in skill-config.json.",
                  file=sys.stderr)
            return 1
        workspace = ws
        plan_path = _resolve_plan_path(workspace)

    changelog_path = ns.changelog.resolve() if ns.changelog else _resolve_changelog_path(workspace)

    written = append_entry(
        changelog_path=changelog_path,
        plan_path=plan_path if plan_path.is_file() else None,
        summary=ns.summary,
        rationale=ns.rationale,
        strategy_shift=ns.strategy_shift,
    )
    print(f"appended entry to {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
