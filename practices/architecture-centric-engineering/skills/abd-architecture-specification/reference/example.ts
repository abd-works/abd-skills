/**
 * example.ts — MERN Domain Module: all template files merged into one file.
 *
 * Replace every placeholder before using:
 *   {{DomainName}}   → PascalCase entity name  (e.g. Recipient)
 *   {{DomainNames}}  → PascalCase plural        (e.g. Recipients)
 *   {{domainName}}   → camelCase singular       (e.g. recipient)
 *   {{domainNames}}  → camelCase plural          (e.g. recipients)
 *   {{appName}}      → npm scope / monorepo name (e.g. app)
 *
 * File layout this merges:
 *   packages/{{domainName}}/
 *     shared/
 *       {{DomainName}}.ts              — entity + value objects (zero framework imports)
 *       {{domainName}}.schema.ts       — Zod schema, DTO types, input types
 *       {{DomainName}}s.ts             — collection class (shared client + server)
 *       {{DomainName}}Repository.ts   — repository interface
 *       index.ts                       — barrel
 *     server/
 *       {{domainName}}.repository.ts  — MongoDB implementation of the repository
 *       {{domainName}}.routes.ts      — Express router factory
 *       index.ts                       — barrel
 *     client/
 *       {{domainName}}.api.ts         — fetch wrapper (one function per route)
 *       use{{DomainNames}}.ts          — React hook
 *       {{DomainName}}ListView.tsx    — container view
 *       {{DomainName}}CardView.tsx    — item view
 *       index.ts                       — barrel
 */

// ─────────────────────────────────────────────────────────────────────────────
// shared/{{DomainName}}.ts
// Entity and value objects — zero framework imports.
// ─────────────────────────────────────────────────────────────────────────────

export type {{DomainName}}StatusType = 'Active' | 'Pending' | 'Inactive';

export class {{DomainName}}Status {
  constructor(
    public readonly status: {{DomainName}}StatusType,
    public readonly createdAt: Date
  ) {}

  isActive(): boolean {
    return this.status === 'Active';
  }

  isPending(): boolean {
    return this.status === 'Pending';
  }
}

export interface {{DomainName}} {
  id: string;
  name: string;
  status: {{DomainName}}Status;
  createdAt: Date;
}

// ─────────────────────────────────────────────────────────────────────────────
// shared/{{domainName}}.schema.ts
// Zod schema used at repository boundary (.parse()) and API/form boundary (.safeParse()).
// Both client/ and server/ import this — single source of truth.
// ─────────────────────────────────────────────────────────────────────────────

import { z } from 'zod';

export const {{DomainName}}Schema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1, '{{DomainName}} name is required').max(140),
  status: z.enum(['Active', 'Pending', 'Inactive']),
  createdAt: z.coerce.date(),
});

export const Create{{DomainName}}InputSchema = z.object({
  name: z.string().min(1, 'Name is required').max(140),
});

export type Create{{DomainName}}Input = {
  name: string;
};

export type {{DomainName}}DTO = {
  id: string;
  name: string;
  status: 'Active' | 'Pending' | 'Inactive';
  createdAt: Date;
};

// ─────────────────────────────────────────────────────────────────────────────
// shared/{{DomainName}}s.ts
// Collection class — wraps {{DomainName}}[] with fluent query methods.
// Used identically on client and server: same logic, zero duplication.
// ─────────────────────────────────────────────────────────────────────────────

export class {{DomainName}}s {
  constructor(private readonly items: {{DomainName}}[]) {}

  filterByStatus(status: {{DomainName}}StatusType): {{DomainName}}s {
    return new {{DomainName}}s(this.items.filter(r => r.status.status === status));
  }

  search(query: string): {{DomainName}}s {
    const lower = query.toLowerCase();
    return new {{DomainName}}s(
      this.items.filter(r => r.name.toLowerCase().includes(lower))
    );
  }

  toArray(): {{DomainName}}[] {
    return [...this.items];
  }

  get length(): number {
    return this.items.length;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// shared/{{DomainName}}Repository.ts
// Repository interface — server provides the concrete implementation.
// ─────────────────────────────────────────────────────────────────────────────

export interface {{DomainName}}Repository {
  findAll(): Promise<{{DomainName}}[]>;
  findById(id: string): Promise<{{DomainName}} | null>;
  save(input: Create{{DomainName}}Input): Promise<{{DomainName}}>;
}

// ─────────────────────────────────────────────────────────────────────────────
// shared/index.ts
// ─────────────────────────────────────────────────────────────────────────────

// export * from './{{DomainName}}';
// export * from './{{domainName}}.schema';
// export * from './{{DomainName}}s';
// export * from './{{DomainName}}Repository';

// ─────────────────────────────────────────────────────────────────────────────
// server/{{domainName}}.repository.ts
// MongoDB implementation. Validates raw docs with the shared Zod schema at the
// repository boundary — only typed domain entities propagate further.
// ─────────────────────────────────────────────────────────────────────────────

import { Collection, Db } from 'mongodb';

function toDomainEntity(dto: {{DomainName}}DTO): {{DomainName}} {
  return {
    id: dto.id,
    name: dto.name,
    status: new {{DomainName}}Status(dto.status, dto.createdAt),
    createdAt: dto.createdAt,
  };
}

export class {{DomainName}}sRepository implements {{DomainName}}Repository {
  private collection: Collection;

  constructor(db: Db) {
    this.collection = db.collection('{{domainNames}}');
  }

  async findAll(): Promise<{{DomainName}}[]> {
    const docs = await this.collection.find().toArray();
    return docs.map(doc => toDomainEntity({{DomainName}}Schema.parse(doc)));
  }

  async findById(id: string): Promise<{{DomainName}} | null> {
    const doc = await this.collection.findOne({ id });
    if (!doc) return null;
    return toDomainEntity({{DomainName}}Schema.parse(doc));
  }

  async save(input: Create{{DomainName}}Input): Promise<{{DomainName}}> {
    const doc = {
      id: crypto.randomUUID(),
      name: input.name,
      status: 'Pending',
      createdAt: new Date(),
    };
    await this.collection.insertOne(doc);
    return toDomainEntity({{DomainName}}Schema.parse(doc));
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// server/{{domainName}}.routes.ts
// Express router factory. Route paths use kebab-case of the domain verb.
// Every route has a corresponding function in client/{{domainName}}.api.ts.
// ─────────────────────────────────────────────────────────────────────────────

import { Router } from 'express';

export function create{{DomainName}}sRouter(repo: {{DomainName}}sRepository): Router {
  const router = Router();

  router.get('/', async (req, res) => {
    const all = await repo.findAll();
    const activeOnly = req.query.active_only === 'true';
    let collection = new {{DomainName}}s(all);
    if (activeOnly) {
      collection = collection.filterByStatus('Active');
    }
    res.json(collection.toArray());
  });

  router.get('/:id', async (req, res) => {
    const item = await repo.findById(req.params.id);
    if (!item) {
      res.status(404).json({ error: 'Not found' });
      return;
    }
    res.json(item);
  });

  router.post('/', async (req, res) => {
    const validation = Create{{DomainName}}InputSchema.safeParse(req.body);
    if (!validation.success) {
      res.status(400).json({ error: validation.error.issues[0].message });
      return;
    }
    const created = await repo.save(validation.data);
    res.status(201).json(created);
  });

  return router;
}

// ─────────────────────────────────────────────────────────────────────────────
// server/index.ts
// ─────────────────────────────────────────────────────────────────────────────

// export { {{DomainName}}sRepository } from './{{domainName}}.repository';
// export { create{{DomainName}}sRouter } from './{{domainName}}.routes';

// ─────────────────────────────────────────────────────────────────────────────
// client/{{domainName}}.api.ts
// Fetch wrapper — one function per server route. Function names match the domain
// verb exactly. Wire format → typed objects via the shared schema happens here.
// ─────────────────────────────────────────────────────────────────────────────

const API_BASE = '/api/{{domainNames}}';

export async function list{{DomainName}}s(
  filters?: { activeOnly?: boolean }
): Promise<{{DomainName}}[]> {
  const params = new URLSearchParams();
  if (filters?.activeOnly) params.set('active_only', 'true');
  const response = await fetch(`${API_BASE}?${params}`);
  return response.json();
}

export async function get{{DomainName}}(id: string): Promise<{{DomainName}}> {
  const response = await fetch(`${API_BASE}/${id}`);
  return response.json();
}

export async function create{{DomainName}}(
  input: Record<string, unknown>
): Promise<{{DomainName}}> {
  const response = await fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });
  return response.json();
}

// ─────────────────────────────────────────────────────────────────────────────
// client/use{{DomainNames}}.ts
// React hook — loads domain entities from the API, exposes search/filter using
// the SHARED {{DomainName}}s collection class (same logic as server-side).
// ─────────────────────────────────────────────────────────────────────────────

import { useState, useEffect, useCallback } from 'react';

export function use{{DomainName}}s() {
  const [items, setItems] = useState<{{DomainName}}[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    list{{DomainName}}s({ activeOnly: true })
      .then(setItems)
      .finally(() => setLoading(false));
  }, []);

  const filterBySearch = useCallback((query: string) => {
    const collection = new {{DomainName}}s(items);
    return collection.search(query).toArray();
  }, [items]);

  return { items, loading, filterBySearch };
}

// ─────────────────────────────────────────────────────────────────────────────
// client/{{DomainName}}ListView.tsx
// Container view — search input + list of card views.
// No business logic: delegates to the hook; hook delegates to the collection class.
// ─────────────────────────────────────────────────────────────────────────────

export function {{DomainName}}ListView({ onSelectItem }: { onSelectItem?: (item: {{DomainName}}) => void }) {
  const { items, loading, filterBySearch } = use{{DomainName}}s();
  const [searchQuery, setSearchQuery] = useState('');

  const displayed = searchQuery ? filterBySearch(searchQuery) : items;

  if (loading) return <p>Loading...</p>;

  return (
    <div className="{{domainName}}-list">
      <input
        type="search"
        placeholder="Search..."
        value={searchQuery}
        onChange={(e: any) => setSearchQuery(e.target.value)}
      />
      {displayed.map(item => (
        <{{DomainName}}CardView key={item.id} item={item} onSelect={onSelectItem} />
      ))}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// client/{{DomainName}}CardView.tsx
// Item view — presentational, one entity per card.
// Receives a {{DomainName}} and delegates any interaction to the caller.
// ─────────────────────────────────────────────────────────────────────────────

export function {{DomainName}}CardView({
  item,
  onSelect,
}: {
  item: {{DomainName}};
  onSelect?: (item: {{DomainName}}) => void;
}) {
  return (
    <div
      className="{{domainName}}-card"
      onClick={() => onSelect?.(item)}
      role={onSelect ? 'button' : undefined}
    >
      <h3>{item.name}</h3>
      <span className="status">{item.status.status}</span>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// client/index.ts
// ─────────────────────────────────────────────────────────────────────────────

// export { {{DomainName}}ListView } from './{{DomainName}}ListView';
// export { {{DomainName}}CardView } from './{{DomainName}}CardView';
// export { use{{DomainName}}s } from './use{{DomainName}}s';
