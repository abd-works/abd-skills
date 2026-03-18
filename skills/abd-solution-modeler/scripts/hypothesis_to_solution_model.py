#!/usr/bin/env python3
"""Transform hypothesis.json to solution_model.json v1 (Structure phase).

Reads hypothesis (concepts, concept_hierarchy, registries) and produces
solution_model.json with concepts, behaviors, interaction_tree, evidence_refs.
"""
import json
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_DIR / "scripts"))
from _config import hypothesis_path, solution_model_path


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _main() -> None:
    hyp_path = hypothesis_path()
    out_path = solution_model_path()
    hyp = _load(hyp_path)
    if not hyp:
        print(f"No hypothesis at {hyp_path}", file=sys.stderr)
        sys.exit(1)

    concepts_data = hyp.get("concepts", {})
    hierarchy = hyp.get("concept_hierarchy", {})
    registries = hyp.get("registries", {})
    actions = registries.get("actions", {})

    # Collect all concept names (hierarchy + concepts)
    all_concepts: set[str] = set()
    for parent, children in hierarchy.items():
        all_concepts.add(parent)
        all_concepts.update(children)
    all_concepts.update(concepts_data.keys())

    # Build concepts array
    concepts_out = []
    for cid in sorted(all_concepts):
        data = concepts_data.get(cid, {})
        performs = data.get("performs", [])
        receives = data.get("receives", [])
        ev_refs = list(performs) + list(receives)
        parent = next((p for p, ch in hierarchy.items() if cid in ch), None)
        concepts_out.append({
            "id": cid,
            "module": "Core",
            "kind": "aggregate_root" if parent is None and cid in hierarchy else "entity",
            "inherits": parent,
            "summary": "",
            "properties": [],
            "operations": [],
            "relationships": [],
            "behavior_refs": [],
            "story_refs": [],
            "evidence_refs": ev_refs[:20],
        })

    # Build behaviors from actions (subject performs predicate on object)
    behaviors_out = []
    seen = set()
    for aid, act in list(actions.items())[:80]:
        subj = (act.get("subject") or "").strip()
        pred = (act.get("predicate") or "").strip()
        obj = (act.get("object") or "").strip()
        if not pred or (subj, pred, obj) in seen:
            continue
        seen.add((subj, pred, obj))
        owner = subj or obj or "System"
        if owner not in all_concepts:
            continue
        beh_id = f"beh_{aid}"
        behaviors_out.append({
            "id": beh_id,
            "name": pred.replace(" ", "_").lower() or "unknown",
            "owner": owner,
            "collaborators": [obj] if obj and obj != owner else [],
            "linked_steps": [],
            "story_refs": [],
            "evidence_refs": [aid],
        })

    # Interaction tree skeleton (superhero RPG)
    interaction_tree = {
        "epics": [
            {
                "id": "epic_character",
                "name": "Character Creation",
                "statement": "Player creates a hero with abilities and powers.",
                "triggering_actor": "Player",
                "responding_actor": "Gamemaster",
                "pre_condition": "",
                "sub_epics": [],
                "stories": [
                    {
                        "id": "story_build_hero",
                        "name": "Build Hero",
                        "statement": "Player allocates ability scores and selects powers.",
                        "actors": ["Player", "Character"],
                        "steps": [],
                        "scenarios": [],
                    }
                ],
            },
            {
                "id": "epic_combat",
                "name": "Combat",
                "statement": "Hero engages in combat using attacks and defenses.",
                "triggering_actor": "Hero",
                "responding_actor": "System",
                "pre_condition": "",
                "sub_epics": [],
                "stories": [
                    {
                        "id": "story_resolve_attack",
                        "name": "Resolve Attack",
                        "statement": "Attacker rolls against target defense; effect applied on hit.",
                        "actors": ["Character", "Defense", "Effect"],
                        "steps": [],
                        "scenarios": [],
                    }
                ],
            },
        ]
    }

    # evidence_refs registry
    evidence_refs = {
        "actions": actions,
        "decisions": registries.get("decisions", {}),
        "states": registries.get("states", {}),
        "relationships": registries.get("relationships", {}),
    }

    out = {
        "concepts": concepts_out,
        "behaviors": behaviors_out,
        "interaction_tree": interaction_tree,
        "evidence_refs": evidence_refs,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote solution_model.json: {len(concepts_out)} concepts, {len(behaviors_out)} behaviors -> {out_path}")


if __name__ == "__main__":
    _main()
