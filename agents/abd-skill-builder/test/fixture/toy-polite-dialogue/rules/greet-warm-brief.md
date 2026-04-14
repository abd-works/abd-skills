---
id: greet_warm
title: Greet warm and brief
scanner: greet_warm
impact: MEDIUM
---

## Greet warm and brief

The **Greet** phase MUST open with a human-acknowledging line and stay short (no long preamble).

**DO** acknowledge the user before offering help.

**DO NOT** open with a demand, a command, or a wall of text before greeting.

This rule is enforced by `scripts/scanner_greet_warm.py` (binding in `rules/scanners.json`).
