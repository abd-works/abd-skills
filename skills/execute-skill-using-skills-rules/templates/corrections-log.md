# Corrections log — structure

**Canonical spec:** The field table and snippets below are the **single** definition for corrections — [**SKILL.md**](../SKILL.md) **What you can do → item 4** links here instead of duplicating the table.

**Purpose:** During review, **do not edit skill sources** until the **correct output** is confirmed. Record each problem here first; complete **item 4 — fix the output** before **item 4 — fix the skill**. Full narrative: [**SKILL.md**](../SKILL.md) item 4.

---

## Where to create the file

- Under **`active_skill_workspace`** from **`skill-config.json` → `workspace`** (engagement / project tree).
- **Not** inside the skill install directory.

**Example paths** (pick one convention per engagement):

- `docs/corrections-log.md`
- `.skill-builder/corrections-log.md`

---

## One entry per problem — fields

| Field | Content |
| --- | --- |
| **Rule** | Rule id or `rules/<file>.md` name |
| **Affects** | Scope where this correction applies, as a short mapping: `stage:`, `story:`, `rule:`, optional `slice:`, `run:`, `role:`. At least one value is required. Use `stage: *` / `story: *` for global. This is what the delivery lead filters on before surfacing entries to a team member. |
| **DO / DO NOT** | **Forward-looking:** the behavior to apply from now on (prefer clear **DO**). Put the historical mistake only in **Example (wrong)** — do not let this field be mostly "do not do what we did before." |
| **Example (wrong)** | What the output actually did |
| **Example (correct)** | What it should have done — fill **only after** the right output is confirmed |
| **Scanner or validator** | If applicable: **`scanner:`** in rule frontmatter, **`scanners/...-scanner.py`**, or host **`build.build_pipeline`** step |
| **Likely source** | One of: `prompt gap` · `rule not read` · `edge case` · `automation gap` |

**Duplicate violations:** If the **same guidance** was violated again, add another **Example (wrong)** under the **same entry** instead of opening a new entry.

---

## Phrasing (altered behavior, not the negative case)

- **DO / DO NOT** and any text you later promote into **`rules/`** or **`SKILL.md`** should read like **maintainable guidance**: what the next run should **do** or **check**, tied to artifacts when possible.
- **Example (wrong)** is the right place for what went wrong once. Avoid encoding that failure as the **primary** normative line (e.g. filling **DO / DO NOT** with "never open with a paragraph about workshops" instead of "open **## DO** with scope: `impact-map.md` and `impact-map.txt`").
- **Example (correct)** should mirror that positive shape once the output is fixed.

**Wrong vs right (phrasing):**

| Wrong | Right |
| --- | --- |
| **DO NOT:** Do not paste meta saying "this is not facilitation." | **DO:** First normative heading is **## DO**; bullets name the file and checks. |
| **DO NOT:** Stop writing rules about process. | **DO:** Each **DO** is decidable from the named artifact (see target authoring skill). |

**Scope (`Affects`) — how it's used:**

- The **delivery lead** reads the log before every run and handoff. It surfaces to the active **team member** only entries whose **Affects** intersects the current stage, current run scope (slice / story), or the role being bootstrapped.
- **Team members** must still read the file, but the lead is responsible for flagging the entries it expects to apply. Missing `Affects` means the lead cannot filter — leave it empty only when the correction truly is cross-cutting, and then set `stage: *` / `story: *` explicitly.
- **Stages** values map 1:1 to `agents/abd-delivery-lead/stages/<stage>.md`: `discovery`, `prioritization`, `exploration`, `scenarios`, `acceptance-tests`, `engineering`.
- **Roles** values: `product-owner`, `analyst`, `engineer`.

---

## Markdown shape (whole file)

Use a heading per entry; keep a **Status** line so you know if the **output** phase (item 4) is done for that entry.

```markdown
# Corrections log

Engagement: <name or path>
Skill / phase: <what was being reviewed>

---

## Entry: <short label>

- **Status:** open | confirmed
- **Rule:** `rules/<stem>.md` or rule id
- **Affects:**
  - stage: <one of discovery | prioritization | exploration | scenarios | acceptance-tests | engineering | `*`>
  - story: <story id or verb-noun name, or `*`>
  - slice: <slice/increment name, optional>
  - run: <run label from agile-delivery-plan.md, optional>
  - role: <product-owner | analyst | engineer, optional>
  - rule: <rule id if narrower than Rule above, optional>
- **DO / DO NOT:** <plain statement>
- **Example (wrong):**
  <what the model or artifact did>
- **Example (correct):**
  <leave blank until confirmed; then fill>
- **Scanner or validator:** <e.g. `scanners/foo-scanner.py` or `build.build_pipeline[1]`>
- **Likely source:** prompt gap | rule not read | edge case | automation gap

---

## Entry: <next problem>

...
```

---

## Single entry — copy-paste snippet

```markdown
## Entry: <label>

- **Status:** open
- **Rule:**
- **Affects:**
  - stage:
  - story:
  - slice:
  - run:
  - role:
  - rule:
- **DO / DO NOT:**
- **Example (wrong):**
- **Example (correct):**
- **Scanner or validator:**
- **Likely source:**

```

When the regenerated output is right: set **Status** to **confirmed**, fill **Example (correct)**, then you may promote fixes in **item 4 — fix the skill** (sources + **`bundle_rules_into_skill_md.py`** / full validation).

---

## Wrong vs right (process)

| Wrong | Right |
| --- | --- |
| Log a problem and **immediately** edit **skill sources** or **`rules/`** before output is validated | Log → re-generate → iterate on **output** until correct → then fill **Example (correct)** |
| Patch **Bundled rules** or **`AGENTS.md`** to “pass” review | Edit **`rules/`** (and other sources as needed), run **`bundle_rules_into_skill_md.py`**; use the target repo’s own merge only if it maintains **`AGENTS.md`** / **`built/`** |
| **DO / DO NOT** repeats the mistake as the main instruction | **DO / DO NOT** states **altered behavior**; mistake stays in **Example (wrong)** only |
