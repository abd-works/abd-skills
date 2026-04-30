/**
 * useDomainNames.ts — React hook for domain entity state management.
 *
 * Loads domain entities from the API and exposes search/filter using
 * the SHARED DomainNames collection class — same logic as server-side.
 */
import { useState, useEffect, useCallback } from 'react';
import { DomainName, DomainNames } from '@project/domainName/shared';
import { fetchDomainNames } from './domainName.api';

export function useDomainNames() {
  const [items, setItems] = useState<DomainName[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchDomainNames({ activeOnly: true })
      .then(setItems)
      .finally(() => setLoading(false));
  }, []);

  const filterBySearch = useCallback((query: string) => {
    const collection = new DomainNames(items);
    return collection.search(query).toArray();
  }, [items]);

  return { items, loading, filterBySearch };
}
