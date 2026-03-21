"""
Orchestrate full pipeline: convert → chunk → index chunks → embed → index.

Usage:
  python index_memory.py --path <source_folder>   # convert, chunk, index chunks, embed (full pipeline)
  python index_memory.py --memory <memory_name>   # chunk + index chunks + embed (chunks already exist or convert ran)
  python index_memory.py --replace                # rebuild entire index from all memory

Run from workspace root. Requires: markitdown, openai, faiss-cpu, numpy. Set OPENAI_API_KEY.

ROOT (memory storage) for --path: the **source folder you pass**. Chunks live under `<source>/memory/`
(topic flow) or `<parent>/memory/context/` when the folder is named `context`. Set CONTENT_MEMORY_ROOT
only when running --memory without a source (chunk+embed only).

After a successful --path pipeline, creates **<hub>/<source_folder_name> -> <source>/memory**
under the memory hub root (default: cwd, ABD_CONTENT_ROOT, or --junction-workspace / --memory-root).
Skip with --no-junction or SKIP_MEMORY_JUNCTION=1.

Chunk index: index_chunks runs after chunk; writes chunk_index.json to story-synthesizer/context/
when that path exists. Required for abd-story-synthesizer evidence extraction.
"""

import os
import subprocess
import sys
from pathlib import Path

from _config import ROOT, MEMORY, ensure_root, get_default_context_folder
from memory_junction import ensure_named_source_junction

ensure_root()
SCRIPTS = Path(__file__).resolve().parent


def _strip_junction_flags(args: list[str]) -> tuple[list[str], Path | None, bool]:
    """Remove --no-junction, --junction-workspace, --memory-root; return (args, hub_root_or_none, skip)."""
    skip = "--no-junction" in args
    out = [a for a in args if a != "--no-junction"]
    ws_flag: Path | None = None
    i = 0
    hub_flags = ("--junction-workspace", "--memory-root")
    while i < len(out):
        if out[i] in hub_flags and i + 1 < len(out):
            ws_flag = Path(out[i + 1]).resolve()
            out = out[:i] + out[i + 2 :]
            continue
        i += 1
    return out, ws_flag, skip


def _memory_hub_root(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit
    env = os.environ.get("ABD_CONTENT_ROOT", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return Path.cwd().resolve()


def _run(script: str, args: list[str], content_root: Path | None = None) -> bool:
    """Run a script; return True on success.
    When content_root is set, use it as cwd and CONTENT_MEMORY_ROOT so memory lives with the source."""
    cmd = [sys.executable, str(SCRIPTS / script)] + args
    cwd = str(content_root) if content_root else str(ROOT)
    env = os.environ.copy()
    if content_root:
        env["CONTENT_MEMORY_ROOT"] = str(content_root)
    r = subprocess.run(cmd, cwd=cwd, env=env)
    return r.returncode == 0


def main():
    args = sys.argv[1:]
    replace = "--replace" in args
    if replace:
        args = [a for a in args if a != "--replace"]
    args, junction_workspace_flag, skip_junction = _strip_junction_flags(args)

    # Full rebuild: embed all memory with --replace
    if replace and not any(a in args for a in ("--path", "--memory")):
        if not _run("embed_and_index.py", ["--replace"]):
            sys.exit(1)
        print("Full index rebuilt.")
        return

    # --path: convert → chunk → embed (or default: skill_space_path/context when no folder specified)
    path_idx = next((i for i, a in enumerate(args) if a == "--path"), None)
    src = None
    if path_idx is not None and path_idx + 1 < len(args):
        src = args[path_idx + 1]
    elif not any(a in args for a in ("--path", "--memory")):
        default = get_default_context_folder()
        if default is not None:
            src = str(default)
            print(f"Using default context folder: {src}\n")
    if src is not None:
        src_path = Path(src).resolve()
        # Folder named "context" (e.g. skill_space_path/context): keep legacy layout
        # chunks at <parent>/memory/context/ so project RAG stays under project root.
        if src_path.name == "context":
            content_root = src_path.parent
            memory_name = "context"
            memory_dir = content_root / "memory" / memory_name
            print(f"Pipeline: convert -> chunk -> index chunks -> sync SharePoint -> embed for {src}")
            print(f"Memory root (project): {content_root}  |  chunks: {memory_dir}\n")
            if not _run("convert_to_markdown.py", ["--memory", str(src_path)], content_root=content_root):
                sys.exit(1)
            if not _run("chunk_markdown.py", ["--path", str(src_path)], content_root=content_root):
                sys.exit(1)
            chunk_folder = memory_dir
            _run("index_chunks.py", ["--context-path", str(chunk_folder)], content_root=content_root)
            if not _run("sync_sharepoint_urls.py", ["--memory", memory_name], content_root=content_root):
                sys.exit(1)
            embed_args = ["--memory", memory_name]
            if replace:
                embed_args.append("--replace")
            if not _run("embed_and_index.py", embed_args, content_root=content_root):
                sys.exit(1)
            if not skip_junction:
                ensure_named_source_junction(
                    _memory_hub_root(junction_workspace_flag),
                    source_folder=src_path,
                    memory_dir=memory_dir,
                )
            print("\nDone: indexed.")
            return

        # Topic / memory source: chunks under <source>/memory/
        content_root = src_path
        memory_dir = content_root / "memory"
        print(f"Pipeline: convert -> chunk -> index chunks -> sync SharePoint -> embed for {src}")
        print(f"Topic root (CONTENT_MEMORY_ROOT): {content_root}")
        print(f"Chunks + RAG: {memory_dir}\n")
        if not _run("convert_to_markdown.py", ["--memory", str(src_path)], content_root=content_root):
            sys.exit(1)
        if not _run(
            "chunk_markdown.py",
            ["--path", str(src_path), "--output", str(memory_dir)],
            content_root=content_root,
        ):
            sys.exit(1)
        chunk_folder = memory_dir
        _run("index_chunks.py", ["--context-path", str(chunk_folder)], content_root=content_root)
        if not _run("sync_sharepoint_urls.py", [], content_root=content_root):
            sys.exit(1)
        embed_args: list[str] = []
        if replace:
            embed_args.append("--replace")
        if not _run("embed_and_index.py", embed_args, content_root=content_root):
            sys.exit(1)
        if not skip_junction:
            ensure_named_source_junction(
                _memory_hub_root(junction_workspace_flag),
                source_folder=src_path,
                memory_dir=memory_dir,
            )
        print("\nDone: indexed.")
        return

    # --memory / --path: chunk → embed (assumes convert already ran or chunks exist)
    mem_idx = next((i for i, a in enumerate(args) if a == "--memory"), None)
    path_idx = next((i for i, a in enumerate(args) if a == "--path"), None)
    src = None
    if path_idx is not None and path_idx + 1 < len(args):
        src = args[path_idx + 1]
    elif mem_idx is not None and mem_idx + 1 < len(args):
        src = args[mem_idx + 1]
    if src:
        src_path = Path(src).resolve()
        memory_name = src_path.name
        # Chunks go to src when src is "context" folder, else MEMORY/memory_name
        chunk_folder = src_path if memory_name == "context" else MEMORY / memory_name
        print(f"Pipeline: chunk -> index chunks -> sync SharePoint -> embed for {src}\n")
        if not _run("chunk_markdown.py", ["--path", src]):
            sys.exit(1)
        _run("index_chunks.py", ["--context-path", str(chunk_folder)])
        if not _run("sync_sharepoint_urls.py", ["--memory", memory_name]):
            sys.exit(1)
        embed_args = ["--memory", memory_name]
        if replace:
            embed_args.append("--replace")
        if not _run("embed_and_index.py", embed_args):
            sys.exit(1)
        print("\nDone: indexed.")
        return

    print("Usage:")
    print("  python index_memory.py --path <source_folder>   # full pipeline")
    print("  python index_memory.py --path <folder> [--memory-root <hub>] [--junction-workspace <hub>] [--no-junction]")
    print("  python index_memory.py --memory <memory_name>   # chunk + embed (convert already ran)")
    print("  python index_memory.py                          # if skill_space_path set: use <skill_space_path>/context")
    print("  python index_memory.py --replace                # rebuild entire index")


if __name__ == "__main__":
    main()
