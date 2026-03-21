#!/usr/bin/env python3
"""DEPRECATED: Use parse_and_curate.py instead.

Chunk converted markdown into smaller pieces. Step 1b — Context to Memory.

Superseded by: convert_to_markdown → discover_context_structure → parse_and_curate
See docs/plan-context-curation.md and parts/context.md.
"""
import re
import shutil
import sys
from pathlib import Path

MIN_CHUNK_LINES = 5


def _find_image_refs(text: str) -> list[str]:
    return re.findall(r"!\[[^\]]*\]\(<?([^)>]+)>?\)", text)


def _copy_images(refs: list[str], src_base: Path, dst_base: Path) -> None:
    for ref in refs:
        src = src_base / ref
        if not src.exists():
            continue
        dst = dst_base / ref
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(str(src), str(dst))


def _chunk_by_slides(text: str) -> list[tuple[str, str]]:
    parts = re.split(r"(<!-- Slide number: \d+ -->)", text)
    chunks, current_label, current_lines = [], "preamble", []
    for part in parts:
        m = re.match(r"<!-- Slide number: (\d+) -->", part)
        if m:
            if current_lines and "".join(current_lines).strip():
                chunks.append((current_label, "".join(current_lines)))
            current_label = f"slide_{int(m.group(1)):02d}"
            current_lines = [part]
        else:
            current_lines.append(part)
    if current_lines and "".join(current_lines).strip():
        chunks.append((current_label, "".join(current_lines)))
    return chunks


def _chunk_by_headings(text: str) -> list[tuple[str, str]]:
    lines = text.split("\n")
    chunks, current_lines, chunk_idx = [], [], 0
    for line in lines:
        if re.match(r"^#{1,2}\s", line) and len(current_lines) >= MIN_CHUNK_LINES:
            chunks.append((f"section_{chunk_idx:02d}", "\n".join(current_lines)))
            current_lines, chunk_idx = [], chunk_idx + 1
        current_lines.append(line)
    if current_lines:
        chunks.append((f"section_{chunk_idx:02d}", "\n".join(current_lines)))
    return chunks


def _chunk_by_section_markers(text: str) -> list[tuple[str, str]]:
    lines = text.split("\n")
    chunks, current_lines, chunk_idx = [], [], 0
    section_pat = re.compile(r"^CHAPTER\s+\d+\b", re.IGNORECASE)
    for line in lines:
        if section_pat.search(line) and len(current_lines) >= MIN_CHUNK_LINES:
            chunks.append((f"section_{chunk_idx:02d}", "\n".join(current_lines)))
            current_lines, chunk_idx = [], chunk_idx + 1
        current_lines.append(line)
    if current_lines:
        chunks.append((f"section_{chunk_idx:02d}", "\n".join(current_lines)))
    return chunks


def _has_markdown_headings(text: str) -> bool:
    return bool(re.search(r"^#{1,2}\s", text, re.MULTILINE))


def _is_slide_deck(text: str) -> bool:
    return bool(re.search(r"<!-- Slide number: \d+ -->", text))


def _is_chunked_output(path: Path) -> bool:
    return bool(re.search(r"__(?:slide|section|page)_\d+\.md$", path.name, re.IGNORECASE))


def _extract_source_ref(text: str) -> tuple[str | None, str | None]:
    m = re.search(r"<!--\s*Source:\s*([^|]+)\s*\|\s*([^>]+)\s*-->", text)
    if m:
        return (m.group(1).strip(), m.group(2).strip())
    m = re.search(r"<!--\s*Source:\s*([^>]+)\s*-->", text)
    return (m.group(1).strip(), None) if m else (None, None)


def _add_chunk_source_ref(content: str, source_path: str | None, source_url: str | None, location: str) -> str:
    if not source_path:
        return content
    loc = f", {location}" if location else ""
    url = f" | {source_url}" if source_url else ""
    return f"<!-- Source: {source_path}{loc}{url} -->\n\n" + content


def chunk_file(md_path: Path, conv_root: Path, chunk_root: Path) -> int:
    text = md_path.read_text(encoding="utf-8")
    stem, (source_path, source_url) = md_path.stem, _extract_source_ref(text)
    chunk_root.mkdir(parents=True, exist_ok=True)

    if _is_slide_deck(text):
        chunks = _chunk_by_slides(text)
    elif text.count("\n") > 200:
        chunks = _chunk_by_headings(text) if _has_markdown_headings(text) else _chunk_by_section_markers(text)
    else:
        chunks = [(stem, text)]

    def _loc(label: str) -> str:
        if label.startswith("slide_"):
            return f"slide {int(label.split('_')[1])}"
        if label.startswith("section_"):
            return f"section {int(label.split('_')[1]) + 1}"
        return ""

    written = 0
    for label, content in chunks:
        if not content.strip():
            continue
        content = _add_chunk_source_ref(content, source_path, source_url, _loc(label))
        out = chunk_root / (f"{stem}__{label}.md" if len(chunks) > 1 else f"{stem}.md")
        out.write_text(content, encoding="utf-8")
        for ref in _find_image_refs(content):
            _copy_images([ref], conv_root, chunk_root)
        written += 1
    return written


def main():
    print("DEPRECATED: Use parse_and_curate.py. Pipeline: convert → discover_context_structure → parse_and_curate", file=sys.stderr)
    import argparse
    parser = argparse.ArgumentParser(description="Chunk markdown for map-models-specs. Run convert_to_markdown first.")
    parser.add_argument("--path", required=True, help="Source folder with .md files")
    parser.add_argument("--output", required=True, help="Output folder for chunks")
    args = parser.parse_args()

    src_root = Path(args.path).resolve()
    chunk_base = Path(args.output).resolve()
    if not src_root.exists():
        print(f"Path not found: {src_root}")
        sys.exit(1)

    md_files = sorted(
        f for f in src_root.rglob("*.md")
        if "images" not in f.parts and not _is_chunked_output(f)
    )
    if not md_files:
        print(f"No markdown in {src_root}. Run convert_to_markdown.py first.")
        sys.exit(1)

    print(f"Source: {src_root}  ({len(md_files)} files) -> {chunk_base}\n")
    total = 0
    for i, f in enumerate(md_files, 1):
        conv_root = f.parent
        rel_parent = f.parent.relative_to(src_root)
        chunk_root = chunk_base / rel_parent
        rel = f.relative_to(src_root)
        label = str(rel) if rel != Path(".") else f.name
        print(f"  [{i}/{len(md_files)}] {label} ... ", end="", flush=True)
        try:
            n = chunk_file(f, conv_root, chunk_root)
            total += n
            print(f"OK  ({n} chunks)")
        except Exception as e:
            print(f"FAIL  {e}")
    print(f"\nDone: {total} chunks.")


if __name__ == "__main__":
    main()
