/**
 * domain-module.ts - Structural index for the domain-module/ template folder.
 *
 * The full template has been split into the domain-module/ folder which mirrors
 * the real package layout an agent should generate for each domain:
 *
 *   domain-module/
 *     shared/          Domain core - entities, value objects, Zod schemas, collection classes
 *     server/          Express tier - repository, service, controller, routes
 *     client/          React tier - API client, hook, list component, card component
 *     _lib/            Stub types - ambient declarations for zod, mongodb, express, react
 *     tsconfig.json    TypeScript config with path aliases
 *
 * HOW TO USE:
 *   1. Copy domain-module/ as packages/{yourDomain}/
 *   2. Replace every 'DomainName' (PascalCase) with your entity name, e.g. Recipient.
 *   3. Replace every 'domainName' (camelCase) with the lowercase plural, e.g. recipients.
 *   4. Delete _lib/ and tsconfig.json - use real npm packages in your project.
 *   5. Run peer-review against mern-technical-architecture rules before opening a PR.
 *
 * KEY RULES:
 *   - Domain logic belongs on domain classes in shared/, not in services.
 *   - shared/ has ZERO framework imports (no Express, no React, no MongoDB).
 *   - Both client/ and server/ import from shared/ - never duplicate.
 *   - Zod schemas validate at repository boundary (server) AND form boundary (client).
 *   - Tests mirror Gherkin scenarios: Given/When/Then helpers, 3 tiers per sub-epic.
 *
 * Reference: inputs/mern-architecture.md for the authoritative architecture guide.
 */
export {};