---
title: Domain–Interaction Sync
impact: HIGH
tags: [step2, domain, interaction, sync]
scanner: scan_domain_interaction_sync
---

## Every Concept Must Participate in at Least One Story

**DO** ensure every concept in the module participates in at least one story — as caller, receiver, or in pre-condition.

**DO NOT** have orphan concepts — concepts that appear in the domain model but in no story. Concepts participate as callers/receivers; state flows through Pre-Condition, Triggering-State, Resulting-State.

- Right: Concept "Check" appears in story trigger "**Player** rolls **Check**" and response "**System** returns **Degree**"
- Wrong: Concept "Check" in module.concepts but no story references it
