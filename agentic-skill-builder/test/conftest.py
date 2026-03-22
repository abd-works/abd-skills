"""Ensure `src/` is on sys.path for tests without editable install."""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Avoid posting pipeline stage messages to Slack when developers have webhooks in .secrets.
os.environ.setdefault("AGENTIC_SKILL_BUILDER_SLACK_PIPELINE_LOG", "0")

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
