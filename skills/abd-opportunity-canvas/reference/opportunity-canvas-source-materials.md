# Opportunity canvas — ABD source materials (extracts)

**Purpose:** The abd-answers RAG index mostly captured the generic “why / when” slide, not the **field-level** definition of the canvas. These notes ground the skill in **authoritative ABD assets** on disk.

## Source files (SharePoint / OneDrive)

| Role | Path |
|------|------|
| Visual **template** (eight labels on one slide) | `01 Agile Practices/4) Validated Learning/Supporting Material/Canvas/Opportunity Canvas Template.pptx` |
| **Training deck** (questions, flow, worked examples) | `02 Training/canvas.pptx` |

**Conversion:** `python convert_to_markdown.py --file <path>.pptx` (abd-answers `scripts/source-convert/`). The template was copied to a local temp path when OneDrive returned **Permission denied** on a direct read; the **02 Training** deck converted in place. Pipeline output mirrors: `data/assets/abd-answers-memory-pipeline/markdown/02 Training/canvas.md` (in **abd-answers** repo when conversion is run there).

---

## 1) Canonical ABD opportunity canvas (eight rows) — **authoritative structure**

**Normative copy:** the same eight sections and questions live in **`SKILL.md` → “Canonical ABD Opportunity Canvas (eight rows)”.** Fill-in output for agents and teams is **`templates/opportunity-canvas.md`**: **sections** with the **guiding questions** printed under each heading, then **`CUSTOMER_PROBLEMS:`** … **`COST_DRIVERS:`** (and `OPPORTUNITY:`, `ALTERNATIVES:`, `ASSUMPTION:`). Edit **`SKILL.md`** when the source slide changes, then align **`templates/`** and this file.

**Use only this** eight-row, two-column layout: **left column = section title**, **right column = guiding questions** (Agile by Design master slide, e.g. **page 46**). A **screenshot** of that table is in **`reference/opportunity-canvas-p46.png`**. Do **not** add extra rows (e.g. a separate “customer segmentation” row) or paraphrase the prompts into a different shape.

| **Section** | **Guiding questions** |
|-------------|------------------------|
| **Customer Problems** | What are our key customer segments and what are the unique requirements of each customer segment? |
| **Solution Features** | What is our Unique Value Proposition to our Customer Segments? What customer problem are we solving? What are the major features of our solution? |
| **Increments Of Value** | What channels will be leveraged to have our Product reach our Customer Segments? |
| **Key Metrics of Success** | What are the key metrics that will tell us how our product is doing? |
| **Revenue Drivers** | For what value are our Customers really willing to pay? |
| **Key Activities and Resources** | What Key Activities does our Product Require (e.g. to Build, to Support, etc.)? What Key Resources [People] and Capabilities [Process] does our Product leverage? |
| **Key Partners** | Who are our Key Partners? Who are our key Suppliers? |
| **Cost Drivers** | What are the most important costs drivers inherent in our Product? |

Wording and spelling (*costs drivers*, *really*, bracket *People* / *Process*) follow the **source slide**; change the deck, not the skill, if you want copy-edits globally.

**Template PPTX** lists the same **eight titles**; **`02 Training/canvas.pptx`** carries the same questions (e.g. on the table / slide 7 in the pipeline extract). **Business model canvas** / holistic product hypothesis appears in **speaker notes**, not as a substitute for the table above.

**Why / when** (separate slide): shared understanding, explicit assumptions, align vision, validate risks and unknowns.

---

## 2) `templates/` line-prefix: **ABD row names (normative)**

**Normative** output uses **one prefix per §1 section** (see **`templates/opportunity-canvas.md`**): `CUSTOMER_PROBLEMS:` … `COST_DRIVERS:`, plus `OPPORTUNITY:`, `ALTERNATIVES:`, and `ASSUMPTION:` (with **`validate by:`**). This matches the **whiteboard 1:1**.

**Optional legacy crosswalk** (spreadsheets, older scanners): same substance can be *summarized* with `PROBLEM:`, `USERS:`, `SOLUTIONS:`, `METRICS:`, `BUSINESS_CHALLENGES:`—only when a consumer cannot ingest the ABD prefixes. Do not treat the legacy set as a second “official” model.

| **§1 section** | **Normative line prefix in templates** |
|----------------|----------------------------------------|
| Customer Problems | `CUSTOMER_PROBLEMS:` |
| Solution Features | `SOLUTION_FEATURES:` |
| Increments Of Value | `INCREMENTS_OF_VALUE:` |
| Key Metrics of Success | `KEY_METRICS_OF_SUCCESS:` |
| Revenue Drivers | `REVENUE_DRIVERS:` |
| Key Activities and Resources | `KEY_ACTIVITIES_AND_RESOURCES:` |
| Key Partners | `KEY_PARTNERS:` |
| Cost Drivers | `COST_DRIVERS:` |
| *(handle)* | `OPPORTUNITY:` |
| *(options)* | `ALTERNATIVES:` |
| *(bets to test)* | `ASSUMPTION:` + **validate by:** |

---

## 3) Training deck (full markdown extract)

Verbatim pipeline extract is saved alongside for audit and re-chunking:

- **`reference/canvas-pptx-extract.md`** — full `canvas.pptx` → markdown (examples include Apple iPod, payment scenario).

---

## 4) Example use — filled eight-box canvas (*canvas.pptx* slide 11, Agile by Design)

This is the **payment / mobile / wallet** worked example from the training deck: each **row** is a canvas area; bullets are the “sticky” ideas for that row (teach the pattern, not a product recommendation).

| Row | What’s on the canvas |
|-----|----------------------|
| **Customer Problems** | **Merchants** — pain in their world. **MNOs** (mobile network operators) — their issues. **Acquirers / issuers** — problems in the financial space. |
| **Solution Features** | **Merchant** — speed of moving customers through lines. **Customer** — fast payment, convenient on a phone. **Issuer** — mobile innovation, new channel to reach debit users. **End customers** — e.g. “emotional spenders” vs “mature pragmatists” (segmentation). |
| **Increments Of Value** | **Mobile app**; **branding & advertising**; **partner networks** (ecosystem). |
| **Key Metrics of Success** | **Scale targets** — e.g. 1–2 issuers, ~1K customers, 1–2 merchants. **Engagement** — e.g. +10% social media, +15% web traffic. |
| **Revenue Drivers** | Who pays: **merchants (X)**, **MNOs (A)**, **customers (Y)**, **acquirers & issuers (Z)** — willingness to pay by segment. |
| **Key Activities and Resources** | **Internal** — delivery team, legal, marketing, finance, past products. **Phases** — market validation → solution delivery → lab validation → pilot → roll-out marketing. **Marketing** as its own workstream. |
| **Key Partners** | **White-label** — dev services as a white-label from Partner X. **Software** — SDK and wallet provider. **Agency** — collateral, campaign, PR. |
| **Cost Drivers** | **Development**, **test tools**, **scripting**, **legal**, **certification**. |

**Line-prefix sketch:** use **`templates/opportunity-canvas.md`**—fill **`CUSTOMER_PROBLEMS:`** with segments (merchants, MNOs, issuers, …), **`SOLUTION_FEATURES:`** and **`INCREMENTS_OF_VALUE:`** with the value and reach story, metrics/revenue/cost/activities/partners rows from the example slide, and **`ASSUMPTION:`** for bets. The **scheduling** example in the template shows the same **prefix set** in full.

---

## 5) New slides: validated learning, Kanban, and assumption checklist (*canvas.pptx* slides 12–14)

The **updated** training deck extends the **eight-box** work with a **downstream** loop: pull **uncertainty** from the **Idea/Opportunity Canvas** into a **Validated Learning Kanban** and run explicit **assumption tests**. Full wording is in **`reference/canvas-pptx-extract.md`**.

| Slide | What it does |
|-------|----------------|
| **12** | **Bridge:** The team **collaborates** on the **Idea Canvas** to find **uncertainty** that is then **validated** on a **“Validated Learning Kanban Board”** (backlog by **common area**; columns / flow **Plan → Validation → Learning**). Speaker note: use **Kanban** to **coordinate** validation; **stand-ups** with IT, marketing, product, legal, security. |
| **13** | **How:** **Create a Validated Learning Kanban** to test assumptions; **refine the Opportunity Canvas** with learnings. **Example** pattern: *We don’t know X about customers* → *therefore* we will *do a small manual experiment* with a *cohort* → *validate reaction* (uncertainty → **Plan / Validate / Learn** on an **Uncertainty Backlog**). |
| **14** | **Top validation / area checklist** for backlog and risk triage. Ask whether items carry **uncertainty** across: **Problem / solution fit** (top pain, early adopters, whether capabilities match segment problems) · **Capability / market fit** (UVP vs competitors, increments and brand, market size, benefits vs investment, value increments, cost of delay, segment diversity) · **Technology feasibility** (architecture risk, integrations, org capabilities, procurement, **key partners**’ technical help) · **Delivery feasibility** (what depends on **partners** / internal **resources**, relationships, risks if resources are constrained, which resources **accelerate**) · **Other** (legal, compliance, marketing/brand, security, post-deploy support, **timelines** for increments, **key metrics of success** with segments). Use this as a **rubric** to turn canvas rows into `ASSUMPTION:` + `validate by:` and Kanban test cards. |
