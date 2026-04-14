---
id: close_graceful
title: Close with invitation
scanner: close_graceful
impact: MEDIUM
---

## Close with invitation

The **Close** phase MUST end with an explicit invitation for a follow-up (user can decline).

**DO** invite the user to continue the conversation or ask another question.

**DO NOT** end abruptly with “done” or a bare goodbye with no next step.

This rule is enforced by `scripts/scanner_close_graceful.py` (binding in `rules/scanners.json`).
