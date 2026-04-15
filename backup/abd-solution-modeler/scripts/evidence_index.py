#!/usr/bin/env python3
"""Phase 6: Build concept-anchored evidence index from evidence files.

Reads evidence/*.json (actions, decisions, states, relationships, terms)
and builds evidence_index.json with concepts as keys, evidence IDs grouped by type.
Replaces flat edge list with concept-anchored lookup for downstream AI phases.
"""
import argparse
import json
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent


def _load_json(path: Path) -> list | dict:
    if not path.exists():
        return [] if path.suffix == ".json" and "terms" in path.name or "actions" in path.name else {}
    return json.loads(path.read_text(encoding="utf-8"))


def _collect_concepts(terms: list, actions: list, states: list, relationships: list) -> set[str]:
    """Collect all concept names from evidence."""
    concepts = set()
    for t in terms if isinstance(terms, list) else []:
        if isinstance(t, dict) and t.get("name"):
            concepts.add(t["name"])
    for a in actions if isinstance(actions, list) else []:
        if isinstance(a, dict):
            if a.get("subject"):
                concepts.add(a["subject"])
            if a.get("object"):
                concepts.add(a["object"])
    for s in states if isinstance(states, list) else []:
        if isinstance(s, dict) and s.get("entity"):
            concepts.add(s["entity"])
    for r in relationships if isinstance(relationships, list) else []:
        if isinstance(r, dict):
            if r.get("from_entity"):
                concepts.add(r["from_entity"])
            if r.get("to_entity"):
                concepts.add(r["to_entity"])
    return concepts


def _build_index(evidence_dir: Path) -> dict:
    terms = _load_json(evidence_dir / "terms.json")
    actions = _load_json(evidence_dir / "actions.json")
    decisions = _load_json(evidence_dir / "decisions.json")
    states = _load_json(evidence_dir / "states.json")
    relationships = _load_json(evidence_dir / "relationships.json")

    if not isinstance(terms, list):
        terms = []
    if not isinstance(actions, list):
        actions = []
    if not isinstance(decisions, list):
        decisions = []
    if not isinstance(states, list):
        states = []
    if not isinstance(relationships, list):
        relationships = []

    concepts = _collect_concepts(terms, actions, states, relationships)

    # Build concept -> evidence ID mappings
    index: dict[str, dict[str, list[str]]] = {}
    for c in concepts:
        index[c] = {
            "term_ids": [],
            "performs": [],
            "receives": [],
            "states": [],
            "decisions": [],
            "relationships": [],
        }

    # Terms
    term_map: dict[str, str] = {}
    for t in terms:
        if not isinstance(t, dict):
            continue
        tid = t.get("term_id", "")
        name = t.get("name", "")
        if tid and name:
            term_map[name] = tid
            if name in index:
                index[name]["term_ids"].append(tid)

    # Actions: subject performs, object receives
    actions_registry: dict[str, dict] = {}
    for a in actions:
        if not isinstance(a, dict):
            continue
        aid = a.get("action_id", "")
        subj = a.get("subject", "").strip()
        obj = a.get("object", "").strip()
        pred = a.get("predicate", "").strip()
        if aid:
            actions_registry[aid] = {
                "subject": subj,
                "predicate": pred,
                "object": obj,
                "raw": a.get("raw", ""),
            }
        if subj and subj in index:
            index[subj]["performs"].append(aid)
        if obj and obj in index:
            index[obj]["receives"].append(aid)

    # Decisions: associate by entity mentions in condition (simplified: all concepts get all)
    decisions_registry: dict[str, dict] = {}
    for d in decisions:
        if not isinstance(d, dict):
            continue
        did = d.get("decision_id", "")
        if did:
            decisions_registry[did] = {
                "trigger": d.get("trigger", ""),
                "condition": d.get("condition", ""),
                "raw": d.get("raw", ""),
            }
        raw = (d.get("raw", "") or "").lower()
        for c in concepts:
            if c.lower() in raw and did not in index[c]["decisions"]:
                index[c]["decisions"].append(did)

    # States
    states_registry: dict[str, dict] = {}
    for s in states:
        if not isinstance(s, dict):
            continue
        sid = s.get("state_id", "")
        entity = s.get("entity", "").strip()
        if sid:
            states_registry[sid] = {
                "entity": entity,
                "state_description": s.get("state_description", ""),
                "raw": s.get("raw", ""),
            }
        if entity and entity in index:
            index[entity]["states"].append(sid)

    # Relationships
    relationships_registry: dict[str, dict] = {}
    for r in relationships:
        if not isinstance(r, dict):
            continue
        rid = r.get("relationship_id", "")
        from_ent = r.get("from_entity", "").strip()
        to_ent = r.get("to_entity", "").strip()
        if rid:
            relationships_registry[rid] = {
                "from_entity": from_ent,
                "type": r.get("type", ""),
                "to_entity": to_ent,
                "raw": r.get("raw", ""),
            }
        if from_ent and from_ent in index:
            index[from_ent]["relationships"].append(rid)
        if to_ent and to_ent in index and rid not in index[to_ent]["relationships"]:
            index[to_ent]["relationships"].append(rid)

    return {
        "concepts": index,
        "registries": {
            "actions": actions_registry,
            "decisions": decisions_registry,
            "states": states_registry,
            "relationships": relationships_registry,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 6: Build concept-anchored evidence index")
    parser.add_argument("--input-dir", "-i", help="Directory with evidence files")
    parser.add_argument("--output", "-o", help="Output path for evidence_index.json")
    args = parser.parse_args()

    if str(_SKILL_DIR / "scripts") not in sys.path:
        sys.path.insert(0, str(_SKILL_DIR / "scripts"))
    from _config import evidence_dir, output_dir

    ev_dir = Path(args.input_dir).resolve() if args.input_dir else evidence_dir()
    out_path = Path(args.output).resolve() if args.output else evidence_dir() / "evidence_index.json"

    index = _build_index(ev_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

    n_concepts = len(index.get("concepts", {}))
    print(f"Built evidence index: {n_concepts} concepts -> {out_path}")


if __name__ == "__main__":
    main()
