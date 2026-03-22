#!/usr/bin/env python3
"""Post a message to Slack via Incoming Webhook (see conf/.secrets).

Usage (from repo root):
  python scripts/notify_slack.py "Your message here"
  python scripts/notify_slack.py
    (uses default completion ping — reply **keep going** in the IDE when ready)

Exit code: 0 on success, 1 on failure or missing webhook.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from agentic_skill_builder.slack_notify import WEBHOOK_ENV_KEY, notify_slack  # noqa: E402

DEFAULT_MESSAGE = (
    ":bell: **agentic-skill-builder** — work item finished. "
    "Reply in Cursor with **keep going** when you want to continue."
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Send a Slack Incoming Webhook message (AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL)."
    )
    parser.add_argument(
        "message",
        nargs="*",
        help="Message body (omit for default completion ping)",
    )
    args = parser.parse_args()
    text = " ".join(args.message).strip() if args.message else DEFAULT_MESSAGE
    ok, msg = notify_slack(text)
    print(msg)
    if msg.startswith("SKIP"):
        print(
            f"Set {WEBHOOK_ENV_KEY} in conf/.secrets - see conf/.secrets.example",
            file=sys.stderr,
        )
        return 1
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
