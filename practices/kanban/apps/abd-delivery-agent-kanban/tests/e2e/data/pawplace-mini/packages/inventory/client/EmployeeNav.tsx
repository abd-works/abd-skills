import React from 'react';
import { layoutTokens } from '../../shared/layout-tokens';

interface EmployeeNavProps {
  storeIdentity: string;
  activeSection?: 'Fulfillment' | 'Update stock';
  onSignOut?: () => void;
}

export function EmployeeNav({
  storeIdentity,
  activeSection,
  onSignOut,
}: EmployeeNavProps) {
  return (
    <header
      data-testid="employee-header"
      style={{
        padding: layoutTokens.spacing[2],
        background: layoutTokens.staffSurface,
      }}
    >
      <nav aria-label="employee header · store · Fulfillment · Sign out">
        <span style={layoutTokens.body}>{storeIdentity}</span>
        <span style={{ margin: `0 ${layoutTokens.spacing[2]}px` }} aria-hidden="true">
          ·
        </span>
        {activeSection === 'Fulfillment' ? (
          <strong>Fulfillment</strong>
        ) : (
          <span>Fulfillment</span>
        )}
        <span style={{ margin: `0 ${layoutTokens.spacing[2]}px` }} aria-hidden="true">
          ·
        </span>
        {activeSection === 'Update stock' ? (
          <strong>Update stock</strong>
        ) : (
          <span>Update stock</span>
        )}
        <button
          type="button"
          style={{ marginLeft: layoutTokens.spacing[2] }}
          onClick={onSignOut}
        >
          Sign out
        </button>
      </nav>
    </header>
  );
}
