"""Put the delivery-agent-kanban app root on sys.path for script and test imports."""
from __future__ import annotations

import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent.parent
KANBAN_PRACTICE_ROOT = APP_ROOT.parent.parent
SKILL_SCRIPTS_DIR = KANBAN_PRACTICE_ROOT / "skills" / "abd-kanban" / "scripts"


def ensure_app_on_path() -> Path:
    root = str(APP_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    return APP_ROOT


def ensure_skill_scripts_on_path() -> Path:
    ensure_app_on_path()
    scripts = str(SKILL_SCRIPTS_DIR)
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    return SKILL_SCRIPTS_DIR
