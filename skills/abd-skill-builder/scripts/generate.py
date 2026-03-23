#!/usr/bin/env python3
"""CLI entry: `python scripts/generate.py --phase <slug>` — same as `generate_prompt.py`.

Use this when you run an **AI-chat** phase: the script prints the instruction text you read and
follow (not ad-hoc prose). See `parts/phases/plan-script-build.md` and `library/process-approach.md`.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent


def _main() -> int:
    spec = importlib.util.spec_from_file_location(
        "_generate_prompt_impl", _ROOT / "generate_prompt.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load generate_prompt.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return int(mod.main())


if __name__ == "__main__":
    raise SystemExit(_main())
