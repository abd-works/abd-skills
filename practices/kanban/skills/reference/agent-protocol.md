
# Kanban — Agent Protocol

Read this file when any kanban practice skill tells you to. It defines the three conventions shared by all skills in this family.

---

## Output file resolution (deliverables)

**Canonical layout:** [../../reference/artifact-layout.md](../../reference/artifact-layout.md) — **read before every write**.

| Stage | Where to write |
| --- | --- |
| Shaping | `<workspace>/docs/end-to-end/shaping/` |
| Discovery | `<workspace>/docs/end-to-end/discovery/` |
| Exploration → Engineering (active increment) | `<workspace>/docs/increments/<n>-<slug>/{exploration,specification,engineering}/` |
| After increment archived | Merge into `<workspace>/docs/end-to-end/{exploration,specification,engineering}/` |

**`docs/end-to-end/`** has **one subfolder per stage**. **`shaping/`**, **`specification/`**, and **`engineering/`** are flat inside. **`discovery/`** and **`exploration/`** use four concern subfolders each (`domain/`, `stories/`, `ux/`, `architecture/`). Shaping and discovery fill directly; exploration/spec/engineering fill as increments roll up. See [artifact-layout.md](../../reference/artifact-layout.md).

**War room:** `<workspace>/docs/planning/delivery-war-room/` only.

Resolution order: user path → artifact-layout.md → practice skill default.

---

## Read-gates

Before authoring any artifact:

- Read **[artifact-layout.md](../../reference/artifact-layout.md)** for the ticket's stage and increment.
- Read every file in **`reference/`** and **`rules/`** for the active skill.

---

## Per-rule verdict format (validation)

After generating, re-read every file in **`rules/`** for the active skill. For **each rule**, emit:

```
Rule: <rule-filename>  ->  PASS
Rule: <rule-filename>  ->  FAIL  <offending line or reason>
```

**No rule may be silently skipped.** Fix every FAIL and every scanner violation before calling the work done.
