import React, { useCallback, useState } from 'react';
import type { ProductStockAtStore } from '../../catalog/shared/catalog-types';
import { layoutTokens } from '../../shared/layout-tokens';
import { EmployeeNav } from './EmployeeNav';

interface StockMaintenanceViewProps {
  storeIdentity: string;
  stockRows: ProductStockAtStore[];
  onSaveLevels?: (
    updates: ProductStockAtStore[],
  ) => { ok: true } | { ok: false; message: string };
}

export function StockMaintenanceView({
  storeIdentity,
  stockRows,
  onSaveLevels,
}: StockMaintenanceViewProps) {
  const [draftLevels, setDraftLevels] = useState<Record<string, number>>(() =>
    Object.fromEntries(stockRows.map((row) => [row.catalogItemIdentity, row.productStockLevels])),
  );
  const [validationMessage, setValidationMessage] = useState<string | null>(null);
  const [editingProduct, setEditingProduct] = useState<string | null>(null);

  const handleSave = useCallback(() => {
    const updates: ProductStockAtStore[] = stockRows.map((row) => ({
      ...row,
      productStockLevels: draftLevels[row.catalogItemIdentity] ?? row.productStockLevels,
    }));
    for (const row of updates) {
      const levels = row.productStockLevels;
      if (!Number.isFinite(levels) || levels < 0 || !Number.isInteger(levels)) {
        setValidationMessage('validation message');
        return;
      }
    }
    const result = onSaveLevels?.(updates);
    if (result && !result.ok) {
      setValidationMessage(result.message);
      return;
    }
    setValidationMessage(null);
    setEditingProduct(null);
  }, [draftLevels, onSaveLevels, stockRows]);

  return (
    <main data-testid="update-stock">
      <EmployeeNav storeIdentity={storeIdentity} activeSection="Update stock" />
      <aside
        data-testid="store-panel"
        aria-label="store"
        style={{ padding: layoutTokens.spacing[2], background: layoutTokens.surfaceMuted }}
      >
        <label style={layoutTokens.label}>
          store
          <input type="text" readOnly value={storeIdentity} aria-readonly="true" />
        </label>
      </aside>
      {validationMessage && (
        <div
          data-testid="validation-error-area"
          role="alert"
          style={{ color: layoutTokens.danger, padding: layoutTokens.spacing[2] }}
        >
          {validationMessage}
        </div>
      )}
      <table
        data-testid="stock-list"
        aria-label="stock list"
        style={{ width: '100%', borderCollapse: 'collapse' }}
      >
        <thead>
          <tr>
            <th scope="col" style={layoutTokens.label}>
              product
            </th>
            <th scope="col" style={layoutTokens.label}>
              product stock levels
            </th>
            <th scope="col">
              <span className="sr-only">actions</span>
            </th>
          </tr>
        </thead>
        <tbody>
          {stockRows.map((row) => {
            const isEditing = editingProduct === row.catalogItemIdentity;
            const level = draftLevels[row.catalogItemIdentity] ?? row.productStockLevels;
            return (
              <tr key={row.catalogItemIdentity}>
                <td style={layoutTokens.body}>{row.catalogItemIdentity}</td>
                <td style={layoutTokens.body}>
                  {isEditing ? (
                    <input
                      type="number"
                      step={1}
                      aria-label={`product stock levels ${row.catalogItemIdentity}`}
                      value={level}
                      onChange={(e) => {
                        const parsed = e.target.value === '' ? NaN : Number(e.target.value);
                        setDraftLevels((prev) => ({
                          ...prev,
                          [row.catalogItemIdentity]: parsed,
                        }));
                      }}
                    />
                  ) : (
                    level
                  )}
                </td>
                <td>
                  <button
                    type="button"
                    onClick={() => setEditingProduct(row.catalogItemIdentity)}
                  >
                    edit level
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <div style={{ padding: layoutTokens.spacing[2] }}>
        <button type="button" onClick={handleSave} style={{ color: layoutTokens.accent }}>
          save levels
        </button>
      </div>
    </main>
  );
}
