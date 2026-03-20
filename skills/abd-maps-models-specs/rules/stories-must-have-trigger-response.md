---
title: Stories Must Have Trigger and Response
impact: HIGH
tags: [step2, step3, step5, step6, interaction, stories]
scanner: scanners/stories_have_trigger_response.py
---

## Every Story Must Have Trigger and Response

**DO** ensure every story has `trigger` (Actor + action) and `response` (system or other actor). Ground in `**Concept**` where domain concepts participate.

**DO NOT** leave a story with only a name. Trigger and response ground the story in domain and connect it to the story map.

- Right: `trigger: "**Player** rolls d20 for **Check**"`, `response: "**System** returns **Degree**"`
- Wrong: Story with only `name` and no trigger/response
