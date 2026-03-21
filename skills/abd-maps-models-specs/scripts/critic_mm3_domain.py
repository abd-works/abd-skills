#!/usr/bin/env python3
"""MM3 domain critic — scores pipeline + optional map/model text against rules/mm3_domain_critic.json."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "rules" / "mm3_domain_critic.json"
ONTO = ROOT / "test" / "mm3" / "maps-models-specs" / "mm3_target_ontology.json"
CTX = ROOT / "test" / "mm3" / "context"
INDEX = CTX / "context_index.json"
HANDBOOK = ROOT / "test" / "mm3" / "docs" / "HeroesHandbook.md"


def _read_text(p: Path, limit: int | None = None) -> str:
    if not p.is_file():
        return ""
    t = p.read_text(encoding="utf-8", errors="replace")
    if limit and len(t) > limit:
        return t[:limit]
    return t


def _score_invariant(inv: dict, model_text: str, corpus_text: str) -> dict:
    """Return status pass/warn/fail and score 0..1 for one invariant."""
    mids = inv.get("model_keywords") or []
    anti = inv.get("anti_model_keywords") or []
    ck = inv.get("corpus_keywords") or []

    model_hits = sum(1 for k in mids if k and k in model_text)
    anti_hits = sum(1 for k in anti if k and k in model_text)
    corpus_hits = sum(1 for k in ck if k and re.search(re.escape(k), corpus_text, re.I))

    mscore = min(1.0, model_hits / max(len(mids), 1)) if mids else 0.0
    cscore = min(1.0, corpus_hits / max(len(ck), 1)) if ck else 0.0
    if anti_hits:
        mscore = max(0.0, mscore - 0.2 * anti_hits)

    if mids and model_text.strip():
        combined = 0.65 * mscore + 0.35 * cscore
        status = "pass" if combined >= 0.55 and not anti_hits else "warn" if combined >= 0.25 else "fail"
    else:
        combined = cscore
        status = "pass" if combined >= 0.4 else "warn" if combined >= 0.15 else "fail"

    return {
        "id": inv["id"],
        "severity": inv.get("severity", "medium"),
        "summary": inv.get("summary", ""),
        "status": status,
        "score": round(combined, 3),
        "model_keyword_hits": model_hits,
        "corpus_keyword_hits": corpus_hits,
        "anti_hits": anti_hits,
    }


def run_critic(
    *,
    model_paths: list[Path],
    pipeline_ok: bool,
) -> dict:
    rules = json.loads(RULES.read_text(encoding="utf-8"))
    model_text = ""
    for mp in model_paths:
        model_text += "\n" + _read_text(mp, limit=500_000)

    corpus_text = _read_text(HANDBOOK, limit=1_200_000)
    if not corpus_text:
        corpus_text = _read_text(INDEX, limit=400_000)

    invariants = []
    scores = []
    for inv in rules.get("invariants", []):
        r = _score_invariant(inv, model_text, corpus_text)
        invariants.append(r)
        scores.append(r["score"])

    overall = sum(scores) / max(len(scores), 1) if scores else 0.0
    if not pipeline_ok:
        overall *= 0.5

    onto_hits = 0
    if ONTO.is_file():
        onto = json.loads(ONTO.read_text(encoding="utf-8"))
        names = onto.get("core_types") or []
        for n in names:
            if n and n in model_text:
                onto_hits += 1
        if model_text.strip() and names:
            overall = max(overall, 0.25 * (onto_hits / len(names)))

    rec: list[str] = []
    if not model_paths or not any(p.is_file() for p in model_paths):
        rec.append("Add a map/model/spec artifact (e.g. map-model-spec.md/json) so model_keywords can be scored.")
    for r in invariants:
        if r["status"] == "fail":
            rec.append(f"Tighten model around: {r['id']} — {r['summary'][:120]}")
    if not pipeline_ok:
        rec.append("Fix pipeline (audit / heuristics / validate) before trusting scores.")

    return {
        "schema_version": "1",
        "overall_score": round(min(1.0, overall), 3),
        "pipeline_ok": pipeline_ok,
        "ontology_type_hits": onto_hits,
        "invariants": invariants,
        "recommendations": rec + (rules.get("notes_for_automated_critic") or [])[:3],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--model",
        action="append",
        default=[],
        metavar="PATH",
        help="Optional map/model/spec file to score (repeatable)",
    )
    ap.add_argument(
        "--pipeline-ok",
        action="store_true",
        help="Mark pipeline as green for scoring multiplier",
    )
    ap.add_argument("--json-out", type=Path, help="Write full critic JSON here")
    args = ap.parse_args()

    paths = [Path(p) for p in args.model]
    out = run_critic(model_paths=paths, pipeline_ok=args.pipeline_ok)
    print("overall_score:", out["overall_score"])
    print("pipeline_ok:", out["pipeline_ok"])
    for inv in out["invariants"]:
        print(f"  {inv['id']}: {inv['status']} ({inv['score']})")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(out, indent=2), encoding="utf-8")
        print("Wrote", args.json_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
