#!/usr/bin/env python3
"""Report Pass 1 results from progress.log: unique concept names and chunk coverage.

Use after classify_chunks.py (Step 5) to summarize what the AI discovered.
Writes a readable report file with one concept per line and blank lines between each.

Usage:
    python scripts/list_pass1_concepts.py [path/to/progress.log] [--out report.txt]
    Default log: scripts/progress.log
    Default out: scripts/pass1_report.txt (concepts separated by newlines for readability)
"""
import argparse
import re
import sys
from pathlib import Path


def extract_pass1_report(log_path: Path) -> dict:
    """Parse progress.log; return dict with expected_chunks, chunk_ids_in_stream, concepts."""
    log = log_path.read_text(encoding="utf-8")
    concepts = set()
    for m in re.finditer(r'"concept"\s*:\s*"([^"]+)"', log):
        concepts.add(m.group(1))
    chunk_ids = set(re.findall(r'"chunk_id"\s*:\s*"([^"]+)"', log))

    # Optional: read expected chunk count from log header (e.g. "Chunks: 725")
    expected = None
    if mo := re.search(r"Chunks:\s*(\d+)", log[:2000]):
        expected = int(mo.group(1))

    return {
        "expected_chunks": expected,
        "chunk_ids_in_stream": len(chunk_ids),
        "concepts": sorted(concepts),
    }


def format_report(data: dict, log_path: Path, concepts_separated_by_blank_line: bool = True) -> str:
    """Build report text. If concepts_separated_by_blank_line, put a blank line between each concept."""
    lines = [
        "=== Pass 1 classification report ===",
        f"Source: {log_path}",
        "",
    ]
    if data["expected_chunks"] is not None:
        lines.append(f"Chunks (expected): {data['expected_chunks']}")
    lines.append(f"Chunk IDs in AI stream: {data['chunk_ids_in_stream']}")
    if data["expected_chunks"] is not None and data["chunk_ids_in_stream"] != data["expected_chunks"]:
        gap = data["expected_chunks"] - data["chunk_ids_in_stream"]
        lines.append(f"  (gap: {gap} chunk IDs not present in logged stream)")
    lines.append(f"Unique concepts discovered: {len(data['concepts'])}")
    lines.extend(["", "Concepts:", ""])
    sep = "\n\n" if concepts_separated_by_blank_line else "\n"
    lines.append(sep.join(data["concepts"]))
    lines.extend(["", "", f"Total: {len(data['concepts'])} concepts"])
    return "\n".join(lines)


def main() -> int:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Report Pass 1 concepts and chunk coverage from progress.log")
    parser.add_argument("log", nargs="?", default=str(base / "progress.log"), help="Path to progress.log")
    parser.add_argument("--out", "-o", default=str(base / "pass1_report.txt"), help="Write report to this file")
    args = parser.parse_args()

    log_path = Path(args.log)
    if not log_path.exists():
        print(f"Error: log not found: {log_path}", file=sys.stderr)
        return 1

    data = extract_pass1_report(log_path)
    report = format_report(data, log_path, concepts_separated_by_blank_line=True)

    out_path = Path(args.out)
    out_path.write_text(report, encoding="utf-8")
    print(f"Wrote report to {out_path}", file=sys.stderr)
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
