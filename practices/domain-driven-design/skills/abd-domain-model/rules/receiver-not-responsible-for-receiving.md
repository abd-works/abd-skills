# Rule: Receiver not responsible for receiving

**Scanner:** Manual review

A passing model places the method on the actor that performs the action, not on the receiver of the action. The receiver appears as a parameter or collaborator. A failing model puts the action on the target — making the receiver responsible for being acted upon.

## DO

"The lead assigns an agent to a ticket."

The lead is the actor. The method lives on the lead:

```markdown
### **KanbanLead**

----
assign(Ticket, Agent): Assignment
	Agent
	Ticket
```

Ticket and Agent are receivers — they appear as parameters.

## DO NOT

Putting the action on the receiver:

```markdown
### **Ticket**

----
beAssigned(Agent): Ticket
```

```markdown
### **Agent**

----
receiveAssignment(Ticket): Assignment
```

The ticket is not responsible for being assigned. The agent is not responsible for receiving an assignment. The actor (KanbanLead) performs the action.

**Source:** Engagement convention (domain-model skill).
