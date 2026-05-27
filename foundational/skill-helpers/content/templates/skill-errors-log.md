# Corrections log — structure

**Purpose:** When output is wrong, **do not edit the source** until the **correct output** is confirmed. Record each problem here first; complete the **fix the output** loop before the optional **improve the source** step. Full narrative: `skill-helpers/instructions/log-and-fix-skill-errors.instructions.md`.

---

## Where to create the file

- In the project or engagement workspace — wherever the output lives.
- **Not** inside the skill or tool that produced the output.

**Example paths** (pick one convention per project):

- `docs/skill-errors-log.md`
- `logs/skill-errors-log.md`
- `.corrections/skill-errors-log.md`

---

## One entry per problem — fields

| Field | Content |
| --- | --- |
| **Context** | What produced the output (skill name, prompt, pipeline, etc.) — omit if obvious from the file location |
| **DO / DO NOT** | **Forward-looking:** the behavior to apply from now on (prefer clear **DO**). Put the historical mistake only in **Example (wrong)** — do not let this field be mostly "do not do what we did before." |
| **Example (wrong)** | What the output actually did |
| **Example (correct)** | What it should have done — fill **only after** the right output is confirmed |
| **Likely source** | One of: `prompt gap` · `instruction not read` · `edge case` · `automation gap` · `unclear expectation` |

**Duplicate violations:** If the **same guidance** was violated again, add another **Example (wrong)** under the **same entry** instead of opening a new entry.

---

## Phrasing (altered behavior, not the negative case)

- **DO / DO NOT** should read like **maintainable guidance**: what the next run should **do** or **check**, tied to artifacts when possible.
- **Example (wrong)** is the right place for what went wrong once. Avoid encoding that failure as the **primary** normative line (e.g. filling **DO / DO NOT** with "never open with a paragraph about workshops" instead of "open **## DO** with scope: `impact-map.md` and `impact-map.txt`").
- **Example (correct)** should mirror that positive shape once the output is fixed.

| Wrong | Right |
| --- | --- |
| **DO NOT:** Do not paste meta saying "this is not facilitation." | **DO:** First normative heading is **## DO**; bullets name the file and checks. |
| **DO NOT:** Stop writing rules about process. | **DO:** Each **DO** is decidable from the named artifact (see target authoring skill). |

---

## Markdown shape (whole file)

Use a heading per entry; keep a **Status** line so you know if the output phase is done for that entry.

```markdown
# Corrections log

Project: <name or path>
Source: <what produced the output, if useful>

---

## Entry: <short label>

- **Status:** open | confirmed
- **Context:** <skill / prompt / pipeline — omit if obvious>
- **DO / DO NOT:** <plain statement>
- **Example (wrong):**
  <what the output actually did>
- **Example (correct):**
  <leave blank until confirmed; then fill>
- **Likely source:** prompt gap | instruction not read | edge case | automation gap | unclear expectation

---

## Entry: <next problem>

...
```

---

## Single entry — copy-paste snippet

```markdown
## Entry: <label>

- **Status:** open
- **Context:**
- **DO / DO NOT:**
- **Example (wrong):**
- **Example (correct):**
- **Likely source:**

```

When the regenerated output is right: set **Status** to **confirmed**, fill **Example (correct)**, then you may optionally improve the source (see `skill-helpers/instructions/log-and-fix-skill-errors.instructions.md` **Improve the source**).

---

## Wrong vs right (process)

| Wrong | Right |
| --- | --- |
| Log a problem and **immediately** edit sources before output is validated | Log → re-generate → iterate on **output** until correct → then fill **Example (correct)** |
| **DO / DO NOT** repeats the mistake as the main instruction | **DO / DO NOT** states **altered behavior**; mistake stays in **Example (wrong)** only |
