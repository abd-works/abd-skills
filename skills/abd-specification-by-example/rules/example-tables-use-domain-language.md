# Rule: Example tables use domain language

Example tables ground scenarios in **domain** data: column names follow the model, values are concrete and meaningful, and tables connect to steps through **concept names** and collaboration language (e.g. “owned by enterprise”). Prefer **source** rows that explain an outcome over bare counts or flags that hide what was renamed, added, or removed—unless this scenario only **consumes** a result produced upstream.

## DO

- Name each table after a **domain concept**; columns are **attributes** of that concept, not UI labels.
- Omit implementation-only ID columns when they add no specification value; relate concepts with readable columns and table ordering / collaboration phrasing.
- When the scenario **computes** a report or aggregate, show the **inputs** (renamed rows, new rows) that justify the output—not only `renames_count = 1`.
- Use domain terminology consistent with the model (Recipient, BeneficiaryBank, PaymentAmount—not “dropdown value”).

```text
Recipient (creates() from Enterprise):
| recipient_name | recipient_status |
| Global Supply  | Active           |
```

## DON'T

- Build tables around UI controls (`button_enabled`, `modal_visible`) when the story is about domain outcomes.
- Use disconnected “lookup” layouts that force readers to mentally join unrelated tables when a parent/child structure is part of the domain.
- Encode only aggregated outputs (`renames_count`, `reflects_additions: true`) for the scenario that is **responsible** for producing those aggregates—show the underlying entities unless the scenario only applies someone else’s report.

```text
# WRONG — UI-ish columns
| dropdown_selection | checkbox_state |

# WRONG — only counts when this scenario builds the report
| renames_count | new_count |
| 1             | 2         |
```
