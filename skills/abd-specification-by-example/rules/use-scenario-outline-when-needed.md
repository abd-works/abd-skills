# Rule: Use scenario outline when the story needs data variation

Use a **Scenario Outline** with **Examples** when the **same** steps apply across multiple rows: calculations, fee tables, boundary sweeps, or named entity variations. Prefer separate **Scenario**s when setups differ materially, business meaning diverges, or you only have **one** row.

## DO

- Outline **formula-like** or **table-driven** behavior (inputs → outputs) with a concise Examples block.
- Keep placeholders in steps consistent with Examples column headers.

```gherkin
Scenario Outline: Modifier depends on rank
  Given ability rank <rank>
  When modifier is calculated
  Then modifier is <modifier>

  Examples:
    | rank | modifier |
    | 10   | 0        |
    | 12   | +1       |
```

## DON'T

- Wrap a single concrete path in an outline with one Examples row—use a normal **Scenario**.
- Use outlines when scenarios need different **Given** contexts that are clearer as separate scenarios.

```gherkin
# WRONG — outline adds noise for one row
Scenario Outline: User saves profile
  Examples:
    | name |
    | Jane |
```
