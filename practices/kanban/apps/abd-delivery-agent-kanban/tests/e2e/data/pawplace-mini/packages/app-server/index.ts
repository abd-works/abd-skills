import express from 'express';

import {
  CartApi,
  CartRepository,
  CartService,
  createCartRouter,
} from '../cart/server/index';

import {
  CatalogApi,
  CatalogRepository,
  CatalogService,
  createCatalogRouter,
} from '../catalog/server/index';

import {
  FulfillmentApi,
  FulfillmentRepository,
  FulfillmentService,
  createFulfillmentRouter,
} from '../fulfillment/server/index';

import {
  StoreApi,
  StoreRepository,
  StoreService,
  createStoreRouter,
} from '../store/server/index';

import {
  CheckoutApi,
  CheckoutRepository,
  CheckoutService,
  createCheckoutRouter,
} from '../checkout/server/index';

export function createAppServer(options?: {
  cartRepository?: CartRepository;
  storeRepository?: StoreRepository;
  catalogRepository?: CatalogRepository;
  fulfillmentRepository?: FulfillmentRepository;
}) {
  const cartRepository = options?.cartRepository ?? new CartRepository();
  const storeRepository = options?.storeRepository ?? new StoreRepository();
  const catalogRepository = options?.catalogRepository ?? new CatalogRepository();
  const fulfillmentRepository =
    options?.fulfillmentRepository ?? new FulfillmentRepository();

  const checkoutRepository = new CheckoutRepository();
  const cartService = new CartService(cartRepository);
  const checkoutService = new CheckoutService(
    checkoutRepository,
    cartRepository,
    fulfillmentRepository,
  );
  const storeService = new StoreService(storeRepository);
  const catalogService = new CatalogService(catalogRepository, storeRepository);
  const fulfillmentService = new FulfillmentService(fulfillmentRepository);

  cartService.seedCatalogDefaults();

  const cartApi = new CartApi(cartService);
  const checkoutApi = new CheckoutApi(checkoutService);
  const storeApi = new StoreApi(storeService);
  const catalogApi = new CatalogApi(catalogService);
  const fulfillmentApi = new FulfillmentApi(fulfillmentService);

  const app = express();
  app.use(express.json());
  const router = express.Router();

  router.post('/sessions', (req, res) => {
    if (req.body?.selectedStoreIdentity) {
      cartApi.createSession(req, res);
      return;
    }
    storeApi.createDiscoverySession(req, res);
  });

  app.use('/api/v1', router);
  app.use('/api/v1', createStoreRouter(storeApi));
  app.use('/api/v1', createCatalogRouter(catalogApi));
  app.use('/api/v1', createCartRouter(cartApi));
  app.use('/api/v1', createCheckoutRouter(checkoutApi));
  app.use('/api/v1', createFulfillmentRouter(fulfillmentApi));

  return {
    app,
    service: cartService,
    cartService,
    checkoutService,
    storeService,
    catalogService,
    fulfillmentService,
    cartRepository,
    checkoutRepository,
    storeRepository,
    catalogRepository,
    fulfillmentRepository,
  };
}
