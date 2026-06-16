# Rule: Slash terms resolved before model

**Scanner:** Manual review

A passing model contains no `A / B` slash terms in any heading, property name, or method name. Every slash term from the Domain Language has been resolved to a single concept before modeling begins. A failing model carries unresolved slash terms forward into class names, properties, or methods.

## DO

UL had `Skill / Practice` as an unresolved term. Before modeling, resolve it:

Decision: "Skill" is the runtime capability an agent has. "Practice" is the body of knowledge a skill draws from. They are separate concepts.

```markdown
### **Skill**

Skill(SkillName)
------
name: SkillName
----
execute(Context): Outcome

### **Practice**

Practice(PracticeName)
------
name: PracticeName
skills: Skill
```

## DO NOT

Carrying slash terms into the model:

```markdown
### **Skill / Practice**

Skill / Practice(Name)
------
name: Name
```

Or embedding them in properties:

```markdown
------
skill/practice: SkillPractice
```

Or in method names:

```markdown
----
assign_skill/practice(Agent): Assignment
```

**Source:** Engagement convention (domain-model skill).
