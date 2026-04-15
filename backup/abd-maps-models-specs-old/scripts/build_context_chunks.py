#!/usr/bin/env python3
"""DEPRECATED: parse_and_curate.py produces context_index.json + chunks/*.md instead.

Build context_chunks.json from markdown chunks. Step 1 — Context to Memory.

Superseded by: convert_to_markdown → discover_context_structure → parse_and_curate
See docs/plan-context-curation.md and parts/context.md.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path


def _stable_id(path: str, content: str) -> str:
    return hashlib.sha256(f"{path}:{content[:200]}".encode()).hexdigest()[:12]


def build_context_chunks(context_path: Path) -> list[dict]:
    """Build list of {chunk_id, source, text} from .md files."""
    chunks = []
    md_files = sorted(context_path.rglob("*.md"))
    if not md_files:
        return chunks

    for md in md_files:
        content = md.read_text(encoding="utf-8", errors="replace").strip()
        if not content:
            continue
        rel_path = str(md.relative_to(context_path))
        # source: stem for lookup (e.g. HeroesHandbook.md__section_002)
        source = md.stem if rel_path == md.name else rel_path.replace("/", "__").replace("\\", "__").removesuffix(".md")
        chunk_id = _stable_id(rel_path, content)
        chunks.append({
            "chunk_id": chunk_id,
            "source": source,
            "text": content,
        })
    return chunks


def main():
    print("DEPRECATED: Use parse_and_curate.py. Pipeline: convert → discover_context_structure → parse_and_curate", file=sys.stderr)
    parser = argparse.ArgumentParser(
        description="Build context_chunks.json for map-models-specs. Run after chunk_markdown."
    )
    parser.add_argument("--context-path", required=True, help="Path to chunked context directory")
    parser.add_argument("--output", default=None, help="Output path for context_chunks.json")
    args = parser.parse_args()

    context_path = Path(args.context_path).resolve()
    if not context_path.exists():
        print(f"Error: context path does not exist: {context_path}", file=sys.stderr)
        sys.exit(1)

    chunks = build_context_chunks(context_path)
    if not chunks:
        print(f"Warning: no markdown chunks found in {context_path}", file=sys.stderr)

    output_path = Path(args.output).resolve() if args.output else context_path / "context_chunks.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(chunks, indent=2), encoding="utf-8")
    print(f"context_chunks.json: {len(chunks)} chunks")
    print(f"Written to: {output_path}")


if __name__ == "__main__":
    main()
