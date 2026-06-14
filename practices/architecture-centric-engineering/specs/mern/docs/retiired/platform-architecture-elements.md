# MERN Domain-First — Platform Architecture Elements

> **Diagram:** `platform-architecture.drawio`
> **When to use:** Copy this file per project; replace `{placeholders}` with real names and descriptions. Add or remove elements to match your actual integrations.

---

## Client Applications

### `{SystemName}` SPA (Client Application)
React 18 browser application; the primary interface through which `{primary user role}` performs `{key capabilities}`. Built by Vite 5 and hydrated entirely client-side. Served from CDN or static hosting.

---

## Backend Services

### `{SystemName}` API (Backend Service)
Node.js 20 / Express 4 REST API; single entry point for all browser requests. Mounts domain-scoped routers for each domain module, enforces JWT validation and CORS globally, translates Result values to HTTP responses, and orchestrates all outbound external calls.

---

## Data Stores

### `{PrimaryStore}` (Data Store)
MongoDB 7 replica set; source of truth for all mutable platform state. Each domain module writes to and reads from its own collection; no cross-collection queries.

---

## CDN / Edge

### `{CDN Provider}` (CDN / Edge)
`{Provider description}`; serves the Vite-built static bundle (HTML shell, JS chunks, CSS) to browser clients. All static asset requests are answered at the edge; no requests reach the API container for static files.

*If static hosting is used instead of a CDN, describe the hosting service here.*

---

## Identity

### `{Identity Provider}` (Identity)
`{Provider description}`; issues signed JWTs on successful login. The SPA redirects unauthenticated users here; the API validates JWT signatures via the IdP's JWKS endpoint on every protected request.

*Protocol: OAuth 2.0 + OIDC*

---

## External Integrations

### `{External Service A}` (External Integration)
`{Provider / protocol description}`; `{what is exchanged or triggered}`. Accessed exclusively through the `I{ExternalServiceA}` adapter interface in the `{module}` domain module.

### `{External Service B}` *(optional)*
`{Provider / protocol description}`; `{what is exchanged or triggered}`.

*Add one entry per external integration. Remove placeholder entries that do not apply.*

---

## Technology Badges

| Element | Technology badge |
|---|---|
| `{SystemName}` SPA | React 18 / React Router 6 / TanStack Query 5 / TypeScript 5 / Vite 5 |
| `{SystemName}` API | Node.js 20 / Express 4 / TypeScript 5 / Zod 3 / Pino |
| `{PrimaryStore}` | MongoDB 7 (replica set) |
| `{CDN Provider}` | `{CDN technology}` |
| `{Identity Provider}` | OAuth 2.0 + OIDC |
| `{External Service A}` | `{protocol}` |

---

## Legend

| Visual | Meaning |
|---|---|
| Blue band | Client / Access Layer |
| Green band | Application Layer (API + domain services) |
| Red band | Data & External Services Layer |
| Solid bidirectional arrow | Synchronous request + response |
| Dashed arrow | Async, redirect, or secondary protocol |
| Cylinder shape | Document or data store |
