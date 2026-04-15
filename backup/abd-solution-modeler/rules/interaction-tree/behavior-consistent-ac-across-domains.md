---
title: Keep acceptance criteria consistent across connected domains
impact: HIGH
---

## Keep acceptance criteria consistent across connected domains

At small scale, AC can cover multiple domain objects together. As domain objects develop distinct behavior, keep AC consistent in structure across connected domains. AC crossing multiple domain behaviors is a signal to split the story.

**DO** at small scale keep AC together. As you scale, scope AC to one domain and keep structure consistent.
- At small scale, AC covering multiple domain objects together is acceptable: `User submits payment → System validates and routes` — covering wire and ACH together is fine when each has simple, similar validation
- As domain objects develop distinct behavior, scope AC to one domain: `User submits wire payment → System validates intermediary bank and routes to wire rail` — one payment type, one flow
- Keep AC consistent in structure across connected domains: wire and ACH stories both follow the same pattern with domain-specific details as the only variation
- AC crossing multiple domains is the signal to split the story: if an AC mentions both wire validation AND ACH routing, split into two stories

**DO NOT** write AC that mixes domain behaviors or write inconsistent AC across connected domains.
- Example (wrong): `User submits payment → System validates wire rules AND ACH rules AND check rules` — too broad when each has distinct validation
- Example (wrong): Wire story has 5 detailed AC covering every validation step, ACH story has 1 vague AC — keep the depth and structure parallel
