"""
Search memory using semantic (vector) retrieval.

Usage:
  python search_memory.py "agile transformation approach" [--rag <memory/rag>] [--k 5] [--format text|json]
  (--rag defaults to <ROOT>/memory/rag — same ROOT as _config.)

Run from your topic folder (or set CONTENT_MEMORY_ROOT). Returns top-k chunks from the FAISS vector index.
Requires: pip install openai faiss-cpu numpy
Set OPENAI_API_KEY environment variable.
"""

import json
import os
import sys
from pathlib import Path

import _config  # noqa: F401 — loads OPENAI_API_KEY from .env/.secrets
from _config import MEMORY

EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_RAG_DIR = MEMORY / "rag"
DEFAULT_K = 5


def _embed_query(query: str) -> list[float]:
    """Embed query via OpenAI API."""
    from openai import OpenAI

    client = OpenAI()
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=[query])
    return resp.data[0].embedding


def search(query: str, rag_dir: Path, k: int = DEFAULT_K) -> list[dict]:
    """Return top-k chunks with content, source, and score."""
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is required.", file=sys.stderr)
        sys.exit(1)

    try:
        import numpy as np
        import faiss
    except ImportError as e:
        print(f"Missing dependency: {e}", file=sys.stderr)
        print("Run: pip install openai faiss-cpu numpy", file=sys.stderr)
        sys.exit(1)

    index_file = rag_dir / "index.faiss"
    metadata_file = rag_dir / "metadata.json"

    if not index_file.exists() or not metadata_file.exists():
        print(
            "No vector index found. Run embed_and_index.py first "
            f"(expected under {rag_dir}).",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(metadata_file, encoding="utf-8") as f:
        data = json.load(f)
    metadata = data["chunks"] if isinstance(data, dict) and "chunks" in data else data

    index = faiss.read_index(str(index_file))

    q_embedding = np.array(_embed_query(query), dtype="float32")
    q_norm = np.linalg.norm(q_embedding)
    if q_norm > 0:
        q_embedding = (q_embedding / q_norm).astype("float32")
    q_embedding = q_embedding.reshape(1, -1)

    k = min(k, len(metadata))
    scores, indices = index.search(q_embedding, k)

    out = []
    for idx, score in zip(indices[0], scores[0]):
        if idx < 0 or idx >= len(metadata):
            continue
        m = metadata[idx]
        out.append({
            "content": m.get("content", ""),
            "source": m.get("source", m.get("path", "")),
            "path": m.get("path", ""),
            "score": round(float(score), 3),
        })
    return out


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        print(
            'Usage: python search_memory.py "<query>" [--rag <memory/rag>] [--k 5] [--format text|json]'
        )
        return

    query = args[0]
    k = DEFAULT_K
    fmt = "text"
    rag_dir: Path | None = None
    i = 1
    while i < len(args):
        if args[i] == "--k" and i + 1 < len(args):
            k = int(args[i + 1])
            i += 2
        elif args[i] == "--format" and i + 1 < len(args):
            fmt = args[i + 1].lower()
            i += 2
        elif args[i] == "--rag" and i + 1 < len(args):
            rag_dir = Path(args[i + 1]).resolve()
            i += 2
        else:
            i += 1

    if rag_dir is None:
        rag_dir = DEFAULT_RAG_DIR.resolve()
        if not rag_dir.is_dir():
            print(
                "Error: pass --rag <memory/rag>, or set CONTENT_MEMORY_ROOT / cd to your topic folder "
                f"so default {rag_dir} exists.",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"Using default RAG dir: {rag_dir}")

    results = search(query, rag_dir=rag_dir, k=k)

    if fmt == "json":
        print(json.dumps(results, indent=2))
    else:
        for i, r in enumerate(results, 1):
            src = r.get("source") or r.get("path") or ""
            score = r.get("score")
            print(f"--- Result {i} ({src})" + (f" score={score}" if score else "") + " ---")
            print(r["content"][:500] + ("..." if len(r["content"]) > 500 else ""))
            print()


if __name__ == "__main__":
    main()
