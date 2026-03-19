"""Quick debug: run Option B on just 2 chunks to verify OpenAI response parsing."""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "option-b"))
from classify_chunks import build_module_context, ai_extract_batch, parse_json_objects

skill_dir = Path(__file__).resolve().parent.parent.parent.parent
step1 = json.loads((skill_dir / "test/experiment/step1-output-v2.json").read_text(encoding="utf-8"))
chunks = json.loads((skill_dir / "test/mm3/solution/context/context_chunks.json").read_text(encoding="utf-8"))

module_context = build_module_context(step1)
batch = [chunks[10], chunks[11]]  # two non-trivial chunks

print(f"Testing with chunks: {batch[0]['chunk_id']}, {batch[1]['chunk_id']}")
print(f"API key set: {'yes' if os.environ.get('OPENAI_API_KEY') else 'NO'}")
print()

results = ai_extract_batch(batch, module_context, model="gpt-4o-mini")
print(f"Got {len(results)} results:")
for r in results:
    print(json.dumps(r, indent=2))
