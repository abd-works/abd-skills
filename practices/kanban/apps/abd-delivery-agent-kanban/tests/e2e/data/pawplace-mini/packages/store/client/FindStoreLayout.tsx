import React from 'react';
import { tokens } from '../../shared/layout-tokens';
import { CustomerNav } from './CustomerNav';

export interface FindStoreLayoutProps {
  activeTab: 'map' | 'list';
  children: React.ReactNode;
  onTabChange?: (tab: 'map' | 'list') => void;
}

export function FindStoreLayout({ activeTab, children, onTabChange }: FindStoreLayoutProps) {
  const tabStyle = (active: boolean): React.CSSProperties => ({
    ...tokens.label,
    padding: `${tokens.spacing.sm}px ${tokens.spacing.md}px`,
    border: 'none',
    borderBottom: active ? `2px solid ${tokens.accent}` : '2px solid transparent',
    background: 'transparent',
    cursor: 'pointer',
    color: active ? tokens.accent : tokens.label.color,
  });

  return (
    <div data-testid="find-store-layout" style={{ background: tokens.surface, minHeight: '100%' }}>
      <CustomerNav activeSection="find-store" />
      <div
        role="tablist"
        aria-label="Find Store tab bar"
        style={{ display: 'flex', gap: tokens.spacing.sm, padding: tokens.spacing.md }}
      >
        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'map'}
          style={tabStyle(activeTab === 'map')}
          onClick={() => onTabChange?.('map')}
        >
          Map
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'list'}
          style={tabStyle(activeTab === 'list')}
          onClick={() => onTabChange?.('list')}
        >
          List
        </button>
      </div>
      <main style={{ padding: tokens.spacing.md }}>{children}</main>
    </div>
  );
}
