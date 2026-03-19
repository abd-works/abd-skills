"""Chunk size statistics."""
import json
from pathlib import Path

chunks = json.loads(Path("test/mm3/solution/context/context_chunks.json").read_text(encoding="utf-8"))
sizes = [len(c["text"]) for c in chunks]
sizes.sort()

total = len(sizes)
print(f"Total chunks: {total}")
print(f"Min:    {min(sizes):,} chars")
print(f"Max:    {max(sizes):,} chars")
print(f"Mean:   {sum(sizes)//total:,} chars")
print(f"Median: {sizes[total//2]:,} chars")
print(f"P25:    {sizes[total//4]:,} chars")
print(f"P75:    {sizes[3*total//4]:,} chars")
print(f"P90:    {sizes[int(total*0.9)]:,} chars")
print()
print("Chunks that exceed 1,000 char limit used in B:")
over = [c for c in chunks if len(c["text"]) > 1000]
print(f"  {len(over)} of {total} chunks ({100*len(over)//total}%) exceed 1,000 chars")
over2 = [c for c in chunks if len(c["text"]) > 2000]
print(f"  {len(over2)} of {total} chunks ({100*len(over2)//total}%) exceed 2,000 chars")
over3 = [c for c in chunks if len(c["text"]) > 3000]
print(f"  {len(over3)} of {total} chunks ({100*len(over3)//total}%) exceed 3,000 chars")
