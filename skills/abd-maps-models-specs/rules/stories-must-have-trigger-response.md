---
rule_id: stories-must-have-trigger-response
phases: [step1]
order: 20
scanner: scripts/scanners/stories_have_trigger_response.py
impact: HIGH
---

## Stories must express actor → system interaction

A story is not a feature title alone. It is a minimal interaction: something an actor does (trigger) and how the system responds (response). Without both, the story cannot be validated, traced to evidence, or tested.

The scanner (`scripts/scanners/stories_have_trigger_response.py`) checks that `trigger` and `response` are populated and non-trivial.

**DO** write `trigger` and `response` as sentences. Use `**Actor**` / `**System**` and `**Concept**` bolding where domain concepts participate, matching how they appear under `epic.stories[]` or `epic.sub_epics[].stories[]` in `map-model-spec.json`.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Retail", "concepts": [] },
      "epic": {
        "name": "Checkout",
        "stories": [
          {
            "name": "Price basket with promotions",
            "trigger": "**Cashier** adds **LineItem** rows to **Cart**",
            "response": "**System** applies **Promotion** rules and refreshes **Cart** totals"
          }
        ]
      }
    }
  ]
}
```

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Payments", "concepts": [] },
      "epic": {
        "name": "Wire",
        "stories": [
          {
            "name": "Submit wire transfer",
            "trigger": "**Customer** submits **WireTransfer** instruction",
            "response": "**System** runs **LimitChecker** and queues **SettlementBatch** when allowed"
          }
        ]
      }
    }
  ]
}
```

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Combat", "concepts": [] },
      "epic": {
        "name": "Attacks",
        "stories": [
          {
            "name": "Resolve attack",
            "trigger": "**Player** declares **Attack** against **Creature**",
            "response": "**System** compares the roll to **ArmorClass** and applies **Damage** on a hit"
          }
        ]
      }
    }
  ]
}
```

**DO NOT** leave `trigger` or `response` empty, or fill them with titles only.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Retail", "concepts": [] },
      "epic": {
        "name": "Checkout",
        "stories": [{ "name": "Checkout" }]
      }
    }
  ]
}
```

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Payments", "concepts": [] },
      "epic": {
        "name": "Wire",
        "stories": [
          {
            "name": "Wire transfer",
            "trigger": "User stuff",
            "response": "It works"
          }
        ]
      }
    }
  ]
}
```

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Combat", "concepts": [] },
      "epic": {
        "name": "Combat",
        "stories": [
          {
            "name": "Combat",
            "trigger": "Combat",
            "response": "Resolved"
          }
        ]
      }
    }
  ]
}
```
