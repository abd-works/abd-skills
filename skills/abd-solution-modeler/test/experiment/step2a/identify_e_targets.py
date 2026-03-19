"""Identify chunks that Option E should send to AI.

Criteria:
  - Code (Option C) found <= 3 concept mentions (low text signal)
  - BUT chunk has structural indicators of high information density:
      * All-caps column headers on consecutive lines (stat blocks, tables)
      * Numeric patterns suggesting stat arrays (e.g. "36 + 84 + 1 + 17")
      * Known stat-block keywords (STRENGTH, STAMINA, AGILITY, etc.)
      * Character archetype headers (PL10, PL8, etc.)

These are the chunks the code can't read well but AI extracts a lot from.
"""
import json
import re
from pathlib import Path

c_data = json.loads(Path("test/experiment/step2a/option-c/chunk_evidence.json").read_text(encoding="utf-8"))
chunks_raw = json.loads(Path("test/mm3/solution/context/context_chunks.json").read_text(encoding="utf-8"))
chunk_text = {c["chunk_id"]: c["text"] for c in chunks_raw}

# Known stat-block / character-sheet indicators
STAT_KEYWORDS = re.compile(
    r'\b(STRENGTH|STAMINA|AGILITY|DEXTERITY|FIGHTING|INTELLECT|AWARENESS|PRESENCE|'
    r'PL\s*\d+|Power Point Totals|Abilities \d+|Powers \d+|Advantages \d+|Skills \d+|Defenses \d+)\b'
)
NUMERIC_BUDGET = re.compile(r'\d+\s*\+\s*\d+\s*\+\s*\d+')  # budget totals like "36 + 84 + 1"
ALLCAPS_RUN = re.compile(r'(?:^[A-Z][A-Z\s]{2,20}$\n){2,}', re.MULTILINE)

targets = []
skipped = []

for e in c_data["evidence"]:
    cid = e["chunk_id"]
    text = chunk_text.get(cid, "")
    c_concepts = e.get("concept_count", 0)

    is_stat_block = bool(STAT_KEYWORDS.search(text))
    is_budget = bool(NUMERIC_BUDGET.search(text))
    has_allcaps_run = bool(ALLCAPS_RUN.search(text))

    # Target: low code signal + high-density indicators
    if c_concepts <= 3 and (is_stat_block or is_budget or has_allcaps_run):
        targets.append({
            "chunk_id": cid,
            "source": e.get("source", ""),
            "c_concepts": c_concepts,
            "c_rels": e.get("relationship_count", 0),
            "stat_block": is_stat_block,
            "budget": is_budget,
            "allcaps": has_allcaps_run,
        })
    else:
        skipped.append(cid)

print(f"Option E targets: {len(targets)} chunks  (skipped: {len(skipped)})")
print(f"Estimated AI calls: {(len(targets) + 4) // 5} batches of 5")
print()
print(f"{'chunk_id':16s} {'C:con':6s} {'C:rel':6s} {'stat':5s} {'budget':7s}  source")
print("-" * 80)
for t in sorted(targets, key=lambda x: x["source"]):
    print(f"{t['chunk_id']:16s} {t['c_concepts']:6d} {t['c_rels']:6d} {'Y' if t['stat_block'] else 'N':5s} {'Y' if t['budget'] else 'N':7s}  {t['source'][:40]}")
