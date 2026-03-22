# Configuration

Place **non-secret** defaults here (graph names, paths templates, feature flags).

## Secrets file (canonical)

| File | Role |
| ---- | ---- |
| **`conf/.secrets`** | **Gitignored.** `KEY=value` lines (same shape as `.env`). Put **`OPENAI_API_KEY`**, **`AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL`**, and optionally **`AGENTIC_SKILL_BUILDER_SLACK_NOTIFY_USER_ID`** (Jeff’s member ID for `@jeff.anderson` pings) — see **`.secrets.example`**. |
| **`conf/.secrets.example`** | **Committed** template — copy to **`conf/.secrets`** and fill in; never commit `.secrets`. |

Alternatively you can export **`AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL`** in the shell or use a repo-root **`.env`** (also gitignored). Implementation should load **`conf/.secrets`** first if present, then environment.

## Slack — human-in-the-loop (HITL)

Orchestration **pings** you on Slack whenever the LangGraph (or a manual review gate) **requires your attention**. See **`docs/plans/langgraph-agentic-orchestration-plan.md` §5.4**.

| What | Where |
| ---- | ----- |
| **Join this Slack workspace** (bookmark for humans) | [Agile by Design — invite link](https://join.slack.com/share/enQtMTA3NDMxMDA3OTI1NzktOWJjMDA2MDhhNjdiNDkwOTE2YWVmYzk4NTAwOGRiZTQ2M2M3YzJmODBmNGNhN2FmY2U1M2RiMzY4NjBlMzRjYg) |
| **Webhook URL** | **`AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL`** in **`conf/.secrets`** (see **`.secrets.example`**) |
| **@jeff.anderson on every ping** | Set **`AGENTIC_SKILL_BUILDER_SLACK_NOTIFY_USER_ID`** to Jeff’s Slack **member ID** (starts with `U`, e.g. from Profile → … → **Copy member ID**). Incoming Webhooks do not turn `@jeff.anderson` text into a mention; the API needs `<@U123…>`, which this ID supplies. |

Create an **Incoming Webhook** in Slack (Apps → your app → Incoming Webhooks) targeting the channel where you want HITL messages, then paste the URL into **`conf/.secrets`** under that key.

**Also:** **`conf/slack.env.example`** documents the same variable for people who prefer a **`.env`** file at repo root instead of `conf/.secrets`.

## Verify outbound connectivity

From the repo root:

```bash
python scripts/diagnose_connectivity.py
```

This checks the OpenAI API (Bearer token) and the Slack Incoming Webhook. Environment variables override values in **`conf/.secrets`**.

**Send a custom ping** (or a default “reply **keep going**” message):

```bash
python scripts/notify_slack.py "Your summary here"
```
