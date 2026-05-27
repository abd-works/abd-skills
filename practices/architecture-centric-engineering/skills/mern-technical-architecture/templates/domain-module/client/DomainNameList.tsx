/**
 * DomainNameList.tsx — Container component with search and list rendering.
 *
 * Uses the useDomainNames hook for state and delegates item display
 * to the presentational DomainNameCard component.
 *
 * Accepts an optional onSelectItem callback so the app composition root
 * can navigate to the detail view when a user clicks an item.
 */
import { useState } from 'react';
import { DomainName } from '@appName/domainName-shared';
import { useDomainNames } from './useDomainNames';
import { DomainNameCard } from './DomainNameCard';

interface DomainNameListProps {
  onSelectItem?: (item: DomainName) => void;
}

export function DomainNameList({ onSelectItem }: DomainNameListProps) {
  const { items, loading, filterBySearch } = useDomainNames();
  const [searchQuery, setSearchQuery] = useState('');

  const displayed = searchQuery ? filterBySearch(searchQuery) : items;

  if (loading) return <p>Loading...</p>;

  return (
    <div className="domainName-list">
      <input
        type="search"
        placeholder="Search..."
        value={searchQuery}
        onChange={(e: any) => setSearchQuery(e.target.value)}
      />
      {displayed.map(item => (
        <DomainNameCard key={item.id} item={item} onSelect={onSelectItem} />
      ))}
    </div>
  );
}
