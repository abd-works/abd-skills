#!/usr/bin/env python3
"""Post-extraction self-check per evidence_extraction phase instructions."""
import json
from pathlib import Path

def main():
    base = Path(__file__).parent.parent / "test" / "mm3" / "solution"
    actions = json.loads((base / "evidence" / "actions.json").read_text(encoding="utf-8"))
    decisions = json.loads((base / "evidence" / "decisions.json").read_text(encoding="utf-8"))
    guidance = json.loads((base / "generated" / "domain" / "concept_guidance.json").read_text(encoding="utf-8"))
    priority = {c.lower() for c in guidance.get("priority_concepts", [])}

    # Top 20 predicates
    pred_counts = {}
    for a in actions:
        p = a.get("predicate", "")
        pred_counts[p] = pred_counts.get(p, 0) + 1
    top20 = sorted(pred_counts.items(), key=lambda x: -x[1])[:20]
    print("=== TOP 20 PREDICATES (actions.json) ===")
    for p, c in top20:
        print(f"  {c:5}  {p}")
    print()

    # Weak subjects
    weak = {"you", "it", "perhaps", "they", "we"}
    weak_found = []
    for a in actions:
        sub = (a.get("subject") or "").lower()
        obj = (a.get("object") or "").lower()
        if sub in weak or obj in weak:
            weak_found.append((a.get("action_id"), sub, obj, (a.get("raw") or "")[:80]))
    print("=== WEAK SUBJECTS (full scan) ===")
    for w in weak_found[:15]:
        print(f"  {w[0]}: sub={w[1]} obj={w[2]} | {w[3]}...")
    print(f"  Total: {len(weak_found)}")
    print()

    # Prose fragments
    fragments = ["alternatively", "otherwise", "compare"]
    frag_found = []
    for a in actions:
        raw = (a.get("raw") or "").lower()
        for f in fragments:
            if f in raw:
                frag_found.append((a.get("action_id"), f, (a.get("raw") or "")[:80]))
                break
    print("=== PROSE FRAGMENTS (transitional phrases) ===")
    for f in frag_found[:10]:
        print(f"  {f[0]}: {f[1]} | {f[2]}...")
    print(f"  Total: {len(frag_found)}")
    print()

    # Suspect objects: non-priority, long table fragments (not DC/FLAT/GEAR/AMMO/GM - those are valid)
    valid_objects = {"gm", "dc", "flat", "gear", "ammo", "damage class"}
    non_priority = []
    for a in actions:
        obj = (a.get("object") or "").strip()
        if not obj:
            continue
        obj_lower = obj.lower()
        if obj_lower in priority or obj_lower in valid_objects:
            continue
        # Long compound = likely table fragment (skip short all-caps like DC, FLAT)
        if len(obj) > 30 and " " in obj:
            non_priority.append((a.get("action_id"), obj[:55], (a.get("raw") or "")[:65]))
    print("=== SUSPECT OBJECTS (non-priority, archetype/chapter-like) ===")
    for n in non_priority[:25]:
        print(f"  {n[0]}: object=\"{n[1]}\" | {n[2]}...")
    print(f"  Total: {len(non_priority)}")
    print()

    # Narrative flavor: "The X does..."
    narrative = []
    for a in actions:
        raw = (a.get("raw") or "")
        if raw.startswith("The ") and (" does " in raw or " may " in raw or " typically " in raw):
            narrative.append((a.get("action_id"), raw[:80]))
    print("=== NARRATIVE FLAVOR (The X does/may/typically) ===")
    for n in narrative[:10]:
        print(f"  {n[0]}: {n[1]}...")
    print(f"  Total: {len(narrative)}")
    print()

    # Summary
    print("=== SUMMARY ===")
    issues = []
    if weak_found:
        issues.append(f"Weak subjects: {len(weak_found)}")
    if frag_found:
        issues.append(f"Prose fragments: {len(frag_found)}")
    if non_priority:
        issues.append(f"Suspect objects: {len(non_priority)}")
    if narrative:
        issues.append(f"Narrative flavor: {len(narrative)}")
    if issues:
        print("JUNK FOUND. Consider: add to block_list, tighten extractor, or remove manually.")
        print("  " + "; ".join(issues))
    else:
        print("No junk detected in sampled checks.")
    print()
    print("Predicate clusters not mapping to epic concepts may signal missing behavior coverage (Phase 5).")

if __name__ == "__main__":
    main()
