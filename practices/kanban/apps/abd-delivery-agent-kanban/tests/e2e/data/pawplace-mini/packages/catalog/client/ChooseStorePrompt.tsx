import React from 'react';
import { layoutTokens } from '../../shared/layout-tokens';

interface ChooseStorePromptProps {
  onFindStore?: () => void;
}

export function ChooseStorePrompt({ onFindStore }: ChooseStorePromptProps) {
  return (
    <section
      data-testid="choose-store-prompt"
      role="region"
      aria-label="choose store prompt"
      style={{ padding: layoutTokens.spacing[2], background: layoutTokens.surfaceMuted }}
    >
      <p style={layoutTokens.body}>choose a store first</p>
      <a href="/stores/map" onClick={(e) => { e.preventDefault(); onFindStore?.(); }}>
        Find Store
      </a>
    </section>
  );
}
