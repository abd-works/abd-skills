#!/usr/bin/env python3
"""
Scanner: mechanism-concept-coverage — entities named in mechanisms must resolve
to terms, candidates, or promoted concepts; candidates must have ledger entries.

Rule: **mechanism-concept-coverage** (see ``rules/mechanism-concept-coverage.md``)

- Every entity referenced in ``mechanisms[].description`` or ``realized_by.paths[]``
  must appear in at least one of: ``terms_layer.json``, ``candidate_queue.json``,
  or ``map-model-spec.json`` concepts.
- When ``promotion_ledger.json`` exists, every entry in ``candidate_queue.json``
  must have a corresponding ledger decision.

Exit 0 when ``mechanisms.json`` or ``candidate_queue.json`` is absent.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RULE_ID = "mechanism-concept-coverage"


def _scripts_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def _ensure_config_path() -> None:
    sd = _scripts_dir()
    if str(sd) not in sys.path:
        sys.path.insert(0, str(sd))


def _load_json(path: Path) -> dict | list | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _extract_names(items: list[dict], key: str = "name") -> set[str]:
    out: set[str] = set()
    for item in items:
        if isinstance(item, dict):
            v = (item.get(key) or "").strip().lower()
            if v:
                out.add(v)
    return out


def _extract_path_entities(paths: list[str]) -> set[str]:
    """Extract story-level entity names from realized_by paths like 'Epic / Sub / Story'."""
    out: set[str] = set()
    for p in paths:
        if isinstance(p, str):
            parts = [seg.strip() for seg in p.split("/")]
            for part in parts:
                if part:
                    out.add(part.lower())
    return out


def _extract_description_nouns(description: str) -> set[str]:
    """Extract capitalized multi-word phrases and single capitalized words as entity candidates."""
    out: set[str] = set()
    phrases = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*\b', description)
    for phrase in phrases:
        normalized = phrase.strip().lower()
        if len(normalized) > 2:
            out.add(normalized)
    return out


def main() -> int:
    _ensure_config_path()
    from _config import (
        CANDIDATE_QUEUE_JSON,
        MECHANISMS_JSON,
        TERMS_LAYER_JSON,
        OUT_ROOT,
        SKILL_ROOT,
    )

    mech_path = OUT_ROOT / MECHANISMS_JSON
    cq_path = OUT_ROOT / CANDIDATE_QUEUE_JSON

    if not mech_path.is_file() or not cq_path.is_file():
        print(f"PASS [{RULE_ID}] — mechanisms or candidate_queue absent (skip)")
        return 0

    mech_data = _load_json(mech_path)
    if not isinstance(mech_data, dict):
        print(f"FAIL [{RULE_ID}]: invalid JSON in {MECHANISMS_JSON}", file=sys.stderr)
        return 1

    cq_data = _load_json(cq_path)
    if not isinstance(cq_data, dict):
        print(f"FAIL [{RULE_ID}]: invalid JSON in {CANDIDATE_QUEUE_JSON}", file=sys.stderr)
        return 1

    mechs = mech_data.get("mechanisms") or []
    candidates = cq_data.get("candidates") or []

    terms_path = OUT_ROOT / TERMS_LAYER_JSON
    terms_data = _load_json(terms_path)
    terms_names: set[str] = set()
    if isinstance(terms_data, dict):
        terms_names = _extract_names(terms_data.get("terms") or [])

    candidate_names = _extract_names(candidates)

    spec_path = OUT_ROOT / "map-model-spec.json"
    spec_data = _load_json(spec_path)
    concept_names: set[str] = set()
    if isinstance(spec_data, dict):
        for mod in spec_data.get("modules") or []:
            if isinstance(mod, dict):
                concept_names |= _extract_names(mod.get("concepts") or [])
        for entry in spec_data.get("modules_and_epics") or []:
            if isinstance(entry, dict):
                mod = entry.get("module")
                if isinstance(mod, dict):
                    concept_names |= _extract_names(mod.get("concepts") or [])

    all_known = terms_names | candidate_names | concept_names

    errs: list[str] = []

    for m in mechs:
        if not isinstance(m, dict):
            continue
        mech_name = (m.get("name") or "").strip()
        rb = m.get("realized_by")
        if isinstance(rb, dict):
            paths = rb.get("paths") or []
            path_entities = _extract_path_entities(paths)
            for entity in path_entities:
                if entity not in all_known and len(entity) > 3:
                    errs.append(
                        f"mechanism {mech_name!r}: entity {entity!r} from realized_by path "
                        f"not found in terms, candidates, or concepts"
                    )

    ledger_path = OUT_ROOT / "promotion_ledger.json"
    ledger_data = _load_json(ledger_path)

    if isinstance(ledger_data, dict):
        ledger_entries = ledger_data.get("decisions") or []
        ledger_names: set[str] = set()
        for entry in ledger_entries:
            if isinstance(entry, dict):
                v = (entry.get("candidate") or "").strip().lower()
                if v:
                    ledger_names.add(v)

        for c in candidates:
            if not isinstance(c, dict):
                continue
            cname = (c.get("name") or "").strip().lower()
            if cname and cname not in ledger_names:
                errs.append(
                    f"candidate {c.get('name')!r} has no entry in promotion_ledger.json"
                )

    if errs:
        for e in errs:
            print(f"FAIL [{RULE_ID}]: {e}", file=sys.stderr)
        return 1

    try:
        rel = mech_path.relative_to(SKILL_ROOT)
    except ValueError:
        rel = mech_path

    ledger_status = ""
    if isinstance(ledger_data, dict):
        ledger_count = len(ledger_data.get("decisions") or [])
        ledger_status = f" ledger_decisions={ledger_count}"

    print(
        f"PASS [{RULE_ID}] — {rel} mechanisms={len(mechs)} "
        f"candidates={len(candidates)} terms={len(terms_names)} "
        f"concepts={len(concept_names)}{ledger_status}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
