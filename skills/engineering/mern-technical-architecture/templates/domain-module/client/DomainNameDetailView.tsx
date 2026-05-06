/**
 * DomainNameDetailView.tsx — Detail view for a single domain entity.
 *
 * Displays the full entity with its sub-items and provides mutation controls
 * (add, edit, move, delete) for the user interactions defined in the specs.
 *
 * Use this detail view when the requirements say users can inspect an entity
 * and perform follow-up actions on it. Some mutation endpoints may exist only
 * for integrations or internal workflows and should not automatically appear
 * as UI controls.
 */
import { DomainName } from '@appName/domainName-shared';

interface DomainNameDetailViewProps {
  entity: DomainName;
  onUpdated: (entity: DomainName) => void;
  onBack: () => void;
}

export function DomainNameDetailView({ entity, onUpdated, onBack }: DomainNameDetailViewProps) {
  return (
    <div className="domainName-detail-view">
      <header>
        <button onClick={onBack}>← Back</button>
        <h2>{entity.name}</h2>
      </header>
      {/* Render sub-items and mutation controls here.
          Provide UI controls only for the actions users are meant to perform
          in the product flow. If the specs define add, edit, or move actions,
          wire those controls to the corresponding API functions and invoke
          onUpdated with the fresh entity returned by the server. */}
    </div>
  );
}
