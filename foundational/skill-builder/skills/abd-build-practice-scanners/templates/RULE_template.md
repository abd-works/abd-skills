<!--
  Typical rule file for agilebydesign-skills.
  Copy to skills/<your-skill>/rules/<rule-slug>.md and replace every {{PLACEHOLDER}}.

  Bundle rule prose into the skill’s SKILL.md (between execute-skill-using-skills-rules markers) with:
    python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/<your-skill>

  Conventions (match skills/abd-story-mapping and skills/abd-acceptance-criteria):
  - One rule per file; slug is the filename stem (kebab-case).
  - Optional YAML frontmatter below; omit the whole block if unused.
  - Body uses ATX headings: # Rule title, ## DO, ## DON'T (bundle demotes headings when inlining).
  - Put long examples in fenced code blocks (```gherkin, ```text, etc.).
-->

---
# Optional frontmatter — delete unused keys or omit entire --- block.
scanner: {{OPTIONAL_SCANNER_ID_OR_SCRIPT_NAME}}
---

# Rule: {{RULE_TITLE}}

{{One short paragraph: what this rule enforces, for whom, and why it matters in context.}}

## DO

- {{Concrete, testable guidance}}
- {{Concrete, testable guidance}}

```{{language}}
{{Minimal good example}}
```

## DON'T

- {{Named anti-pattern}}
- {{Named anti-pattern}}

```{{language}}
{{Minimal contrast example (WRONG vs CORRECT)}}
```
