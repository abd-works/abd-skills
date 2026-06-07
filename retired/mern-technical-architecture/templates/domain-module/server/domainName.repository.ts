/**
 * domainName.repository.ts — MongoDB data access for the domain entity.
 *
 * Validates raw documents with the shared Zod schema at the repository
 * boundary, ensuring only typed domain entities propagate through the system.
 */
import { Collection, Db } from 'mongodb';
import { DomainName, DomainNameStatus, DomainNameSchema, DomainNameDTO, CreateDomainNameInput } from '@appName/domainName-shared';

function toDomainEntity(dto: DomainNameDTO): DomainName {
  return {
    id: dto.id,
    enterpriseId: dto.enterpriseId,
    name: dto.name,
    status: new DomainNameStatus(dto.status, dto.createdAt),
    createdAt: dto.createdAt,
  };
}

export class DomainNamesRepository {
  private collection: Collection;

  constructor(db: Db) {
    this.collection = db.collection('domainNames');
  }

  async findAll(): Promise<DomainName[]> {
    const docs = await this.collection.find().toArray();
    return docs.map(doc => toDomainEntity(DomainNameSchema.parse(doc)));
  }

  async findById(id: string): Promise<DomainName | null> {
    const doc = await this.collection.findOne({ id });
    if (!doc) return null;
    return toDomainEntity(DomainNameSchema.parse(doc));
  }

  async findByIds(ids: string[]): Promise<DomainName[]> {
    const docs = await this.collection.find({ id: { $in: ids } }).toArray();
    return docs.map(doc => toDomainEntity(DomainNameSchema.parse(doc)));
  }

  async findByEnterprise(enterpriseId: string): Promise<DomainName[]> {
    const docs = await this.collection.find({ enterpriseId }).toArray();
    return docs.map(doc => toDomainEntity(DomainNameSchema.parse(doc)));
  }

  async save(enterpriseId: string, input: CreateDomainNameInput): Promise<DomainName> {
    const doc = {
      id: crypto.randomUUID(),
      enterpriseId,
      name: input.name,
      status: 'Pending',
      createdAt: new Date(),
    };
    await this.collection.insertOne(doc);
    return toDomainEntity(DomainNameSchema.parse(doc));
  }
}
