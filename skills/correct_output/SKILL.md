---
name: correct-output
catalog_garden_tier: foundational
catalogue_one_liner: >-
  Fix the deliverable first, log corrections, iterate until right — only then improve the source.
description: >-
  After something is wrong with generated output, follow the correction process: fix the output
  first, log problems, iterate until correct, then optionally improve whatever produced it.
---

# correct-output

## Purpose

This skill governs **what to do when generated output is wrong**. The core principle is **output first, source second**: fix the artifact the user cares about before changing whatever produced it.

It works regardless of whether the output came from a skill with rules, a prompt, a pipeline, or anything else.

## When to use this skill

Load this skill when:

- Generated output has a **problem** — wrong shape, missing content, violated expectation, or reviewer feedback.
- You need a **structured loop** for iterating on broken output instead of ad-hoc guessing.
- The user says things like "that's wrong," "fix this," "correct the output," or "run the correction process."

## Instructions

### Where the corrections log lives (on disk — not chat)

- Use the **corrections ledger in the repository you are actually editing** (the engagement / deliverable repo).
- If that repo **already** has a log, **append there** (example: **`abd-ooad/corrections-log.md`** in some engagements).
- If there is **no** log yet, create **`corrections-log.md` at the root of that repository**, started from **[templates/corrections-log.md](./templates/corrections-log.md)**.
- **Mandatory:** Write the entry **on disk in the same turn** as you address the problem. **Chat is not the system of record.**
- **Process corrections** count: user fixes how you work (norms, additive rules, what to log) → **log those too** in that same file.

There is **no** dependency on `AGENTS.md`; path is **either** an existing ledger in the repo **or** repo-root `corrections-log.md`.

### Fix the output — iterate until the deliverable is right

Do **not** jump to changing whatever produced the output. Keep the **deliverable** right first.

1. **Identify** — Note the problem; open the **on-disk** corrections log for this project (see **Where the corrections log lives** above).

2. **Log (initial)** — **Append** an entry: **DO / DO NOT** + **Example (wrong)**; leave **Example (correct)** blank until you are done iterating. **Phrasing:** Write **DO / DO NOT** as **altered behavior** — what to do next — not as a long restatement of the mistake. **Example (wrong)** carries the failure; normative text should stay **forward-looking** (see **[templates/corrections-log.md](./templates/corrections-log.md)** **Phrasing**).

3. **Re-generate** — Apply the correction explicitly; expect **multiple turns** before the output is good enough.

4. **Review** — Refine the deliverable and log notes as you go; repeat until you are **actually satisfied**, not after the first fix attempt.

5. **Confirm** — Only then fill **Example (correct)** and mark the entry done.

### Improve the source — only when the user asks

Once the output is right and the log has entries, the user may ask you to fix whatever caused the problems. This is a **separate, user-initiated** step — never do it automatically.

When the user says "fix the source," "correct what caused this," or similar:

1. Read the corrections log as a **set** — all logged entries, not just the latest.
2. Find **root causes** (missing instruction, vague wording, edge case, wrong assumption, etc.).
3. **Propose** a set of suggested fixes. Do **not** implement them — present them and wait.
4. Only implement when the user explicitly tells you to proceed.

What "the source" is depends on context:

- A skill with `rules/` → propose edits to `rules/*.md`, re-bundle / re-validate.
- A prompt or template → propose changes to that prompt or template.
- Code that generated the output → propose code changes.
- Nothing formal → the log itself is the record; no source to fix.

---

## Corrections log — field reference

Each entry in the log uses these fields:

| Field | Content |
| --- | --- |
| **Context** | What produced the output (skill name, prompt, pipeline, etc.) — or omit if obvious |
| **DO / DO NOT** | **Forward-looking:** the behavior to apply from now on. Put the historical mistake only in **Example (wrong)**. |
| **Example (wrong)** | What the output actually did |
| **Example (correct)** | What it should have done — fill **only after** the right output is confirmed |
| **Likely source** | One of: `prompt gap` · `instruction not read` · `edge case` · `automation gap` · `unclear expectation` |

**Duplicate violations:** If the **same guidance** was violated again, add another **Example (wrong)** under the **same entry** instead of opening a new entry.

---

## Phrasing (altered behavior, not the negative case)

- **DO / DO NOT** should read like **maintainable guidance**: what the next run should **do** or **check**.
- **Example (wrong)** is the right place for what went wrong once. Avoid encoding that failure as the **primary** normative line.
- **Example (correct)** should mirror that positive shape once the output is fixed.

| Wrong | Right |
| --- | --- |
| **DO NOT:** Do not paste meta saying "this is not facilitation." | **DO:** First normative heading is **## DO**; bullets name the file and checks. |
| **DO NOT:** Stop writing rules about process. | **DO:** Each **DO** is decidable from the named artifact. |

---

## Wrong vs right (process)

| Wrong | Right |
| --- | --- |
| See a problem and **immediately** edit sources / rules / prompts | Log the problem, fix the **output**, move on |
| Automatically analyze root causes and propose source fixes | Wait until the user explicitly asks to improve the source |
| Implement proposed fixes without user approval | Present suggestions, wait for go-ahead |
| **DO / DO NOT** repeats the mistake as the main instruction | **DO / DO NOT** states **altered behavior**; mistake stays in **Example (wrong)** only |
| Declare "fixed" after one attempt | Iterate until **actually satisfied** — multiple turns are normal |

---

## Templates

- [**corrections-log.md**](./templates/corrections-log.md) — Field definitions and copy-paste snippet for new entries.