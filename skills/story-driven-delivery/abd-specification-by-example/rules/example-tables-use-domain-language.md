---

---

# Rule: Example tables use domain language (outline template)

This rule applies to **`specification-by-example-outline.md`** — scenarios that use example tables. It does not apply to plain scenarios, which use inline values instead.

Example tables ground an outline in domain data: column names follow the domain model, values are concrete and meaningful, and tables connect to steps through the matching `{column_name}` tokens.

## DO

- Name each table after a domain concept; columns are attributes of that concept, not UI labels.
- Use domain terminology consistent with the model (Recipient, PaymentAmount — not "dropdown value").
- Omit surrogate ID columns when they add no specification value.
- When the scenario computes a report or aggregate, show the inputs that justify the output — not just counts.

```text
Recipient:
| recipient_name | recipient_status |
| Global Supply  | Active           |
``
## DON'T

- Build tables around UI controls (`button_enabled`, `modal_visible`) when the story is about domain outcomes.
- Encode only aggregated outputs (`renames_count: 1`) for the scenario responsible for producing that aggregate — show the underlying entities.

```text
# WRONG — UI columns
| dropdown_selection | checkbox_state |

# WRONG — only counts when this scenario builds the report
| renames_count | new_count |
| 1             | 2         |
``