#!/usr/bin/env python3
"""Check outbound connectivity to OpenAI API and Slack Incoming Webhook.

Loads `conf/.secrets` (KEY=value lines) then applies environment overrides.
Exit code: 0 if all configured checks pass; 1 if any configured check fails.

Usage (from repo root):
  python scripts/diagnose_connectivity.py
"""

from __future__ import annotations

import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from agentic_skill_builder.slack_notify import (  # noqa: E402
    SECRETS_PATH,
    merged_config,
    post_slack_incoming_webhook,
)

OPENAI_MODELS_URL = "https://api.openai.com/v1/models"


def check_openai(api_key: str) -> tuple[bool, str]:
    if not api_key:
        return False, "SKIP (OPENAI_API_KEY not set)"
    req = urllib.request.Request(
        OPENAI_MODELS_URL,
        method="GET",
        headers={
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            code = resp.getcode()
            if code != 200:
                return False, f"HTTP {code}"
        return True, "OK (GET /v1/models)"
    except urllib.error.HTTPError as e:
        hint = " (check OPENAI_API_KEY)" if e.code == 401 else ""
        return False, f"HTTP {e.code}: {e.reason}{hint}"
    except urllib.error.URLError as e:
        return False, f"network error: {e.reason}"
    except OSError as e:
        return False, str(e)


def check_slack(webhook_url: str) -> tuple[bool, str]:
    if not webhook_url:
        return False, "SKIP (AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL not set)"
    ok, msg = post_slack_incoming_webhook(
        webhook_url,
        ":white_check_mark: `agentic-skill-builder` connectivity test (Slack webhook)",
    )
    return ok, msg


def main() -> int:
    import argparse

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--slack-only",
        action="store_true",
        help="Only test Slack webhook (skip OpenAI).",
    )
    p.add_argument(
        "--openai-only",
        action="store_true",
        help="Only test OpenAI (skip Slack).",
    )
    args, _unknown = p.parse_known_args()
    if args.slack_only and args.openai_only:
        print("Use only one of --slack-only or --openai-only.", file=sys.stderr)
        return 2

    cfg = merged_config()
    openai_key = cfg.get("OPENAI_API_KEY", "")
    slack_url = cfg.get("AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL", "")

    print(f"Secrets file: {SECRETS_PATH} ({'found' if SECRETS_PATH.is_file() else 'missing — use env only'})")
    print()

    results: list[tuple[str, bool, str]] = []

    if not args.slack_only:
        ok_oai, msg_oai = check_openai(openai_key)
        results.append(("OpenAI API", ok_oai, msg_oai))

    if not args.openai_only:
        ok_sl, msg_sl = check_slack(slack_url)
        results.append(("Slack webhook", ok_sl, msg_sl))

    any_fail = False
    any_skip = False
    for name, ok, msg in results:
        if msg.startswith("SKIP"):
            any_skip = True
            status = "SKIP"
        elif ok:
            status = "PASS"
        else:
            status = "FAIL"
            any_fail = True
        print(f"  [{status}] {name}: {msg}")

    print()
    if any_fail:
        print("One or more checks failed. Fix credentials or network, then re-run.")
        return 1
    slack_configured = bool(cfg.get("AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL", "").strip())
    openai_configured = bool(openai_key.strip())
    if any_skip and not (openai_configured and slack_configured):
        print("Some checks were skipped (missing vars). Set keys in conf/.secrets or env for full coverage.")
        return 0
    print("All configured checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
