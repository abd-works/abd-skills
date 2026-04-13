"""Shared config: ROOT, MEMORY, ASSETS for resolving relative paths.

``ROOT`` is resolved in order (bootstrap from **this skill**, not from other repos or bots):

1. ``CONTENT_MEMORY_ROOT`` (environment), if set — **set this** for a stable topic/corpus folder
2. Current working directory — use when you ``cd`` to your corpus before running scripts

There is **no** separate skill-config path for the topic root; do not confuse with agile_bots
``WORKING_AREA``, MCP, or bot config.

Under ``ROOT``: ``markdown/`` (converted sources + **structural scan reports**), ``memory/`` (chunks, ``context_chunking_spec.yaml``, ``rag/`` for FAISS when embedded).
"""
import os
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPTS.parent
_REPO_ROOT = _SKILL_ROOT.parent.parent

try:
    from dotenv import load_dotenv

    for p in (
        _REPO_ROOT / "conf" / ".secrets",
        _REPO_ROOT / "conf" / ".env",
        _SKILL_ROOT / ".env",
        Path.cwd() / ".env",
    ):
        if p.exists():
            load_dotenv(p, override=True)
except ImportError:
    pass


def _get_root() -> Path:
    if "CONTENT_MEMORY_ROOT" in os.environ and os.environ["CONTENT_MEMORY_ROOT"].strip():
        return Path(os.environ["CONTENT_MEMORY_ROOT"]).expanduser().resolve()
    return Path.cwd().resolve()


def ensure_root() -> None:
    """Exit if ROOT points at a missing path."""
    if not ROOT.exists():
        print("Memory path not found:", ROOT, file=sys.stderr)
        print(
            "Set CONTENT_MEMORY_ROOT to your topic/corpus folder, or cd to that folder before running scripts.",
            file=sys.stderr,
        )
        sys.exit(1)


ROOT = _get_root()
MEMORY = ROOT / "memory"
ASSETS = ROOT / "assets"
