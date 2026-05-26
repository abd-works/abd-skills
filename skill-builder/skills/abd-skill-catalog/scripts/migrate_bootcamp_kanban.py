file:///c%3A/dev/agilebydesign-skills/catalog/kanban-layout/index.html#/overview"""One-shot migration: extract spotlights from bootcamp part3, embed catalog kanban only."""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Allow running from scripts/
sys.path.insert(0, str(Path(__file__).resolve().parent))

from kanban_layout import (  # noqa: E402
    BOOTCAMP_CATALOG_PREFIX,
    _bootcamp_part3_path,
    _read_bootcamp_part3,
    build_bootcamp_catalog_embed_html,
    ensure_kanban_spotlights_source,
    patch_bootcamp_part3_catalog_embed,
)

if __name__ == "__main__":
    repo = Path(__file__).resolve().parents[4]
    src = ensure_kanban_spotlights_source(repo)
    print(f"spotlights source: {src}")
    if patch_bootcamp_part3_catalog_embed(repo):
        print(f"patched: {_bootcamp_part3_path(repo)}")
    else:
        print("part3 already uses catalog embed")
