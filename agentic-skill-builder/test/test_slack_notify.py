"""Tests for slack_notify (no network when webhook unset)."""

from __future__ import annotations

from agentic_skill_builder.slack_notify import (
    format_slack_text,
    merged_config,
    post_slack_incoming_webhook,
    validate_incoming_webhook_url,
)


def test_validate_rejects_bot_token() -> None:
    err = validate_incoming_webhook_url("xoxp-1-fake-token")
    assert err is not None
    assert "token" in err.lower() or "webhook" in err.lower()


def test_validate_rejects_xoxe_enterprise_style_token() -> None:
    err = validate_incoming_webhook_url("xoxe.xoxp-1-not-a-url")
    assert err is not None


def test_validate_accepts_hooks_url() -> None:
    # Use a path without the /services/… token shape — GitHub push protection flags that pattern even for fakes.
    assert validate_incoming_webhook_url("https://hooks.slack.com/workbench/incoming-webhook-test") is None


def test_post_slack_rejects_token_as_url() -> None:
    ok, msg = post_slack_incoming_webhook("xoxp-not-a-url", "hello")
    assert ok is False
    assert "webhook" in msg.lower() or "token" in msg.lower()


def test_post_slack_empty_url_skips() -> None:
    ok, msg = post_slack_incoming_webhook("", "hello")
    assert ok is False
    assert "SKIP" in msg


def test_merged_config_reads_env_override(monkeypatch) -> None:
    monkeypatch.setenv("AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL", "https://hooks.slack.com/workbench/test")
    cfg = merged_config()
    assert cfg.get("AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL") == "https://hooks.slack.com/workbench/test"


def test_format_slack_text_prefixes_user_mention() -> None:
    cfg = {
        "AGENTIC_SKILL_BUILDER_SLACK_NOTIFY_USER_ID": "U012ABCDEF",
    }
    assert format_slack_text("Hello", cfg) == "<@U012ABCDEF> Hello"


def test_format_slack_text_ignores_invalid_id() -> None:
    cfg = {"AGENTIC_SKILL_BUILDER_SLACK_NOTIFY_USER_ID": "not-a-user-id"}
    assert format_slack_text("Hello", cfg) == "Hello"


def test_notify_slack_skips_without_webhook(monkeypatch, tmp_path) -> None:
    """Avoid reading real conf/.secrets so CI and dev machines behave the same."""
    import agentic_skill_builder.slack_notify as sn

    monkeypatch.setattr(sn, "SECRETS_PATH", tmp_path / "missing.secrets")
    monkeypatch.delenv("AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL", raising=False)
    ok, msg = sn.notify_slack("x")
    assert ok is False
    assert "SKIP" in msg
