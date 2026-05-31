import { z } from 'zod';

export const addProductToCartBodySchema = z.object({
  catalogItemIdentity: z.string().min(1),
});

export const updateCartQuantityBodySchema = z.object({
  cartQuantity: z.number().int().min(0),
});

export const cartLineDtoSchema = z.object({
  catalogItemIdentity: z.string(),
  cartQuantity: z.number().int(),
  unitPrice: z.number(),
  lineTotal: z.number(),
});

export const shoppingCartDtoSchema = z.object({
  customerDisplayName: z.string(),
  selectedStoreIdentity: z.string(),
  cartLines: z.array(cartLineDtoSchema),
  guestCheckoutOffered: z.boolean(),
  guestCheckoutBlocked: z.boolean(),
  removeDistinctFromZeroQuantityEdit: z.boolean().optional(),
  zeroQuantityRejectedMessage: z.string().optional(),
  directedToRemove: z.boolean().optional(),
  unavailableWarning: z.string().optional(),
});

export type CartLineDto = z.infer<typeof cartLineDtoSchema>;
export type ShoppingCartDto = z.infer<typeof shoppingCartDtoSchema>;
