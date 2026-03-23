#!/usr/bin/env python3
"""Phase 2 — emit terms, mechanisms, candidate queue JSON under phase2/."""

from __future__ import annotations

import json
from pathlib import Path

from _config import (
    CANDIDATE_QUEUE_JSON,
    MECHANISMS_JSON,
    PHASE2,
    SKILL_ROOT,
    TERMS_LAYER_JSON,
)


def main() -> None:
    PHASE2.mkdir(parents=True, exist_ok=True)
    (PHASE2 / TERMS_LAYER_JSON).write_text(
        json.dumps({"terms": [], "schema": "phase2/v1"}, indent=2),
        encoding="utf-8",
    )
    (PHASE2 / MECHANISMS_JSON).write_text(
        json.dumps({"mechanisms": [], "schema": "phase2/v1"}, indent=2),
        encoding="utf-8",
    )
    (PHASE2 / CANDIDATE_QUEUE_JSON).write_text(
        json.dumps({"candidates": [], "schema": "phase2/v1"}, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote phase2 artifacts under {PHASE2.relative_to(SKILL_ROOT)}")


if __name__ == "__main__":
    main()
