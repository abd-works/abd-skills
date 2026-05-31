import { z } from 'zod';

export const catalogProductRowSchema = z.object({
  catalogItemIdentity: z.string(),
});

export const chooseStorePromptSchema = z.object({
  chooseStorePromptShown: z.literal(true),
  productRows: z.array(catalogProductRowSchema),
});

export const catalogBrowseSchema = z.union([
  z.array(catalogProductRowSchema),
  chooseStorePromptSchema,
]);

export const productDetailSchema = z.object({
  catalogItemIdentity: z.string(),
  description: z.string(),
  unitPrice: z.number(),
  realTimeStock: z.number(),
  stockAvailability: z.enum(['available', 'unavailable']),
  selectedStoreIdentity: z.string(),
  cartCheckoutPaymentActionsOffered: z.boolean(),
});

export const stockMaintenanceRowSchema = z.object({
  storeIdentity: z.string(),
  catalogItemIdentity: z.string(),
  productStockLevels: z.number(),
  editable: z.boolean(),
});

export const stockMaintenanceViewSchema = z.object({
  storeIdentity: z.string(),
  rows: z.array(stockMaintenanceRowSchema),
});

export const saveStockLevelsBodySchema = z.object({
  storeIdentity: z.string().min(1),
  updates: z.array(
    z.object({
      catalogItemIdentity: z.string().min(1),
      productStockLevels: z.number(),
    }),
  ),
});

export const saveStockLevelsResponseSchema = z.object({
  ok: z.boolean(),
  message: z.string().optional(),
});

export type CatalogProductRowDto = z.infer<typeof catalogProductRowSchema>;
export type ProductDetailDto = z.infer<typeof productDetailSchema>;
export type StockMaintenanceViewDto = z.infer<typeof stockMaintenanceViewSchema>;
export type SaveStockLevelsResponseDto = z.infer<typeof saveStockLevelsResponseSchema>;
