import React from 'react';
import { layoutTokens } from '../../shared/layout-tokens';

export type CustomerNavSection = 'Find Store' | 'catalog';

interface CustomerNavProps {
  currentSection: CustomerNavSection;
  onNavigate?: (section: CustomerNavSection) => void;
}

export function CustomerNav({ currentSection, onNavigate }: CustomerNavProps) {
  const linkStyle = (active: boolean): React.CSSProperties => ({
    marginRight: layoutTokens.spacing[2],
    color: active ? layoutTokens.accent : layoutTokens.body.color,
    fontWeight: active ? 600 : 400,
    textDecoration: 'none',
    borderBottom: active ? `2px solid ${layoutTokens.accent}` : 'none',
  });

  return (
    <header data-testid="customer-nav" style={{ padding: layoutTokens.spacing[2] }}>
      <nav aria-label="site header · Find Store · catalog">
        <a
          href="/stores/map"
          style={linkStyle(currentSection === 'Find Store')}
          aria-current={currentSection === 'Find Store' ? 'page' : undefined}
          onClick={(e) => {
            e.preventDefault();
            onNavigate?.('Find Store');
          }}
        >
          Find Store
        </a>
        <a
          href="/catalog"
          style={linkStyle(currentSection === 'catalog')}
          aria-current={currentSection === 'catalog' ? 'page' : undefined}
          onClick={(e) => {
            e.preventDefault();
            onNavigate?.('catalog');
          }}
        >
          catalog
        </a>
      </nav>
    </header>
  );
}
