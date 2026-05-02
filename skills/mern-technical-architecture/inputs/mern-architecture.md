# MERN Stack Architecture - Domain-First Approach

## Table of Contents

- [MERN Stack Architecture - Domain-First Approach](#mern-stack-architecture---domain-first-approach)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Architecture Layers](#architecture-layers)
    - [Domain Participants](#domain-participants)
    - [Archiecture](#archiecture)
      - [Classes](#classes)
      - [Flow :](#flow-)
        - [Walkthrough Notation](#walkthrough-notation)
        - [Wallkthrough](#wallkthrough)
    - [Example Code](#example-code)
      - [2. Backend (packages/recipients/server)](#2-backend-packagesrecipientsserver)
      - [3. Frontend (packages/recipients/client)](#3-frontend-packagesrecipientsclient)
  - [Testing Architecture](#testing-architecture)
    - [Testing Philosophy](#testing-philosophy)
    - [Testing Pyramid - Story-Driven Spec by Example](#testing-pyramid---story-driven-spec-by-example)
    - [Story-to-Test Alignment](#story-to-test-alignment)
    - [Test Structure Pattern (Given/When/Then Helpers)](#test-structure-pattern-givenwhenthen-helpers)
      - [Base Helper (Shared Logic)](#base-helper-shared-logic)
      - [Server Helper (Supertest + Node.js Test Runner)](#server-helper-supertest--nodejs-test-runner)
      - [Client Helper (Vitest + Testing Library)](#client-helper-vitest--testing-library)
      - [E2E Helper (Playwright)](#e2e-helper-playwright)
    - [Server-Side Tests](#server-side-tests)
    - [Client-Side Tests](#client-side-tests)
    - [E2E Tests with Playwright](#e2e-tests-with-playwright)
    - [Test Configuration](#test-configuration)
  - [References](#references)

---

## Overview

This document describes a domain-first MERN (MongoDB, Express, React, Node.js) architecture that prioritizes:

1. **Domain modules over technical modules** - organizing code by business capability, then by layer
2. **High alignment to ubiquitous language** - scenarios ,  domain models, tests and code use consistent terminology
3. **Minimizing logic duplication** - shared validation, types, and business rules, and domaon objects across client and service tiers
4. **Clean Architecture principles** - dependencies point inward toward the domain core

---

## Architecture Layers

┌─────────────────────────────────────────────────────────────────────┐
│  PRESENTATION                                                       │
│  ─────────────                                                      │
│  Tech: React, React Router, TanStack Query, Zustand/Redux           │
│  Impl: Components (.tsx), Hooks, Context, CSS Modules               │
│  Role: Render UI, capture user input, manage local UI state         │
└─────────────────────────────────────────────────────────────┬───────┘
                                                              │ HTTP/JSON
┌─────────────────────────────────────────────────────────────▼───────┐
│  INTERFACE ADAPTERS                                                 │
│  ─────────────────                                                  │
│  Tech: Express.js (Router, Middleware), Axios/Fetch (client-side)   │
│  Impl: routes.ts, controller.ts, mapper.ts, api.ts                  │
│  Role: Translate HTTP ↔ Application calls, parse req, format res    │
└─────────────────────────────────────────────────────────────┬───────┘
                                                              │ Function calls
┌─────────────────────────────────────────────────────────────▼───────┐
│  APPLICATION (Use Cases)                                            │
│  ───────────────────────                                            │
│  Tech: Plain TypeScript classes (NO framework - intentional)        │
│  Impl: service.ts (e.g., RecipientsService, NotificationService)    │
│  Role: Orchestrate use cases, coordinate domain + infra, no HTTP    │
└─────────────────────────────────────────────────────────────┬───────┘
                                                              │ Function calls
┌─────────────────────────────────────────────────────────────▼───────┐
│  DOMAIN CORE                                                        │
│  ───────────                                                        │
│  Tech: Plain TypeScript (NO framework - portable to browser+Node)   │
│  Impl: Entity classes, Value Objects, Zod schemas, domain methods   │
│  Role: Business rules, validation, domain logic                     │
│  *** SHARED BETWEEN FRONTEND AND BACKEND via @appName/{domain}-shared ***│
└─────────────────────────────────────────────────────────────┬───────┘
                                                              │ Driver calls
┌─────────────────────────────────────────────────────────────▼───────┐
│  INFRASTRUCTURE                                                     │
│  ──────────────                                                     │
│  Tech: MongoDB Driver, Nodemailer, AWS SDK, Redis, etc.             │
│  Impl: repository.ts, email.service.ts, cache.service.ts            │
│  Role: Persist data, call external APIs, send emails                │
└─────────────────────────────────────────────────────────────────────┘
```


## File Structure

Organize by **domain module** first, then by technical layer within each module:

### Why Domain-First?

| Principle | Benefit |
|-----------|---------|
| **Localize dependencies** | All code for "recipients" lives in `packages/recipients/`. Changes rarely ripple to other domains. |
| **Change together, live together** | When a feature changes, you edit files in one folder—not scattered across `controllers/`, `models/`, `views/`. |
| **Scales with domain count** | Adding a new domain = adding a new folder. No cross-cutting reorganization needed. |
| **Clear ownership** | Teams can own entire domains. "Who owns recipients?" → the team that owns `packages/recipients/`. |
| **Independent deployability** | Each domain module can become its own microservice later without restructuring. |


**Pattern (domain-first):**

```
project-root/
├── packages/
│   ├── recipients/                  # Recipients domain module
│   │   ├── shared/                  # Shared domain logic
│   │   │   ├── Recipient.ts                 # Entity
│   │   │   ├── RecipientId.ts               # Value Object
│   │   │   ├── RecipientEmail.ts            # Value Object with validation
│   │   │   ├── RecipientSelection.ts        # Aggregate
│   │   │   ├── RecipientRules.ts            # Business rules
│   │   │   ├── recipient.schema.ts          # Zod/Yup validation schema
│   │   │   ├── index.ts
│   │   │   └── package.json
│   │   │
│   │   ├── client/                  # React frontend for recipients
│   │   │   ├── RecipientList.tsx
│   │   │   ├── RecipientSelector.tsx
│   │   │   ├── RecipientCard.tsx
│   │   │   ├── useRecipients.ts             # Custom hook
│   │   │   ├── recipients.api.ts            # API client
│   │   │   ├── recipients.state.ts          # Local state
│   │   │   ├── index.ts
│   │   │   └── package.json
│   │   │
│   │   └── server/                  # Express backend for recipients
│   │       ├── recipients.routes.ts
│   │       ├── recipients.controller.ts
│   │       ├── recipients.repository.ts
│   │       ├── recipients.service.ts        # Application service
│   │       ├── recipients.mapper.ts         # DTO <-> Entity mapping
│   │       ├── index.ts
│   │       └── package.json
│   │
│   ├── Payments/               # Payments domain module
│   │   ├── shared/
│   │   ├── client/
│   │   └── server/
│   │
│   ├── app-server/                  # Main Express app (composes domain servers)
│   │   ├── app.ts
│   │   └── package.json
│   │
│   └── app-client/                  # Main React app (composes domain clients)
│       ├── App.tsx
│       └── package.json
│
├── tests/                           # Story specs; tooling in tests/vitest, tests/playwright
│   ├── vitest/                      # vitest.config.ts + vitest.setup.ts
│   └── playwright/                  # playwright.config.ts + test-results / playwright-report
├── deploy/
│   └── turbo.json                   # Turborepo task graph (optional; `npm run turbo -- run build`)
└── package.json                     # Workspace root
```
## Example

Story: Select Recipient for Wire Payment
```gherkin
  Background:
    Given User "Jane Doe" is logged into ChannelOne 2.0
    And User is entitled to "Wire.Create" function
    And Enterprise "Acme Corp" has wire service enabled

  Scenario: User views list of active recipients when initiating wire payment
    Given Enterprise has the following recipients:
      | name               | status   | bank_name              | swift_bic    | account_number   |
      | Global Trading Ltd | Active   | HSBC Hong Kong         | HSBCHKHHHKH  | 123456789        |
      | Domestic Supplier  | Active   | Chase Bank             | CHASUS33     | 987654321        |
      | New Vendor Inc     | Pending  | Bank of America        | BOFAUS3N     | 555555555        |
    When User initiates wire payment creation
    Then RecipientSelection displays only Active recipients
    And RecipientSelection excludes "New Vendor Inc" with Pending status
    And each recipient shows name, bank name, and masked account number

  Scenario: User selects recipient and proceeds to payment details
    Given Enterprise has Recipient "Global Trading Ltd" with Active status
    And Recipient has BeneficiaryBank with SWIFT/BIC "HSBCHKHHHKH"
    And Recipient has no IntermediateBank configured
    When User selects "Global Trading Ltd" for wire payment
    And User clicks "Continue to Payment Details"
    Then WirePayment is created with selected Recipient
    And User navigates to Step 2 (Enter Payment Details)

  Scenario: User cannot select pending recipient (MX country variance)
    Given country is "MX" with 30-minute pending period
    And Recipient "New Vendor Inc" was created 15 minutes ago
    And Recipient status is "Pending"
    When User views recipient list
    Then "New Vendor Inc" is not selectable
    And tooltip shows "Available in 15 minutes"

  Scenario: User with intermediate bank entitlement sees routing details
    Given User is entitled to "Wire.IntermediateBank" function
    And Recipient "Global Trading Ltd" has IntermediateBank "Citibank NY"
    When User views Recipient details
    Then RecipientDetails shows IntermediateBank section
    And IntermediateBank shows SWIFT/BIC "CITIUS33"
```
---


### Domain Participants

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           RECIPIENT DOMAIN                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────┐         owns          ┌──────────────┐                   │
│   │  Enterprise  │◆───────────────────────│   Account   │                   │
│   │              │                        │             │                   │
│   │ • name       │         owns          │ • number     │                   │
│   │ • wireConfig │◆────────┐             │ • type                          │
│   └──────────────┘         │             │ • balance    │                   │
│          │                 │             └──────────────┘                   │
│          │ assigns         │                                                │
│          ▼                 │                                                │
│   ┌──────────────┐         │             ┌──────────────────┐               │
│   │     User     │         │             │ WireServiceConfig │              │
│   │              │         └────────────▶│                  │              │
│   │ • name       │                       │ • functions[]    │               │
│   │ • email      │                       │ • accountTypes[] │               │
│   └──────────────┘                       │ • intermBankFlag │               │
│          │                               └──────────────────┘               │
│          │ has                                                              │
│          ▼                                                                  │
│   ┌──────────────┐                                                          │
│   │  Entitlement │         Enterprise owns Recipients                       │
│   │              │         ─────────────────────────────                    │
│   │ • function   │                        │                                 │
│   │ • status     │                        ▼                                 │
│   └──────────────┘               ┌──────────────┐                           │
│                                  │   Recipient  │                           │
│                                  │              │                           │
│                                  │ • name       │◆──────┐                  │
│                                  │ • accountNo  │       │ has               │
│                                  │ • status     │       ▼                   │
│                                  │              │  ┌──────────────────┐     │
│                                  └──────────────┘  │ RecipientStatus  │     │
│                                         │          │                  │     │
│                                         │ has      │ • Active         │     │
│                                         ▼          │ • Pending        │     │
│                              ┌──────────────────┐  │ • Inactive       │     │
│                              │  BeneficiaryBank │  └──────────────────┘     │
│                              │                  │          │                │
│                              │ • swiftBic       │          │ eligibility    │
│                              │ • abaRouting     │          ▼                │
│                              │ • name           │  ┌──────────────────┐     │
│                              │ • address        │  │RecipientSelection│     │
│                              └──────────────────┘  │                  │     │
│                                         ▲          │ • filter(active) │     │
│                                         │ routes   │ • forPayment()   │     │
│                              ┌──────────────────┐  └──────────────────┘     │
│                              │ IntermediateBank │                           │
│                              │                  │                           │
│                              │ • swiftBic       │                           │
│                              │ • name           │                           │
│                              │ • entitlementReq │                           │
│                              └──────────────────┘                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```
---

📊 **[View Class Diagram](recipient-domain.mmd)**

| Concept | Module | Responsibility | Collaborators |
|---------|--------|---------------|---------------|
| **Enterprise** | `onboarding.enterprise` | Owns accounts and recipients; maintains wire service configuration | Account, WireServiceConfiguration, User |
| **User** | `onboarding.user` | Has entitlements for wire functions; initiates payments | Entitlement, Enterprise |
| **Entitlement** | `onboarding.entitlement` | Grants user permission for specific wire functions (Create, View, Approve) | User |
| **Recipient** | `recipient` | Beneficiary entity with bank details and activation status | BeneficiaryBank, RecipientStatus, IntermediateBank |
| **RecipientStatus** | `recipient` | Lifecycle state (Active, Pending, Inactive); determines payment eligibility | Recipient |
| **BeneficiaryBank** | `recipient.bank` | Holds bank identification (SWIFT/BIC, ABA routing) and address | Recipient |
| **IntermediateBank** | `recipient.bank` | Optional routing bank; requires entitlement flag | BeneficiaryBank, Entitlement |
| **RecipientSelection** | `payment.recipient` | Filters recipients by Active status for wire payment creation | Recipient, RecipientStatus |
| **Recipients** | `recipient` | Collection class wrapping Recipient[] with filter/search methods | Recipient |

**Country Variance:**
| Concept | US | MX |
|---------|-----|-----|
| RecipientStatus | Immediate activation | 30-minute pending period before Active |
| IntermediateBank | Optional (entitlement flag) | Same |


### Archiecture
#### Classes

📊 **[View Implementation Class Diagram](recipient-implementation.mmd)**

| Class | Layer | Package | Responsibility |
|-------|-------|---------|----------------|
| **Recipient** | Domain | `shared/` | Entity representing a beneficiary with bank details and status |
| **RecipientStatus** | Domain | `shared/` | Value object managing lifecycle state (Active/Pending/Inactive) with country-specific pending rules |
| **BeneficiaryBank** | Domain | `shared/` | Value object holding bank identification (SWIFT/BIC, ABA) and address |
| **IntermediateBank** | Domain | `shared/` | Optional value object for routing banks |
| **Recipients** | Domain | `shared/` | Collection class wrapping `Recipient[]` with fluent `filterByStatus()`, `search()` methods |
| **RecipientSelection** | Domain | `shared/` | Aggregate for payment eligibility logic: `getEligibleForPayment()`, `filterByBankType()` |
| **RecipientSchema** | Domain | `shared/` | Zod schema validating Recipient structure; used by repository and API |
| **SelectRecipientsSchema** | Domain | `shared/` | Zod schema validating selection input (min 1 recipient) |
| **BeneficiaryBankSchema** | Domain | `shared/` | Zod schema validating bank details (SWIFT format, ABA digits) |
| **RecipientsRouter** | Interface | `server/` | Express router defining `GET /api/recipients` and `POST /api/recipients/select` |
| **RecipientsController** | Interface | `server/` | Handles HTTP parsing, delegates to service, formats responses |
| **RecipientsService** | Application | `server/` | Orchestrates use cases: load recipients, apply filters, coordinate repository |
| **RecipientsRepository** | Infrastructure | `server/` | MongoDB data access: `findAll()`, `findByIds()`, validates docs with RecipientSchema |
| **RecipientSelector** | Presentation | `client/` | React component rendering recipient list with search/filter UI |
| **RecipientCard** | Presentation | `client/` | Presentational component for single recipient with checkbox |
| **useRecipients** | Presentation | `client/` | React hook managing recipients state, selection, and filtering |
| **RecipientsApi** | Interface | `client/` | API client with `fetchRecipients()` and `selectRecipients()` functions |

#### Flow : 
example: User initiates wire payment creation and views list of active recipients to select for payment

📊 **[View Sequence Diagram](flow-load-recipients.mmd)**

##### Walkthrough Notation
```
result: <actual_value> = Object.method(param: value)
    -> nested_result: <value> = Collaborator.method()
        -> deeper: <value> = Another.method()
        return deeper: <value>
    return result: <actual_value>
```
##### Wallkthrough
```
RecipientSelector (React Component)
    # Entry point: React component mounts when user navigates to page
    recipients = RecipientSelector.mount()
    
        # Component calls custom hook to manage recipient data and loading state
        -> state = useRecipients()
        
            # Hook immediately sets loading=true to show spinner/skeleton UI
            -> setLoading(true)
            
            # Async call to API client function; control leaves React, enters network layer
            -> response = fetchRecipients({activeOnly: true})
            
                ─────────── HTTP GET /api/recipients?activeOnly=true ───────────
                # REQUEST CROSSES NETWORK BOUNDARY: browser -> server
                
                    RecipientsRouter (Express)
                        # Express router receives request, delegates to controller
                        -> RecipientsController.list(req, res)
                        
                            # Controller extracts enterpriseId from authenticated user context
                            -> enterpriseId = req.user.enterpriseId
                            
                            # Controller extracts activeOnly from query params
                            -> filters = { activeOnly: req.query.activeOnly === 'true' }
                            
                            # Controller delegates to service layer (application logic)
                            -> recipients = RecipientsService.getRecipients(enterpriseId, filters)
                            
                                # Service delegates to repository for enterprise-scoped data
                                -> allRecipients = RecipientsRepository.findByEnterprise(enterpriseId)
                                
                                    ─────────── MongoDB Query ───────────
                                    # QUERY CROSSES DATABASE BOUNDARY: Node.js -> MongoDB
                                    
                                    # Query scoped to enterprise (tenant isolation)
                                    -> docs = db.collection('recipients').find({ enterpriseId }).toArray()
                                    
                                    # Each doc validated/transformed using SHARED Zod schema
                                    -> validated = docs.map(doc => RecipientSchema.parse(doc))  # SHARED
                                    
                                    # Repository returns typed domain entities, not raw docs
                                    return allRecipients
                                
                                # Wrap raw array in domain collection for fluent filtering
                                -> recipients = new Recipients(allRecipients)   # SHARED
                                
                                # Apply filter using domain-oriented method on collection
                                -> filtered = recipients.filterByStatus('Active')   # SHARED
                                
                                # Service returns filtered collection as array to controller
                                return filtered.toArray()
                            
                            # Controller serializes response as JSON and sends to client
                            -> res.json({recipients, total: 2})
                            
                ─────────────────────────────────────────────────────────────────
                # RESPONSE CROSSES NETWORK BOUNDARY: server -> browser
                
            # Hook receives response, updates React state with recipient array
            -> setRecipients(response.recipients)
            
            # Hook clears loading flag, UI can now render actual data
            -> setLoading(false)
            
            # Hook returns state bag to component
            return {recipients, loading, error}
        
        # Component maps each Recipient entity to a presentational card component
        -> cards = recipients.map(r => <RecipientCard recipient={r} />)
        
        # Final render: container div with recipient cards as children
        return <div>{cards}</div>
```
### Example Code


```typescript
// packages/recipients/shared/RecipientStatus.ts
export type RecipientStatusType = 'Active' | 'Pending' | 'Inactive';

export class RecipientStatus {
  constructor(
    public readonly status: RecipientStatusType,
    public readonly createdAt: Date,
    private readonly countryCode: 'US' | 'MX' | 'CA' = 'US'
  ) {}

  private static readonly MX_PENDING_PERIOD_MS = 30 * 60 * 1000;

  isEligibleForPayment(): boolean {
    return this.status === 'Active';
  }

  isPending(): boolean {
    return this.status === 'Pending';
  }

  get remainingPendingMinutes(): number | null {
    if (this.countryCode !== 'MX' || this.status !== 'Pending') return null;
    const elapsed = Date.now() - this.createdAt.getTime();
    const remaining = Math.max(0, RecipientStatus.MX_PENDING_PERIOD_MS - elapsed);
    return Math.ceil(remaining / 60000);
  }
}

// packages/recipients/shared/BeneficiaryBank.ts
export interface BeneficiaryBank {
  swiftBic: string;
  abaRouting?: string;
  name: string;
  addressLine1: string;
  addressLine2?: string;
  city: string;
  country: string;
}

export const BeneficiaryBankSchema = z.object({
  swiftBic: z.string().regex(/^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$/, 'Invalid SWIFT/BIC'),
  abaRouting: z.string().regex(/^\d{9}$/, 'ABA must be 9 digits').optional(),
  name: z.string().min(1).max(140),
  addressLine1: z.string().min(1).max(70),
  addressLine2: z.string().max(70).optional(),
  city: z.string().min(1).max(35),
  country: z.string().length(2),
});

// packages/recipients/shared/IntermediateBank.ts
export interface IntermediateBank {
  swiftBic: string;
  name: string;
}

// packages/recipients/shared/Recipient.ts
import { z } from 'zod';

export interface Recipient {
  id: string;
  enterpriseId: string;
  name: string;
  accountNumber: string;
  accountNumberFull: string;
  status: RecipientStatus;
  beneficiaryBank: BeneficiaryBank;
  intermediateBank?: IntermediateBank;
  createdAt: Date;
  activatedAt?: Date;
}

export const RecipientSchema = z.object({
  id: z.string().uuid(),
  enterpriseId: z.string().uuid(),
  name: z.string().min(1, 'Beneficiary name is required').max(140),
  accountNumber: z.string().min(1),
  accountNumberFull: z.string().min(1),
  status: z.enum(['Active', 'Pending', 'Inactive']),
  beneficiaryBank: BeneficiaryBankSchema,
  intermediateBank: z.object({
    swiftBic: z.string(),
    name: z.string(),
  }).optional(),
  createdAt: z.coerce.date(),
  activatedAt: z.coerce.date().optional(),
});

export type RecipientDTO = z.infer<typeof RecipientSchema>;

// packages/recipients/shared/RecipientSelection.ts
export class RecipientSelection {
  constructor(
    private readonly recipients: Recipient[],
    private readonly countryCode: 'US' | 'MX' | 'CA' = 'US'
  ) {}

  getEligibleForPayment(): Recipient[] {
    return this.recipients.filter(r => r.status.isEligibleForPayment());
  }

  filterByBankType(type: 'domestic' | 'international'): Recipient[] {
    return this.getEligibleForPayment().filter(r => {
      const hasDomesticRouting = !!r.beneficiaryBank.abaRouting;
      return type === 'domestic' ? hasDomesticRouting : !hasDomesticRouting;
    });
  }

  search(query: string): Recipient[] {
    const lower = query.toLowerCase();
    return this.getEligibleForPayment().filter(r =>
      r.name.toLowerCase().includes(lower) ||
      r.beneficiaryBank.name.toLowerCase().includes(lower)
    );
  }

  getPendingWithWaitTime(): Array<{ recipient: Recipient; minutesRemaining: number }> {
    if (this.countryCode !== 'MX') return [];
    return this.recipients
      .filter(r => r.status.isPending())
      .map(r => ({
        recipient: r,
        minutesRemaining: r.status.remainingPendingMinutes || 0,
      }));
  }
}

// packages/recipients/shared/Recipients.ts
export class Recipients {
  constructor(private readonly items: Recipient[]) {}

  filterByStatus(status: RecipientStatusType): Recipients {
    return new Recipients(this.items.filter(r => r.status.status === status));
  }

  filterByEnterprise(enterpriseId: string): Recipients {
    return new Recipients(this.items.filter(r => r.enterpriseId === enterpriseId));
  }

  search(query: string): Recipients {
    const lower = query.toLowerCase();
    return new Recipients(this.items.filter(r =>
      r.name.toLowerCase().includes(lower) ||
      r.beneficiaryBank.name.toLowerCase().includes(lower)
    ));
  }

  toArray(): Recipient[] {
    return [...this.items];
  }

  get length(): number {
    return this.items.length;
  }
}
```

#### 2. Backend (packages/recipients/server)

```typescript
// packages/recipients/server/recipients.repository.ts
import { Collection, Db } from 'mongodb';
import { Recipient, RecipientSchema } from '@channelone/recipients-shared';

export class RecipientsRepository {
  private collection: Collection;

  constructor(db: Db) {
    this.collection = db.collection('recipients');
  }

  async findAll(): Promise<Recipient[]> {
    const docs = await this.collection.find().toArray();
    return docs.map(doc => RecipientSchema.parse(doc));
  }

  async findByIds(ids: string[]): Promise<Recipient[]> {
    const docs = await this.collection.find({ id: { $in: ids } }).toArray();
    return docs.map(doc => RecipientSchema.parse(doc));
  }

  async findByEnterprise(enterpriseId: string): Promise<Recipient[]> {
    const docs = await this.collection.find({ enterpriseId }).toArray();
    return docs.map(doc => RecipientSchema.parse(doc));
  }
}

// packages/recipients/server/recipients.service.ts
import { Recipient, Recipients, SelectRecipientsInput } from '@channelone/recipients-shared';
import { RecipientsRepository } from './recipients.repository';

export class RecipientsService {
  constructor(private repo: RecipientsRepository) {}

  async getRecipients(enterpriseId: string, filters?: { activeOnly?: boolean }): Promise<Recipient[]> {
    const allRecipients = await this.repo.findByEnterprise(enterpriseId);
    let recipients = new Recipients(allRecipients);
    if (filters?.activeOnly) {
      recipients = recipients.filterByStatus('Active');
    }
    
    return recipients.toArray();
  }

  async selectRecipients(input: SelectRecipientsInput): Promise<Recipient[]> {
    return this.repo.findByIds(input.recipientIds);
  }
}

// packages/recipients/server/recipients.routes.ts
import { Router } from 'express';
import { SelectRecipientsSchema } from '@channelone/recipients-shared';
import { RecipientsService } from './recipients.service';

export function createRecipientsRouter(service: RecipientsService): Router {
  const router = Router();

  router.get('/', async (req, res) => {
    const enterpriseId = req.user.enterpriseId;
    const { activeOnly } = req.query;
    const recipients = await service.getRecipients(enterpriseId, {
      activeOnly: activeOnly === 'true',
    });
    res.json({ recipients, total: recipients.length });
  });

  router.post('/select', async (req, res) => {
    const result = SelectRecipientsSchema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ errors: result.error.issues });
    }
    
    const selectedRecipients = await service.selectRecipients(result.data);
    res.json({ selected: selectedRecipients });
  });

  return router;
}
```
----

#### 3. Frontend (packages/recipients/client)

```typescript
// packages/recipients/client/recipients.api.ts
import { Recipient, SelectRecipientsInput } from '@channelone/recipients-shared';

const API_BASE = '/api/recipients';

export async function fetchRecipients(filters?: { 
  activeOnly?: boolean 
}): Promise<Recipient[]> {
  const params = new URLSearchParams();
  if (filters?.activeOnly) params.set('activeOnly', 'true');
  
  const response = await fetch(`${API_BASE}?${params}`);
  const data = await response.json();
  return data.recipients;
}

export async function selectRecipients(input: SelectRecipientsInput): Promise<Recipient[]> {
  const response = await fetch(`${API_BASE}/select`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });
  const data = await response.json();
  return data.selected;
}

// packages/recipients/client/useRecipients.ts
import { useState, useEffect, useCallback } from 'react';
import { Recipient, Recipients } from '@channelone/recipients-shared';
import { fetchRecipients } from './recipients.api';

export function useRecipients() {
  const [recipients, setRecipients] = useState<Recipient[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchRecipients({ activeOnly: true })
      .then(setRecipients)
      .finally(() => setLoading(false));
  }, []);

  const toggleRecipient = useCallback((id: string) => {
    setSelected(prev => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  }, []);

  const getSelectedRecipients = useCallback(() => {
    return recipients.filter(r => selected.has(r.id));
  }, [recipients, selected]);

  const filterBySearch = useCallback((query: string) => {
    const collection = new Recipients(recipients);
    return collection.search(query).toArray();
  }, [recipients]);

  return {
    recipients,
    selected,
    loading,
    toggleRecipient,
    getSelectedRecipients,
    filterBySearch,
  };
}

// packages/recipients/client/RecipientSelector.tsx
import React, { useState } from 'react';
import { useRecipients } from './useRecipients';
import { RecipientCard } from './RecipientCard';
import { selectRecipients } from './recipients.api';
import { SelectRecipientsSchema } from '@channelone/recipients-shared';

export function RecipientSelector() {
  const {
    recipients,
    selected,
    loading,
    toggleRecipient,
    getSelectedRecipients,
    filterBySearch,
  } = useRecipients();

  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState<string | null>(null);

  const displayedRecipients = searchQuery 
    ? filterBySearch(searchQuery) 
    : recipients;

  const handleConfirmSelection = async () => {
    const input = { recipientIds: Array.from(selected) };
    const validation = SelectRecipientsSchema.safeParse(input);
    if (!validation.success) {
      setError(validation.error.issues[0].message);
      return;
    }

    try {
      await selectRecipients(input);
    } catch (err) {
      setError('Failed to confirm selection');
    }
  };

  return (
    <div className="recipient-selector">
      <header>
        <h1>Select Recipient for Wire Payment</h1>
        
        <div className="filters">
          <input
            type="search"
            placeholder="Search by name or bank..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
          />
        </div>
      </header>

      {loading && <p>Loading recipients...</p>}
      
      {error && <p className="error">{error}</p>}

      <div className="recipient-list">
        {displayedRecipients.map(recipient => (
          <RecipientCard
            key={recipient.id}
            recipient={recipient}
            isSelected={selected.has(recipient.id)}
            onToggle={() => toggleRecipient(recipient.id)}
          />
        ))}
      </div>

      <footer>
        <p>{selected.size} recipient(s) selected</p>
        <button 
          onClick={handleConfirmSelection}
          disabled={selected.size === 0}
        >
          Confirm Selection
        </button>
      </footer>
    </div>
  );
}

// packages/recipients/client/RecipientCard.tsx
import React from 'react';
import { Recipient } from '@channelone/recipients-shared';

interface RecipientCardProps {
  recipient: Recipient;
  isSelected: boolean;
  onToggle: () => void;
}

export function RecipientCard({ recipient, isSelected, onToggle }: RecipientCardProps) {
  return (
    <div 
      className={`recipient-card ${isSelected ? 'selected' : ''}`}
      onClick={onToggle}
    >
      <input 
        type="checkbox" 
        checked={isSelected} 
        onChange={onToggle}
      />
      <div className="info">
        <h3>{recipient.name}</h3>
        <p className="bank">{recipient.beneficiaryBank.name}</p>
        <span className="account">Account: {recipient.accountNumber}</span>
      </div>
    </div>
  );
}
```


```






##### Understanding The Walkthrough

This trace demonstrates the **complete request/response lifecycle** from the moment a user opens the page until they see recipient cards rendered on screen. The flow follows Clean Architecture conventions: the React component (presentation layer) delegates to a custom hook, which calls an API client function. That function makes an HTTP request that crosses the network boundary into the Express server.

On the server side, the request flows inward through architectural layers: router → controller → service → repository → database. Each layer has a single responsibility. The router handles URL matching, the controller handles HTTP concerns (parsing params, sending responses), the service contains application logic (filtering), and the repository handles data access. Raw MongoDB documents are validated immediately using the shared `RecipientSchema`, ensuring only valid domain objects propagate through the system. This is the first "touch point" of shared logic.

The second touch point is the `Recipients` collection class, a domain aggregate from the shared package. Instead of a static utility like `RecipientFilters.activeOnly()`, we use a **domain-oriented approach**: `new Recipients(allRecipients).filterByStatus('Active')`. This reads naturally as "get recipients, filtered by Active status." The `Recipients` class encapsulates all filtering logic and can be instantiated on frontend or backend, ensuring the **exact same filtering behavior** everywhere. The response then travels back up the call stack and across the network, where the hook updates React state and triggers a re-render. The entire flow—from mount to display—typically completes in 100-300ms.

**Key Observations:**
- `RecipientSchema.parse()` validates data on backend (same schema usable on frontend)
- `Recipients.filterByStatus('Active')` is domain collection method used in service layer
- Frontend receives validated, typed `Recipient[]` with matching domain entities
- Each `RecipientCard` displays name, bank name, and masked account number per story requirements

---

---


## Strategies to Minimize Logic Duplication

The following strategies show how shared code eliminates duplication across client and server tiers. Each strategy references the domain participants and architecture flow diagrams described above.

### Strategy 1: Shared Validation Schemas

Define validation rules once using Zod or Yup in the shared package. Both `RecipientForm` (client) and `RecipientsController` (server) import and execute the same `RecipientSchema` and `SelectRecipientsSchema`. As shown in the Architecture Flow, the schema validates on the client before the HTTP call (fast feedback), then re-validates on the server (security). The `RecipientSchema.parse()` call in the repository ensures raw MongoDB documents become typed domain entities. Error messages like "Select at least one recipient" appear identically on client and server because they're defined once in the shared schema.

### Strategy 2: Domain Entities with Business Logic

Encapsulate business rules as methods and properties on shared domain classes. The `RecipientStatus` value object (shown in Domain Participants) provides `isEligibleForPayment()` and the `remainingPendingMinutes` property that enforce country-specific rules (MX 30-minute pending). The `Recipients` collection class wraps `Recipient[]` with `filterByStatus('Active')` and `search(query)` methods. As demonstrated in the walkthrough, the service layer instantiates these classes to apply business logic, and the frontend can use the same `Recipients.search()` for client-side filtering—both using identical code from the shared package.

### Strategy 3: Shared Type Definitions

Define TypeScript interfaces (`RecipientListResponse`, `SelectRecipientsRequest`) in the shared package. The API client (`recipients.api.ts`) and controller (`recipients.controller.ts`) both import these types, creating a compile-time contract. Per the Architecture Flow, when `useRecipients` calls `fetchRecipients()`, TypeScript knows the response shape; if a developer accesses `response.count` instead of `response.total`, the compiler catches it. Types are erased at runtime (zero cost) but catch API mismatches during development.



### Strategy Comparison

| Strategy | Where Logic Lives | When to Use |
|----------|------------------|-------------|
| **Shared Validation Schemas** | `@channelone/{domain}-shared` (Zod/Yup) | Forms, API input validation |
| **Domain Entities** | `@channelone/{domain}-shared` (classes) | Complex business rules, aggregates |
| **Shared Type Definitions** | `@channelone/{domain}-shared` (interfaces) | API contracts, type safety |


---


### Implementation Flow



#### Monorepo Setup with Turborepo

```json
// deploy/turbo.json (repo root: turbo --root-turbo-json deploy/turbo.json run <task>, or npm run turbo -- run <task>)
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["build"]
    },
    "lint": {}
  }
}
```

```json
// package.json (root)
{
  "name": "project-monorepo",
  "private": true,
  "workspaces": [
    "packages/*/shared",
    "packages/*/client",
    "packages/*/server",
    "packages/app-server",
    "packages/app-client"
  ],
  "devDependencies": {
    "turbo": "^2.0.0"
  },
  "scripts": {
    "build": "turbo run build",
    "test": "turbo run test",
    "dev": "turbo run dev --parallel"
  }
}
```

```json
// packages/recipients/shared/package.json
{
  "name": "@channelone/recipients-shared",
  "main": "index.ts",
  "types": "index.ts"
}

// packages/recipients/client/package.json
{
  "name": "@channelone/recipients-client",
  "dependencies": {
    "@channelone/recipients-shared": "*"
  }
}

// packages/recipients/server/package.json
{
  "name": "@channelone/recipients-server",
  "dependencies": {
    "@channelone/recipients-shared": "*"
  }
}
```

---

## Testing Architecture

Tests mirror story scenarios across three tiers: **Server-Side**, **Client-Side**, and **E2E**. Each tier tests the same scenarios with different emphasis based on what that layer is responsible for.

### Testing Philosophy

| Principle | Application |
|-----------|-------------|
| **Scenarios drive tests** | Story scenarios from the story graph drive all tests at every tier |
| **Given/When/Then structure** | Tests use explicit helper methods mirroring scenario steps: `givenUserLoggedIn()`, `whenUserSelectsRecipient()`, `thenRecipientIsHighlighted()` |
| **Same scenario, tier emphasis** | Server: receiving, validating, saving, returning. Client: submitting, rendering, navigating. E2E: complete user workflows |
| **Ubiquitous language** | Test names mirror Gherkin scenarios exactly: "user views list of active recipients when initiating wire payment" |
| **No isolated domain unit tests** | Domain logic is tested through server/client/E2E tests that exercise it in context |
| **Layer-specific adjustments OK** | Same scenario may emphasize different aspects per tier (see Story-to-Test Alignment) |

### Testing Pyramid - Story-Driven Spec by Example

Tests mirror story scenarios from the story graph. Each tier tests the **same scenarios** with different emphasis. Test files are organized by **domain/sub-epic** with tier suffixes:

| Tier | Tool | Emphasis | Location |
|------|------|----------|----------|
| **Server-Side** | Node.js Test Runner + Supertest | Receiving requests, validating, saving, returning responses | `tests/{epic}/{sub-epic}/*_server.test.ts` |
| **Client-Side** | Vitest + Testing Library | Submitting forms, rendering states, navigating flows | `tests/{epic}/{sub-epic}/*_client.test.tsx` |
| **E2E** | Playwright | Complete user workflows end-to-end | `tests/{epic}/{sub-epic}/*_e2e.spec.ts` |

**Test Folder Structure (domain-first, tier suffixes):**

**CRITICAL HIERARCHY RULE (mirrors Python agile_bots/test pattern):**
| Story Graph Level | Maps To | Example |
|-------------------|---------|---------|
| Epic | Folder | `tests/create-wire-payment/` |
| Higher Sub-Epic | Folder | `tests/create-wire-payment/select-recipient/` |
| **Lowest Sub-Epic** | **File** (3 per tier) | `select-recipient_server.test.ts` |
| Story | Test Class | `class TestViewActiveRecipients { ... }` |
| Scenario | Test Method | `async test_user_views_list_of_active_recipients() { ... }` |

  ```
  project-root/
├── tests/
│   ├── create-wire-payment/                    # Epic: Create Wire Payment
│   │   ├── select-recipient/                   # Sub-Epic: Select Recipient (lowest level)
│   │   │   ├── helpers/
│   │   │   │   ├── select-recipient.base.ts          # Shared test data & abstract helpers
│   │   │   │   ├── select-recipient.server.ts        # Server-tier helper (Supertest)
│   │   │   │   ├── select-recipient.client.ts        # Client-tier helper (Testing Library)
│   │   │   │   └── select-recipient.e2e.ts           # E2E-tier helper (Playwright)
│   │   │   ├── select-recipient_server.test.ts       # ONE file per sub-epic per tier
│   │   │   ├── select-recipient_client.test.tsx      # Contains ALL stories as describe blocks
│   │   │   └── select-recipient_e2e.spec.ts          # Contains ALL scenarios as it() methods
│   │   │
│   │   ├── enter-payment-details/              # Sub-Epic: Enter Payment Details (lowest level)
│   │   │   ├── helpers/
│   │   │   │   ├── enter-payment-details.base.ts
│   │   │   │   ├── enter-payment-details.server.ts
│   │   │   │   ├── enter-payment-details.client.ts
│   │   │   │   └── enter-payment-details.e2e.ts
│   │   │   ├── enter-payment-details_server.test.ts
│   │   │   ├── enter-payment-details_client.test.tsx
│   │   │   └── enter-payment-details_e2e.spec.ts
│   │   │
│   │   └── review-and-submit/                  # Sub-Epic: Review and Submit (lowest level)
│   │       ├── helpers/
│   │       ├── review-and-submit_server.test.ts
│   │       ├── review-and-submit_client.test.tsx
│   │       └── review-and-submit_e2e.spec.ts
│   │
│   ├── manage-recipients/                      # Epic: Manage Recipients
│   │   ├── add-recipient/                      # Sub-Epic: Add Recipient (lowest level)
│   │   │   ├── helpers/
│   │   │   ├── add-recipient_server.test.ts
│   │   │   ├── add-recipient_client.test.tsx
│   │   │   └── add-recipient_e2e.spec.ts
│   │   │
│   │   └── edit-recipient/                     # Sub-Epic: Edit Recipient (lowest level)
│   │       ├── edit-recipient_server.test.ts
│   │       ├── edit-recipient_client.test.tsx
│   │       └── edit-recipient_e2e.spec.ts
│   │
│   └── approve-payment/                        # Epic: Approve and Authorize Payment
│       └── ...
│
├── packages/                                   # Source code (domain modules)
│   ├── recipients/
│   ├── payments/
│   └── ...
```

**Inside Each Test File - Class per Story, Method per Scenario:**

Following the Python test structure pattern from `agile_bots/test/`:

```typescript
// select-recipient_server.test.ts
// File = Sub-Epic, Class = Story, Method = Scenario

import { beforeEach, afterEach } from 'node:test';
import { SelectRecipientServerHelper } from './helpers/select-recipient.server';

// ============================================================================
// STORY: View Active Recipients
// ============================================================================

class TestViewActiveRecipients {
  helper = new SelectRecipientServerHelper();

  async setup() { await this.helper.setup(); }
  async cleanup() { await this.helper.cleanup(); }

  /**
   * SCENARIO: user views list of active recipients when initiating wire payment
   * GIVEN: User is logged into ChannelOne
   * AND: Enterprise has Recipients with Active status
   * WHEN: User initiates wire payment
   * THEN: Only Active recipients are displayed
   */
  async test_user_views_list_of_active_recipients_when_initiating_wire_payment() {
    await this.helper.givenUserLoggedIntoChannelOne();
    await this.helper.givenEnterpriseHasRecipientsWithActiveStatus();
    await this.helper.whenUserInitiatesWirePayment();
    await this.helper.thenOnlyActiveRecipientsDisplayed();
  }

  /**
   * SCENARIO: user sees empty state when no active recipients exist
   * GIVEN: User is logged into ChannelOne
   * AND: Enterprise has no recipients
   * WHEN: User initiates wire payment
   * THEN: Empty state is displayed
   */
  async test_user_sees_empty_state_when_no_active_recipients_exist() {
    await this.helper.givenUserLoggedIntoChannelOne();
    await this.helper.givenEnterpriseHasNoRecipients();
    await this.helper.whenUserInitiatesWirePayment();
    await this.helper.thenEmptyStateDisplayed();
  }
}

// ============================================================================
// STORY: Select Recipient For Payment
// ============================================================================

class TestSelectRecipientForPayment {
  helper = new SelectRecipientServerHelper();

  async setup() { await this.helper.setup(); }
  async cleanup() { await this.helper.cleanup(); }

  /**
   * SCENARIO: user selects a recipient from the list
   * GIVEN: Active recipients are displayed
   * WHEN: User selects a recipient
   * THEN: Recipient selection is confirmed
   */
  async test_user_selects_a_recipient_from_the_list() {
    await this.helper.givenActiveRecipientsDisplayed();
    await this.helper.whenUserSelectsRecipient();
    await this.helper.thenRecipientSelectionConfirmed();
  }

  /**
   * SCENARIO: user cannot proceed without selecting a recipient
   * GIVEN: Active recipients are displayed
   * WHEN: User attempts to proceed without selection
   * THEN: Validation error is displayed
   */
  async test_user_cannot_proceed_without_selecting_a_recipient() {
    await this.helper.givenActiveRecipientsDisplayed();
    await this.helper.whenUserAttemptsToProceesWithoutSelection();
    await this.helper.thenValidationErrorDisplayed();
  }
}

// Test runner registration (framework-specific)
export { TestViewActiveRecipients, TestSelectRecipientForPayment };
```

---

### Story-to-Test Alignment

Each story's scenarios drive tests at multiple layers. The **same scenario** appears in different test files with layer-appropriate emphasis:

```
Story: "User views list of active recipients when initiating wire payment"

┌─────────────────────────────────────────────────────────────────────┐
│  SERVER TEST                                                        │
│  Emphasis: receiving, validating, saving, returning                 │
│  ─────────────────────────────────────────────────────────────────  │
│  Given: Enterprise has Recipients with Active status                │
│  When:  Server receives GET /api/recipients?activeOnly=true         │
│  Then:  Response includes only Active recipients                    │
│         Response includes recipient name, bank name, masked account │
│         Pending/Inactive recipients are excluded from response      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  CLIENT TEST                                                        │
│  Emphasis: submitting, rendering, navigating                        │
│  ─────────────────────────────────────────────────────────────────  │
│  Given: API returns list of active recipients                       │
│  When:  User lands on recipient selection step                      │
│  Then:  RecipientSelection renders recipient cards                  │
│         Each card displays name, bank name, masked account          │
│         Selection highlights recipient and enables Continue button  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  E2E TEST                                                           │
│  Emphasis: complete workflow, all layers integrated                 │
│  ─────────────────────────────────────────────────────────────────  │
│  Given: User is logged in with wire creation entitlement            │
│         Enterprise has active recipients in database                │
│  When:  User navigates to Create Wire Payment                       │
│  Then:  Step 1 displays with active recipients only                 │
│         User can select recipient and proceed to Step 2             │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Test Structure Pattern (Given/When/Then Helpers)

Tests use helper classes with explicit given/when/then methods that mirror scenario steps. Helpers use **inheritance** to share common setup logic while allowing tier-specific implementations:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SelectRecipientBaseHelper (abstract)                                       │
│  ───────────────────────────────────────                                    │
│  Shared test data definitions and scenario step signatures                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  # Test Data (shared across all tiers)                                      │
│  ACTIVE_RECIPIENTS = [                                                      │
│    { name: 'Acme Corporation', status: 'Active', bankName: 'Chase Bank' }   │
│  ]                                                                          │
│                                                                             │
│  # Abstract methods - each tier implements HOW                              │
│  abstract seedRecipients(data[]): Promise<void>                             │
│  abstract cleanup(): Promise<void>                                          │
│  abstract executeAction(): Promise<void>                                    │
│                                                                             │
│  # Concrete GIVEN methods - call abstract implementations                   │
│  givenEnterpriseHasRecipientsWithActiveStatus() {                           │
│    await this.seedRecipients(ACTIVE_RECIPIENTS);                            │
│  }                                                                          │
│  givenEnterpriseHasNoActiveRecipients() {                                   │
│    await this.cleanup();                                                    │
│  }                                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
           │                        │                        │
           ▼                        ▼                        ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│  ServerHelper       │  │  ClientHelper       │  │  E2EHelper          │
│  extends Base       │  │  extends Base       │  │  extends Base       │
├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤
│ seedRecipients() {  │  │ seedRecipients() {  │  │ seedRecipients() {  │
│   // MongoDB insert │  │   // vi.mock API    │  │   // seed API call  │
│ }                   │  │ }                   │  │ }                   │
│                     │  │                     │  │                     │
│ whenUserInitiates() │  │ whenUserSelects() { │  │ whenUserSelects() { │
│   // Supertest req  │  │   // userEvent      │  │   // page.click     │
│ }                   │  │ }                   │  │ }                   │
│                     │  │                     │  │                     │
│ thenActiveOnly() {  │  │ thenHighlighted() { │  │ thenHighlighted() { │
│   // assert(resp)   │  │   // screen.get     │  │   // expect(loc)    │
│ }                   │  │ }                   │  │ }                   │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

#### Base Helper (Shared Logic)

```typescript
// tests/create-wire-payment/select-recipient/helpers/select-recipient.base.ts

export interface RecipientData {
  name: string;
  status: 'Active' | 'Pending' | 'Inactive';
  bankName: string;
  accountMasked: string;
}

export abstract class SelectRecipientBaseHelper {
  protected enterprise: { id: string };
  protected user: { token: string };

  // Shared test data - same across all tiers
  static readonly ACTIVE_RECIPIENTS: RecipientData[] = [
    { name: 'Acme Corporation', status: 'Active', bankName: 'Chase Bank', accountMasked: '****1234' },
    { name: 'Global Supplies LLC', status: 'Active', bankName: 'Bank of America', accountMasked: '****5678' },
  ];

  static readonly MIXED_STATUS_RECIPIENTS: RecipientData[] = [
    { name: 'Active Vendor Inc', status: 'Active', bankName: 'Chase Bank', accountMasked: '****1111' },
    { name: 'Pending Vendor LLC', status: 'Pending', bankName: 'Wells Fargo', accountMasked: '****2222' },
    { name: 'Inactive Supplier', status: 'Inactive', bankName: 'Citi', accountMasked: '****3333' },
  ];

  // Abstract methods - each tier implements HOW to do these
  protected abstract seedRecipients(data: RecipientData[]): Promise<void>;
  protected abstract seedUser(options: { hasWireEntitlement: boolean }): Promise<void>;
  abstract cleanup(): Promise<void>;

  // Concrete GIVEN methods - shared scenario step logic
  async givenUserLoggedIntoChannelOne(options = { hasWireEntitlement: true }): Promise<void> {
    await this.seedUser(options);
  }

  async givenEnterpriseHasRecipientsWithActiveStatus(
    data: RecipientData[] = SelectRecipientBaseHelper.ACTIVE_RECIPIENTS
  ): Promise<void> {
    await this.seedRecipients(data);
  }

  async givenEnterpriseHasRecipientsWithMixedStatuses(
    data: RecipientData[] = SelectRecipientBaseHelper.MIXED_STATUS_RECIPIENTS
  ): Promise<void> {
    await this.seedRecipients(data);
  }

  async givenEnterpriseHasNoActiveRecipients(): Promise<void> {
    await this.cleanup();
  }
}
```

#### Server Helper (Supertest + Node.js Test Runner)

```typescript
// tests/create-wire-payment/select-recipient/helpers/select-recipient.server.ts

import request from 'supertest';
import assert from 'node:assert';
import { SelectRecipientBaseHelper, RecipientData } from './select-recipient.base';
import { app } from '@channelone/app-server';
import { db } from '@channelone/app-server-db';

export class SelectRecipientServerHelper extends SelectRecipientBaseHelper {
  private response: request.Response;

  // Implement abstract: seed directly to MongoDB
  protected async seedRecipients(data: RecipientData[]): Promise<void> {
    this.enterprise = { id: 'test-enterprise-id' };
    await db.collection('recipients').insertMany(
      data.map(r => ({ ...r, enterpriseId: this.enterprise.id }))
    );
  }

  protected async seedUser(options: { hasWireEntitlement: boolean }): Promise<void> {
    this.user = await createTestUser({ 
      enterpriseId: this.enterprise.id,
      hasWireCreationEntitlement: options.hasWireEntitlement 
    });
  }

  async cleanup(): Promise<void> {
    await db.collection('recipients').deleteMany({});
    await db.collection('users').deleteMany({});
  }

  // WHEN helpers - use Supertest for HTTP requests
  async whenUserInitiatesCreateWirePayment(): Promise<void> {
    this.response = await request(app)
      .get('/api/recipients')
      .query({ activeOnly: 'true', enterpriseId: this.enterprise.id })
      .set('Authorization', `Bearer ${this.user.token}`);
  }

  async whenUserAttemptsToAccessWirePayment(): Promise<void> {
    this.response = await request(app)
      .get('/api/recipients')
      .set('Authorization', `Bearer ${this.user.token}`);
  }

  // THEN helpers - assert on HTTP Response
  thenRecipientSelectionIncludesActiveRecipientsOnly(expectedNames: string[]): void {
    assert.strictEqual(this.response.status, 200);
    const actualNames = this.response.body.recipients.map(r => r.name);
    assert.deepStrictEqual(actualNames.sort(), expectedNames.sort());
    for (const r of this.response.body.recipients) {
      assert.strictEqual(r.status, 'Active');
    }
  }

  thenPendingAndInactiveExcluded(excludedNames: string[]): void {
    const actualNames = this.response.body.recipients.map(r => r.name);
    for (const name of excludedNames) {
      assert.ok(!actualNames.includes(name), `${name} should be excluded`);
    }
  }

  thenRecipientIncludesBankDetails(): void {
    for (const r of this.response.body.recipients) {
      assert.ok(r.beneficiaryBank.name, 'Missing bank name');
      assert.match(r.accountNumber, /^\*{4}\d{4}$/, 'Account not masked');
    }
  }

  thenEmptyStateReturned(): void {
    assert.strictEqual(this.response.status, 200);
    assert.strictEqual(this.response.body.recipients.length, 0);
  }

  thenAccessDeniedWithMessage(expectedMessage: string): void {
    assert.strictEqual(this.response.status, 403);
    assert.strictEqual(this.response.body.message, expectedMessage);
  }
}
```

#### Client Helper (Vitest + Testing Library)

```typescript
// tests/create-wire-payment/select-recipient/helpers/select-recipient.client.ts

import { vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SelectRecipientBaseHelper, RecipientData } from './select-recipient.base';
import { RecipientSelectionStep } from '@channelone/recipients-client';
import * as api from '@channelone/recipients-client/recipients.api';

vi.mock('@channelone/recipients-client/recipients.api');

export class SelectRecipientClientHelper extends SelectRecipientBaseHelper {
  private container: ReturnType<typeof render>;

  // Implement abstract: mock API response instead of seeding DB
  protected async seedRecipients(data: RecipientData[]): Promise<void> {
    vi.mocked(api.fetchRecipients).mockResolvedValue(
      data.filter(r => r.status === 'Active').map((r, i) => ({
        id: String(i + 1),
        name: r.name,
        bankName: r.bankName,
        accountMasked: r.accountMasked,
        status: r.status,
      }))
    );
  }

  protected async seedUser(options: { hasWireEntitlement: boolean }): Promise<void> {
    if (!options.hasWireEntitlement) {
      vi.mocked(api.fetchRecipients).mockRejectedValue({
        status: 403,
        message: 'You do not have permission to create wire payments'
      });
    }
  }

  async cleanup(): Promise<void> {
    vi.resetAllMocks();
    vi.mocked(api.fetchRecipients).mockResolvedValue([]);
  }

  // WHEN helpers - render and interact via Testing Library
  async whenUserLandsOnRecipientSelection(): Promise<void> {
    this.container = render(<RecipientSelectionStep enterpriseId="acme-corp" />);
    await waitFor(() => {
      // Wait for loading to complete
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
    });
  }

  async whenUserSelectsRecipient(name: string): Promise<void> {
    await userEvent.click(screen.getByText(name));
  }

  async whenUserClicksContinue(): Promise<void> {
    await userEvent.click(screen.getByRole('button', { name: /continue/i }));
  }

  // THEN helpers - assert via screen queries
  thenRecipientIsDisplayed(name: string): void {
    expect(screen.getByText(name)).toBeInTheDocument();
  }

  thenRecipientIsHighlighted(name: string): void {
    expect(screen.getByText(name).closest('[data-selected]')).toHaveAttribute('data-selected', 'true');
  }

  thenContinueButtonEnabled(): void {
    expect(screen.getByRole('button', { name: /continue/i })).not.toBeDisabled();
  }

  thenContinueButtonDisabled(): void {
    expect(screen.getByRole('button', { name: /continue/i })).toBeDisabled();
  }

  thenEmptyStateDisplayed(): void {
    expect(screen.getByText('No active recipients available')).toBeInTheDocument();
  }

  thenAccessDeniedDisplayed(message: string): void {
    expect(screen.getByText(message)).toBeInTheDocument();
  }
}
```

#### E2E Helper (Playwright)

```typescript
// tests/create-wire-payment/select-recipient/helpers/select-recipient.e2e.ts

import { Page, expect } from '@playwright/test';
import { SelectRecipientBaseHelper, RecipientData } from './select-recipient.base';

export class SelectRecipientE2EHelper extends SelectRecipientBaseHelper {
  constructor(private readonly page: Page) {
    super();
  }

  // Implement abstract: seed via API endpoint or fixture
  protected async seedRecipients(data: RecipientData[]): Promise<void> {
    await this.page.request.post('/api/test/seed-recipients', {
      data: { recipients: data }
    });
  }

  protected async seedUser(options: { hasWireEntitlement: boolean }): Promise<void> {
    // Login via page (handled in test beforeEach)
  }

  async cleanup(): Promise<void> {
    await this.page.request.post('/api/test/cleanup');
  }

  // WHEN helpers - Playwright page interactions
  async whenUserNavigatesToCreateWirePayment(): Promise<void> {
    await this.page.goto('/wire-payment/create');
    await this.page.waitForSelector('[data-testid="recipient-list"]');
  }

  async whenUserSelectsRecipient(name: string): Promise<void> {
    await this.page.getByText(name).click();
  }

  async whenUserClicksContinue(): Promise<void> {
    await this.page.getByRole('button', { name: /continue/i }).click();
  }

  // THEN helpers - Playwright assertions
  async thenRecipientIsDisplayed(name: string): Promise<void> {
    await expect(this.page.getByText(name)).toBeVisible();
  }

  async thenRecipientIsHighlighted(name: string): Promise<void> {
    await expect(this.page.getByText(name).locator('..')).toHaveAttribute('data-selected', 'true');
  }

  async thenContinueButtonEnabled(): Promise<void> {
    await expect(this.page.getByRole('button', { name: /continue/i })).toBeEnabled();
  }

  async thenNavigatedToPaymentDetails(): Promise<void> {
    await expect(this.page).toHaveURL(/.*payment-details/);
  }

  async thenEmptyStateDisplayed(): Promise<void> {
    await expect(this.page.getByText('No active recipients available')).toBeVisible();
  }
}
```
---

### Server-Side Tests

**Emphasis: Receiving requests, validating data, saving state, returning responses**

Server tests mirror story scenarios with focus on what the server receives and returns. **One file per sub-epic** containing all stories as classes, with scenarios as methods. Pattern matches `agile_bots/test/` structure.

``` typescript
// tests/create-wire-payment/select-recipient/select-recipient_server.test.ts
// File = Sub-Epic, Class = Story, Method = Scenario (mirrors Python test pattern)

import { SelectRecipientServerHelper } from './helpers/select-recipient.server';

// ============================================================================
// STORY: View Active Recipients for Wire Payment
// Sub-Epic: Select Recipient | Epic: Create Wire Payment
// Server emphasis: Receiving request, filtering by status, returning active recipients only
// ============================================================================

class TestViewActiveRecipientsForWirePayment {
  helper = new SelectRecipientServerHelper();

  async cleanup() { await this.helper.cleanup(); }

  /**
   * SCENARIO: User views list of active recipients when initiating wire payment
   * GIVEN: User is logged into ChannelOne 2.0
   * AND: Enterprise has Recipients with Active status
   * WHEN: Server receives GET /api/recipients?activeOnly=true
   * THEN: Response includes only Active recipients
   */
  async test_user_views_list_of_active_recipients_when_initiating_wire_payment() {
    await this.helper.givenUserLoggedIntoChannelOne();
    await this.helper.givenEnterpriseHasRecipientsWithActiveStatus([
      { name: 'Acme Corporation', status: 'Active', bankName: 'Chase Bank', accountMasked: '****1234' },
      { name: 'Global Supplies LLC', status: 'Active', bankName: 'Bank of America', accountMasked: '****5678' },
      { name: 'Tech Solutions Inc', status: 'Active', bankName: 'Wells Fargo', accountMasked: '****9012' },
    ]);

    await this.helper.whenUserInitiatesCreateWirePayment();

    this.helper.thenRecipientSelectionIncludesActiveRecipientsOnly([
      'Acme Corporation', 'Global Supplies LLC', 'Tech Solutions Inc'
    ]);
    this.helper.thenRecipientIncludesBankDetails();
  }

  /**
   * SCENARIO: System excludes pending recipients from wire payment selection
   * GIVEN: Enterprise has Recipients with mixed statuses
   * WHEN: Server receives GET /api/recipients?activeOnly=true
   * THEN: Only Active recipients returned, Pending/Inactive excluded
   */
  async test_system_excludes_pending_recipients_from_wire_payment_selection() {
    await this.helper.givenUserLoggedIntoChannelOne();
    await this.helper.givenEnterpriseHasRecipientsWithMixedStatuses([
      { name: 'Active Vendor Inc', status: 'Active' },
      { name: 'New Vendor LLC', status: 'Pending' },
      { name: 'Old Supplier Corp', status: 'Inactive' },
    ]);

    await this.helper.whenUserInitiatesCreateWirePayment();

    this.helper.thenRecipientSelectionIncludesActiveRecipientsOnly(['Active Vendor Inc']);
    this.helper.thenPendingAndInactiveExcluded(['New Vendor LLC', 'Old Supplier Corp']);
  }

  /**
   * SCENARIO: System displays empty state when no active recipients exist
   * GIVEN: Enterprise has no active recipients
   * WHEN: Server receives GET /api/recipients?activeOnly=true
   * THEN: Response returns empty list with guidance
   */
  async test_system_displays_empty_state_when_no_active_recipients_exist() {
    await this.helper.givenUserLoggedIntoChannelOne();
    await this.helper.givenEnterpriseHasNoActiveRecipients();

    await this.helper.whenUserInitiatesCreateWirePayment();

    this.helper.thenEmptyStateReturned();
  }

  /**
   * SCENARIO: User without wire creation entitlement cannot view recipient selection
   * GIVEN: User does not have WirePayment.Create entitlement
   * WHEN: Server receives GET /api/recipients
   * THEN: Response returns 403 with access denied message
   */
  async test_user_without_wire_creation_entitlement_cannot_view_recipient_selection() {
    await this.helper.givenUserLoggedIntoChannelOne({ hasWireEntitlement: false });
    await this.helper.givenEnterpriseHasRecipientsWithActiveStatus([]);

    await this.helper.whenUserAttemptsToAccessWirePayment();

    this.helper.thenAccessDeniedWithMessage('You do not have permission to create wire payments');
  }
}

export { TestViewActiveRecipientsForWirePayment };
```

---

### Client-Side Tests

**Emphasis: Submitting requests, rendering state, navigating between steps**

Client tests mirror the SAME story scenarios with focus on what the user sees and interacts with. **One file per sub-epic** containing all stories as classes, each with scenarios as methods.

```typescript
// tests/create-wire-payment/select-recipient/select-recipient_client.test.tsx
// File = Sub-Epic, Class = Story, Method = Scenario (mirrors Python test pattern)

import { SelectRecipientClientHelper } from './helpers/select-recipient.client';

// ============================================================================
// STORY: View Active Recipients for Wire Payment
// Sub-Epic: Select Recipient | Epic: Create Wire Payment
// Client emphasis: Rendering recipient list, displaying details, handling empty state
// ============================================================================

class TestViewActiveRecipientsForWirePayment {
  helper = new SelectRecipientClientHelper();

  async cleanup() { await this.helper.cleanup(); }

  /**
   * SCENARIO: User views list of active recipients when initiating wire payment
   * GIVEN: Enterprise has Recipients with Active status (mocked API)
   * WHEN: User lands on recipient selection step
   * THEN: RecipientSelection renders active recipients
   */
  async test_user_views_list_of_active_recipients_when_initiating_wire_payment() {
    await this.helper.givenEnterpriseHasRecipientsWithActiveStatus();
    await this.helper.whenUserLandsOnRecipientSelection();
    this.helper.thenRecipientIsDisplayed('Acme Corporation');
    this.helper.thenRecipientIsDisplayed('Global Supplies LLC');
  }

  /**
   * SCENARIO: System displays empty state when no active recipients exist
   * GIVEN: No active recipients exist
   * WHEN: User lands on recipient selection step
   * THEN: RecipientSelection indicates no active Recipients available
   */
  async test_system_displays_empty_state_when_no_active_recipients_exist() {
    await this.helper.givenEnterpriseHasNoActiveRecipients();
    await this.helper.whenUserLandsOnRecipientSelection();
    this.helper.thenEmptyStateDisplayed();
  }

  /**
   * SCENARIO: User without wire creation entitlement cannot view recipient selection
   * GIVEN: User does not have wire entitlement
   * WHEN: User attempts to view recipient selection
   * THEN: System displays access denied message
   */
  async test_user_without_wire_creation_entitlement_cannot_view_recipient_selection() {
    await this.helper.givenUserLoggedIntoChannelOne({ hasWireEntitlement: false });
    await this.helper.whenUserLandsOnRecipientSelection();
    this.helper.thenAccessDeniedDisplayed('You do not have permission to create wire payments');
  }
}

// ============================================================================
// STORY: Select Recipient for Wire Payment
// Sub-Epic: Select Recipient | Epic: Create Wire Payment
// Client emphasis: Selection highlighting, enabling Continue button, navigation
// ============================================================================

class TestSelectRecipientForWirePayment {
  helper = new SelectRecipientClientHelper();

  async cleanup() { await this.helper.cleanup(); }

  /**
   * SCENARIO: User selects recipient and proceeds to payment details
   * GIVEN: Enterprise has Recipients with Active status
   * WHEN: User lands on recipient selection step and selects Recipient
   * THEN: RecipientSelection highlights selected recipient and enables Continue
   */
  async test_user_selects_recipient_and_proceeds_to_payment_details() {
    await this.helper.givenEnterpriseHasRecipientsWithActiveStatus();
    await this.helper.whenUserLandsOnRecipientSelection();
    await this.helper.whenUserSelectsRecipient('Acme Corporation');
    this.helper.thenRecipientIsHighlighted('Acme Corporation');
    this.helper.thenContinueButtonEnabled();
  }

  /**
   * SCENARIO: Continue button disabled when no recipient selected
   * GIVEN: Enterprise has Recipients with Active status
   * WHEN: User lands on recipient selection step (no selection made)
   * THEN: Progression to payment details is disabled
   */
  async test_continue_button_disabled_when_no_recipient_selected() {
    await this.helper.givenEnterpriseHasRecipientsWithActiveStatus();
    await this.helper.whenUserLandsOnRecipientSelection();
    this.helper.thenContinueButtonDisabled();
  }
}

export { TestViewActiveRecipientsForWirePayment, TestSelectRecipientForWirePayment };
```

---

### E2E Tests with Playwright

**Emphasis: Complete user workflows from login to confirmation**

E2E tests mirror the SAME story scenarios testing the complete flow across all layers. **One file per sub-epic** containing all stories as classes. The E2E helper inherits from the base helper and wraps Playwright page interactions.

```typescript
// tests/create-wire-payment/select-recipient/select-recipient_e2e.spec.ts
// File = Sub-Epic, Class = Story, Method = Scenario (mirrors Python test pattern)

import { Page } from '@playwright/test';
import { SelectRecipientE2EHelper } from './helpers/select-recipient.e2e';
import { LoginPage } from './pages/login.page';

// ============================================================================
// STORY: View Active Recipients for Wire Payment
// Sub-Epic: Select Recipient | Epic: Create Wire Payment
// E2E emphasis: Complete user workflows from login through step completion
// ============================================================================

class TestViewActiveRecipientsForWirePayment {
  helper: SelectRecipientE2EHelper;
  page: Page;

  async setup(page: Page) {
    this.page = page;
    this.helper = new SelectRecipientE2EHelper(page);
    const loginPage = new LoginPage(page);
    await loginPage.loginAs('jane.doe@acme.com', { entitlement: 'WirePayment.Create' });
  }

  async cleanup() { await this.helper.cleanup(); }

  /**
   * SCENARIO: user views list of active recipients when initiating wire payment
   * GIVEN: Enterprise has Recipients with Active status
   * WHEN: User initiates Create Wire Payment
   * THEN: RecipientSelection includes Active Recipients
   */
  async test_user_views_list_of_active_recipients_when_initiating_wire_payment() {
    await this.helper.givenEnterpriseHasRecipientsWithActiveStatus();
    await this.helper.whenUserNavigatesToCreateWirePayment();
    await this.helper.thenRecipientIsDisplayed('Acme Corporation');
    await this.helper.thenRecipientIsDisplayed('Global Supplies LLC');
  }

  /**
   * SCENARIO: system displays empty state when no active recipients exist
   * GIVEN: No active recipients exist
   * WHEN: User initiates Create Wire Payment
   * THEN: RecipientSelection indicates no active Recipients available
   */
  async test_system_displays_empty_state_when_no_active_recipients_exist() {
    await this.helper.givenEnterpriseHasNoActiveRecipients();
    await this.helper.whenUserNavigatesToCreateWirePayment();
    await this.helper.thenEmptyStateDisplayed();
  }
}

// ============================================================================
// STORY: Select Recipient for Wire Payment
// Sub-Epic: Select Recipient | Epic: Create Wire Payment
// E2E emphasis: Complete flow from viewing to selection to next step
// ============================================================================

class TestSelectRecipientForWirePayment {
  helper: SelectRecipientE2EHelper;
  page: Page;

  async setup(page: Page) {
    this.page = page;
    this.helper = new SelectRecipientE2EHelper(page);
    const loginPage = new LoginPage(page);
    await loginPage.loginAs('jane.doe@acme.com', { entitlement: 'WirePayment.Create' });
  }

  async cleanup() { await this.helper.cleanup(); }

  /**
   * SCENARIO: user selects recipient and proceeds to payment details
   * GIVEN: Enterprise has Recipients with Active status
   * WHEN: User navigates to Create Wire Payment and selects Recipient
   * THEN: RecipientSelection highlights selected and enables progression
   */
  async test_user_selects_recipient_and_proceeds_to_payment_details() {
    await this.helper.givenEnterpriseHasRecipientsWithActiveStatus();
    await this.helper.whenUserNavigatesToCreateWirePayment();
    await this.helper.whenUserSelectsRecipient('Acme Corporation');
    await this.helper.thenRecipientIsHighlighted('Acme Corporation');
    await this.helper.thenContinueButtonEnabled();
    await this.helper.whenUserClicksContinue();
    await this.helper.thenNavigatedToPaymentDetails();
  }
}

export { TestViewActiveRecipientsForWirePayment, TestSelectRecipientForWirePayment };
```

---

### Test Configuration

```json
// package.json (root) - monorepo test scripts
{
  "scripts": {
    "test": "turbo run test",
    "test:server": "node --import tsx --test tests/**/*_server.test.ts",
    "test:client": "vitest run -c tests/vitest/vitest.config.ts",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui"
  }
}
```

```typescript
// tests/vitest/vitest.config.ts (run: vitest run -c tests/vitest/vitest.config.ts)
// root = repo root; setup: tests/vitest/vitest.setup.ts
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.join(__dirname, '..', '..');

export default defineConfig({
  root: repoRoot,
  plugins: [react()],
  test: {
    environment: 'jsdom',
    include: ['tests/**/*_client.test.{ts,tsx}'],
    setupFiles: [path.join(__dirname, 'vitest.setup.ts')],
    globals: true,
  },
});
```

```typescript
// tests/playwright/playwright.config.ts (run: playwright test -c tests/playwright/playwright.config.ts)
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '../', // parent of tests/playwright — story-aligned specs under tests/
  testMatch: '**/*_e2e.spec.ts',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## References
