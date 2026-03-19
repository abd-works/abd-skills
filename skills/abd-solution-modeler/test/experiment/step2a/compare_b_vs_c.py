"""Show chunks where C found many more concepts than B, and explain why."""
import json
from pathlib import Path

c_data = json.loads(Path("test/experiment/step2a/option-c/chunk_evidence.json").read_text(encoding="utf-8"))
b_data = json.loads(Path("test/experiment/step2a/option-b/chunk_evidence.json").read_text(encoding="utf-8"))
chunks_raw = json.loads(Path("test/mm3/solution/context/context_chunks.json").read_text(encoding="utf-8"))
chunk_text = {c["chunk_id"]: c["text"] for c in chunks_raw}

b_by_id = {e["chunk_id"]: e for e in b_data["evidence"]}

print("Chunks where C found 3+ MORE concepts than B:")
print(f"{'chunk_id':16s} {'C:con':6s} {'B:con':6s} {'diff':5s}  source")
print("-" * 70)
gaps = []
for e in c_data["evidence"]:
    cid = e["chunk_id"]
    b_e = b_by_id.get(cid, {})
    c_n = e.get("concept_count", 0)
    b_n = b_e.get("concept_count", 0)
    if c_n - b_n >= 3:
        gaps.append((c_n - b_n, cid, c_n, b_n, e.get("source", "")))

for diff, cid, cn, bn, src in sorted(gaps, reverse=True)[:15]:
    print(f"{cid:16s} {cn:6d} {bn:6d} {diff:5d}  {src[:40]}")

print()
print("=== DETAIL ON TOP 3 GAPS ===")
for diff, cid, cn, bn, src in sorted(gaps, reverse=True)[:3]:
    c_e = next(e for e in c_data["evidence"] if e["chunk_id"] == cid)
    b_e = b_by_id.get(cid, {})
    
    c_concepts = [(pc["concept"], pc.get("primary_type","?")) for pc in c_e.get("primary_concepts", [])]
    b_concepts = [(pc["concept"], pc.get("evidence_type","?")) for pc in b_e.get("primary_concepts", [])]
    b_concept_names = {x[0] for x in b_concepts}
    
    print(f"\n{'='*60}")
    print(f"Chunk: {cid}  ({src})")
    print(f"C found {cn} concepts, B found {bn} concepts (gap: {diff})")
    print(f"\nC concepts:")
    for name, t in c_concepts:
        flag = "  <-- B MISSED" if name not in b_concept_names else ""
        print(f"  {name} [{t}]{flag}")
    print(f"\nB concepts:")
    for name, t in b_concepts:
        print(f"  {name} [{t}]")
    print(f"\nText preview:")
    print(chunk_text.get(cid, "")[:300])
