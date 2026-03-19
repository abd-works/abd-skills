"""Find chunks that are high on both concept count AND relationship count.
These are the candidates for the hybrid D approach — worth spending AI on."""
import json
from pathlib import Path

# Load both C and B evidence
c_data = json.loads(Path("test/experiment/step2a/option-c/chunk_evidence.json").read_text(encoding="utf-8"))
b_data = json.loads(Path("test/experiment/step2a/option-b/chunk_evidence.json").read_text(encoding="utf-8"))
chunks_raw = json.loads(Path("test/mm3/solution/context/context_chunks.json").read_text(encoding="utf-8"))
chunk_text = {c["chunk_id"]: c["text"] for c in chunks_raw}

# Build lookup for Option B by chunk_id
b_by_id = {e["chunk_id"]: e for e in b_data["evidence"]}

# Score each chunk: concepts + (relationships * 3) — relationships weighted more
scores = []
for e in c_data["evidence"]:
    cid = e["chunk_id"]
    c_concepts = e.get("concept_count", 0)
    c_rels = e.get("relationship_count", 0)
    b = b_by_id.get(cid, {})
    b_concepts = b.get("concept_count", 0)
    b_rels = b.get("relationship_count", 0)
    score = c_concepts + (c_rels * 3) + b_concepts + (b_rels * 5)
    scores.append({
        "chunk_id": cid,
        "source": e.get("source", ""),
        "score": score,
        "c_concepts": c_concepts,
        "c_rels": c_rels,
        "b_concepts": b_concepts,
        "b_rels": b_rels,
    })

scores.sort(key=lambda x: -x["score"])

print("Top 15 chunks by combined concept + relationship score")
print("(C=code signals, B=AI signals, score weights rels more heavily)")
print(f"{'chunk_id':16s} {'score':6s} {'C:con':6s} {'C:rel':6s} {'B:con':6s} {'B:rel':6s}  source")
print("-" * 90)
for s in scores[:15]:
    print(f"{s['chunk_id']:16s} {s['score']:6d} {s['c_concepts']:6d} {s['c_rels']:6d} {s['b_concepts']:6d} {s['b_rels']:6d}  {s['source'][:40]}")

print()
print("=== DETAIL ON TOP 5 ===")
for s in scores[:5]:
    cid = s["chunk_id"]
    print(f"\n{'='*60}")
    print(f"Chunk: {cid}  ({s['source']})")
    print(f"Score: {s['score']}  C:concepts={s['c_concepts']} C:rels={s['c_rels']}  B:concepts={s['b_concepts']} B:rels={s['b_rels']}")
    
    # Show B relationships
    b = b_by_id.get(cid, {})
    rels = b.get("cross_module_relationships", [])
    if rels:
        print("AI-found relationships:")
        for r in rels:
            print(f"  {r['from']['concept']} ({r['from']['module']}) --{r['relationship']}--> {r['to']['concept']} ({r['to']['module']})")
            print(f"    Justification: {r.get('justification','')}")
    
    # Show B concepts not found by C
    c_e = next((e for e in c_data["evidence"] if e["chunk_id"] == cid), {})
    c_concept_names = {pc["concept"] for pc in c_e.get("primary_concepts", [])}
    b_concept_names = {pc["concept"] for pc in b.get("primary_concepts", [])}
    new_concepts = b_concept_names - c_concept_names
    if new_concepts:
        print(f"Concepts B found that C missed: {new_concepts}")
    
    # Show chunk text preview
    text = chunk_text.get(cid, "")[:300]
    print(f"Text preview: {text[:200]}...")
