#!/usr/bin/env python3
"""Review evidence graph for junk (archetypes, headers, weak objects)."""
import json
from pathlib import Path
from collections import Counter

def main():
    base = Path(__file__).parent.parent / "test" / "mm3" / "solution"
    graph_path = base / "evidence" / "evidence_graph.json"
    if not graph_path.exists():
        print(f"Not found: {graph_path}")
        return

    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    guidance = json.loads((base / "generated" / "domain" / "concept_guidance.json").read_text(encoding="utf-8"))
    priority = {c.lower() for c in guidance.get("priority_concepts", [])}

    performs = graph.get("performs", [])
    modifies = graph.get("modifies", [])

    # Valid concepts (priority + aliases)
    valid = priority | {"gm", "dc", "gear", "ammo", "damage class", "charges", "gadgeteer", "mystic", "psychic"}

    # Junk patterns in "to" field (predicate + object)
    archetype_like = ("energy controllers", "gadgeteer", "gadgeteers", "the mystic", "mystic", "psychics",
                      "prejudice", "battlesuit", "construct", "crime fighter", "elemental", "martial artist",
                      "mimic", "paragon", "powerhouse", "shapeshifter", "speedster", "summoner",
                      "weapon master", "weather controller", "totem")
    header_like = ("abilities all", "gadgeteer gadgeteers", "mystic the mystic", "secret origins",
                   "per rank", "one of the following")
    weak_to = ("with", "it", "you", "they", "this", "that")

    junk_performs = []
    to_counter = Counter()
    for p in performs:
        to_val = (p.get("to") or "").strip()
        to_lower = to_val.lower()
        to_counter[to_val] += 1

        # Check for junk
        is_junk = False
        reason = []
        if any(a in to_lower for a in archetype_like):
            is_junk = True
            reason.append("archetype-like")
        if any(h in to_lower for h in header_like):
            is_junk = True
            reason.append("header-like")
        if to_lower.split()[0] in weak_to if to_lower else False:
            is_junk = True
            reason.append("weak predicate/object")
        if len(to_val) > 55:
            is_junk = True
            reason.append("too long")
        if p.get("from", "").strip():
            from_lower = p["from"].lower()
            if from_lower not in valid and from_lower not in priority:
                if any(a in from_lower for a in archetype_like) or any(h in from_lower for h in header_like):
                    is_junk = True
                    reason.append("junk from-concept")

        if is_junk:
            junk_performs.append((p.get("action_id"), p.get("from"), p.get("to"), "; ".join(reason)))

    # Top "to" values (action labels)
    print("=== TOP 25 PERFORMS 'to' (action labels) ===")
    for to_val, count in to_counter.most_common(25):
        print(f"  {count:4}  {to_val[:70]}")
    print()

    print("=== JUNK PERFORMS (sample 40) ===")
    for j in junk_performs[:40]:
        print(f"  {j[0]}: from={j[1][:25]:25} to={j[2][:45]:45} [{j[3]}]")
    print(f"  Total junk performs: {len(junk_performs)}")
    print()

    # Modifies junk
    junk_modifies = []
    for m in modifies:
        f = (m.get("from") or "").strip().lower()
        t = (m.get("to") or "").strip().lower()
        if f in weak_to or t in weak_to:
            junk_modifies.append((m.get("relationship_id"), m.get("from"), m.get("to")))
        if len(f) > 40 or len(t) > 40:
            junk_modifies.append((m.get("relationship_id"), m.get("from"), m.get("to"), "long"))
    print("=== JUNK MODIFIES ===")
    for j in junk_modifies[:20]:
        print(f"  {j}")
    print(f"  Total junk modifies: {len(junk_modifies)}")
    print()

    # Summary
    total_performs = len(performs)
    pct = 100 * len(junk_performs) / total_performs if total_performs else 0
    print("=== SUMMARY ===")
    print(f"Performs: {total_performs} total, {len(junk_performs)} junk ({pct:.1f}%)")
    print(f"Modifies: {len(modifies)} total, {len(junk_modifies)} junk")
    if junk_performs:
        print("\nJunk in performs comes from actions with archetype names, chapter headers, or weak objects.")
        print("Consider: add more reject_fragments, weak_object_tokens, or archetype patterns to block_list.")

if __name__ == "__main__":
    main()
