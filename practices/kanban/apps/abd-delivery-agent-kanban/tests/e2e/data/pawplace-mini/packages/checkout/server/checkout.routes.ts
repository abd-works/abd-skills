import { Router } from 'express';
import { CheckoutApi } from './checkout.api';

export function createCheckoutRouter(api: CheckoutApi): Router {
  const router = Router();
  router.post('/checkout/guest', (req, res) => api.startGuestCheckout(req, res));
  router.get('/checkout', (req, res) => api.getSession(req, res));
  router.post('/checkout/click-and-collect-store', (req, res) => api.selectStore(req, res));
  router.post('/checkout/billing-address', (req, res) => api.enterBilling(req, res));
  router.post('/checkout/payment-method', (req, res) => api.selectPaymentMethod(req, res));
  router.post('/checkout/stripe-wave/outcome', (req, res) => api.configureStripeWave(req, res));
  router.post('/checkout/process-payment', (req, res) => api.processPayment(req, res));
  router.get('/checkout/confirmation', (req, res) => api.getConfirmation(req, res));
  return router;
}
