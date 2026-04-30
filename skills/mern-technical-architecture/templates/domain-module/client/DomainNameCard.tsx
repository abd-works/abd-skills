/**
 * DomainNameCard.tsx — Presentational component for a single domain entity.
 *
 * Receives a DomainName entity as a prop and renders its display fields.
 * No state, no side effects — pure presentation.
 */
import { DomainName } from '@project/domainName/shared';

interface DomainNameCardProps {
  item: DomainName;
  [key: string]: any;
}

export function DomainNameCard({ item }: DomainNameCardProps) {
  return (
    <div className="domainName-card">
      <h3>{item.name}</h3>
      <span className="status">{item.status.status}</span>
    </div>
  );
}
