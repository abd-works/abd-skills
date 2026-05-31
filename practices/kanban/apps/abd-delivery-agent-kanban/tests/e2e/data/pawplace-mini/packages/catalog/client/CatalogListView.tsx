import React from 'react';
import type { CatalogProduct } from '../shared/catalog-types';
import { useSelectedStore } from '../../shared/selected-store';
import { layoutTokens } from '../../shared/layout-tokens';
import { CustomerNav } from './CustomerNav';
import { SelectedStorePanel } from './SelectedStorePanel';
import { ChooseStorePrompt } from './ChooseStorePrompt';

interface CatalogListViewProps {
  products: CatalogProduct[];
  onViewProduct?: (product: CatalogProduct) => void;
  onChangeStore?: () => void;
  onFindStore?: () => void;
  onNavigate?: (section: 'Find Store' | 'catalog') => void;
}

export function CatalogListView({
  products,
  onViewProduct,
  onChangeStore,
  onFindStore,
  onNavigate,
}: CatalogListViewProps) {
  const { selectedStore } = useSelectedStore();

  return (
    <main data-testid="browse-catalog">
      <CustomerNav currentSection="catalog" onNavigate={onNavigate} />
      {selectedStore ? (
        <>
          <SelectedStorePanel store={selectedStore} onChangeStore={onChangeStore} />
          <table
            data-testid="product-list"
            aria-label="product list"
            style={{ width: '100%', borderCollapse: 'collapse' }}
          >
            <thead>
              <tr>
                <th scope="col" style={layoutTokens.label}>
                  product
                </th>
                <th scope="col" style={layoutTokens.label}>
                  price
                </th>
                <th scope="col">
                  <span className="sr-only">actions</span>
                </th>
              </tr>
            </thead>
            <tbody>
              {products.map((product) => (
                <tr key={product.catalogItemIdentity}>
                  <td style={layoutTokens.body}>{product.catalogItemIdentity}</td>
                  <td style={layoutTokens.body}>{product.unitPrice.toFixed(2)}</td>
                  <td>
                    <button
                      type="button"
                      onClick={() => onViewProduct?.(product)}
                    >
                      view product
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      ) : (
        <ChooseStorePrompt onFindStore={onFindStore ?? onChangeStore} />
      )}
    </main>
  );
}
