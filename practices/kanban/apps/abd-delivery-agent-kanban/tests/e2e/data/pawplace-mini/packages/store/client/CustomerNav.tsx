import React from 'react';
import { tokens } from '../../shared/layout-tokens';

export interface CustomerNavProps {
  activeSection?: 'find-store' | 'catalog';
}

export function CustomerNav({ activeSection = 'find-store' }: CustomerNavProps) {
  const linkStyle = (active: boolean): React.CSSProperties => ({
    ...tokens.body,
    fontWeight: active ? tokens.display.fontWeight : tokens.body.fontWeight,
    color: active ? tokens.accent : tokens.body.color,
    textDecoration: 'none',
    marginRight: tokens.spacing.md,
  });

  return (
    <header data-testid="site-header" style={{ padding: tokens.spacing.md, borderBottom: `1px solid ${tokens.surfaceMuted}` }}>
      <nav aria-label="site header · Find Store · catalog">
        <a href="/stores/map" style={linkStyle(activeSection === 'find-store')}>
          Find Store
        </a>
        <a href="/catalog" style={linkStyle(activeSection === 'catalog')}>
          catalog
        </a>
      </nav>
    </header>
  );
}
