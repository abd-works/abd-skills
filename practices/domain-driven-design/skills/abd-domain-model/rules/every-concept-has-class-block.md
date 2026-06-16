# Rule: Every concept has a class block

**Scanner:** Manual review

A passing model has one `### **ClassName**` block for every concept listed in the Domain Language. No concept is silently dropped and no class is invented without UL backing. A failing model omits UL concepts or introduces classes that have no corresponding UL entry.

## DO

If the Domain Language lists: Ticket, Stage, Agent, Skill, Board

```markdown
### **Ticket**
...

### **Stage**
...

### **Agent**
...

### **Skill**
...

### **Board**
...
```

Every UL concept has a block. Every block traces to a UL concept.

## DO NOT

Silently dropping a concept:

```markdown
### **Ticket**
...

### **Stage**
...

### **Board**
...
```

Where are `Agent` and `Skill`? They were in the UL but have no block.

Inventing a class without UL backing:

```markdown
### **TicketProcessor**
...
```

If `TicketProcessor` does not appear in the Domain Language, it must not appear in the model.

**Source:** Engagement convention (domain-model skill).
