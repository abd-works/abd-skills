# Rule: Consolidate Superficial Stories

**Scanner:** Manual review (policy; pairs with *Review and Expand Stories* — see below)


Consolidate stories that differ **only superficially** (same logic, different data values or enumeration). Combine into **one parameterized story** where it applies.

**Relationship to other rules:** This rule removes **data-value duplication** (same behavior, different inputs). *Review and Expand Stories* splits by **component behavior**. Apply **consolidation first**, then expansion if you still need component-level depth.

## DO

- Merge stories that share the same validation logic but differ only by the value validated (e.g. six ability scores → one **`Assign Ability (STR, DEX, …)`** story).
- Merge stories that share the same calculation but differ only by attribute (e.g. multiple “calculate X modifier” → **`Calculate Ability Modifiers`**).
- Merge the same operation across entity types when only the type differs (e.g. create character / weapon / armor → **`Create Game Entity (types…)`**).

## DON'T

- Enumerate every permutation when logic is identical and only data changes — use one parameterized story (e.g. one **`Validate Input Format`** for email, phone, postal code).
- Split by data value when business rules are the same (e.g. separate add-book / add-electronics / add-clothing → **`Add Product`**).
- One story per status when the **workflow pattern** is the same — prefer one **`Update Order Status`** story with allowed values.
