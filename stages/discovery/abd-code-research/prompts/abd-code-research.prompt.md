---
name: abd-code-research
description: Survey a codebase in two passes — Explorer (research paths + source notes) then Deep Dive (one deep-dive file per path) — to produce structured research that primes abd-architecture-outline, abd-architecture-blueprint, and abd-architecture-specification.
---

Read the skill at `../skills/abd-code-research/SKILL.md` and follow it to survey the codebase.

**Pass 1 — Explorer**
- Map folder structure, identify entry points, scan significant files
- Name 5–10 research paths with concern kind, technology, and file evidence
- Capture verbatim source excerpts with file path + line range
- Produce: `code-research/agent-1-explorer/research-paths.md` and `sources.md`

**Pass 2 — Deep Dive**
- Follow each research path in depth
- Extract principles, file structure, participants, flow, and a walkthrough example
- Produce: `code-research/agent-2-deep-dive/<path-name>.md` per path

If the user provides a custom folder name (e.g. `coh-research/`), use that instead of `code-research/`.
