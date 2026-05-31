import { z } from 'zod';

export const customerLocationSchema = z.object({
  latitude: z.number(),
  longitude: z.number(),
});

export const createDiscoverySessionBodySchema = z.object({
  displayName: z.string().min(1),
  customerLocation: customerLocationSchema.optional(),
});

export const selectStoreBodySchema = z.object({
  storeId: z.string().min(1),
});

export const storeRecordSchema = z.object({
  id: z.string(),
  retailLocationIdentity: z.string(),
  geographicPlacement: z.string(),
});

export const storeWithDistanceSchema = storeRecordSchema.extend({
  distanceToStoreKm: z.number().optional(),
  stockAvailabilityShown: z.boolean(),
});

export const storeMapViewSchema = z.object({
  entries: z.array(storeWithDistanceSchema),
  allStoresPresentedWithoutSearchOrFilter: z.boolean(),
  stockAvailabilityShown: z.boolean(),
});

export const storeListViewSchema = z.object({
  rows: z.array(storeWithDistanceSchema),
  alternativeToMap: z.boolean(),
  stockAvailabilityShown: z.boolean(),
});

export const discoverySessionSchema = z.object({
  displayName: z.string(),
  selectedStore: storeRecordSchema.nullable(),
  customerLocation: customerLocationSchema.nullable(),
  activeView: z.enum(['map', 'list']).nullable(),
  catalogScope: z.string().nullable(),
});

export const selectStoreResponseSchema = z.object({
  selectedStore: storeRecordSchema,
  catalogScope: z.string(),
});

export type DiscoverySessionDto = z.infer<typeof discoverySessionSchema>;
export type StoreMapViewDto = z.infer<typeof storeMapViewSchema>;
export type StoreListViewDto = z.infer<typeof storeListViewSchema>;
export type SelectStoreResponseDto = z.infer<typeof selectStoreResponseSchema>;
