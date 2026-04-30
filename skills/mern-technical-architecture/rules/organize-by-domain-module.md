---
scanner: domain_structure_scanner.py
---

# Rule: Organize by Domain Module

Organize code by **business capability** (domain module) first, then by technical layer within each module. This ensures that all code for a single domain lives together — changes rarely ripple to other domains, teams can own entire domains, and each module can become its own microservice later without restructuring.

## DO

- Structure each domain as `packages/{domain}/{shared|client|server}`.
- Include `index.ts` and `package.json` in each tier folder for clean imports.
- Keep the app shell (`app-server/`, `app-client/`) at the packages level as composition roots.
- Place test files under `tests/{epic}/{sub-epic}/` mirroring the domain structure.

```
project-root/
├── packages/
│   ├── recipients/              # Domain module
│   │   ├── shared/              # Domain core (entities, schemas, value objects)
│   │   │   ├── Recipient.ts
│   │   │   ├── recipient.schema.ts
│   │   │   ├── index.ts
│   │   │   └── package.json
│   │   ├── client/              # React frontend for this domain
│   │   │   ├── RecipientSelector.tsx
│   │   │   ├── useRecipients.ts
│   │   │   ├── recipients.api.ts
│   │   │   ├── index.ts
│   │   │   └── package.json
│   │   └── server/              # Express backend for this domain
│   │       ├── recipients.routes.ts
│   │       ├── recipients.controller.ts
│   │       ├── recipients.service.ts
│   │       ├── recipients.repository.ts
│   │       ├── index.ts
│   │       └── package.json
│   ├── app-server/
│   └── app-client/
├── tests/
└── package.json
```

## DON'T

- Organize by technical layer at the top level (`controllers/`, `models/`, `views/`, `routes/`).
- Scatter a single domain's code across multiple unrelated folders.
- Mix multiple domain concerns in a single folder.

```
# WRONG — technical-first organization
project-root/
├── controllers/
│   ├── recipientController.ts    # Recipient logic scattered
│   └── paymentController.ts
├── models/
│   ├── Recipient.ts              # ... across multiple folders
│   └── Payment.ts
├── routes/
│   ├── recipientRoutes.ts        # ... making changes ripple everywhere
│   └── paymentRoutes.ts
└── views/
    ├── RecipientList.tsx
    └── PaymentForm.tsx
```
