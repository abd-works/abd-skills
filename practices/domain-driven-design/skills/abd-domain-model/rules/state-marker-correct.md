# Rule: State marker correct

**Scanner:** Manual review

A passing file declares `state: domain-model` in its YAML front matter. A failing file uses any other state value — `crc`, `domain-language`, `class-model`, or omits the field entirely.

## DO

```yaml
---
state: domain-model
---
```

## DO NOT

```yaml
---
state: domain-model
---
```

```yaml
---
state: domain-language
---
```

```yaml
---
state: class-model
---
```

**Source:** Engagement convention (domain-model skill).
