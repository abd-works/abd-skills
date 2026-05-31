import React from 'react';
import { layoutTokens } from '../../shared/layout-tokens';

interface StockAvailabilityBadgeProps {
  stockAvailability: 'available' | 'unavailable';
}

export function StockAvailabilityBadge({ stockAvailability }: StockAvailabilityBadgeProps) {
  const label = stockAvailability;
  const icon = stockAvailability === 'available' ? '✓' : '○';
  return (
    <span
      data-testid="stock-availability"
      data-availability={stockAvailability}
      aria-label={`stock availability ${label}`}
    >
      <span aria-hidden="true">{icon}</span> {label}
      <span className="sr-only" style={{ color: stockAvailability === 'available' ? layoutTokens.success : layoutTokens.label.color }}>
        {label}
      </span>
    </span>
  );
}
