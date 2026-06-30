# Deep Dive: Diagram Sync & Template Writing

## Principles & Patterns

- **Templates with placeholder tokens**: skills like `drawio-story-sync` and `drawio-domain-sync` ship `.drawio` templates with `{TOKEN}` style placeholders that scripts fill in.
- **draw.io XML uses HTML entities**: newlines inside `<mxCell>` `value` attributes are encoded as `&#10;`. Other entities (`&amp;`, `&lt;`, `&quot;`) are used routinely.
- **Naive `str.replace` is dangerous**: when a template's surrounding XML contains entity-encoded characters, plain-text `.replace("{TOKEN}", "line1\nline2")` either no-ops (placeholder doesn't match) or produces invalid XML (raw `\n` injected next to `&#10;`).
- **No shared post-write verifier**: there is no `common/scripts/verify_no_placeholders_remain.py` helper. Each skill's `## Validate` block can include or omit such a check independently.

## File Structure

```
practices/story-driven-delivery/skills/supporting/drawio-story-sync/
├── SKILL.md
├── scripts/   (renderers; not fully read in this pass)
└── templates/

practices/domain-driven-design/skills/supporting/drawio-domain-sync/
├── SKILL.md
├── scripts/   (renderers; not fully read in this pass)
└── templates/

common/
└── scripts/   ← no verify_no_placeholders helper found
```

## Participants

| Component | Role |
|---|---|
| Per-skill renderer | Reads template; substitutes tokens; writes diagram file |
| draw.io XML template | Contains structure with `{TOKEN}` placeholders alongside HTML-entity-encoded content |
| *(missing) `common/scripts/verify_no_placeholders_remain.py`* | Would assert that the written file has no `{...}` tokens |
| Per-skill `## Validate` block | Currently omits any placeholder-absence check |

## Flow

**Risky flow (per session journal lines 135–139):**
1. Skill loads template containing `{ROUTE_LIST}` and `&#10;` (HTML-entity newline).
2. Skill computes a multi-line value: `"POST /mv/customer/cart\nPATCH /mv/customer/cart"`.
3. Skill runs `xml = xml.replace("{ROUTE_LIST}", value)`.
4. If the surrounding XML uses `&#10;` for newlines, the agent might have written the placeholder template with HTML-entity surroundings — the literal `{ROUTE_LIST}` does match, the `\n` in the replacement does NOT match the surrounding HTML entities, so the result is mixed/invalid.
5. Worse case (the one the journal documents): the agent encoded the value with HTML entities in the source template but used plain `\n` in the replacement — the substitution string contains raw `\n` characters, which draw.io renders as something else or rejects.
6. Worst case: the placeholder string in the template was itself written with entities and the literal placeholder in the replace call doesn't match — zero replacements, no exception.

**Safe flow (proposed in the journal):**
1. Build the entire XML string in memory using `xml.etree.ElementTree` or equivalent, with all content embedded by API (no string substitution).
2. Write the file.
3. Read it back. Assert `{` does not appear in the file content (no unfilled placeholders).
4. Fail fast if any are found.

## Walkthrough Example — pml-midtier session

Journal lines 135–139:

> **DO NOT** use simple string replacement (`str.replace`) to fill draw.io XML template placeholders. draw.io XML uses HTML entities (`&#10;` for newlines, `&amp;`, `&lt;`, etc.) and the literal placeholder strings in the template file will not match the plain-text strings in a Python replace call, causing all replacements to silently no-op — the file stays as a pure template with no error or warning.
> - Example (wrong): `xml = xml.replace("{ROUTE_LIST}", "POST /mv/customer/cart\nPATCH /mv/customer/cart")` — the `\n` never matches `&#10;` in the XML; zero replacements are made; no exception is raised.
> - Example (correct): Write the entire diagram XML directly with all content embedded. Do not rely on search-and-replace for XML template filling.

The countermeasure proposed by the journal:

> **Verify after every write:** After writing any diagram file, read it back and confirm that no `{...}` placeholder tokens remain. If any are found, raise an error — do not proceed silently.
> Example (correct verification): `assert '{' not in path.read_text(encoding='utf-8'), f"Unfilled placeholders remain in {path}"`

This pattern is generic: any template-write step that uses placeholder tokens should call a shared verifier. The session journal effectively spec'd `common/scripts/verify_no_placeholders_remain.py` without naming it.
