# DDD Design Building Blocks — Examples

## CRC before and after DDD building blocks

**Before** — vanilla CRC from `abd-class-responsibility-collaborator`:

```
#### **Order**
place                              | Customer, OrderLine
Order Lines                        | OrderLine, Product
calculate total                    | OrderLine
                                   |   invariant: total = sum of line amounts

#### **OrderLine**
hold quantity and price            | Product
calculate line amount              | (quantity × product price)

#### **Product**
provide price                      | (decimal amount)
provide description                | (name, category)

#### **Customer**
place orders                       | Order
contact info              | Address
```

**After** — the same model with DDD building blocks applied:

```
#### **Order** [Entity, Aggregate Root]
identity: customer + order date + items (no two orders from the same customer with identical items on the same day) |
place order                        | Customer (by ID), OrderLine
order lines                        | OrderLine, Product (by ID)
calculate total                    | OrderLine
                                   |   invariant: total = sum of line amounts
                                   |   invariant: status only advances (Draft→Confirmed→Fulfilled)
                                   |   aggregate boundary: OrderLine, Money

#### **OrderLine** [Value Object, within Order Aggregate]
hold quantity and price            | Money
calculate line amount              | (quantity × unit price)

#### **Money** [Value Object]
represent amount and currency      | (amount, currency)
                                   |   invariant: immutable — arithmetic returns new instances

#### **Product** [Entity, separate Aggregate Root]
identity: SKU                      |
provide price                      | (decimal amount)
provide description                | (name, category)

#### **Customer** [Entity, separate Aggregate Root]
identity: email + phone number (no two customers share both) |
place orders                       | Order (by ID)
maintain contact info              | Address

#### **Address** [Value Object]
represent location                 | (street, city, province, postal code)
                                   |   invariant: immutable — replaced, never mutated

#### **OrderRepository** [Repository — added by DDD]
add order                          | Order
remove order                       | Order
update order                       | Order
find orders by customer            | Customer (by ID)
find orders by status              | (status filter)

#### **OrderConfirmed** [Domain Event — surfaced from place order]
notify: payment, inventory         | Order (by ID), Customer (by ID)
                                   |   payload: order ID, customer ID, lines, total, timestamp

#### **OrderFactory** [Factory — extracted from complex creation]
assemble Order with lines          | OrderLine, Product (by ID), Money
                                   |   invariant: new Order always valid (at least one line, correct total)
```

**What changed:**
- `Order` gained stereotype annotations, aggregate boundary, and an identity rule
- `Money` and `Address` were extracted as Value Objects (were implicit in "price" and "contact info")
- `OrderRepository` was **added** — it didn't exist in the domain model
- `OrderConfirmed` was **surfaced** from the "place order" operation as a Domain Event
- `OrderFactory` was **extracted** because assembly has invariants worth protecting
- Cross-aggregate references became **by ID** (Customer, Product) — no object graph coupling

The business questions surface **which transformations apply** to each concept and **what constraints** each transformation carries.
