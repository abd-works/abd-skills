#!/usr/bin/env python3
"""Convert source files (PDF, DOCX, PPTX, etc.) to markdown. Step 1a — Context to Memory.

Usage:
  python convert_to_markdown.py --path <source_folder> [--output <output_folder>]
  python convert_to_markdown.py --file <file_path> [--output <output_folder>]
  python convert_to_markdown.py --file Handbook.pdf --output docs --strip-chapter 2

When --output is omitted, writes markdown alongside each source file (same folder).
--strip-chapter N removes chapter N from the converted markdown (e.g. 2 = Chapter 2: Secret Origins).
Requires: pip install "markitdown[all]"
"""
import os
import re
import sys
from pathlib import Path

try:
    from markitdown import MarkItDown
except ImportError:
    print('Missing dependency. Run: pip install "markitdown[all]"')
    sys.exit(1)

SUPPORTED = {
    ".pdf", ".pptx", ".docx", ".xlsx", ".xls",
    ".html", ".htm", ".txt", ".csv", ".json", ".xml",
}

_md = MarkItDown()


def strip_chapter(text: str, chapter_num: int) -> str:
    """Remove one chapter from markdown: from first 'CHAPTER N:' through the line before next chapter.
    Stops at the first line that looks like 'CHAPTER M:' where M != N (so repeated running headers don't end the range).
    """
    lines = text.splitlines(keepends=True)
    start = None
    end = None
    prefix = f"CHAPTER {chapter_num}"
    ch_re = re.compile(r"CHAPTER\s*(\d+)\s*:", re.IGNORECASE)
    for i, line in enumerate(lines):
        m = ch_re.search(line)
        if not m:
            continue
        n = int(m.group(1))
        if n == chapter_num:
            if start is None:
                start = i
        elif start is not None:
            end = i
            break
    if start is None:
        return text
    if end is None:
        end = len(lines)
    return "".join(lines[:start] + lines[end:])


def convert_one(src: Path, out_dir: Path, source_ref: bool = True, strip_chapter_num: int | None = None) -> Path:
    """Convert one file to markdown. Returns output path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    text = _md.convert(str(src)).text_content
    if strip_chapter_num is not None:
        text = strip_chapter(text, strip_chapter_num)
    if source_ref:
        try:
            rel = src.as_posix()
            text = f"<!-- Source: {rel} -->\n\n" + text
        except (ValueError, OSError):
            pass
    out = out_dir / (src.stem + ".md")
    out.write_text(text, encoding="utf-8")
    return out


def _walk_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for dirpath, _, filenames in os.walk(root):
        dp = Path(dirpath)
        for name in filenames:
            p = dp / name
            if p.suffix.lower() in SUPPORTED and p.is_file():
                out.append(p)
    return sorted(out)


def run_file_mode(file_path: str, output: Path | None, strip_chapter_num: int | None = None) -> None:
    p = Path(file_path).resolve()
    if not p.is_file():
        print(f"File not found: {file_path}")
        return
    if p.suffix.lower() not in SUPPORTED:
        print(f"Unsupported format: {p.suffix}. Supported: {sorted(SUPPORTED)}")
        return
    out_dir = output or p.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        out = convert_one(p, out_dir, strip_chapter_num=strip_chapter_num)
        kb = out.stat().st_size // 1024
        print(f"Done: 1 file converted ({kb} KB) -> {out}")
    except Exception as e:
        print(f"FAIL  {type(e).__name__}: {e}")


def run_folder_mode(path: str, output: Path | None, strip_chapter_num: int | None = None) -> None:
    root = Path(path).resolve()
    if not root.is_dir():
        print(f"Path not found: {path}")
        return
    files = _walk_files(root)
    if not files:
        print(f"No supported files in {root}")
        return
    out_base = output or root
    print(f"Source: {root}  ({len(files)} files) -> {out_base}\n")
    ok, fail = [], []
    for i, f in enumerate(files, 1):
        rel = f.relative_to(root)
        out_dir = out_base / rel.parent
        label = str(rel)
        print(f"  [{i}/{len(files)}] {label} ... ", end="", flush=True)
        try:
            out = convert_one(f, out_dir, strip_chapter_num=strip_chapter_num)
            kb = out.stat().st_size // 1024
            print(f"OK  ({kb} KB)")
            ok.append(label)
        except Exception as e:
            print(f"FAIL  {type(e).__name__}: {e}")
            fail.append((label, str(e)))
    print(f"\nDone: {len(ok)} converted, {len(fail)} failed.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert source files to markdown for map-models-specs.")
    parser.add_argument("--path", help="Source folder to convert")
    parser.add_argument("--file", help="Single file to convert")
    parser.add_argument("--output", help="Output folder (default: alongside source)")
    parser.add_argument("--strip-chapter", type=int, metavar="N", help="Remove chapter N from output (e.g. 2 = Chapter 2: Secret Origins)")
    args = parser.parse_args()

    out = Path(args.output).resolve() if args.output else None
    strip_ch = getattr(args, "strip_chapter", None)

    if args.file:
        run_file_mode(args.file, out, strip_chapter_num=strip_ch)
        return
    if args.path:
        run_folder_mode(args.path, out, strip_chapter_num=strip_ch)
        return
    print("Usage:")
    print("  python convert_to_markdown.py --path <source_folder> [--output <output_folder>] [--strip-chapter N]")
    print("  python convert_to_markdown.py --file <file_path> [--output <output_folder>] [--strip-chapter N]")


if __name__ == "__main__":
    main()
