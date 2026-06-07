/**
 * domain-module.ts - Structural index for the domain-module/ template folder.
 *
 * The full template has been split into the domain-module/ folder which mirrors
 * the real package layout an agent should generate for each domain:
 *
 *   domain-module/
 *     shared/          Domain core - entities, value objects, Zod schemas, collection classes
 *     server/          Express tier - repository, service, controller, routes
 *     client/          React tier - API client, hook, ListView, CardView, CreateView, DetailView
 *     _lib/            Stub types - ambient declarations for zod, mongodb, express, react
 *     tsconfig.json    TypeScript config with path aliases
 *
 * HOW TO USE:
 *   1. Copy domain-module/ as packages/{yourDomain}/
 *   2. Replace every 'DomainName' (PascalCase) with your entity name, e.g. Recipient.
 *   3. Replace every 'domainName' (camelCase) with the lowercase plural, e.g. recipients.
 *   4. Replace every 'appName' with a purpose-derived app scope, e.g. taskflow, payhub.
 *   5. Delete _lib/ and tsconfig.json - use real npm packages in your project.
 *   6. Run peer-review against mern-technical-architecture rules before opening a PR.
 *
 * KEY RULES:
 *   - Package names use pattern @{appName}/{domainName}-{tier} (valid npm, one slash only).
 *   - Never use generic placeholders like @project or @acme - derive from app purpose.
 *   - Domain logic belongs on domain classes in shared/, not in services.
 *   - shared/ has ZERO framework imports (no Express, no React, no MongoDB).
 *   - Both client/ and server/ import from shared/ - never duplicate.
 *   - Zod schemas validate at repository boundary (server) AND form boundary (client).
 *   - Tests mirror Gherkin scenarios: Given/When/Then helpers, 3 tiers per sub-epic.
 *   - Method names match the domain verb in EVERY layer (shared, API client, controller, service, route).
 *   - Arg names are preserved across layers - only the type narrows, not the name.
 *   - TypeScript uses camelCase; JSON/HTTP bodies use snake_case.
 *   - All mutations return the same aggregate snapshot type.
 *   - React components end with View: DomainNameListView, DomainNameCardView, CreateDomainNameView.
 *
 * CLIENT COMPLETENESS:
 *   - The API client (domainName.api.ts) must export one function per server route, using the same domain verb name.
 *   - Provide a creation view (CreateDomainNameView.tsx) only when the specs define a user-facing create action.
 *   - POST endpoints may be user-facing or system-only; do not mirror server routes into UI mechanically.
 *   - For entities with sub-item operations, provide a detail view (DomainNameDetailView.tsx).
 *   - The list component (DomainNameListView.tsx) accepts an onSelectItem callback for navigation.
 *   - The card component (DomainNameCardView.tsx) accepts an onSelect callback for click-to-navigate.
 *   - The app-client composition root (App.tsx) must manage view state to navigate
 *     between list, create, and detail views. Never render a single static component.
 *
 * Reference: inputs/mern-architecture.md for the authoritative architecture guide.
 */
export {};