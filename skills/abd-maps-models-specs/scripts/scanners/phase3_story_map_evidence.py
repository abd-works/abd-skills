#!/usr/bin/env python3
"""
Scanner: ``phase3/mm3_story_map.json`` — structure + evidence_chunk_ids vs ``context_index.json``.

Rule: **shaped-story-shape** (see ``content/parts/library/shaped-story-map.md``)

- Top-level ``epics[]``; recursive ``sub_epics`` / ``stories`` / ``story_groups``.
- **Substantive** stories: non-empty ``anchor``, or **trigger**/**response** ``actor``/``behavior``,
  or legacy top-level ``actor``/``behavior``, require non-empty ``evidence_chunk_ids[]``;
  each id must appear in ``context_index.json`` ``blocks[]`` when the index exists.
- Stories with ``skip_evidence: true`` (or ``evidence_exempt: true``) skip citation checks.

Exit 0 when ``mm3_story_map.json`` is absent (optional until authored). Same contract as legacy
``scripts/validate_phase3_story_map.py``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterator

RULE_ID = "phase3-story-map-evidence"


def _scripts_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def _ensure_config_path() -> None:
    sd = _scripts_dir()
    if str(sd) not in sys.path:
        sys.path.insert(0, str(sd))


def _load_indexed_chunk_ids() -> set[str] | None:
    from _config import CONTEXT_INDEX

    if not CONTEXT_INDEX.is_file():
        return None
    try:
        data = json.loads(CONTEXT_INDEX.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    blocks = data.get("blocks")
    if not isinstance(blocks, list):
        return None
    out: set[str] = set()
    for b in blocks:
        if isinstance(b, dict):
            cid = b.get("chunk_id") or b.get("block_id")
            if cid:
                out.add(str(cid))
    return out


def _is_substantive_story(story: dict) -> bool:
    if story.get("skip_evidence") or story.get("evidence_exempt"):
        return False
    v = story.get("anchor")
    if isinstance(v, str) and v.strip():
        return True
    for side in ("trigger", "response"):
        block = story.get(side)
        if isinstance(block, dict):
            for sub in ("actor", "behavior"):
                s = block.get(sub)
                if isinstance(s, str) and s.strip():
                    return True
    for key in ("actor", "behavior"):
        s = story.get(key)
        if isinstance(s, str) and s.strip():
            return True
    return False


def _iter_stories_under_epic(epic: dict) -> Iterator[dict]:
    for s in epic.get("stories") or []:
        if isinstance(s, dict):
            yield s
    for sg in epic.get("story_groups") or []:
        if not isinstance(sg, dict):
            continue
        for s in sg.get("stories") or []:
            if isinstance(s, dict):
                yield s
    for child in epic.get("sub_epics") or []:
        if isinstance(child, dict):
            yield from _iter_stories_under_epic(child)


def _iter_all_stories(data: dict) -> Iterator[tuple[str, dict]]:
    for ei, epic in enumerate(data.get("epics") or []):
        if not isinstance(epic, dict):
            continue
        ename = epic.get("name") or f"epic[{ei}]"
        for story in _iter_stories_under_epic(epic):
            yield ename, story


def main() -> int:
    _ensure_config_path()
    from _config import PHASE3, SKILL_ROOT

    story_map = PHASE3 / "mm3_story_map.json"
    PHASE3.mkdir(parents=True, exist_ok=True)
    if not story_map.is_file():
        print(f"PASS [{RULE_ID}] — no mm3_story_map.json (optional until authored; skip)")
        return 0
    try:
        data = json.loads(story_map.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL [{RULE_ID}]: invalid JSON {e}", file=sys.stderr)
        return 1
    if "epics" not in data:
        print(f"FAIL [{RULE_ID}]: mm3_story_map.json must have top-level epics[]", file=sys.stderr)
        return 1
    if not isinstance(data["epics"], list):
        print(f"FAIL [{RULE_ID}]: epics must be a list", file=sys.stderr)
        return 1

    indexed = _load_indexed_chunk_ids()
    errs: list[str] = []

    for epic_name, story in _iter_all_stories(data):
        if not _is_substantive_story(story):
            continue
        sname = story.get("name") or "<unnamed>"
        raw = story.get("evidence_chunk_ids")
        if not isinstance(raw, list) or len(raw) == 0:
            errs.append(
                f"story {epic_name!r} / {sname!r}: substantive (anchor or trigger/response or legacy actor/behavior) "
                "requires non-empty evidence_chunk_ids[]"
            )
            continue
        ids = [str(x).strip() for x in raw if x is not None and str(x).strip()]
        if not ids:
            errs.append(
                f"story {epic_name!r} / {sname!r}: evidence_chunk_ids[] is empty after trim"
            )
            continue
        if indexed is not None:
            for cid in ids:
                if cid not in indexed:
                    errs.append(
                        f"story {epic_name!r} / {sname!r}: evidence_chunk_id {cid!r} "
                        "not in context_index.json blocks[]"
                    )

    if errs:
        for e in errs:
            print(f"FAIL [{RULE_ID}]: {e}", file=sys.stderr)
        return 1

    n_stories = sum(1 for _ in _iter_all_stories(data))
    idx_note = f"indexed_chunks={len(indexed)}" if indexed is not None else "no context_index (ids not resolved)"
    print(
        f"PASS [{RULE_ID}] — {story_map.relative_to(SKILL_ROOT)} epics={len(data['epics'])} "
        f"stories_visited={n_stories} {idx_note}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
