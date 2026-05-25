/**
 * DomainNameCard.tsx — Presentational component for a single domain entity.
 *
 * Receives a DomainName entity as a prop and renders its display fields.
 * Accepts an optional onSelect callback for navigation to the detail view.
 */
import { DomainName } from '@appName/domainName-shared';

interface DomainNameCardProps {
  item: DomainName;
  onSelect?: (item: DomainName) => void;
}

export function DomainNameCard({ item, onSelect }: DomainNameCardProps) {
  return (
    <div
      className="domainName-card"
      onClick={() => onSelect?.(item)}
      role={onSelect ? 'button' : undefined}
    >
      <h3>{item.name}</h3>
      <span className="status">{item.status.status}</span>
    </div>
  );
}
