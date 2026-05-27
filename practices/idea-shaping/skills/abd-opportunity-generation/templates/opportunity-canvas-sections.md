# Opportunity canvas — section format (markdown)  

## Instructions  

- Fill the **Template** block: replace `{{placeholders}}` and write under each **line-prefix** so rules and parity still apply. **Do not** paste this Instructions block into deliverables.  
- Each **section** below names one row of the abd.works table (**`SKILL.md`**, page-46 style) and **embeds the guiding questions** for that row. The **`PREFIX:`** line is the machine-checkable field—keep it.  
- **Paired** **`opportunity-canvas.txt`**: same sections, same prefix lines, same content for the same engagement.  
- **Validated learning** (Kanban, `validate by:`): see **`SKILL.md`** and **`reference/canvas-pptx-extract.md`** slides 12–14.  

---  

## Template  

### Opportunity (bet handle)  

**OPPORTUNITY:** {{bet_name}}  

### Customer Problems  

What are our key customer segments and what are the unique requirements of each customer segment?  

**CUSTOMER_PROBLEMS:**    
{{segments_and_unique_requirements}}  

### Solution Features  

What is our Unique Value Proposition to our Customer Segments? What customer problem are we solving? What are the major features of our solution?  

**SOLUTION_FEATURES:**    
{{uvp_problem_and_major_features}}  

### Increments Of Value  

What are the increments of value we will deliver to our Customer Segments? What is the minimum valuable increment? In what order will value reach each segment?  

**INCREMENTS_OF_VALUE:**    
{{minimum_valuable_increment_and_delivery_order}}  

### Key Metrics of Success  

What are the key metrics that will tell us how our product is doing?  

**KEY_METRICS_OF_SUCCESS:**    
{{observable_measures_of_success}}  

### Revenue Drivers  

For what value are our Customers really willing to pay?  

**REVENUE_DRIVERS:**    
{{what_customers_really_pay_for}}  

### Key Activities and Resources  

What Key Activities does our Product Require (e.g. to Build, to Support, etc.)? What Key Resources [People] and Capabilities [Process] does our Product leverage?  

**KEY_ACTIVITIES_AND_RESOURCES:**    
{{activities_people_and_process}}  

### Key Partners  

Who are our Key Partners? Who are our key Suppliers?  

**KEY_PARTNERS:**    
{{partners_and_suppliers}}  

### Cost Drivers  

What are the most important costs drivers inherent in our Product?  

**COST_DRIVERS:**    
{{important_cost_drivers}}  

### Alternatives  

**ALTERNATIVES:**    
{{credible_alternatives_including_do_nothing_or_buy}}  

### Assumptions to validate  

**ASSUMPTION:** {{belief_that_could_be_wrong}} — validate by: {{who_what_when}}  

---  

## Example (reference)  

**Audience:** Fictional B2B scheduling example—follow **shape**, not these names.  

### Opportunity (bet handle)  

**OPPORTUNITY:** "Same-day" appointment guarantees for service bays  

### Customer Problems  

What are our key customer segments and what are the unique requirements of each customer segment?  

**CUSTOMER_PROBLEMS:**    
Segments: fleet coordinator (primary), dealer service manager, mobile technician, parts desk. Unique requirements: a confirmed slot and bay within the stated window; one place to see changes; evidence when a same-day promise breaks.  

### Solution Features  

What is our Unique Value Proposition to our Customer Segments? What customer problem are we solving? What are the major features of our solution?  

**SOLUTION_FEATURES:**    
UVP: reliable same-day service window the dealer can commit to. Customer problem: reschedules at short notice burn coordinator time and break tech routing. Major features: central calendar with real-time hold on bay + technician; opt-in push when the dealer moves the slot.  

### Increments Of Value  

What are the increments of value we will deliver to our Customer Segments? What is the minimum valuable increment? In what order will value reach each segment?  

**INCREMENTS_OF_VALUE:**    
DMS read-only feed (MVI); mobile push notifications; pilot in one region before broad rollout.  

### Key Metrics of Success  

What are the key metrics that will tell us how our product is doing?  

**KEY_METRICS_OF_SUCCESS:**    
Same-day job completion % by region; coordinator minutes per week on reschedules; penalty incidents per 100 jobs.  

### Revenue Drivers  

For what value are our Customers really willing to pay?  

**REVENUE_DRIVERS:**    
Penalties on missed SLAs in renewal accounts; coordinator labour cost savings; relationship to NPS/renewal rate.  

### Key Activities and Resources  

What Key Activities does our Product Require (e.g. to Build, to Support, etc.)? What Key Resources [People] and Capabilities [Process] does our Product leverage?  

**KEY_ACTIVITIES_AND_RESOURCES:**    
DMS integration and onboarding; runbooks; product + integration capacity; support during pilot.  

### Key Partners  

Who are our Key Partners? Who are our key Suppliers?  

**KEY_PARTNERS:**    
DMS vendor; two pilot dealers committed to the feed; field-service vendor if we later buy.  

### Cost Drivers  

What are the most important costs drivers inherent in our Product?  

**COST_DRIVERS:**    
Integration build and test; pilot support load; DMS test environments.  

### Alternatives  

**ALTERNATIVES:**    
Buy a field-service suite and retire custom integrations; one-region manual coordination pilot to prove pain before build.  

### Assumptions to validate  

**ASSUMPTION:** Dealers will expose a read-only DMS feed in M1 — validate by: signed integration plan with two pilot dealer IT leads  

**ASSUMPTION:** Technicians will enable location sharing during work hours — validate by: opt-in rate >70% in pilot  
