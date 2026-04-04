#!/usr/bin/env python3
"""Emit empty JSON scaffolds for terms_layer, mechanisms, and candidate_queue at output_dir root.

Does not read context chunks or populate rows — authors fill content per
content/parts/library/terms-mechanisms-contract.md.

**Mechanism shape (authored JSON, not emitted here):** each mechanism row should
include **`realized_by`** (paths into ``shaped_story_map.json``). Procedural
**``steps[]``** belong on **stories** in the shaped story map, not as a duplicate
``steps`` array on mechanism objects.

By default, **skips** a file if it already exists (so full ``build.py`` does not wipe
authored Stage 2 JSON). Use ``--force`` to overwrite.
"""

from __future__ import annotations

import argparse
import json

from _config import (
    CANDIDATE_QUEUE_JSON,
    MECHANISMS_JSON,
    OUT_ROOT,
    SKILL_ROOT,
    TERMS_LAYER_JSON,
    TERMS_MECHANISMS_QUEUE_SCHEMA,
    workspace_root,
)


def main() -> None:
    p = argparse.ArgumentParser(description="Emit empty terms/mechanisms/candidate_queue scaffolds")
    p.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing JSON files (default: skip if file exists)",
    )
    args = p.parse_args()

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    schema = TERMS_MECHANISMS_QUEUE_SCHEMA
    writes: list[tuple[str, dict]] = [
        (TERMS_LAYER_JSON, {"terms": [], "schema": schema}),
        (MECHANISMS_JSON, {"mechanisms": [], "schema": schema}),
        (CANDIDATE_QUEUE_JSON, {"candidates": [], "schema": schema}),
    ]
    wrote_any = False
    for name, payload in writes:
        path = OUT_ROOT / name
        if path.is_file() and not args.force:
            print(f"skip scaffold {name} (exists; use --force to overwrite)")
            continue
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        wrote_any = True
    try:
        shown = OUT_ROOT.relative_to(workspace_root())
    except ValueError:
        shown = OUT_ROOT
    try:
        rel_skill = OUT_ROOT.relative_to(SKILL_ROOT)
    except ValueError:
        rel_skill = OUT_ROOT
    if wrote_any:
        print(f"Wrote terms/mechanisms/candidate_queue scaffolds under {shown} (skill-relative: {rel_skill})")
    else:
        print(f"terms/mechanisms/candidate_queue scaffolds unchanged under {shown} (skill-relative: {rel_skill})")


if __name__ == "__main__":
    main()
