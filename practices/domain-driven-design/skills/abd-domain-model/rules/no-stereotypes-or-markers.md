# Rule: No stereotypes or markers

**Scanner:** Manual review

A passing model uses plain class headings, simple domain types, and minimal notation. No UML stereotypes, no generic collection types, no visibility prefixes (except `-` for private), no interaction blocks, and no class description paragraphs. A failing model imports UML or domain-specification embellishments that the domain-model format does not use.

## DO

```markdown
### **Board**

Board(StageBucketLayout)
------
layout: StageBucketLayout
tickets: Ticket
----
advance(Ticket, Stage): Ticket
-validateWip(Stage): Stage
```

Plain heading. Inner domain type only (`Ticket`, not `List<Ticket>`). Private method marked with `-`. No extras.

## DO NOT

```markdown
### **Board** << Aggregate Root >>

A Board represents the central coordination point for ticket flow.

Board(StageBucketLayout)
------
+layout: StageBucketLayout
+tickets: List<Ticket>
+stageMap: Dictionary<StageName, Stage>
----
+advance(Ticket, Stage): Ticket

Initialisation:
  Creates default stage layout on construction.

Interaction:
  Board → StageBucketLayout: validates stage order
  Board → WipPolicy: checks capacity
```

Violations: `<< Aggregate Root >>` stereotype, class description paragraph, `+` visibility prefix, `List<Ticket>`, `Dictionary<StageName, Stage>`, `Initialisation:` block, `Interaction:` block.

**Source:** Engagement convention (domain-model skill).
