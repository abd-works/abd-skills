/**
 * DomainNameList.tsx — Container component with search and list rendering.
 *
 * Uses the useDomainNames hook for state and delegates item display
 * to the presentational DomainNameCard component.
 */
import { useState } from 'react';
import { useDomainNames } from './useDomainNames';
import { DomainNameCard } from './DomainNameCard';

export function DomainNameList() {
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
        <DomainNameCard key={item.id} item={item} />
      ))}
    </div>
  );
}
