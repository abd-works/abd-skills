# Rule: State marker correct

**Scanner:** Manual review

A passing file declares `state: domain-model` in its YAML front matter. A failing file uses any other state value — `crc`, `domain-language`, `class-model`, or omits the field entirely.

## DO

```yaml
---
---
```

## DO NOT

```yaml
---
---
```

```yaml
---
---
```

```yaml
---
---
```

**Source:** Engagement convention (domain-model skill).
