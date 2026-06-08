"""Domain acceptance tests — app domain + skill orchestration scripts on path."""
from __future__ import annotations

import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[3]
E2E_SEED_STUBS = APP_ROOT / "tests" / "e2e" / "_seed" / "pawplace-stubs"
SKILL_SCRIPTS = APP_ROOT.parent.parent / "skills" / "abd-kanban" / "scripts"

for path in (APP_ROOT, SKILL_SCRIPTS):
    entry = str(path)
    if entry not in sys.path:
        sys.path.insert(0, entry)
