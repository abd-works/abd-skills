import json
import tempfile

# Load the JSON
with open("context_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Extract unique source filenames
sources = sorted(set(c.get("source", "") for c in chunks if c.get("source")))

# For each chunk, extract first 500 chars of text
# Sample: max 50 chunks, first 500 chars each
sample_chunks = []
for i, chunk in enumerate(chunks[:50]):
    text = chunk.get("text", "")
    sample_chunks.append({
        "chunk_id": chunk.get("chunk_id", ""),
        "source": chunk.get("source", ""),
        "text_preview": text[:500] if text else ""
    })

# Build summary
summary = {
    "chunk_count": len(chunks),
    "unique_sources_count": len(sources),
    "sources": sources,
    "sample_chunks": sample_chunks
}

# Write to temp file
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tf:
    json.dump(summary, tf, indent=2, ensure_ascii=False)
    temp_path = tf.name

print("Summary written to:", temp_path)
print("Chunk count:", len(chunks))
print("Unique sources:", len(sources))
