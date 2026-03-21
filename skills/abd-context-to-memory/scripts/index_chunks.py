#!/usr/bin/env python3
"""Build chunk index from markdown chunks (reverse index: chunk ID -> path, heading, size).

Use for evidence lookup: which chunk file and section a passage came from. Does NOT re-chunk.
Run after chunk_markdown. Output lives under the same memory root as the chunks.

Usage:
  python index_chunks.py --context-path <chunk_folder> [--output <path>]

When --output is omitted, writes to <context_path>/chunk_index.json (under memory).
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

# Allow import from sibling scripts
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

try:
    from _config import ROOT
except ImportError:
    ROOT = Path.cwd()


def _stable_id(path: str, content: str) -> str:
    return hashlib.sha256(f"{path}:{content[:200]}".encode()).hexdigest()[:12]


def analyze_chunks(context_path: Path) -> dict:
    chunks = []
    seen_hashes: dict[str, str] = {}
    duplicates = []

    md_files = sorted(context_path.rglob("*.md"))
    if not md_files:
        return {"error": f"No markdown chunks found in {context_path}", "chunks": []}

    for md in md_files:
        content = md.read_text(encoding="utf-8", errors="replace").strip()
        if not content:
            continue

        content_hash = hashlib.md5(content.encode()).hexdigest()
        rel_path = str(md.relative_to(context_path))
        chunk_id = _stable_id(rel_path, content)

        if content_hash in seen_hashes:
            duplicates.append({
                "chunk_id": chunk_id,
                "path": rel_path,
                "duplicate_of": seen_hashes[content_hash],
            })
            continue

        seen_hashes[content_hash] = rel_path

        heading = ""
        for line in content.split("\n"):
            if line.startswith("#"):
                heading = line.lstrip("#").strip()
                break

        chunks.append({
            "chunk_id": chunk_id,
            "path": rel_path,
            "heading": heading,
            "char_count": len(content),
            "line_count": content.count("\n") + 1,
        })

    return {
        "context_path": str(context_path),
        "total_chunks": len(chunks),
        "total_duplicates": len(duplicates),
        "chunks": chunks,
        "duplicates": duplicates,
    }


def _default_output_path(context_path: Path) -> Path:
    """Write alongside chunks: <context_path>/chunk_index.json (under memory)."""
    return context_path.resolve() / "chunk_index.json"


def main():
    parser = argparse.ArgumentParser(
        description="Build chunk index (chunk_id -> path, heading). Run after chunk_markdown."
    )
    parser.add_argument("--context-path", required=True, help="Path to chunked context directory")
    parser.add_argument("--output", default=None, help="Output path for chunk_index.json")
    args = parser.parse_args()

    context_path = Path(args.context_path).resolve()
    if not context_path.exists():
        print(f"Error: context path does not exist: {context_path}", file=sys.stderr)
        sys.exit(1)

    result = analyze_chunks(context_path)

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = _default_output_path(context_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Chunk index: {result['total_chunks']} chunks, {result['total_duplicates']} duplicates")
    print(f"Written to: {output_path}")


if __name__ == "__main__":
    main()
