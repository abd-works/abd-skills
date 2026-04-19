"""
Shared paths for abd-answers source-convert scripts (forked from upstream skill abd-context-to-memory).

Aligns with ``packages/answers/server/src/abd-answers-paths.ts``:
  pipeline = ``<repo>/data/assets/abd-answers-memory-pipeline`` (``files/...`` in API is virtual, not a disk folder).

Secrets: load from ``<abd-answers repo>/conf/.secrets`` and ``answers-memory.env``.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # type: ignore[misc, assignment]

_SCRIPT_DIR = Path(__file__).resolve().parent


def _find_abd_answers_repo() -> Path:
    cur = _SCRIPT_DIR
    for _ in range(16):
        pkg = cur / "package.json"
        if pkg.is_file():
            try:
                if json.loads(pkg.read_text(encoding="utf-8")).get("name") == "abd-answers":
                    return cur
            except (json.JSONDecodeError, OSError):
                pass
        if cur.parent == cur:
            break
        cur = cur.parent
    return Path.cwd()


_ABD_ANSWERS_REPO = _find_abd_answers_repo()
# abd-answers repo root (parent of ``data/assets`` when using default layout).
REPO_ROOT = _ABD_ANSWERS_REPO


def _load_conf_secrets() -> None:
    if not load_dotenv:
        return
    conf = _ABD_ANSWERS_REPO / "conf"
    for fname in (".secrets", ".env", "answers-memory.env"):
        p = conf / fname
        if p.is_file():
            load_dotenv(p, override=True)


_load_conf_secrets()

ABD_ANSWERS_PIPELINE_DIR = "abd-answers-memory-pipeline"

# Subfolders under PIPELINE_ROOT — convert → chunk; `rag/` is Pinecone manifest only (see PIPELINE_CONTRACT.md).
# Must match packages/answers/server/src/abd-answers-paths.ts (PIPELINE_*_SEGMENT).
PIPELINE_MARKDOWN_SEGMENT = "markdown"
PIPELINE_CHUNKED_SEGMENT = "chunked"
PIPELINE_RAG_SEGMENT = "rag"
PIPELINE_USERS_SEGMENT = "users"


def resolve_source_assets_root() -> Path:
    """Same idea as ``resolveSourceFilesRootAbs`` in abd-answers-paths.ts (topics hub; may follow ANSWERS_DEFAULT_HUB_PATH)."""
    env = os.environ.get("ANSWERS_DEFAULT_HUB_PATH", "").strip()
    if env:
        hub = Path(env).expanduser().resolve()
        junction = hub / "assets"
        if junction.is_dir():
            return junction
        if hub.name.lower() == "assets" and hub.is_dir():
            return hub
        return hub
    p = _ABD_ANSWERS_REPO / "data" / "assets"
    if p.is_dir():
        return p
    return p


def resolve_repo_data_assets_root() -> Path:
    """Repo ``data/assets`` — matches ``resolveRepoDataAssetsAbs`` in TS; not hub-overridden."""
    return _ABD_ANSWERS_REPO / "data" / "assets"


def resolve_pipeline_root() -> Path:
    return resolve_repo_data_assets_root() / ABD_ANSWERS_PIPELINE_DIR


ASSETS = resolve_source_assets_root()
ROOT = ASSETS
PIPELINE_ROOT = resolve_pipeline_root()
PIPELINE_MARKDOWN = PIPELINE_ROOT / PIPELINE_MARKDOWN_SEGMENT
PIPELINE_CHUNKED = PIPELINE_ROOT / PIPELINE_CHUNKED_SEGMENT
PIPELINE_RAG = PIPELINE_ROOT / PIPELINE_RAG_SEGMENT
# Chunked-output fallback when source path is not under pipeline/assets (same tree as markdown corpus)
MEMORY = PIPELINE_MARKDOWN


def ensure_root() -> None:
    if not ASSETS.exists():
        print("Source assets not found:", ASSETS, file=sys.stderr)
        print(
            "Set ANSWERS_DEFAULT_HUB_PATH to the hub (or folder named assets), "
            "or create repo data/assets.",
            file=sys.stderr,
        )
        sys.exit(1)


# PIPELINE_RAG: Pinecone sync manifest (`pinecone-manifest.json`) and related metadata only.
# Vector search is Pinecone-only (TypeScript); there is no local FAISS index in this repo.


def path_is_pinecone_rag_metadata_only(p: Path) -> bool:
    """
    True if ``p`` is under folders that must not be converted/chunked as corpus:
    legacy ``.../assets/rag/`` or pipeline ``.../abd-answers-memory-pipeline/rag/`` (manifest only).
    """
    parts = [x.casefold() for x in p.resolve().parts]
    pl = ABD_ANSWERS_PIPELINE_DIR.casefold()
    for i in range(len(parts) - 1):
        if parts[i] == "assets" and parts[i + 1] == "rag":
            return True
        if parts[i] == pl and parts[i + 1] == "rag":
            return True
    return False
