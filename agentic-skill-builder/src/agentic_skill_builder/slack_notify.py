"""Slack Incoming Webhook: load secrets and post a message.

Used by HITL pings (`notify_slack`) and by `scripts/diagnose_connectivity.py`.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

# Repo root: src/agentic_skill_builder/slack_notify.py -> parents[2]
REPO_ROOT = Path(__file__).resolve().parents[2]
SECRETS_PATH = REPO_ROOT / "conf" / ".secrets"

WEBHOOK_ENV_KEY = "AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL"
# Slack member ID (Profile → … → Copy member ID) so `<@U…>` pings @jeff.anderson et al.
NOTIFY_USER_ID_ENV_KEY = "AGENTIC_SKILL_BUILDER_SLACK_NOTIFY_USER_ID"


def _slack_user_mention_prefix(cfg: dict[str, str]) -> str:
    """Return `<@U123…> ` when NOTIFY_USER_ID is set (Slack requires ID, not username)."""
    uid = cfg.get(NOTIFY_USER_ID_ENV_KEY, "").strip()
    if not uid:
        return ""
    # Member IDs are typically U… (and sometimes W… in enterprise grids)
    if uid[0] not in ("U", "W") or len(uid) < 4:
        return ""
    return f"<@{uid}> "


def format_slack_text(text: str, cfg: dict[str, str] | None = None) -> str:
    """Prefix message with user mention when NOTIFY_USER_ID is configured."""
    cfg = merged_config() if cfg is None else cfg
    prefix = _slack_user_mention_prefix(cfg)
    return prefix + text if prefix else text


def load_secrets_file(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    out: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        k = key.strip()
        v = val.strip().strip('"').strip("'")
        if k:
            out[k] = v
    return out


def merged_config() -> dict[str, str]:
    """Load `conf/.secrets`, then override with non-empty environment variables."""
    cfg = load_secrets_file(SECRETS_PATH)
    for k, v in os.environ.items():
        if v:
            cfg[k] = v
    return cfg


def validate_incoming_webhook_url(url: str) -> str | None:
    """Return an error string if ``url`` cannot be an Incoming Webhook URL; else ``None``."""
    u = url.strip()
    if not u:
        return None
    if u.startswith("https://hooks.slack.com/"):
        return None
    # Pasted bot / user / app tokens (xoxb-, xoxp-, xoxe., xoxe-, xapp-, …) are not URLs
    if not u.startswith("https://") and (u.startswith("xox") or u.startswith("xapp")):
        return (
            f"{WEBHOOK_ENV_KEY} looks like a Slack OAuth/bot token, not a webhook URL. "
            "Use an Incoming Webhook URL on hostname hooks.slack.com (Slack app: Incoming Webhooks). "
            "Bot tokens use chat.postMessage, not this script."
        )
    if not u.startswith("https://"):
        return f"{WEBHOOK_ENV_KEY} must be an https:// URL (Slack Incoming Webhook)."
    if "hooks.slack.com" not in u:
        return (
            f"{WEBHOOK_ENV_KEY} should use hostname hooks.slack.com (Incoming Webhook), "
            "not another https URL."
        )
    return None


def post_slack_incoming_webhook(webhook_url: str, text: str) -> tuple[bool, str]:
    """POST `text` to a Slack Incoming Webhook URL. Returns (success, detail)."""
    url = webhook_url.strip()
    if not url:
        return False, f"SKIP ({WEBHOOK_ENV_KEY} not set)"
    err = validate_incoming_webhook_url(url)
    if err:
        return False, err
    body = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            code = resp.getcode()
            if code not in (200, 201):
                return False, f"HTTP {code}"
        return True, "OK (POST incoming webhook)"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return False, f"network error: {e.reason}"
    except OSError as e:
        return False, str(e)


def notify_slack(text: str) -> tuple[bool, str]:
    """Post `text` using webhook URL from merged config (secrets + env).

    When ``AGENTIC_SKILL_BUILDER_SLACK_NOTIFY_USER_ID`` is set (e.g. Jeff's member ID),
    the body is prefixed with ``<@U…>`` so Slack notifies that user.
    """
    cfg = merged_config()
    url = cfg.get(WEBHOOK_ENV_KEY, "").strip()
    if not url:
        return False, f"SKIP ({WEBHOOK_ENV_KEY} not set)"
    return post_slack_incoming_webhook(url, format_slack_text(text, cfg))
