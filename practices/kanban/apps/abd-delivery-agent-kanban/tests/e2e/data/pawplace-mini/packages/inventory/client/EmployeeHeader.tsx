import React from 'react';
import { layoutTokens } from '../../shared/layout-tokens';

interface EmployeeHeaderProps {
  storeIdentity: string;
  onSignOut?: () => void;
}

export function EmployeeHeader({ storeIdentity, onSignOut }: EmployeeHeaderProps) {
  return (
    <header
      data-testid="employee-header"
      style={{ padding: layoutTokens.spacing[2], background: layoutTokens.staffSurface }}
      aria-label="employee header · store · Sign out"
    >
      <span style={layoutTokens.body}>store {storeIdentity}</span>
      <nav aria-label="staff nav" style={{ display: 'inline', marginLeft: layoutTokens.spacing[2] }}>
        <span style={layoutTokens.label}>staff nav</span>
      </nav>
      <button type="button" style={{ marginLeft: layoutTokens.spacing[2] }} onClick={onSignOut}>
        Sign out
      </button>
    </header>
  );
}
