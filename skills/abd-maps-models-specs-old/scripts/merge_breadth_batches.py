#!/usr/bin/env python3
"""Parent-merge breadth batch patches into map-model-spec.json.

Unions chunk_ids per concept (same module + name), merges evidence_stage,
bucket lists, open_questions, cross_cutting_notes. Normalizes invalid
evidence_stage values. Injects module.depends_on (step 12 defaults).

Usage (from skill root):
  python scripts/merge_breadth_batches.py \\
    --spec test/mm3/maps-models-specs/map-model-spec.json \\
    --batches-dir test/mm3/maps-models-specs/breadth_batches
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


EV_ORDER = {"hypothesis": 0, "scaffolded": 1, "deepened": 2}


def norm_ev(s: str | None) -> str:
    if not s:
        return "hypothesis"
    s = str(s).strip()
    if s in EV_ORDER:
        return s
    if s == "confirmed":
        return "scaffolded"
    return "hypothesis"


def better_ev(a: str | None, b: str | None) -> str:
    na, nb = norm_ev(a), norm_ev(b)
    return na if EV_ORDER[na] >= EV_ORDER[nb] else nb


def umerge(a: list | None, b: list | None) -> list:
    return sorted(set((a or []) + (b or [])))


def merge_concepts(base: dict, inc: dict) -> dict:
    out = dict(base)
    out["chunk_ids"] = umerge(base.get("chunk_ids"), inc.get("chunk_ids"))
    out["evidence_stage"] = better_ev(base.get("evidence_stage"), inc.get("evidence_stage"))
    ib, bb = inc.get("owns") or "", base.get("owns") or ""
    if len(ib) > len(bb) and norm_ev(inc.get("evidence_stage")) in ("scaffolded", "deepened"):
        out["owns"] = inc["owns"]
        if inc.get("owns_chunk"):
            out["owns_chunk"] = inc["owns_chunk"]
    elif "owns" not in out and inc.get("owns"):
        out["owns"] = inc["owns"]
        out["owns_chunk"] = inc.get("owns_chunk", out.get("owns_chunk"))
    if inc.get("extends") and not base.get("extends"):
        out["extends"] = inc["extends"]
    if inc.get("foundational"):
        out["foundational"] = True
    # properties / operations: append unique by definition
    def merge_po(key: str):
        existing = list(base.get(key) or [])
        seen = {json.dumps(x, sort_keys=True) for x in existing}
        for item in inc.get(key) or []:
            sig = json.dumps(item, sort_keys=True)
            if sig not in seen:
                existing.append(item)
                seen.add(sig)
        if existing:
            out[key] = existing

    merge_po("properties")
    merge_po("operations")
    return out


def inject_depends_on(spec: dict) -> None:
    """Minimal acyclic depends_on for the six-module MM3 spine."""
    by_name: dict[str, dict] = {}
    for pair in spec.get("modules_and_epics", []):
        m = pair.get("module", {})
        n = m.get("name")
        if n:
            by_name[n] = m

    def set_dep(name: str, deps: list[dict]) -> None:
        mod = by_name.get(name)
        if mod is not None:
            mod["depends_on"] = deps

    set_dep(
        "Checks and tasks",
        [
            {
                "dependent_concepts": ["Check", "DifficultyClass"],
                "module": "Ranks and measures",
                "provides_concepts": ["Rank", "MeasurementTable"],
                "reason": "Difficulty values and measurement scales align with ranked tables (cited in check rules).",
            }
        ],
    )
    set_dep(
        "Skills",
        [
            {
                "dependent_concepts": ["Skill", "SkillCheck"],
                "module": "Abilities",
                "provides_concepts": ["Ability", "AbilityRank"],
                "reason": "Skills apply ability ranks and modifiers to trained tasks.",
            },
            {
                "dependent_concepts": ["SkillCheck"],
                "module": "Checks and tasks",
                "provides_concepts": ["Check", "DifficultyClass"],
                "reason": "Skill checks are resolved as checks against DC.",
            },
        ],
    )
    set_dep(
        "Powers",
        [
            {
                "dependent_concepts": ["PowerEffect", "PowerPoints"],
                "module": "Abilities",
                "provides_concepts": ["Ability", "AbilityRank"],
                "reason": "Power builds tie to ability defenses and ranks.",
            },
            {
                "dependent_concepts": ["PowerEffect"],
                "module": "Checks and tasks",
                "provides_concepts": ["Check", "DifficultyClass"],
                "reason": "Powers use attack checks, effect checks, and resistance DCs.",
            },
        ],
    )
    set_dep(
        "Combat resolution",
        [
            {
                "dependent_concepts": ["ResistanceCheck", "Condition"],
                "module": "Abilities",
                "provides_concepts": ["Ability", "AbilityRank"],
                "reason": "Resistance saves use defense abilities; conditions alter capability.",
            },
            {
                "dependent_concepts": ["ResistanceCheck"],
                "module": "Checks and tasks",
                "provides_concepts": ["Check", "DifficultyClass"],
                "reason": "Resistance checks are checks against an effect DC.",
            },
        ],
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--spec",
        required=True,
        help="Path to map-model-spec.json (read/write)",
    )
    ap.add_argument(
        "--batches-dir",
        required=True,
        help="Directory containing batch_*_output.json",
    )
    args = ap.parse_args()

    spec_path = Path(args.spec).resolve()
    batch_dir = Path(args.batches_dir).resolve()

    data = json.loads(spec_path.read_text(encoding="utf-8"))

    batch_files = sorted(batch_dir.glob("batch_*_output.json"), key=lambda p: p.name)
    if not batch_files:
        print("No batch_*_output.json found", file=__import__("sys").stderr)
        return 1

    oq: list[str] = list(data.get("open_questions") or [])
    cc_notes: list[str] = []
    if (data.get("cross_cutting_notes") or "").strip():
        cc_notes.append(str(data["cross_cutting_notes"]).strip())

    # index modules
    for batch_path in batch_files:
        patch = json.loads(batch_path.read_text(encoding="utf-8"))
        for q in patch.get("open_questions") or []:
            if q and q not in oq:
                oq.append(q)
        cn = (patch.get("cross_cutting_notes") or "").strip()
        if cn:
            cc_notes.append(f"[batch {patch.get('batch_id', '?')}] {cn}")

        for item in patch.get("concept_additions") or []:
            mname = item.get("module_name")
            concept = item.get("concept") or {}
            if not mname or not concept.get("name"):
                continue
            concept["evidence_stage"] = norm_ev(concept.get("evidence_stage"))
            found = False
            for pair in data["modules_and_epics"]:
                mod = pair.get("module", {})
                if mod.get("name") != mname:
                    continue
                found = True
                concepts = mod.setdefault("concepts", [])
                cname = concept["name"]
                merged = False
                for i, existing in enumerate(concepts):
                    if existing.get("name") == cname:
                        concepts[i] = merge_concepts(existing, concept)
                        merged = True
                        break
                if not merged:
                    concepts.append(concept)
                break
            if not found:
                print(f"WARN: unknown module_name {mname!r} in {batch_path.name}", file=__import__("sys").stderr)

        for bucket in patch.get("chunk_bucket_additions") or []:
            mname = bucket.get("module_name")
            if not mname:
                continue
            for pair in data["modules_and_epics"]:
                if pair.get("module", {}).get("name") != mname:
                    continue
                cid = pair.setdefault("chunk_ids", {"identified": [], "provisional": [], "ambiguous": []})
                for key in ("identified", "provisional", "ambiguous"):
                    cid[key] = umerge(cid.get(key), bucket.get(key))
                break

    data["open_questions"] = oq
    data["cross_cutting_notes"] = "\n\n".join(cc_notes) if cc_notes else ""

    # Remove N/K from spec (breadth step: do not persist manifest in JSON)
    data.pop("N_chunks", None)

    data["phase"] = "5"
    data["phase_note"] = (
        "Breadth K-read batches merged into concepts and chunk buckets; "
        "hypothesis→scaffolded where batches substantiated. Run scanners + build_chunk_index."
    )

    inject_depends_on(data)

    spec_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote merged spec: {spec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
