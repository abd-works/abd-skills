#!/usr/bin/env python3
"""
Scanner: ``mechanisms.json`` — ``realized_by`` shape, no legacy ``steps`` on mechanisms,
optional cross-check vs ``shaped_story_map.json`` story paths.

Rule: **mechanisms-realized-by** (see ``rules/mechanisms-realized-by.md``)

- ``mechanisms[]`` entries: no non-empty ``steps`` or ``interaction_steps`` on the mechanism object.
- Each mechanism with a non-empty ``name`` should have ``realized_by`` with ``kind``,
  non-empty ``paths[]`` (strings), optional ``note``.
- When ``shaped_story_map.json`` exists, each ``realized_by.paths[]`` string must match a
  collected path ``Epic / … / Story`` in the map (nested sub-epics included).

Exit 0 when ``mechanisms.json`` is absent. Exit 0 when file exists but ``mechanisms[]`` is empty.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

RULE_ID = "mechanisms-contract"


def _scripts_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def _ensure_config_path() -> None:
    sd = _scripts_dir()
    if str(sd) not in sys.path:
        sys.path.insert(0, str(sd))


def _norm_path(s: str) -> str:
    return " / ".join(p.strip() for p in s.split(" / "))


def _collect_story_paths_from_epic(epic: dict) -> set[str]:
    out: set[str] = set()
    en = (epic.get("name") or "").strip()

    def walk_sub_epic(se: dict, chain: list[str]) -> None:
        cname = (se.get("name") or "").strip()
        full = chain + [cname]
        label = " / ".join([en, *full])
        for s in se.get("stories") or []:
            if isinstance(s, dict):
                sn = (s.get("name") or "").strip()
                out.add(_norm_path(f"{label} / {sn}"))
        for sg in se.get("story_groups") or []:
            if not isinstance(sg, dict):
                continue
            for s in sg.get("stories") or []:
                if isinstance(s, dict):
                    sn = (s.get("name") or "").strip()
                    out.add(_norm_path(f"{label} / {sn}"))
        for child in se.get("sub_epics") or []:
            if isinstance(child, dict):
                walk_sub_epic(child, full)

    for se in epic.get("sub_epics") or []:
        if isinstance(se, dict):
            walk_sub_epic(se, [])
    return out


def _all_story_paths(data: dict) -> set[str]:
    paths: set[str] = set()
    for epic in data.get("epics") or []:
        if isinstance(epic, dict):
            paths |= _collect_story_paths_from_epic(epic)
    return paths


def _validate_realized_by(rb: object, mech_name: str) -> list[str]:
    errs: list[str] = []
    if not isinstance(rb, dict):
        return [f"mechanism {mech_name!r}: realized_by must be an object"]
    kind = rb.get("kind")
    if kind not in ("single_story", "ordered_stories"):
        errs.append(
            f"mechanism {mech_name!r}: realized_by.kind must be "
            f"'single_story' or 'ordered_stories' (got {kind!r})"
        )
    paths = rb.get("paths")
    if not isinstance(paths, list) or len(paths) == 0:
        errs.append(f"mechanism {mech_name!r}: realized_by.paths must be a non-empty array of strings")
    else:
        for j, p in enumerate(paths):
            if not isinstance(p, str) or not p.strip():
                errs.append(
                    f"mechanism {mech_name!r}: realized_by.paths[{j}] must be a non-empty string"
                )
    note = rb.get("note")
    if note is not None and not isinstance(note, str):
        errs.append(f"mechanism {mech_name!r}: realized_by.note must be a string when present")
    return errs


def main() -> int:
    _ensure_config_path()
    from _config import MECHANISMS_JSON, OUT_ROOT, SHAPED_STORY_MAP_JSON, SKILL_ROOT

    mech_path = OUT_ROOT / MECHANISMS_JSON
    if not mech_path.is_file():
        print(f"PASS [{RULE_ID}] — no {MECHANISMS_JSON} (skip)")
        return 0

    try:
        data = json.loads(mech_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL [{RULE_ID}]: invalid JSON in {MECHANISMS_JSON}: {e}", file=sys.stderr)
        return 1

    mechs = data.get("mechanisms")
    if mechs is None:
        print(f"FAIL [{RULE_ID}]: missing mechanisms[]", file=sys.stderr)
        return 1
    if not isinstance(mechs, list):
        print(f"FAIL [{RULE_ID}]: mechanisms must be a list", file=sys.stderr)
        return 1

    story_paths: set[str] | None = None
    sm_path = OUT_ROOT / SHAPED_STORY_MAP_JSON
    if sm_path.is_file():
        try:
            sm_data = json.loads(sm_path.read_text(encoding="utf-8"))
            if isinstance(sm_data, dict) and isinstance(sm_data.get("epics"), list):
                story_paths = _all_story_paths(sm_data)
        except json.JSONDecodeError:
            print(f"FAIL [{RULE_ID}]: invalid JSON in {SHAPED_STORY_MAP_JSON}", file=sys.stderr)
            return 1

    errs: list[str] = []
    for i, m in enumerate(mechs):
        if not isinstance(m, dict):
            errs.append(f"mechanisms[{i}] must be an object")
            continue
        name = (m.get("name") or "").strip() or f"<mechanisms[{i}]>"
        if "interaction_steps" in m:
            errs.append(f"mechanism {name!r}: remove legacy interaction_steps (use steps[] on stories)")
        if "steps" in m:
            steps = m.get("steps")
            if isinstance(steps, list) and len(steps) > 0:
                errs.append(
                    f"mechanism {name!r}: procedural steps must not live on the mechanism "
                    f"(found non-empty steps[]; use steps[] on realizing stories in shaped_story_map.json)"
                )
            else:
                errs.append(
                    f"mechanism {name!r}: remove steps from mechanism object (use steps[] on stories)"
                )

        has_name = bool((m.get("name") or "").strip())
        rb = m.get("realized_by")
        if has_name and rb is None:
            errs.append(f"mechanism {name!r}: missing realized_by (name is set)")
        elif rb is not None:
            errs.extend(_validate_realized_by(rb, name))
            if story_paths is not None and isinstance(rb, dict):
                for p in rb.get("paths") or []:
                    if isinstance(p, str) and p.strip():
                        n = _norm_path(p)
                        if n not in story_paths:
                            errs.append(
                                f"mechanism {name!r}: realized_by path not found in "
                                f"{SHAPED_STORY_MAP_JSON}: {p!r}"
                            )

    if errs:
        for e in errs:
            print(f"FAIL [{RULE_ID}]: {e}", file=sys.stderr)
        return 1

    try:
        rel = mech_path.relative_to(SKILL_ROOT)
    except ValueError:
        rel = mech_path
    extra = f" story_paths={len(story_paths)}" if story_paths is not None else " (no shaped map)"
    print(f"PASS [{RULE_ID}] — {rel} mechanisms={len(mechs)}{extra}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
