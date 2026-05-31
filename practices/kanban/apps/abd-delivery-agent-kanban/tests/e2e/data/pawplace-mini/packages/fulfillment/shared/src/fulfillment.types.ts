export type OrderFulfillmentStatus =
  | 'awaiting preparation'
  | 'ready for collection'
  | 'complete'
  | 'collected'
  | 'closed';

export interface FulfillmentQueueRowDto {
  orderId: string;
  customerContact: string;
  orderFulfillment: OrderFulfillmentStatus;
  clickAndCollectStore: string;
  pickupTime: string;
}

export interface FulfillmentOrderDetailDto {
  orderId: string;
  clickAndCollectStore: string;
  orderFulfillment: OrderFulfillmentStatus;
  cartLines: { catalogItemIdentity: string; cartQuantity: number }[];
  customerContact: string;
}
