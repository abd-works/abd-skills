# abd-skill-builder — Component Overview

This document shows the structural parts of an `abd-skill-builder` skill and how they interact at build time and run time.

---

## Component Structure

```
skill-root
Entry point — agent discovery (SKILL.md) and assembled agent instructions (AGENTS.md)
│
├── ┌─────────────────────────────────────────────────────┐
│   │  conf                                               │
│   │  Run time settings (e.g. the current workspace)    │
│   └─────────────────────────────────────────────────────┘
│
├── ┌─────────────────────────────────────────────────────┐
│   │  content                                            │
│   │  All instructional content; source parts and built  │
│   └─────────────────────────────────────────────────────┘
│   ├── ┌─────────────────────────────────────────────────┐
│   │   │  parts                                          │
│   │   │  Files here are merged into AGENTS.md           │
│   │   └─────────────────────────────────────────────────┘
│   │   ├── ┌─────────────────────────────────────────────┐
│   │   │   │  phases/                                    │
│   │   │   │  One file per phase; procedure, steps,      │
│   │   │   │  checklist                                  │
│   │   │   └─────────────────────────────────────────────┘
│   │   └───┌─────────────────────────────────────────────┐
│   │       │  library/                                   │
│   │       │  Cross-cutting definitions and norms        │
│   │       │  reused across phases; one file per topic   │
│   │       └─────────────────────────────────────────────┘
│   └── ┌─────────────────────────────────────────────────┐
│       │  built                                          │
│       │  (static mode only) Pre-generated phase slices  │
│       │  from build.py; not hand-edited                 │
│       └─────────────────────────────────────────────────┘
│
├── ┌─────────────────────────────────────────────────────┐
│   │  rules/                                             │
│   │  Normative constraints; one .md per rule +          │
│   │  optional scanners.json                             │
│   └─────────────────────────────────────────────────────┘
│
├── ┌─────────────────────────────────────────────────────┐
│   │  scripts/                                           │
│   │  Build AGENTS.md, generate phase prompts,          │
│   │  scaffold new skills, set active workspace         │
│   └─────────────────────────────────────────────────────┘
│
├── ┌─────────────────────────────────────────────────────┐
│   │  templates/                                         │
│   │  Structured output templates the AI uses to         │
│   │  generate consistent skill artifacts                │
│   └─────────────────────────────────────────────────────┘
│
└── ┌─────────────────────────────────────────────────────┐
    │  test/                                              │
    │  Automated verification fixtures and suites         │
    └─────────────────────────────────────────────────────┘
```

---

## Capability Design

Each section below describes a problem with generic AI instruction approaches, the solution this skill pattern provides, and a simple diagram of how the pieces interact.

---

### Prompt Generation and Injection

**Problem — Command drift**
Generic AI chat has no stable frame of reference. The model can run the wrong commands, invoke the wrong skill, address the wrong part of a workflow, or silently drop key supporting concepts even when links are present. Skills as flat instruction files don't scale with complexity — the more you add, the more the model loses track.

**Solution**
The CLI drives context-scoped prompt assembly. The user or agent names a phase; the script pulls only the parts relevant to that phase and injects them directly into the AI context. The model receives exactly what it needs, nothing more.

```
┌──────────┐   phase name   ┌──────────────┐   assembled prompt   ┌──────────┐
│   User   │ ─────────────► │ generate.py  │ ──────────────────► │  AI Chat │
│  / Agent │                │  (scripts/)  │                      │          │
└──────────┘                └──────────────┘                      └──────────┘
                                    │
                       pulls from   │
                                    ▼
                        ┌──────────────────────┐
                        │  content/parts/      │
                        │  phases/  library/   │
                        └──────────────────────┘
```

---

### Rules and Scanners

**Problem — Silent violations**
AI models produce output that looks correct but breaks structural or naming conventions. Manual review is slow and inconsistent. Without machine-checkable constraints, standards drift silently across iterations.

**Solution**
Each rule is a markdown file with normative prose the model reads AND a scanner entry that can be run automatically. The model aligns to the rule text; the scanner catches what the model misses.

```
┌──────────────┐   read at prompt time   ┌──────────────────┐
│  rules/*.md  │ ──────────────────────► │  AI follows      │
│  (prose)     │                         │  rule text       │
└──────────────┘                         └──────────────────┘

┌──────────────┐   run after output      ┌──────────────────┐
│ scanners.json│ ──────────────────────► │  Automated check │
│  (checks)    │                         │  flags violation │
└──────────────┘                         └──────────────────┘
```

---

### Correction Approach

**Problem — Problems that slip through**
The user notices something wrong in the output — the AI missed a constraint, the prompt was ambiguous, or there is no rule or scanner that would have caught it. Without a structured way to record these, the same problems recur and fixes stay in the user's head.

**Solution**
When a problem is spotted, record it: what went wrong, which rule or scanner should have caught it (or that none exists), and what the fix is. These records accumulate into a backlog the user can work through to propose new rules, scanner additions, or prompt corrections.

```
┌──────────────────────┐     user spots problem     ┌─────────────────────────┐
│  AI output           │ ─────────────────────────► │  Problem log entry      │
│  (has a mistake)     │                            │  - what went wrong      │
└──────────────────────┘                            │  - rule/scanner missed? │
                                                    │  - or: none exists yet  │
                                                    │  - suggested fix        │
                                                    └────────────┬────────────┘
                                                                 │
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │  Improvement backlog    │
                                                    │  new rule / scanner /   │
                                                    │  prompt correction      │
                                                    └─────────────────────────┘
```

---

### Phases and Process

**Problem — No workflow structure**
Without phases, the AI treats every request as isolated. Context built in one step is lost in the next. Large skills become unmanageable single-prompt instructions.

**Solution**
Work is broken into named phases, each with its own procedure, inputs, outputs, and checklist. `process.md` defines the sequence. The model operates one phase at a time with the right context injected for each.

```
┌─────────────┐   defines   ┌────────────────────────────────────┐
│ process.md  │ ──────────► │  Phase 1 → Phase 2 → Phase 3 → …  │
└─────────────┘             └────────────────────────────────────┘
                                      │ each phase
                                      ▼
                              ┌───────────────────┐
                              │  phases/<slug>.md │
                              │  procedure + steps│
                              │  + checklist      │
                              └───────────────────┘
```

---

### Parts, Built, and Library Files

**Problem — Monolithic instruction files**
A single large instruction file is hard to maintain, impossible to version by topic, and causes the model to lose focus. Changes in one area ripple unpredictably.

**Solution**
Content is split into composable parts. `library/` holds cross-cutting norms reused across phases. `phases/` holds phase-specific procedure. `built/` holds pre-assembled slices (static mode) so no assembly is needed at runtime.

```
┌──────────────────┐                  ┌─────────────────────┐
│  library/*.md    │ ── injected ───► │                     │
│  (shared norms)  │                  │  Assembled prompt   │
└──────────────────┘                  │  for this phase     │
                                      │                     │
┌──────────────────┐                  └─────────────────────┘
│  phases/<slug>   │ ── injected ───►          ▲
│  (phase body)    │                           │  OR (static mode)
└──────────────────┘               ┌───────────────────────┐
                                   │  built/<slug>.md      │
                                   │  pre-generated slice  │
                                   └───────────────────────┘
```

---

### Templates

**Problem — Inconsistent AI output structure**
Without a fixed output shape, the AI invents its own format every time. Downstream scripts and humans cannot rely on predictable artifact layouts.

**Solution**
Templates define the exact structure the AI must follow for each artifact type. The model fills in the template; the shape is guaranteed.

```
┌─────────────────────┐   structure contract   ┌──────────────────────┐
│  templates/*.md     │ ─────────────────────► │  AI generates output │
│  (output shape)     │                        │  matching template   │
└─────────────────────┘                        └──────────────────────┘
```

---

### Step Checklist

**Problem — Lost progress and incomplete phases**
Long AI sessions get interrupted. Without a record of what was done, the model restarts from scratch or skips steps it thinks are complete.

**Solution**
Each phase file contains a `- [ ]` / `- [x]` checklist. The first unchecked box is always the resume point. Progress survives interruptions.

```
┌──────────────────────────────────────────┐
│  phases/<slug>.md                        │
│  - [x] Step 1 — done                    │
│  - [x] Step 2 — done                    │
│  - [ ] Step 3 — resume here  ◄───────── │── agent reads, continues
│  - [ ] Step 4                            │
└──────────────────────────────────────────┘
```

---

### Scripts and Tests

**Problem — Manual assembly and unverified outputs**
Hand-assembling prompts is error-prone. Without automated tests, regressions in skill structure or scanner behaviour go undetected.

**Solution**
Scripts automate every repeatable operation: building AGENTS.md, generating phase prompts, scaffolding new skills, setting the active workspace. Tests verify that the assembled outputs and scanners behave as specified.

```
┌──────────────────────────────────────┐   runs    ┌────────────────────┐
│  scripts/                            │ ────────► │  Repeatable ops    │
│  build · generate · scaffold · conf  │           │  no manual steps   │
└──────────────────────────────────────┘           └────────────────────┘

┌──────────────────────────────────────┐ verifies  ┌────────────────────┐
│  test/                               │ ────────► │  Structure, rules, │
│  fixtures and suites                 │           │  scanner behaviour │
└──────────────────────────────────────┘           └────────────────────┘
```

---
