import React from 'react';
import type { CatalogProduct } from '../shared/catalog-types';
import { stockAvailabilityFromLevels } from '../shared/catalog-types';
import { useSelectedStore } from '../../shared/selected-store';
import { layoutTokens } from '../../shared/layout-tokens';
import { CustomerNav } from './CustomerNav';
import { StockAvailabilityBadge } from './StockAvailabilityBadge';

interface ProductDetailsViewProps {
  product: CatalogProduct;
  realTimeStock: number;
  onBackToCatalog?: () => void;
  onNavigate?: (section: 'Find Store' | 'catalog') => void;
}

export function ProductDetailsView({
  product,
  realTimeStock,
  onBackToCatalog,
  onNavigate,
}: ProductDetailsViewProps) {
  const { selectedStore } = useSelectedStore();
  const stockAvailability = stockAvailabilityFromLevels(realTimeStock);

  return (
    <main data-testid="product-details">
      <CustomerNav currentSection="catalog" onNavigate={onNavigate} />
      {selectedStore && (
        <p
          data-testid="selected-store-chrome"
          style={{ ...layoutTokens.body, padding: layoutTokens.spacing[2] }}
        >
          {selectedStore.storeIdentity} — {selectedStore.streetAddress}
        </p>
      )}
      <section
        data-testid="product-summary"
        aria-label="product summary"
        style={{ padding: layoutTokens.spacing[2] }}
      >
        <dl>
          <div>
            <dt style={layoutTokens.label}>product</dt>
            <dd style={layoutTokens.body}>{product.catalogItemIdentity}</dd>
          </div>
          <div>
            <dt style={layoutTokens.label}>price</dt>
            <dd style={layoutTokens.body}>${product.unitPrice.toFixed(2)}</dd>
          </div>
          <div>
            <dt style={layoutTokens.label}>description</dt>
            <dd style={layoutTokens.body}>{product.description}</dd>
          </div>
          <div>
            <dt style={layoutTokens.label}>real-time stock</dt>
            <dd data-testid="real-time-stock" style={layoutTokens.body}>
              {realTimeStock}
            </dd>
          </div>
          <div>
            <dt style={layoutTokens.label}>stock availability</dt>
            <dd>
              <StockAvailabilityBadge stockAvailability={stockAvailability} />
            </dd>
          </div>
        </dl>
        <div data-testid="product-summary-actions" style={{ marginTop: layoutTokens.spacing[2] }}>
          <button type="button" onClick={onBackToCatalog}>
            back to catalog
          </button>
        </div>
      </section>
    </main>
  );
}
