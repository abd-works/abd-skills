---
state: domain-model
sprint_scope: Increment 2 — Sprint 1 (Cart), Sprint 2 (Checkout & pay), Sprint 3 (Store pickup)
---

# Module: [PawPlace mini — Increment 2]

Scope: Sprint 1 (Cart), Sprint 2 (Checkout & pay), and Sprint 3 (Store pickup). Typed surface derived from `docs/increments/2-click-and-collect/specification/crc.md` and `specification-by-example.md`.

---

# Core Domain

## Increment 2 — Sprint 1: Cart

*Cart* holds line items between *catalog* browsing and checkout. The typed model covers the working container (*Shopping Cart*), per-line state (*Cart Line*, *Cart Quantity*), collection rules (*Cart Lines*), and named customer operations (*Add Product To Cart*, *Update Cart Quantity*, *Remove Product From Cart*).

## **Cart**

### **Cart** << Entity >>

Initialisation: one *Cart* instance per customer session — owns the *Shopping Cart* container for pre-checkout aggregation.
------
+ shoppingCart: Shopping Cart
	Invariant: a shopping cart must contain at least one line before guest checkout can begin
----
+ persistSelectionsWhileBrowsing(shoppingCart: Shopping Cart): Shopping Cart
	Invariant: line items remain while the customer continues browsing
	Interaction:
		return shoppingCart

### **Shopping Cart** << Entity >>

+ Shopping Cart(customer: Customer)
------
+ << composition >> cartLines: Cart Lines
+ customer: Customer
	Invariant: guest checkout is not offered until at least one line exists
----
+ showEachLineWithProductIdentity(): List<Cart Line>
	Interaction:
		return cartLines.allLines()
+ showEditableCartQuantityPerLine(): List<Cart Line>
	Interaction:
		return cartLines.allLines()
+ persistUpdatedCountsWhileBrowsing(): void
	Interaction:
		cartLines.persistCurrentState()
+ blockCheckoutEntryWhenEmpty(): Boolean
	Invariant: checkout entry blocked when no lines exist
	Interaction:
		return cartLines.isEmpty()
+ isEmpty(): Boolean
	Interaction:
		return cartLines.isEmpty()
+ hasAtLeastOneLine(): Boolean
	Interaction:
		return cartLines.lineCount() >= 1
+ calculateOrderTotal(): Money
	Interaction:
		total: Money = Money.zero()
		for each line in cartLines.allLines():
			total = total.add(line.lineTotalFromQuantity(unitPrice: line.product.unitPrice))
		return total
+ handOffLinesToGuestCheckout(guestCheckout: Guest Checkout): List<Cart Line>
	Interaction:
		return cartLines.allLines()
+ clearAllLinesAfterPayment(): void
	Interaction:
		cartLines.clearAll()

### **Cart Line** << Entity >>

+ Cart Line(product: Product, cartQuantity: Cart Quantity)
------
+ product: Product
+ cartQuantity: Cart Quantity
	Invariant: cart quantity for any line must be a positive whole number while the line remains in the shopping cart
----
+ lineTotalFromQuantity(unitPrice: Money): Money
	Invariant: line total derives from cart quantity and product unit price
	Interaction:
		total: Money = unitPrice.multiplyBy(cartQuantity: cartQuantity.value)
		return total
+ matchesProduct(product: Product): Boolean
	Interaction:
		return this.product.equals(other: product)

### **Cart Lines** << Entity >>

Initialisation: empty collection at shopping cart creation — lines added via *Add Product To Cart*.
------
+ << aggregation >> lines: List<Cart Line>
	Invariant: at most one line per product — no duplicate lines for the same product
----
+ mergeAddIntoExistingProductLine(addProductToCart: Add Product To Cart, product: Product, cartQuantity: Cart Quantity): Cart Line
	Invariant: repeat add increases quantity on existing line without duplicate
	Interaction:
		existingLine: Cart Line = findLineForProduct(product: product)
		updatedQuantity: Cart Quantity = existingLine.cartQuantity.increaseBy(amount: cartQuantity.value)
		existingLine.cartQuantity = updatedQuantity
		return existingLine
+ addNewProductLine(addProductToCart: Add Product To Cart, product: Product, cartQuantity: Cart Quantity): Cart Line
	Invariant: new product creates line with at least one quantity
	Interaction:
		newLine: Cart Line = new Cart Line(product: product, cartQuantity: cartQuantity)
		lines.add(newLine)
		return newLine
+ removeProductLineFromCollection(removeProductFromCart: Remove Product From Cart, cartLine: Cart Line): void
	Invariant: removing last line empties shopping cart and blocks guest checkout
	Interaction:
		lines.remove(cartLine)
+ applyQuantityChangeOnLine(updateCartQuantity: Update Cart Quantity, cartLine: Cart Line, newQuantity: Cart Quantity): Cart Line
	Invariant: update must not leave a line with zero cart quantity
	Interaction:
		cartLine.cartQuantity = newQuantity
		return cartLine
+ leaveRemainingLinesUnchanged(excludedLine: Cart Line): List<Cart Line>
	Interaction:
		return lines.filter(line: line != excludedLine)
+ findLineForProduct(product: Product): Cart Line
	Interaction:
		return lines.firstMatching(product: product)
+ hasLineForProduct(product: Product): Boolean
	Interaction:
		return findLineForProduct(product: product) != null
+ allLines(): List<Cart Line>
	Interaction:
		return lines
+ isEmpty(): Boolean
	Interaction:
		return lines.isEmpty()
+ lineCount(): Integer
	Interaction:
		return lines.size()
+ persistCurrentState(): void
	Interaction:
		return
+ clearAll(): void
	Interaction:
		lines.clear()

### **Cart Quantity** << ValueObject >>

+ Cart Quantity(value: Integer)
+ Cart Quantity.one(): Cart Quantity
+ Cart Quantity.zero(): Cart Quantity
------
+ value: Integer
	Invariant: cart quantity must be a positive whole number while the line remains in the shopping cart
----
+ increaseBy(amount: Integer): Cart Quantity
	Invariant: result remains a positive whole number
	Interaction:
		newValue: Integer = value + amount
		return new Cart Quantity(value: newValue)
+ isPositiveWholeNumber(): Boolean
	Interaction:
		return value > 0
+ isZero(): Boolean
	Interaction:
		return value == 0

### **Money** << ValueObject >>

+ Money(amount: Decimal, currency: String)
------
+ amount: Decimal
+ currency: String
----
+ multiplyBy(cartQuantity: Integer): Money
	Interaction:
		return new Money(amount: amount * cartQuantity, currency: currency)
+ add(other: Money): Money
	Interaction:
		return new Money(amount: amount + other.amount, currency: currency)
+ Money.zero(): Money
	Interaction:
		return new Money(amount: 0, currency: currency)

### **Add Product To Cart** << Service >>

Initialisation: stateless service — invoked from product detail with browsing context.
------
+ placeProductFromCatalog(product: Product, shoppingCart: Shopping Cart, cartLines: Cart Lines, customer: Customer, stockAvailability: Stock Availability, selectedStore: Selected Store): Cart Line
	Invariant: respects stock availability at browsing context — unavailable products are not placed without acknowledgment
	Interaction:
		if stockAvailability.isUnavailable(product: product, selectedStore: selectedStore):
			stockAvailability.warnBeforeAddingUnavailableProduct(customer: customer, product: product)
			throw UnavailableProductException(product: product)
		if cartLines.hasLineForProduct(product: product):
			return cartLines.mergeAddIntoExistingProductLine(addProductToCart: this, product: product, cartQuantity: Cart Quantity.one())
		return cartLines.addNewProductLine(addProductToCart: this, product: product, cartQuantity: Cart Quantity.one())
+ increaseQuantityOnExistingLine(cartLines: Cart Lines, product: Product): Cart Line
	Interaction:
		return cartLines.mergeAddIntoExistingProductLine(addProductToCart: this, product: product, cartQuantity: Cart Quantity.one())
+ createLineWithAtLeastOneQuantity(cartLines: Cart Lines, product: Product): Cart Line
	Interaction:
		return cartLines.addNewProductLine(addProductToCart: this, product: product, cartQuantity: Cart Quantity.one())
+ preventUnavailableProductAdd(stockAvailability: Stock Availability, product: Product, selectedStore: Selected Store): void
	Invariant: unavailable product add blocked without acknowledgment
	Interaction:
		if stockAvailability.isUnavailable(product: product, selectedStore: selectedStore):
			throw UnavailableProductException(product: product)

### **Update Cart Quantity** << Service >>

Initialisation: stateless service — invoked from shopping cart line edit controls.
------
+ changeCountOnExistingLine(cartLine: Cart Line, newQuantity: Cart Quantity, cartLines: Cart Lines, customer: Customer): Cart Line
	Invariant: update cart quantity must not leave a line with zero cart quantity — use remove product from cart instead
	Interaction:
		if newQuantity.isZero():
			rejectZeroQuantityUpdate(customer: customer)
		return cartLines.applyQuantityChangeOnLine(updateCartQuantity: this, cartLine: cartLine, newQuantity: newQuantity)
+ saveHigherCountOnIncrease(cartLine: Cart Line, newQuantity: Cart Quantity, cartLines: Cart Lines): Cart Line
	Interaction:
		return cartLines.applyQuantityChangeOnLine(updateCartQuantity: this, cartLine: cartLine, newQuantity: newQuantity)
+ saveLowerPositiveCountOnDecrease(cartLine: Cart Line, newQuantity: Cart Quantity, cartLines: Cart Lines): Cart Line
	Interaction:
		return cartLines.applyQuantityChangeOnLine(updateCartQuantity: this, cartLine: cartLine, newQuantity: newQuantity)
+ rejectZeroQuantityUpdate(customer: Customer): void
	Invariant: zero quantity update rejected with clear message
	Interaction:
		directCustomerToRemoveInstead(customer: customer)
		throw ZeroQuantityRejectedException()
+ directCustomerToRemoveInstead(customer: Customer): void
	Interaction:
		customer.directToRemoveProductFromCart()

### **Remove Product From Cart** << Service >>

Initialisation: stateless service — distinct from zero-quantity edit on shopping cart.
------
+ deleteProductLineFromShoppingCart(cartLine: Cart Line, cartLines: Cart Lines, shoppingCart: Shopping Cart): void
	Invariant: removing the last line empties the shopping cart and blocks guest checkout until add product to cart runs again
	Interaction:
		cartLines.removeProductLineFromCollection(removeProductFromCart: this, cartLine: cartLine)
		if shoppingCart.isEmpty():
			shoppingCart.blockCheckoutEntryWhenEmpty()
+ clearLineCartQuantityOnRemoval(cartLine: Cart Line): void
	Interaction:
		cartLine.cartQuantity = Cart Quantity.zero()
+ offerDistinctFromZeroQuantityEdit(customer: Customer): void
	Invariant: remove action is distinct from update cart quantity to zero
	Interaction:
		return
+ emptyCartWhenLastLineRemoved(shoppingCart: Shopping Cart, cartLines: Cart Lines): void
	Interaction:
		if cartLines.isEmpty():
			shoppingCart.blockCheckoutEntryWhenEmpty()

### references

**Ref — Cart module CRC (Sprint 1)**
Source: docs/increments/2-click-and-collect/specification/crc.md
Locator: Increment 2 — Sprint 1: Cart
Extract: partial

```source
### **Cart Lines**
product lines in shopping cart          | Cart Line, Shopping Cart
merge add into existing product line    | Add Product To Cart, Cart Line, Product
add new product line                    | Add Product To Cart, Cart Line, Product
remove product line from collection     | Remove Product From Cart, Cart Line
                                        |   invariant: at most one line per product — no duplicate lines for the same product

### **Update Cart Quantity**
change count on existing line           | Cart Line, Cart Quantity, Customer
reject zero quantity update             | Customer, Remove Product From Cart
                                        |   invariant: update cart quantity must not leave a line with zero cart quantity — use remove product from cart instead
```

**Ref — Cart specification by example**
Source: docs/increments/2-click-and-collect/specification/specification-by-example.md
Locator: Add Product to Cart, Update Cart Quantity, Remove Product from Cart
Extract: partial

```source
When **Customer** *Alex Rivera* runs **Add Product To Cart** for **Product** *Premium Salmon Kibble* again
Then **Cart Lines** still has exactly one **Cart Line** for **Product** *Premium Salmon Kibble*
  And that **Cart Line** shows **Cart Quantity** *2*

When **Customer** *Alex Rivera* attempts **Update Cart Quantity** on that **Cart Line** to **Cart Quantity** *0*
Then **Update Cart Quantity** rejects the change with a clear message
  And **Customer** *Alex Rivera* is directed to run **Remove Product From Cart** instead
```

### decisions made

- *Cart Line* is the state-carrier for per-line product and quantity — container rules stay on *Cart Lines* and *Shopping Cart* (state-carrier rule).
- *Cart Lines* is a collection entity owning merge-on-add, no-duplicate-line, and scoped removal — matches CRC collection-class rule.
- *Add product to cart*, *Update cart quantity*, and *Remove product from cart* remain services mapping to distinct customer stories (typing call from exploration UL).
- *Money* extracted as value object — line total calculation needs typed unit price and quantity (properties trace to CRC).
- Guest checkout, order, and StripeWave omitted — Sprint 1 stops at cart persistence per increment scope (scope-fit test).

---

## Increment 2 — Sprint 2: Checkout & pay

*Order* converts a non-empty *shopping cart* into a paid *click-and-collect order* through *guest checkout*. The typed model covers checkout session state (*Guest Checkout*), pickup commitment (*Click-and-collect Store*), payment capture (*Billing Address*, *Payment Method*), external card processing (*StripeWave*), placed order (*Click-and-collect Order*), and confirmation (*Order Confirmation*), plus named checkout operations.

## **Order**

### **Order** << Entity >>

Initialisation: aggregate root for checkout-to-confirmation — coordinates *Guest Checkout* through payment to *Click-and-collect Order*.
------
+ guestCheckout: Guest Checkout
	Invariant: every click-and-collect order in this increment is guest-only — no customer account is created or required
----
+ convertShoppingCartToPaidOrder(shoppingCart: Shopping Cart, guestCheckout: Guest Checkout, processCardPayment: Process Card Payment via StripeWave): Click-and-collect Order
	Invariant: conversion requires successful StripeWave payment
	Interaction:
		return processCardPayment.createPaidOrderOnProcessorSuccess(shoppingCart: shoppingCart, guestCheckout: guestCheckout)
+ bindBillingAddressToPlacedOrder(clickAndCollectOrder: Click-and-collect Order, billingAddress: Billing Address): Click-and-collect Order
	Interaction:
		clickAndCollectOrder.billingAddress = billingAddress
		return clickAndCollectOrder
+ bindPaymentMethodToPlacedOrder(clickAndCollectOrder: Click-and-collect Order, paymentMethod: Payment Method): Click-and-collect Order
	Interaction:
		clickAndCollectOrder.paymentMethod = paymentMethod
		return clickAndCollectOrder
+ bindClickAndCollectStoreToOrder(clickAndCollectOrder: Click-and-collect Order, clickAndCollectStore: Click-and-collect Store): Click-and-collect Order
	Invariant: a click-and-collect order must reference exactly one click-and-collect store for pickup
	Interaction:
		clickAndCollectOrder.clickAndCollectStore = clickAndCollectStore
		return clickAndCollectOrder
+ progressPaymentToConfirmation(guestCheckout: Guest Checkout, orderConfirmation: Order Confirmation, stripeWave: StripeWave): Order Confirmation
	Invariant: order confirmation follows successful StripeWave payment only
	Interaction:
		return orderConfirmation.acknowledgePlacedClickAndCollectOrder(guestCheckout: guestCheckout, stripeWave: stripeWave)

### **Click-and-collect Order** << Entity >>

+ Click-and-collect Order(orderId: String, customerContact: String, clickAndCollectStore: Click-and-collect Store, cartLines: List<Cart Line>, billingAddress: Billing Address, paymentMethod: Payment Method, orderTotal: Money)
------
+ orderId: String
+ customerContact: String
+ clickAndCollectStore: Click-and-collect Store
+ billingAddress: Billing Address
+ paymentMethod: Payment Method
+ orderTotal: Money
+ << aggregation >> cartLines: List<Cart Line>
+ paymentConfirmed: Boolean
+ guestOnly: Boolean
	Invariant: a click-and-collect order must reference exactly one click-and-collect store for pickup
----
+ originateFromCompletedGuestCheckout(guestCheckout: Guest Checkout, shoppingCart: Shopping Cart): Click-and-collect Order
	Invariant: paid online pickup at chosen store
	Interaction:
		placedOrder: Click-and-collect Order = new Click-and-collect Order(orderId: generateOrderId(), customerContact: guestCheckout.email, clickAndCollectStore: guestCheckout.clickAndCollectStore, cartLines: shoppingCart.handOffLinesToGuestCheckout(guestCheckout: guestCheckout), billingAddress: guestCheckout.billingAddress, paymentMethod: guestCheckout.paymentMethod, orderTotal: shoppingCart.calculateOrderTotal())
		placedOrder.paymentConfirmed = true
		placedOrder.guestOnly = true
		return placedOrder
+ referenceExactlyOnePickupStore(clickAndCollectStore: Click-and-collect Store): void
	Interaction:
		this.clickAndCollectStore = clickAndCollectStore

### **Guest Checkout** << Entity >>

+ Guest Checkout(customer: Customer, shoppingCart: Shopping Cart)
------
+ customer: Customer
+ shoppingCart: Shopping Cart
+ email: String
+ guestOnlyLabel: Boolean
+ clickAndCollectStore: Click-and-collect Store
+ billingAddress: Billing Address
+ paymentMethod: Payment Method
+ processingPayment: Boolean
+ paymentFailureMessage: String
	Invariant: guest checkout requires a chosen click-and-collect store before payment
	Invariant: guest checkout cannot complete without a valid billing address
----
+ startFromNonEmptyShoppingCart(shoppingCart: Shopping Cart, customer: Customer): Guest Checkout
	Invariant: guest checkout blocked when shopping cart empty
	Interaction:
		if shoppingCart.isEmpty():
			blockCheckoutWhenShoppingCartEmpty(customer: customer)
		return new Guest Checkout(customer: customer, shoppingCart: shoppingCart)
+ collectContactEmail(email: String): void
	Invariant: no persistent customer profile created in this fixture
	Interaction:
		this.email = email
+ blockCheckoutWhenShoppingCartEmpty(customer: Customer): void
	Interaction:
		customer.directBackToCatalogOrCart()
		throw EmptyCartCheckoutBlockedException()
+ collectBillingAddressBeforePayment(billingAddress: Billing Address): void
	Interaction:
		this.billingAddress = billingAddress
+ collectPaymentMethodBeforeStripeWave(paymentMethod: Payment Method): void
	Interaction:
		this.paymentMethod = paymentMethod
+ blockPaymentUntilPrerequisitesMet(): Boolean
	Interaction:
		return clickAndCollectStore != null and billingAddress.isValid() and paymentMethod.isSelected()
+ showPaymentFailureWithoutOrder(failureReason: String): void
	Interaction:
		paymentFailureMessage = failureReason
+ preventDuplicatePaymentSubmission(): Boolean
	Interaction:
		return processingPayment
+ setProcessingPayment(processing: Boolean): void
	Interaction:
		processingPayment = processing

### **Click-and-collect Store** << Entity >>

+ Click-and-collect Store(store: Store)
------
+ store: Store
+ storeIdentity: String
+ storeAddress: String
	Invariant: only one click-and-collect store may be selected on a checkout session at a time
----
+ bindToCheckoutSessionOnSelection(guestCheckout: Guest Checkout, store: Store): Click-and-collect Store
	Interaction:
		bound: Click-and-collect Store = new Click-and-collect Store(store: store)
		guestCheckout.clickAndCollectStore = bound
		return bound
+ showStoreIdentityAndAddress(): String
	Interaction:
		return storeIdentity + " — " + storeAddress
+ replaceBindingWhenCustomerChangesStore(guestCheckout: Guest Checkout, store: Store, selectClickAndCollectStore: Select Click-and-collect Store): Click-and-collect Store
	Interaction:
		return selectClickAndCollectStore.updateBindingWhenCustomerChangesStore(guestCheckout: guestCheckout, store: store)
+ attachToPlacedOrderOnSuccess(clickAndCollectOrder: Click-and-collect Order): void
	Interaction:
		clickAndCollectOrder.referenceExactlyOnePickupStore(clickAndCollectStore: this)
+ blockPaymentUntilStoreChosen(guestCheckout: Guest Checkout): Boolean
	Interaction:
		return guestCheckout.clickAndCollectStore != null

### **Billing Address** << ValueObject >>

+ Billing Address(name: String, street: String, city: String, postalCode: String, country: String)
------
+ name: String
+ street: String
+ city: String
+ postalCode: String
+ country: String
	Invariant: guest checkout cannot complete without a valid billing address
----
+ isValid(): Boolean
	Interaction:
		return name != null and street != null and city != null and postalCode != null and country != null
+ saveOnCheckoutSessionWhenValid(guestCheckout: Guest Checkout): void
	Invariant: reject incomplete or invalid submission
	Interaction:
		if not isValid():
			throw InvalidBillingAddressException()
		guestCheckout.billingAddress = this
+ replacePriorValuesBeforePayment(guestCheckout: Guest Checkout, revised: Billing Address): Billing Address
	Interaction:
		guestCheckout.billingAddress = revised
		return revised
+ attachToClickAndCollectOrderOnPay(clickAndCollectOrder: Click-and-collect Order): void
	Interaction:
		clickAndCollectOrder.billingAddress = this
+ equals(other: Billing Address): Boolean
	Interaction:
		return name == other.name and street == other.street and city == other.city and postalCode == other.postalCode and country == other.country

### **Payment Method** << ValueObject >>

+ Payment Method.cardViaStripeWave(): Payment Method
------
+ processorLabel: String
+ cardSelected: Boolean
	Invariant: only card payment via StripeWave is supported in this fixture
----
+ recordCardChoiceOnCheckoutSession(guestCheckout: Guest Checkout): void
	Interaction:
		cardSelected = true
		guestCheckout.paymentMethod = this
+ blockStripeWaveUntilMethodSelected(guestCheckout: Guest Checkout): Boolean
	Interaction:
		return guestCheckout.paymentMethod != null and guestCheckout.paymentMethod.cardSelected
+ passDetailsToStripeWaveOnPlaceOrder(stripeWave: StripeWave, orderTotal: Money): StripeWaveResult
	Interaction:
		return stripeWave.processCardChargeForOrder(paymentMethod: this, orderTotal: orderTotal)
+ attachToClickAndCollectOrderOnPay(clickAndCollectOrder: Click-and-collect Order): void
	Interaction:
		clickAndCollectOrder.paymentMethod = this
+ isSelected(): Boolean
	Interaction:
		return cardSelected
+ rejectNonCardPaymentAlternatives(): void
	Interaction:
		throw UnsupportedPaymentMethodException()

### **Order Confirmation** << Entity >>

Initialisation: created only after StripeWave reports payment success.
------
+ orderId: String
+ emailSentTo: String
+ confirmationComplete: Boolean
+ confirmationScreenSummary: String
----
+ acknowledgePlacedClickAndCollectOrder(guestCheckout: Guest Checkout, stripeWave: StripeWave): Order Confirmation
	Invariant: order confirmation follows successful StripeWave payment only
	Interaction:
		if not stripeWave.reportedSuccess():
			throw PaymentNotConfirmedException()
		confirmationComplete = true
		return this
+ sendConfirmationEmailAfterSuccess(guestCheckout: Guest Checkout, clickAndCollectOrder: Click-and-collect Order, clickAndCollectStore: Click-and-collect Store): void
	Interaction:
		emailSentTo = guestCheckout.email
+ showOrderSummaryOnConfirmationScreen(clickAndCollectOrder: Click-and-collect Order, clickAndCollectStore: Click-and-collect Store): String
	Interaction:
		confirmationScreenSummary = clickAndCollectOrder.orderId + " — " + clickAndCollectStore.storeIdentity + " — " + clickAndCollectOrder.orderTotal.amount
		return confirmationScreenSummary
+ isComplete(): Boolean
	Interaction:
		return confirmationComplete
+ withholdUntilStripeWaveSuccess(stripeWave: StripeWave): Boolean
	Interaction:
		return stripeWave.reportedSuccess()

### **Select Click-and-collect Store** << Service >>

Initialisation: stateless service — invoked at guest checkout start.
------
+ presentEligibleStoresAtCheckoutStart(stores: List<Store>, guestCheckout: Guest Checkout): List<Click-and-collect Store>
	Interaction:
		return stores.map(store: new Click-and-collect Store(store: store))
+ letCustomerPickOnePickupLocation(clickAndCollectStore: Click-and-collect Store, guestCheckout: Guest Checkout, store: Store): Click-and-collect Store
	Interaction:
		return clickAndCollectStore.bindToCheckoutSessionOnSelection(guestCheckout: guestCheckout, store: store)
+ bindSelectionToCheckoutSession(clickAndCollectStore: Click-and-collect Store, guestCheckout: Guest Checkout): Click-and-collect Store
	Invariant: select click-and-collect store must complete before payment and order confirmation
	Interaction:
		guestCheckout.clickAndCollectStore = clickAndCollectStore
		return clickAndCollectStore
+ updateBindingWhenCustomerChangesStore(guestCheckout: Guest Checkout, store: Store): Click-and-collect Store
	Interaction:
		replacement: Click-and-collect Store = new Click-and-collect Store(store: store)
		guestCheckout.clickAndCollectStore = replacement
		return replacement

### **Enter Billing Address** << Service >>

Initialisation: stateless service — invoked at billing step after store selection.
------
+ presentBillingAddressFieldsAtBillingStep(guestCheckout: Guest Checkout): List<String>
	Interaction:
		return List.of("name", "street", "city", "postalCode", "country")
+ saveValidBillingAddressOnSession(billingAddress: Billing Address, guestCheckout: Guest Checkout): Billing Address
	Interaction:
		billingAddress.saveOnCheckoutSessionWhenValid(guestCheckout: guestCheckout)
		return billingAddress
+ rejectIncompleteOrInvalidSubmission(billingAddress: Billing Address): void
	Invariant: StripeWave not invoked on invalid billing
	Interaction:
		if not billingAddress.isValid():
			throw InvalidBillingAddressException()
+ replacePriorValuesOnRevision(revised: Billing Address, guestCheckout: Guest Checkout): Billing Address
	Interaction:
		return revised.replacePriorValuesBeforePayment(guestCheckout: guestCheckout, revised: revised)
+ attachBillingAddressToPlacedOrder(billingAddress: Billing Address, clickAndCollectOrder: Click-and-collect Order): void
	Interaction:
		billingAddress.attachToClickAndCollectOrderOnPay(clickAndCollectOrder: clickAndCollectOrder)
+ blockStripeWaveOnInvalidBilling(billingAddress: Billing Address): Boolean
	Interaction:
		return billingAddress.isValid()

### **Select Payment Method** << Service >>

Initialisation: stateless service — invoked at payment step after valid billing address.
------
+ presentCardAsOnlyPaymentMethodOption(): Payment Method
	Interaction:
		return Payment Method.cardViaStripeWave()
+ enablePlaceOrderAfterMethodSelection(paymentMethod: Payment Method, guestCheckout: Guest Checkout): void
	Interaction:
		paymentMethod.recordCardChoiceOnCheckoutSession(guestCheckout: guestCheckout)
+ blockStripeWaveWithoutMethodSelection(guestCheckout: Guest Checkout): Boolean
	Interaction:
		return guestCheckout.paymentMethod != null and guestCheckout.paymentMethod.isSelected()
+ rejectNonCardPaymentAlternatives(paymentMethod: Payment Method): void
	Interaction:
		paymentMethod.rejectNonCardPaymentAlternatives()

### **Process Card Payment via StripeWave** << Service >>

Initialisation: stateless service — invoked when checkout prerequisites are complete.
------
+ invokeStripeWaveWhenPrerequisitesMet(guestCheckout: Guest Checkout, stripeWave: StripeWave, billingAddress: Billing Address, clickAndCollectStore: Click-and-collect Store, paymentMethod: Payment Method): StripeWaveResult
	Invariant: no click-and-collect order is created until StripeWave reports payment success
	Interaction:
		if not guestCheckout.blockPaymentUntilPrerequisitesMet():
			throw CheckoutPrerequisitesIncompleteException()
		guestCheckout.setProcessingPayment(processing: true)
		orderTotal: Money = guestCheckout.shoppingCart.calculateOrderTotal()
		return paymentMethod.passDetailsToStripeWaveOnPlaceOrder(stripeWave: stripeWave, orderTotal: orderTotal)
+ createPaidOrderOnProcessorSuccess(shoppingCart: Shopping Cart, guestCheckout: Guest Checkout): Click-and-collect Order
	Interaction:
		placedOrder: Click-and-collect Order = Click-and-collect Order.originateFromCompletedGuestCheckout(guestCheckout: guestCheckout, shoppingCart: shoppingCart)
		guestCheckout.clickAndCollectStore.attachToPlacedOrderOnSuccess(clickAndCollectOrder: placedOrder)
		guestCheckout.billingAddress.attachToClickAndCollectOrderOnPay(clickAndCollectOrder: placedOrder)
		guestCheckout.paymentMethod.attachToClickAndCollectOrderOnPay(clickAndCollectOrder: placedOrder)
		return placedOrder
+ clearShoppingCartAfterSuccessfulPay(shoppingCart: Shopping Cart): void
	Interaction:
		shoppingCart.clearAllLinesAfterPayment()
+ showFailureWithoutCreatingOrder(guestCheckout: Guest Checkout, failureReason: String): void
	Interaction:
		guestCheckout.showPaymentFailureWithoutOrder(failureReason: failureReason)
		guestCheckout.setProcessingPayment(processing: false)
+ preventDuplicatePaymentSubmission(guestCheckout: Guest Checkout): Boolean
	Interaction:
		return guestCheckout.preventDuplicatePaymentSubmission()
+ withholdConfirmationUntilSuccess(orderConfirmation: Order Confirmation, guestCheckout: Guest Checkout, stripeWave: StripeWave): Order Confirmation
	Interaction:
		if stripeWave.reportedSuccess():
			return orderConfirmation.acknowledgePlacedClickAndCollectOrder(guestCheckout: guestCheckout, stripeWave: stripeWave)
		throw PaymentNotConfirmedException()

### references

**Ref — Order module CRC (Sprint 2)**
Source: docs/increments/2-click-and-collect/specification/crc.md
Locator: Increment 2 — Sprint 2: Checkout & pay
Extract: partial

```source
### **Guest Checkout**
pay without account in this fixture       | Customer, Shopping Cart, Click-and-collect Order
collect billing address before payment    | Billing Address, Customer
require click-and-collect store first     | Click-and-collect Store, Select Click-and-collect Store
                                        |   invariant: guest checkout requires a chosen click-and-collect store before payment

### **Process Card Payment via StripeWave**
invoke StripeWave when prerequisites met  | StripeWave, Payment Method, Guest Checkout, Billing Address, Click-and-collect Store
create paid order on processor success      | Click-and-collect Order, Shopping Cart, Guest Checkout
                                        |   invariant: no click-and-collect order is created until StripeWave reports payment success
```

**Ref — Checkout specification by example**
Source: docs/increments/2-click-and-collect/specification/specification-by-example.md
Locator: Select Click-and-Collect Store through Confirm Order and Send Confirmation Email
Extract: partial

```source
When **Customer** *Alex Rivera* runs **Process Card Payment via StripeWave** and **StripeWave** reports payment success
Then **Guest Checkout** produces **Click-and-collect Order** *CNC-1042*
  And **Shopping Cart** for **Customer** *Alex Rivera* has no **Cart Lines** after successful payment

When **StripeWave** reports payment failure *card declined*
Then no **Click-and-collect Order** is created
  And **Order Confirmation** is not sent
```

### decisions made

- *Order* owns checkout-to-confirmation coordination; *Cart* owns pre-payment lines — handoff at successful *process card payment via StripeWave* (independence test).
- *Click-and-collect Store* is distinct from Increment 1 *selected store* — checkout pickup commitment, not browse context (scope-fit test).
- *Select click-and-collect store*, *enter billing address*, *select payment method*, and *process card payment via StripeWave* remain services mapping to distinct stories (typing call).
- *StripeWave* is an external payment port in boundary domain — domain owns when to invoke and how to interpret success (boundary port pattern).
- *Order fulfillment* lifecycle deferred to Sprint 3 — Sprint 2 *click-and-collect order* carries payment and confirmation state only (scope-fit test).

---

## Increment 2 — Sprint 3: Store pickup

*Order fulfillment* spans *store employee* preparation and pickup handoff at the *click-and-collect store*. The typed model covers paid-order queue exposure (*Fulfillment Queue*), lifecycle on placed orders (*Click-and-collect Order*, *Order Fulfillment*), store-scoped employee context (*Click-and-collect Store*), and named employee operations (*Prepare Click-and-collect Orders for Pickup*, *Fulfill Click-and-collect Order*).

## **Order**

### **Order** << Entity >>

Initialisation: extends Sprint 2 paid-order aggregate — Sprint 3 adds fulfillment progression after *Order Confirmation*.
------
+ orderFulfillment: Order Fulfillment
	Invariant: order fulfillment begins only after order confirmation for a paid click-and-collect order
----
+ progressFulfillmentAfterConfirmation(orderConfirmation: Order Confirmation, clickAndCollectOrder: Click-and-collect Order, orderFulfillment: Order Fulfillment): Order Fulfillment
	Invariant: fulfillment progression requires successful payment and order confirmation
	Interaction:
		if clickAndCollectOrder.hasSuccessfulPaymentAndConfirmation(orderConfirmation: orderConfirmation):
			clickAndCollectOrder.awaitPreparationAfterConfirmation(orderFulfillment: orderFulfillment)
			return orderFulfillment
		throw UnconfirmedOrderException(clickAndCollectOrder: clickAndCollectOrder)
+ scopePreparationAndHandoffToStore(clickAndCollectStore: Click-and-collect Store, fulfillmentQueue: Fulfillment Queue): Fulfillment Queue
	Invariant: preparation and handoff remain scoped to the order click-and-collect store
	Interaction:
		return fulfillmentQueue.filterToStoreScope(clickAndCollectStore: clickAndCollectStore)

### **Click-and-collect Order** << Entity >>

+ Click-and-collect Order(orderId: String, customerContact: String, clickAndCollectStore: Click-and-collect Store, orderFulfillment: Order Fulfillment, cartLines: List<Cart Line>, orderConfirmation: Order Confirmation)
------
+ orderId: String
+ customerContact: String
+ clickAndCollectStore: Click-and-collect Store
	Invariant: a click-and-collect order must reference exactly one click-and-collect store for pickup
+ << composition >> orderFulfillment: Order Fulfillment
+ << aggregation >> cartLines: List<Cart Line>
+ orderConfirmation: Order Confirmation
+ paymentConfirmed: Boolean
	Invariant: a click-and-collect order in the fulfillment queue must have successful payment and order confirmation
----
+ awaitPreparationAfterConfirmation(orderFulfillment: Order Fulfillment): void
	Invariant: fulfillment status starts at awaiting preparation after order confirmation
	Interaction:
		orderFulfillment.markAwaitingPreparation()
+ transitionToReadyForCollection(prepareClickAndCollectOrdersForPickup: Prepare Click-and-collect Orders for Pickup): Order Fulfillment
	Invariant: prepare click-and-collect orders for pickup runs only after order confirmation for that order
	Interaction:
		return orderFulfillment.markReadyForCollection(prepareClickAndCollectOrdersForPickup: prepareClickAndCollectOrdersForPickup)
+ blockHandoffUntilPreparationComplete(fulfillClickAndCollectOrder: Fulfill Click-and-collect Order): Boolean
	Invariant: fulfill click-and-collect order must not complete until preparation marks the order ready for collection
	Interaction:
		return orderFulfillment.isAwaitingPreparation()
+ markCollectedOrClosedAfterHandoff(fulfillClickAndCollectOrder: Fulfill Click-and-collect Order): Order Fulfillment
	Invariant: fulfill click-and-collect order completes order fulfillment for that click-and-collect order exactly once
	Interaction:
		return orderFulfillment.markCollectedOrClosed(fulfillClickAndCollectOrder: fulfillClickAndCollectOrder)
+ excludeUnpaidOrdersFromFulfillmentQueue(): Boolean
	Interaction:
		return paymentConfirmed && orderConfirmation.isComplete()
+ hasSuccessfulPaymentAndConfirmation(orderConfirmation: Order Confirmation): Boolean
	Interaction:
		return paymentConfirmed && orderConfirmation.isComplete()
+ isReadyForCollection(): Boolean
	Interaction:
		return orderFulfillment.isReadyForCollection()
+ isAwaitingPreparation(): Boolean
	Interaction:
		return orderFulfillment.isAwaitingPreparation()
+ isFulfillmentComplete(): Boolean
	Interaction:
		return orderFulfillment.isComplete()
+ matchesOrderProof(presentedOrderId: String): Boolean
	Interaction:
		return orderId == presentedOrderId
+ showLinesForHandoffDetail(): List<Cart Line>
	Interaction:
		return cartLines

### **Order Fulfillment** << Entity >>

+ Order Fulfillment(status: OrderFulfillmentStatus)
------
+ status: OrderFulfillmentStatus
	Invariant: order fulfillment completes only after fulfill click-and-collect order succeeds for a prepared order
----
+ markAwaitingPreparation(): void
	Interaction:
		status = OrderFulfillmentStatus.AWAITING_PREPARATION
+ markReadyForCollection(prepareClickAndCollectOrdersForPickup: Prepare Click-and-collect Orders for Pickup): Order Fulfillment
	Invariant: status becomes ready for collection when store employee marks order preparing
	Interaction:
		status = OrderFulfillmentStatus.READY_FOR_COLLECTION
		return this
+ markComplete(fulfillClickAndCollectOrder: Fulfill Click-and-collect Order): Order Fulfillment
	Invariant: order fulfillment completes only after fulfill click-and-collect order succeeds for a prepared order
	Interaction:
		status = OrderFulfillmentStatus.COMPLETE
		return this
+ markCollectedOrClosed(fulfillClickAndCollectOrder: Fulfill Click-and-collect Order): Order Fulfillment
	Invariant: fulfill click-and-collect order completes order fulfillment exactly once
	Interaction:
		status = OrderFulfillmentStatus.COLLECTED
		return this
+ blockPrematureCompletionBeforePrepare(): Boolean
	Invariant: fulfill click-and-collect order must not complete until preparation marks the order ready for collection
	Interaction:
		return status == OrderFulfillmentStatus.AWAITING_PREPARATION
+ isAwaitingPreparation(): Boolean
	Interaction:
		return status == OrderFulfillmentStatus.AWAITING_PREPARATION
+ isReadyForCollection(): Boolean
	Interaction:
		return status == OrderFulfillmentStatus.READY_FOR_COLLECTION
+ isComplete(): Boolean
	Interaction:
		return status == OrderFulfillmentStatus.COMPLETE || status == OrderFulfillmentStatus.COLLECTED || status == OrderFulfillmentStatus.CLOSED
+ isClosedAgainstRepeatPickup(): Boolean
	Interaction:
		return status == OrderFulfillmentStatus.COLLECTED || status == OrderFulfillmentStatus.CLOSED

### **OrderFulfillmentStatus** << ValueObject >>

Constants:
+ AWAITING_PREPARATION: String = "awaiting preparation"
+ READY_FOR_COLLECTION: String = "ready for collection"
+ COMPLETE: String = "complete"
+ COLLECTED: String = "collected"
+ CLOSED: String = "closed"

### **Click-and-collect Store** << Entity >>

Initialisation: checkout-bound pickup location from Sprint 2 — Sprint 3 adds fulfillment queue scoping.
------
+ storeIdentity: String
+ displayName: String
	Invariant: fulfillment queue lists only click-and-collect orders for the employee click-and-collect store context
----
+ scopeFulfillmentQueueToOneLocation(fulfillmentQueue: Fulfillment Queue): Fulfillment Queue
	Interaction:
		return fulfillmentQueue.filterToStoreScope(clickAndCollectStore: this)
+ filterQueueToOrdersForThisStoreOnly(fulfillmentQueue: Fulfillment Queue, storeEmployee: Store Employee): List<Click-and-collect Order>
	Invariant: orders for other store locations are not mixed into one queue
	Interaction:
		return fulfillmentQueue.listPaidOrdersAwaitingPreparation()
+ bindEmployeeContextToStoreAtLogin(storeEmployee: Store Employee, fulfillmentQueue: Fulfillment Queue): Fulfillment Queue
	Interaction:
		storeEmployee.bindToClickAndCollectStore(clickAndCollectStore: this)
		return scopeFulfillmentQueueToOneLocation(fulfillmentQueue: fulfillmentQueue)
+ equals(other: Click-and-collect Store): Boolean
	Interaction:
		return storeIdentity == other.storeIdentity

### **Fulfillment Queue** << Entity >>

+ Fulfillment Queue(clickAndCollectStore: Click-and-collect Store)
------
+ clickAndCollectStore: Click-and-collect Store
+ << aggregation >> awaitingPreparationOrders: List<Click-and-collect Order>
	Invariant: only store employees may access the fulfillment queue and its actions
----
+ listPaidOrdersAwaitingPreparation(): List<FulfillmentQueueRow>
	Invariant: queue row shows order id, customer contact, fulfillment status, and pickup context
	Interaction:
		eligibleOrders: List<Click-and-collect Order> = awaitingPreparationOrders.filter(order: order.excludeUnpaidOrdersFromFulfillmentQueue())
		rows: List<FulfillmentQueueRow> = for each order in eligibleOrders: FulfillmentQueueRow.fromClickAndCollectOrder(clickAndCollectOrder: order)
		return rows
+ excludeUnpaidOrUnconfirmedSessions(orderConfirmation: Order Confirmation, clickAndCollectOrder: Click-and-collect Order): List<Click-and-collect Order>
	Invariant: unpaid or failed-checkout sessions are excluded from prepare click-and-collect orders for pickup
	Interaction:
		return awaitingPreparationOrders.filter(order: order.hasSuccessfulPaymentAndConfirmation(orderConfirmation: orderConfirmation))
+ removeOrderFromActiveQueueOnFulfill(fulfillClickAndCollectOrder: Fulfill Click-and-collect Order, clickAndCollectOrder: Click-and-collect Order): void
	Interaction:
		awaitingPreparationOrders.remove(clickAndCollectOrder)
+ openOrderDetailForHandoffPrep(fulfillClickAndCollectOrder: Fulfill Click-and-collect Order, storeEmployee: Store Employee, clickAndCollectOrder: Click-and-collect Order): Click-and-collect Order
	Interaction:
		return clickAndCollectOrder
+ filterToStoreScope(clickAndCollectStore: Click-and-collect Store): Fulfillment Queue
	Invariant: fulfillment queue lists only click-and-collect orders for the employee click-and-collect store context
	Interaction:
		scopedOrders: List<Click-and-collect Order> = awaitingPreparationOrders.filter(order: order.clickAndCollectStore.equals(other: clickAndCollectStore))
		return new Fulfillment Queue(clickAndCollectStore: clickAndCollectStore, awaitingPreparationOrders: scopedOrders)
+ containsOrder(clickAndCollectOrder: Click-and-collect Order): Boolean
	Interaction:
		return awaitingPreparationOrders.contains(clickAndCollectOrder)
+ addConfirmedOrder(clickAndCollectOrder: Click-and-collect Order, orderConfirmation: Order Confirmation): void
	Invariant: only paid click-and-collect order entries with order confirmation appear in the queue
	Interaction:
		if clickAndCollectOrder.hasSuccessfulPaymentAndConfirmation(orderConfirmation: orderConfirmation):
			awaitingPreparationOrders.add(clickAndCollectOrder)

### **FulfillmentQueueRow** << ValueObject >>

+ FulfillmentQueueRow.fromClickAndCollectOrder(clickAndCollectOrder: Click-and-collect Order): FulfillmentQueueRow
------
+ orderId: String
+ customerContact: String
+ orderFulfillmentStatus: OrderFulfillmentStatus
+ clickAndCollectStoreName: String
----
+ showOrderIdContactStatusAndPickupContext(): FulfillmentQueueRow
	Interaction:
		return this

### **Order Confirmation** << Entity >>

Initialisation: Sprint 2 boundary reference — Sprint 3 uses queue exposure after successful payment.
------
+ confirmationComplete: Boolean
----
+ isComplete(): Boolean
	Interaction:
		return confirmationComplete
+ exposeOrderToFulfillmentQueue(fulfillmentQueue: Fulfillment Queue, clickAndCollectOrder: Click-and-collect Order): void
	Invariant: order confirmation follows successful StripeWave payment only
	Interaction:
		fulfillmentQueue.addConfirmedOrder(clickAndCollectOrder: clickAndCollectOrder, orderConfirmation: this)

### **Prepare Click-and-collect Orders for Pickup** << Service >>

Initialisation: stateless service — invoked by store employee on fulfillment queue routes.
------
+ openQueueForClickAndCollectStore(fulfillmentQueue: Fulfillment Queue, storeEmployee: Store Employee, clickAndCollectStore: Click-and-collect Store): List<FulfillmentQueueRow>
	Invariant: only store employees may access the fulfillment queue and its actions
	Interaction:
		scopedQueue: Fulfillment Queue = clickAndCollectStore.scopeFulfillmentQueueToOneLocation(fulfillmentQueue: fulfillmentQueue)
		return scopedQueue.listPaidOrdersAwaitingPreparation()
+ listPaidOrdersAwaitingPreparation(fulfillmentQueue: Fulfillment Queue): List<FulfillmentQueueRow>
	Interaction:
		return fulfillmentQueue.listPaidOrdersAwaitingPreparation()
+ markOrderPreparingOrStagingEquivalent(clickAndCollectOrder: Click-and-collect Order, orderFulfillment: Order Fulfillment): Order Fulfillment
	Interaction:
		return clickAndCollectOrder.transitionToReadyForCollection(prepareClickAndCollectOrdersForPickup: this)
+ updateStatusToReadyForCollection(clickAndCollectOrder: Click-and-collect Order, orderFulfillment: Order Fulfillment): Order Fulfillment
	Invariant: prepare click-and-collect orders for pickup runs only after order confirmation for that order
	Interaction:
		return markOrderPreparingOrStagingEquivalent(clickAndCollectOrder: clickAndCollectOrder, orderFulfillment: orderFulfillment)
+ keepOrderScopedToItsClickAndCollectStore(clickAndCollectStore: Click-and-collect Store, clickAndCollectOrder: Click-and-collect Order): Boolean
	Invariant: prepare click-and-collect orders for pickup does not reassign the order to another store
	Interaction:
		return clickAndCollectOrder.clickAndCollectStore.equals(other: clickAndCollectStore)

### **Fulfill Click-and-collect Order** << Service >>

Initialisation: stateless service — invoked from fulfillment order detail when preparation is complete.
------
+ openPreparedOrderFromQueue(fulfillmentQueue: Fulfillment Queue, clickAndCollectOrder: Click-and-collect Order, storeEmployee: Store Employee): Click-and-collect Order
	Interaction:
		return fulfillmentQueue.openOrderDetailForHandoffPrep(fulfillClickAndCollectOrder: this, storeEmployee: storeEmployee, clickAndCollectOrder: clickAndCollectOrder)
+ showLinesStoreAndFulfillmentStatus(clickAndCollectOrder: Click-and-collect Order, clickAndCollectStore: Click-and-collect Store, orderFulfillment: Order Fulfillment): Click-and-collect Order
	Interaction:
		return clickAndCollectOrder
+ enableHandoffWhenPreparationComplete(orderFulfillment: Order Fulfillment, storeEmployee: Store Employee): Boolean
	Interaction:
		return orderFulfillment.isReadyForCollection()
+ blockHandoffWhenPreparationIncomplete(orderFulfillment: Order Fulfillment, prepareClickAndCollectOrdersForPickup: Prepare Click-and-collect Orders for Pickup): Boolean
	Invariant: fulfill click-and-collect order must not complete until preparation marks the order ready for collection
	Interaction:
		return orderFulfillment.blockPrematureCompletionBeforePrepare()
+ markOrderFulfillmentCompleteOnConfirm(orderFulfillment: Order Fulfillment, clickAndCollectOrder: Click-and-collect Order): Order Fulfillment
	Invariant: order fulfillment completes only after fulfill click-and-collect order succeeds for a prepared order
	Interaction:
		if clickAndCollectOrder.blockHandoffUntilPreparationComplete(fulfillClickAndCollectOrder: this):
			throw PreparationIncompleteException(clickAndCollectOrder: clickAndCollectOrder)
		return clickAndCollectOrder.markCollectedOrClosedAfterHandoff(fulfillClickAndCollectOrder: this)
+ removeOrderFromActivePreparationQueue(fulfillmentQueue: Fulfillment Queue, clickAndCollectOrder: Click-and-collect Order): void
	Interaction:
		fulfillmentQueue.removeOrderFromActiveQueueOnFulfill(fulfillClickAndCollectOrder: this, clickAndCollectOrder: clickAndCollectOrder)
+ closeOrderAgainstRepeatPickupActions(clickAndCollectOrder: Click-and-collect Order, customer: Customer): Boolean
	Invariant: fulfill click-and-collect order completes order fulfillment for that click-and-collect order exactly once
	Interaction:
		return clickAndCollectOrder.isFulfillmentComplete()
+ confirmHandoffAtPickup(clickAndCollectOrder: Click-and-collect Order, orderFulfillment: Order Fulfillment, fulfillmentQueue: Fulfillment Queue, storeEmployee: Store Employee, customer: Customer): Order Fulfillment
	Invariant: order fulfillment completes when the customer collects the order at the click-and-collect store
	Interaction:
		if blockHandoffWhenPreparationIncomplete(orderFulfillment: orderFulfillment, prepareClickAndCollectOrdersForPickup: new Prepare Click-and-collect Orders for Pickup()):
			throw PreparationIncompleteException(clickAndCollectOrder: clickAndCollectOrder)
		completedFulfillment: Order Fulfillment = markOrderFulfillmentCompleteOnConfirm(orderFulfillment: orderFulfillment, clickAndCollectOrder: clickAndCollectOrder)
		removeOrderFromActivePreparationQueue(fulfillmentQueue: fulfillmentQueue, clickAndCollectOrder: clickAndCollectOrder)
		customer.collectClickAndCollectOrderAtStore(clickAndCollectOrder: clickAndCollectOrder, clickAndCollectStore: clickAndCollectOrder.clickAndCollectStore)
		return completedFulfillment
+ verifyOrderProofMatchesCustomer(clickAndCollectOrder: Click-and-collect Order, presentedOrderId: String, customer: Customer): Boolean
	Interaction:
		return clickAndCollectOrder.matchesOrderProof(presentedOrderId: presentedOrderId)

### references

**Ref — Order fulfillment and employee operations**
Source: docs/increments/2-click-and-collect/specification/crc.md
Locator: Increment 2 — Sprint 3: Store pickup
Extract: partial

```source
### **Fulfillment Queue**
paid orders awaiting preparation per store  | Click-and-collect Order, Click-and-collect Store, Order Confirmation
exclude unpaid or unconfirmed sessions      | Order Confirmation, Click-and-collect Order
                                        |   invariant: only store employees may access the fulfillment queue and its actions

### **Fulfill Click-and-collect Order**
block handoff when preparation incomplete   | Order Fulfillment, Prepare Click-and-collect Orders for Pickup
mark order fulfillment complete on confirm    | Order Fulfillment, Click-and-collect Order
                                        |   invariant: fulfill click-and-collect order completes order fulfillment for that click-and-collect order exactly once
```

**Ref — Fulfillment specification by example**
Source: docs/increments/2-click-and-collect/specification/specification-by-example.md
Locator: Background — Sprint 3; Prepare Click-and-Collect Orders for Pickup; Fulfill Click-and-Collect Order
Extract: partial

```source
When **Store Employee** *Jordan Kim* marks **Click-and-collect Order** *CNC-1042* as preparing through **Prepare Click-and-collect Orders for Pickup**
Then **Click-and-collect Order** *CNC-1042* **Order Fulfillment** status becomes *ready for collection*

When **Store Employee** *Jordan Kim* confirms **Fulfill Click-and-collect Order** at pickup
Then **Order Fulfillment** for **Click-and-collect Order** *CNC-1042* is *complete*
  And **Fulfillment Queue** removes **Click-and-collect Order** *CNC-1042* from the active preparation queue

When **Store Employee** *Jordan Kim* opens **Click-and-collect Order** *CNC-1042* and attempts **Fulfill Click-and-collect Order**
Then **Fulfill Click-and-collect Order** blocks handoff with a warning that preparation is incomplete
  And **Order Fulfillment** for **Click-and-collect Order** *CNC-1042* is not marked *complete*
```

### decisions made

- *Fulfillment Queue* is collection entity owning store-scoped listing, exclusion rules, and queue removal on fulfill — matches CRC collection-class rule.
- *Order Fulfillment* is lifecycle carrier on *Click-and-collect Order* with typed *OrderFulfillmentStatus* — preparation and handoff states do not belong on checkout classes alone (state-carrier rule).
- *Prepare click-and-collect orders for pickup* and *fulfill click-and-collect order* remain separate services mapping to distinct employee stories with sequential invariants (typing call).
- *Order Confirmation* extends Sprint 2 confirmation with fulfillment queue exposure — checkout email and summary remain on Sprint 2 class (scope-fit test).
- *Store Employee* fulfillment actions live in Boundary Domain — queue access is unavailable to *Customer* role (receiver-not-responsible-for-receiving).

---

# Boundary Domain

### **Customer** << Entity >>

Initialisation: anonymous session instance — carries *Shopping Cart* and references Increment 1 *Selected Store*.
------
+ displayName: String
+ shoppingCart: Shopping Cart
+ selectedStore: Selected Store
----
+ addProductToCart(product: Product, addProductToCart: Add Product To Cart, stockAvailability: Stock Availability): Cart Line
	Interaction:
		return addProductToCart.placeProductFromCatalog(product: product, shoppingCart: shoppingCart, cartLines: shoppingCart.cartLines, customer: this, stockAvailability: stockAvailability, selectedStore: selectedStore)
+ openShoppingCartToViewLines(): List<Cart Line>
	Interaction:
		return shoppingCart.showEachLineWithProductIdentity()
+ updateCartQuantityOnLine(cartLine: Cart Line, newQuantity: Cart Quantity, updateCartQuantity: Update Cart Quantity): Cart Line
	Interaction:
		return updateCartQuantity.changeCountOnExistingLine(cartLine: cartLine, newQuantity: newQuantity, cartLines: shoppingCart.cartLines, customer: this)
+ removeProductFromCartOnLine(cartLine: Cart Line, removeProductFromCart: Remove Product From Cart): void
	Interaction:
		removeProductFromCart.deleteProductLineFromShoppingCart(cartLine: cartLine, cartLines: shoppingCart.cartLines, shoppingCart: shoppingCart)
+ continueBrowsingWithPersistedCart(): Shopping Cart
	Interaction:
		shoppingCart.persistUpdatedCountsWhileBrowsing()
		return shoppingCart
+ browseCatalogWithEmptyCart(): void
	Interaction:
		return
+ directToRemoveProductFromCart(): void
	Interaction:
		return
+ directBackToCatalogOrCart(): void
	Interaction:
		return
+ startGuestCheckoutFromShoppingCart(guestCheckout: Guest Checkout): Guest Checkout
	Interaction:
		return guestCheckout.startFromNonEmptyShoppingCart(shoppingCart: shoppingCart, customer: this)
+ selectClickAndCollectStoreAtCheckout(store: Store, selectClickAndCollectStore: Select Click-and-collect Store, guestCheckout: Guest Checkout): Click-and-collect Store
	Interaction:
		clickAndCollectStore: Click-and-collect Store = new Click-and-collect Store(store: store)
		return selectClickAndCollectStore.letCustomerPickOnePickupLocation(clickAndCollectStore: clickAndCollectStore, guestCheckout: guestCheckout, store: store)
+ enterBillingAddressAtCheckout(billingAddress: Billing Address, enterBillingAddress: Enter Billing Address, guestCheckout: Guest Checkout): Billing Address
	Interaction:
		return enterBillingAddress.saveValidBillingAddressOnSession(billingAddress: billingAddress, guestCheckout: guestCheckout)
+ selectPaymentMethodAtCheckout(selectPaymentMethod: Select Payment Method, guestCheckout: Guest Checkout): Payment Method
	Interaction:
		paymentMethod: Payment Method = selectPaymentMethod.presentCardAsOnlyPaymentMethodOption()
		selectPaymentMethod.enablePlaceOrderAfterMethodSelection(paymentMethod: paymentMethod, guestCheckout: guestCheckout)
		return paymentMethod
+ processCardPaymentAtCheckout(processCardPayment: Process Card Payment via StripeWave, guestCheckout: Guest Checkout, stripeWave: StripeWave, orderConfirmation: Order Confirmation): Click-and-collect Order
	Interaction:
		stripeWaveResult: StripeWaveResult = processCardPayment.invokeStripeWaveWhenPrerequisitesMet(guestCheckout: guestCheckout, stripeWave: stripeWave, billingAddress: guestCheckout.billingAddress, clickAndCollectStore: guestCheckout.clickAndCollectStore, paymentMethod: guestCheckout.paymentMethod)
		if stripeWaveResult.isSuccess():
			placedOrder: Click-and-collect Order = processCardPayment.createPaidOrderOnProcessorSuccess(shoppingCart: shoppingCart, guestCheckout: guestCheckout)
			processCardPayment.clearShoppingCartAfterSuccessfulPay(shoppingCart: shoppingCart)
			orderConfirmation.sendConfirmationEmailAfterSuccess(guestCheckout: guestCheckout, clickAndCollectOrder: placedOrder, clickAndCollectStore: placedOrder.clickAndCollectStore)
			return placedOrder
		processCardPayment.showFailureWithoutCreatingOrder(guestCheckout: guestCheckout, failureReason: stripeWaveResult.failureReason())
		throw PaymentFailedException()
+ collectClickAndCollectOrderAtStore(clickAndCollectOrder: Click-and-collect Order, clickAndCollectStore: Click-and-collect Store): void
	Invariant: customer collects order lines at click-and-collect store after fulfill click-and-collect order succeeds
	Interaction:
		return

### **Product** << Entity >>

+ Product(catalogItemIdentity: String, unitPrice: Money)
------
+ catalogItemIdentity: String
+ unitPrice: Money
----
+ equals(other: Product): Boolean
	Interaction:
		return catalogItemIdentity == other.catalogItemIdentity

### **Stock Availability** << Service >>

Initialisation: stateless boundary service — reads Increment 1 inventory at browsing context.
------
+ isUnavailable(product: Product, selectedStore: Selected Store): Boolean
	Interaction:
		return lookupAvailability(product: product, selectedStore: selectedStore) == AvailabilityStatus.UNAVAILABLE
+ warnBeforeAddingUnavailableProduct(customer: Customer, product: Product): void
	Invariant: customer sees clear warning before unavailable product is placed
	Interaction:
		return
+ blockOrWarnOnUnavailableAdd(product: Product, selectedStore: Selected Store, customer: Customer): void
	Interaction:
		if isUnavailable(product: product, selectedStore: selectedStore):
			warnBeforeAddingUnavailableProduct(customer: customer, product: product)

### **Selected Store** << Entity >>

Initialisation: reference from Increment 1 — browsing context for add-from-detail.
------
+ storeIdentity: String
----
+ scopesCatalogBrowse(): String
	Interaction:
		return storeIdentity

### **Store** << Entity >>

+ Store(retailLocationIdentity: String, geographicPlacement: String)
------
+ retailLocationIdentity: String
+ geographicPlacement: String
----
+ supplyIdentityAndAddressAtCheckout(): Click-and-collect Store
	Interaction:
		return new Click-and-collect Store(store: this)
+ equals(other: Store): Boolean
	Interaction:
		return retailLocationIdentity == other.retailLocationIdentity

### **StripeWave** << Service >>

Initialisation: external payment processor port — invoked only through *Process Card Payment via StripeWave*.
------
+ lastResult: StripeWaveResult
----
+ processCardChargeForOrder(paymentMethod: Payment Method, orderTotal: Money): StripeWaveResult
	Invariant: a click-and-collect order is not confirmed until StripeWave reports payment success
	Interaction:
		lastResult = StripeWaveResult.fromProcessorResponse(outcome: processorCharge(paymentMethod: paymentMethod, orderTotal: orderTotal))
		return lastResult
+ returnSuccessOrFailureToGuestCheckout(guestCheckout: Guest Checkout, result: StripeWaveResult): StripeWaveResult
	Interaction:
		if result.isFailure():
			guestCheckout.showPaymentFailureWithoutOrder(failureReason: result.failureReason())
		return result
+ withholdOrderConfirmationOnFailure(orderConfirmation: Order Confirmation, result: StripeWaveResult): Boolean
	Interaction:
		return result.isSuccess()
+ reportedSuccess(): Boolean
	Interaction:
		return lastResult.isSuccess()

### **StripeWaveResult** << ValueObject >>

+ StripeWaveResult.fromProcessorResponse(outcome: String): StripeWaveResult
------
+ outcome: String
----
+ isSuccess(): Boolean
	Interaction:
		return outcome == "success"
+ isFailure(): Boolean
	Interaction:
		return outcome == "card declined"
+ failureReason(): String
	Interaction:
		return outcome

### **Store Employee** << Entity >>

+ Store Employee(displayName: String, boundClickAndCollectStore: Click-and-collect Store)
------
+ displayName: String
+ boundClickAndCollectStore: Click-and-collect Store
	Invariant: store employee fulfillment actions are unavailable to customer role
----
+ bindToClickAndCollectStore(clickAndCollectStore: Click-and-collect Store): void
	Interaction:
		boundClickAndCollectStore = clickAndCollectStore
+ openFulfillmentQueueForStore(fulfillmentQueue: Fulfillment Queue, prepareClickAndCollectOrdersForPickup: Prepare Click-and-collect Orders for Pickup): List<FulfillmentQueueRow>
	Interaction:
		return prepareClickAndCollectOrdersForPickup.openQueueForClickAndCollectStore(fulfillmentQueue: fulfillmentQueue, storeEmployee: this, clickAndCollectStore: boundClickAndCollectStore)
+ markOrdersPreparingForPickup(clickAndCollectOrder: Click-and-collect Order, prepareClickAndCollectOrdersForPickup: Prepare Click-and-collect Orders for Pickup): Order Fulfillment
	Interaction:
		return prepareClickAndCollectOrdersForPickup.updateStatusToReadyForCollection(clickAndCollectOrder: clickAndCollectOrder, orderFulfillment: clickAndCollectOrder.orderFulfillment)
+ openPreparedOrderFromQueue(fulfillmentQueue: Fulfillment Queue, clickAndCollectOrder: Click-and-collect Order, fulfillClickAndCollectOrder: Fulfill Click-and-collect Order): Click-and-collect Order
	Interaction:
		return fulfillClickAndCollectOrder.openPreparedOrderFromQueue(fulfillmentQueue: fulfillmentQueue, clickAndCollectOrder: clickAndCollectOrder, storeEmployee: this)
+ confirmFulfillClickAndCollectOrder(clickAndCollectOrder: Click-and-collect Order, fulfillClickAndCollectOrder: Fulfill Click-and-collect Order, fulfillmentQueue: Fulfillment Queue, customer: Customer): Order Fulfillment
	Interaction:
		return fulfillClickAndCollectOrder.confirmHandoffAtPickup(clickAndCollectOrder: clickAndCollectOrder, orderFulfillment: clickAndCollectOrder.orderFulfillment, fulfillmentQueue: fulfillmentQueue, storeEmployee: this, customer: customer)
+ verifyOrderProofAtPickup(clickAndCollectOrder: Click-and-collect Order, presentedOrderId: String, customer: Customer, fulfillClickAndCollectOrder: Fulfill Click-and-collect Order): Boolean
	Interaction:
		return fulfillClickAndCollectOrder.verifyOrderProofMatchesCustomer(clickAndCollectOrder: clickAndCollectOrder, presentedOrderId: presentedOrderId, customer: customer)

### references

**Ref — Cart boundary concepts**
Source: docs/increments/2-click-and-collect/specification/crc.md
Locator: Boundary Domain
Extract: partial

```source
### **Customer**
add product to cart from catalog       | Add Product To Cart, Product, Shopping Cart
open shopping cart to view lines       | Shopping Cart, Cart Line
update cart quantity on line           | Update Cart Quantity, Cart Line
remove product from cart on line       | Remove Product From Cart, Cart Line
continue browsing with persisted cart  | Shopping Cart, Cart Lines

### **Stock Availability**
availability at browsing context       | Product, Add Product To Cart
block or warn on unavailable add       | Add Product To Cart, Customer

### **Store**
supply identity and address at checkout | Click-and-collect Store, Guest Checkout

### **StripeWave**
process card charge for order          | Payment Method, Process Card Payment via StripeWave
return success or failure to guest checkout | Guest Checkout
```

### decisions made

- *Product* and *Stock Availability* remain Catalog and Increment 1 boundaries — cart references them without redefining assortment (scope-fit test).
- *Customer* owns cart and checkout entry actions; *Guest Checkout* and operation services own session and payment rules — CRC receiver-not-responsible rule preserved at typed layer.
- *Selected Store* scopes catalog browse; *Click-and-collect Store* scopes checkout pickup — distinct boundary commitments (scope-fit test).
- *StripeWave* remains thin external port — domain decides when to charge and how to interpret outcomes (boundary port pattern).
- *Store Employee* owns fulfillment queue and handoff actions; *Customer* collects after *fulfill click-and-collect order* — Sprint 3 boundary extension (receiver-not-responsible-for-receiving).
