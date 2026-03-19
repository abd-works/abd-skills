import json
from pathlib import Path

f = Path("test/experiment/step2a/option-b/chunk_evidence.json")
run_log = Path("test/experiment/step2a/option-b/run_log.json")

if run_log.exists():
    print("RUN COMPLETE")
    data = json.loads(run_log.read_text(encoding="utf-8"))
    print(json.dumps(data, indent=2))
elif not f.exists():
    print("No output file yet — agent has not started writing")
else:
    data = json.loads(f.read_text(encoding="utf-8"))
    evidence = data.get("evidence", [])
    total = len(evidence)
    with_concepts = sum(1 for e in evidence if e.get("primary_concepts"))
    empty = total - with_concepts
    print(f"Status:         IN PROGRESS")
    print(f"Chunks in file: {total} / 267")
    print(f"With concepts:  {with_concepts}")
    print(f"Empty results:  {empty}")
    print(f"AI calls:       {data.get('ai_calls', '?')}")
    print(f"Elapsed:        {data.get('elapsed_seconds', '?')}s")
    # Show last 3 chunks processed
    if evidence:
        print("\nLast 3 chunks processed:")
        for e in evidence[-3:]:
            nc = len(e.get("primary_concepts", []))
            nr = len(e.get("cross_module_relationships", []))
            print(f"  {e['chunk_id']}  concepts:{nc}  relationships:{nr}  [{e.get('source','')[:40]}]")
