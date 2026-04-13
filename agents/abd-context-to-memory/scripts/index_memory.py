"""
Full pipeline: convert -> draft spec -> chunk -> embed into local FAISS vector store.

Usage:
  python index_memory.py [--path <source_folder>]
  python index_memory.py --path <source_folder> --skip-convert
  python index_memory.py --path <source_folder> --skip-spec
  python index_memory.py --path <source_folder> --skip-convert --skip-spec
  python index_memory.py --rebuild [--path <source_folder>]

Steps:
  1. Convert  -- source docs -> markdown/
  2. Spec     -- structural reports -> markdown/; drafted YAML -> memory/context_chunking_spec.yaml
  3. Chunk    -- apply spec -> memory/
  4. Embed    -- chunks -> memory/rag/ (FAISS)

Run from your topic/corpus folder or set CONTENT_MEMORY_ROOT.
"""

import subprocess
import sys
from pathlib import Path

from _config import ROOT

AGENT_ROOT = Path(__file__).resolve().parents[1]
SKILLS = AGENT_ROOT / "skills"
SPEC_FILENAME = "context_chunking_spec.yaml"

SKILL_SCRIPTS = {
    "convert_to_markdown.py": SKILLS / "abd-convert-to-markdown" / "scripts",
    "draft_chunking_spec.py": SKILLS / "abd-chunk-markdown" / "scripts",
    "chunk_markdown.py": SKILLS / "abd-chunk-markdown" / "scripts",
    "embed_and_index.py": SKILLS / "abd-embed-vectors" / "scripts",
}


def run(script: str, args: list[str], cwd: Path) -> None:
    script_dir = SKILL_SCRIPTS.get(script)
    if script_dir is None:
        print(f"ERROR: unknown script {script}")
        sys.exit(1)
    script_path = script_dir / script
    if not script_path.exists():
        print(f"ERROR: script not found: {script_path}")
        sys.exit(1)
    result = subprocess.run(
        [sys.executable, str(script_path)] + args,
        cwd=str(cwd),
        env={**__import__("os").environ, "PYTHONPATH": str(script_dir)},
    )
    if result.returncode != 0:
        print(f"ERROR: {script} failed.")
        sys.exit(1)


def main():
    args = sys.argv[1:]

    skip_convert = "--skip-convert" in args
    skip_spec = "--skip-spec" in args
    rebuild = "--rebuild" in args
    args = [a for a in args if a not in ("--skip-convert", "--skip-spec", "--rebuild")]

    path_idx = next((i for i, a in enumerate(args) if a == "--path"), None)
    if path_idx is not None and path_idx + 1 < len(args):
        src = Path(args[path_idx + 1]).resolve()
    else:
        src = ROOT.resolve()
        print(f"Using default topic folder (CONTENT_MEMORY_ROOT or cwd): {src}")
    if not src.exists():
        print(f"ERROR: source folder not found: {src}")
        sys.exit(1)

    memory_dir = src / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)

    total_steps = 4
    step = 0

    step += 1
    if not skip_convert:
        print(f"[{step}/{total_steps}] Converting documents in {src} -> markdown/")
        run("convert_to_markdown.py", ["--memory", str(src)], cwd=src)
    else:
        print(f"[{step}/{total_steps}] Skipping convert (--skip-convert)")

    step += 1
    spec_path = memory_dir / SPEC_FILENAME
    if skip_spec:
        print(f"[{step}/{total_steps}] Skipping spec draft (--skip-spec)")
    else:
        print(
            f"[{step}/{total_steps}] Structural scan -> markdown/; chunking spec -> {spec_path.name} under memory/ when new"
        )
        run("draft_chunking_spec.py", ["--path", str(src)], cwd=src)
        print()
        print("  Review: markdown/structural_scan_report.*")
        print(f"  Spec: {spec_path} (if drafted)")
        print("  Edit boundaries, taxonomy, and defaults to match your sources.")
        print()

    step += 1
    print(f"[{step}/{total_steps}] Chunking markdown -> {memory_dir}")
    run("chunk_markdown.py", ["--path", str(src), "--output", str(memory_dir)], cwd=src)

    step += 1
    print(f"[{step}/{total_steps}] Embedding chunks -> {memory_dir / 'rag'}")
    embed_args = ["--path", str(memory_dir)]
    if rebuild:
        embed_args.append("--replace")
    run("embed_and_index.py", embed_args, cwd=src)

    print(f"\nDone. Index: {memory_dir / 'rag'}")


if __name__ == "__main__":
    main()
