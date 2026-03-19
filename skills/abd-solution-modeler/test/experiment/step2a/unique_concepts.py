"""Show exact unique concept names per option — what each found that others didn't."""
import json
from pathlib import Path
from collections import defaultdict

c_data = json.loads(Path("test/experiment/step2a/option-c/chunk_evidence.json").read_text(encoding="utf-8"))
b_data = json.loads(Path("test/experiment/step2a/option-b/chunk_evidence.json").read_text(encoding="utf-8"))
e_data = json.loads(Path("test/experiment/step2a/option-e/chunk_evidence.json").read_text(encoding="utf-8"))

def get_concepts(data):
    names = set()
    for e in data["evidence"]:
        for pc in e.get("primary_concepts", []):
            name = pc.get("concept","").strip()
            if name:
                names.add(name)
    return names

c_concepts = get_concepts(c_data)
b_concepts = get_concepts(b_data)
e_concepts = get_concepts(e_data)

print(f"Option C: {len(c_concepts)} unique concept names")
print(f"Option B: {len(b_concepts)} unique concept names")
print(f"Option E: {len(e_concepts)} unique concept names")

print()
print("=== In B but NOT in C (B discovered these, C missed them) ===")
b_only = sorted(b_concepts - c_concepts)
for n in b_only:
    print(f"  {n}")

print()
print("=== In C but NOT in B (C covered these, B missed them) ===")
c_only = sorted(c_concepts - b_concepts)
for n in c_only:
    print(f"  {n}")

print()
print("=== In ALL THREE ===")
all_three = sorted(c_concepts & b_concepts & e_concepts)
for n in all_three:
    print(f"  {n}")
