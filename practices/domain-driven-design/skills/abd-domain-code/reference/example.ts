/**
 * Product Catalog — reference Class Model (domain specification fidelity).
 * Runnable TypeScript illustrating typed properties, factory methods,
 * value objects, entity identity, and stock collaboration functions.
 * Companion diagram: reference/example.drawio
 */

// ---------------------------------------------------------------------------
// Stock availability — errors and validation
// ---------------------------------------------------------------------------

export class NegativeQuantityError extends Error {
  constructor(quantity: number) {
    super(`Quantity must not be negative: ${quantity}`);
    this.name = 'NegativeQuantityError';
  }
}

export class InsufficientStockError extends Error {
  constructor(requested: number, available: number) {
    super(`Insufficient stock: requested ${requested}, available ${available}`);
    this.name = 'InsufficientStockError';
  }
}

function assertStockAvailabilityInputs(
  productSku: string,
  storeCode: string,
  stockLevel: number,
): void {
  if (!productSku) throw new Error('productSku is required');
  if (!storeCode) throw new Error('storeCode is required');
  if (stockLevel < 0) throw new NegativeQuantityError(stockLevel);
}

function assertNonNegativeStockLevel(stockLevel: number): void {
  if (stockLevel < 0) throw new NegativeQuantityError(stockLevel);
}

// ---------------------------------------------------------------------------
// Stock availability — labels and reservation collaborations
// ---------------------------------------------------------------------------

export function walkInAvailabilityLabel(stock: StockAvailability): string {
  if (stock.availableToSellQuantity > 0) return 'In Stock';
  if (stock.backorderEnabled) return 'Backorder Available';
  return 'Out of Stock';
}

export function staffStockLabel(stock: StockAvailability): string {
  if (stock.availableToSellQuantity > 0) {
    return `In Stock -- ${stock.availableToSellQuantity} available`;
  }
  if (stock.backorderEnabled) return 'Backorder Available';
  return 'Out of Stock';
}

function applyStockLevel(stock: StockAvailability, newStockLevel: number): void {
  stock._stockLevel = newStockLevel;
  stock._quantityOnHand = newStockLevel;
  stock._availableToSellQuantity = stock._quantityOnHand - stock._reservedQuantity;
}

function notifyIfLowStock(stock: StockAvailability): void {
  stock._restockAlertTriggered =
    stock._restockAlertTriggered || stock._availableToSellQuantity <= stock.lowStockThreshold;
}

export function gateOrderFlow(stock: StockAvailability, requestedQuantity: number): boolean {
  if (requestedQuantity <= stock.availableToSellQuantity) return true;
  return stock.backorderEnabled;
}

export function reserveStock(stock: StockAvailability, quantity: number): void {
  if (quantity > stock.availableToSellQuantity) {
    throw new InsufficientStockError(quantity, stock.availableToSellQuantity);
  }
  stock._reservedQuantity += quantity;
  stock._availableToSellQuantity = stock._quantityOnHand - stock._reservedQuantity;
}

export function releaseReservedStock(stock: StockAvailability, quantity: number): void {
  if (quantity > stock.reservedQuantity) {
    throw new Error(`Cannot release ${quantity}: only ${stock.reservedQuantity} reserved`);
  }
  stock._reservedQuantity -= quantity;
  stock._availableToSellQuantity = stock._quantityOnHand - stock._reservedQuantity;
}

export function refreshStockFromEmployeeEdit(stock: StockAvailability, newStockLevel: number): void {
  assertNonNegativeStockLevel(newStockLevel);
  applyStockLevel(stock, newStockLevel);
  notifyIfLowStock(stock);
}

export function updateQuantityOnHand(stock: StockAvailability, newQuantity: number): void {
  refreshStockFromEmployeeEdit(stock, newQuantity);
}

// ---------------------------------------------------------------------------
// Key Abstraction: Product Catalog
// ---------------------------------------------------------------------------

/** << Entity >> — per-store stock position for a product SKU. */
export class StockAvailability {
  readonly productSku: string;
  readonly storeCode: string;
  _stockLevel: number;
  _quantityOnHand: number;
  _reservedQuantity: number;
  _availableToSellQuantity: number;
  reorderPoint: number;
  reorderQuantity: number;
  lowStockThreshold: number;
  lastRestockedDate: Date | null;
  expectedRestockDate: Date | null;
  backorderEnabled: boolean;
  _restockAlertTriggered = false;

  constructor(productSku: string, storeCode: string, stockLevel: number, reservedQuantity = 0) {
    assertStockAvailabilityInputs(productSku, storeCode, stockLevel);
    this.productSku = productSku;
    this.storeCode = storeCode;
    this._stockLevel = stockLevel;
    this._quantityOnHand = stockLevel;
    this._reservedQuantity = reservedQuantity;
    this._availableToSellQuantity = stockLevel - reservedQuantity;
    this.reorderPoint = 0;
    this.reorderQuantity = 0;
    this.lowStockThreshold = 5;
    this.lastRestockedDate = null;
    this.expectedRestockDate = null;
    this.backorderEnabled = false;
  }

  get stockLevel(): number { return this._stockLevel; }
  get quantityOnHand(): number { return this._quantityOnHand; }
  get reservedQuantity(): number { return this._reservedQuantity; }
  get availableToSellQuantity(): number { return this._availableToSellQuantity; }
  get restockAlertTriggered(): boolean { return this._restockAlertTriggered; }

  perStoreWalkInAvailabilityDisplay(): string {
    return walkInAvailabilityLabel(this);
  }
}

/** << ValueObject >> — product image metadata owned by a product. */
export class ProductImage {
  readonly imageFile: string;
  readonly altText: string;
  readonly displayOrder: number;
  readonly uploadedDate: Date;

  constructor(imageFile: string, altText: string, displayOrder: number) {
    if (!imageFile) throw new Error('imageFile is required');
    if (!altText) throw new Error('altText is required');
    if (displayOrder < 0) throw new Error('displayOrder must be non-negative');

    this.imageFile = imageFile;
    this.altText = altText;
    this.displayOrder = displayOrder;
    this.uploadedDate = new Date();
  }
}

/** << Entity >> — hierarchical product category. */
export class Category {
  readonly categoryName: string;
  parentCategory: string;
  displayOrder: number;
  activeStatus: boolean;
  private _children: Category[] = [];

  constructor(categoryName: string) {
    if (!categoryName) throw new Error('categoryName is required');

    this.categoryName = categoryName;
    this.parentCategory = '';
    this.displayOrder = 0;
    this.activeStatus = true;
  }

  acceptProduct(_product: Product): void {
    // Registers a product under this category (aggregation tracking)
  }

  children(): Category[] {
    return [...this._children];
  }

  addChild(child: Category): void {
    this._children.push(child);
  }

  breadcrumb(): string {
    if (!this.parentCategory) return this.categoryName;
    return `${this.parentCategory} > ${this.categoryName}`;
  }
}

/** << ValueObject >> — mandatory 1–5 integer star rating on a customer review. */
export class StarRating {
  readonly value: number;

  private constructor(value: number) {
    this.value = value;
  }

  static of(value: number): StarRating {
    if (!Number.isInteger(value) || value < 1 || value > 5) {
      throw new InvalidStarRatingError(value);
    }
    return new StarRating(value);
  }
}

export class InvalidStarRatingError extends Error {
  constructor(value: number) {
    super(`Star rating must be an integer between 1 and 5, got ${value}`);
    this.name = 'InvalidStarRatingError';
  }
}

const SUPPORTED_REVIEW_PHOTO_FORMATS = ['image/jpeg', 'image/png', 'image/webp'] as const;
const MAX_REVIEW_PHOTO_BYTES = 5 * 1024 * 1024;

export interface ReviewPhotoSnapshot {
  storageKey: string;
  originalFilename: string;
  contentType: string;
  sizeBytes: number;
}

/** << ValueObject >> — image attachment metadata on a customer review. */
export class ReviewPhoto {
  readonly storageKey: string;
  readonly originalFilename: string;
  readonly contentType: string;
  readonly sizeBytes: number;

  private constructor(snapshot: ReviewPhotoSnapshot) {
    this.storageKey = snapshot.storageKey;
    this.originalFilename = snapshot.originalFilename;
    this.contentType = snapshot.contentType;
    this.sizeBytes = snapshot.sizeBytes;
  }

  static create(input: {
    storageKey: string;
    originalFilename: string;
    contentType: string;
    sizeBytes: number;
  }): ReviewPhoto {
    if (!SUPPORTED_REVIEW_PHOTO_FORMATS.includes(input.contentType as (typeof SUPPORTED_REVIEW_PHOTO_FORMATS)[number])) {
      throw new UnsupportedReviewPhotoFormatError();
    }
    if (input.sizeBytes > MAX_REVIEW_PHOTO_BYTES) {
      throw new ReviewPhotoTooLargeError();
    }
    return new ReviewPhoto(input);
  }
}

export class UnsupportedReviewPhotoFormatError extends Error {
  constructor() {
    super('Supported formats: JPEG, PNG, WebP');
    this.name = 'UnsupportedReviewPhotoFormatError';
  }
}

export class ReviewPhotoTooLargeError extends Error {
  constructor() {
    super('Image must be under 5 MB');
    this.name = 'ReviewPhotoTooLargeError';
  }
}

export interface CustomerReviewSnapshot {
  reviewId: string;
  authorId: string;
  productSku: string;
  starRating: number;
  body: string | null;
  photos: ReviewPhotoSnapshot[];
  createdAt: string;
}

export interface CreateReviewInput {
  authorId: string;
  productSku: string;
  starRating: number;
  body?: string | null;
}

function newReviewId(): string {
  return globalThis.crypto.randomUUID();
}

/** << Entity >> — verified purchaser opinion attached to a product. */
export class CustomerReview {
  readonly reviewId: string;
  readonly authorId: string;
  readonly productSku: string;
  readonly starRating: StarRating;
  readonly body: string | null;
  readonly photos: ReviewPhoto[];
  readonly createdAt: Date;

  private constructor(params: {
    reviewId: string;
    authorId: string;
    productSku: string;
    starRating: StarRating;
    body: string | null;
    photos: ReviewPhoto[];
    createdAt: Date;
  }) {
    this.reviewId = params.reviewId;
    this.authorId = params.authorId;
    this.productSku = params.productSku;
    this.starRating = params.starRating;
    this.body = params.body;
    this.photos = params.photos;
    this.createdAt = params.createdAt;
  }

  static create(input: CreateReviewInput, reviewId = newReviewId()): CustomerReview {
    return new CustomerReview({
      reviewId,
      authorId: input.authorId,
      productSku: input.productSku,
      starRating: StarRating.of(input.starRating),
      body: input.body?.trim() ? input.body.trim() : null,
      photos: [],
      createdAt: new Date(),
    });
  }

  attachPhoto(photo: ReviewPhoto): CustomerReview {
    return new CustomerReview({
      reviewId: this.reviewId,
      authorId: this.authorId,
      productSku: this.productSku,
      starRating: this.starRating,
      body: this.body,
      photos: [...this.photos, photo],
      createdAt: this.createdAt,
    });
  }

  toSnapshot(): CustomerReviewSnapshot {
    return {
      reviewId: this.reviewId,
      authorId: this.authorId,
      productSku: this.productSku,
      starRating: this.starRating.value,
      body: this.body,
      photos: this.photos.map((photo) => ({
        storageKey: photo.storageKey,
        originalFilename: photo.originalFilename,
        contentType: photo.contentType,
        sizeBytes: photo.sizeBytes,
      })),
      createdAt: this.createdAt.toISOString(),
    };
  }
}

/** << Entity >> — sellable catalog item. */
export class Product {
  readonly name: string;
  readonly sku: string;
  price: number;
  brand: string;
  description: string;
  weight: number | null;
  length: number | null;
  width: number | null;
  height: number | null;
  images: ProductImage[];
  categories: Category[];
  stockAvailability: StockAvailability[];
  customerReviews: CustomerReview[];
  aggregateStarRating: number;
  reviewCount: number;

  constructor(name: string, sku: string, price: number, brand: string) {
    if (!name) throw new Error('name is required');
    if (!sku) throw new Error('sku is required');
    if (price <= 0) throw new Error('price must be positive');
    if (!brand) throw new Error('brand is required');

    this.name = name;
    this.sku = sku;
    this.price = price;
    this.brand = brand;
    this.description = '';
    this.weight = null;
    this.length = null;
    this.width = null;
    this.height = null;
    this.images = [];
    this.categories = [];
    this.stockAvailability = [];
    this.customerReviews = [];
    this.aggregateStarRating = 0;
    this.reviewCount = 0;
  }

  addReview(review: CustomerReview): void {
    this.customerReviews.push(review);
    this.reviewCount = this.customerReviews.length;
    this.aggregateStarRating = this.customerReviews.reduce(
      (sum, r) => sum + r.starRating.value,
      0,
    ) / this.reviewCount;
  }

  snapshotPrice(): number {
    return this.price;
  }
}

/** << Service >> — browse, search, and filter the product collection. */
export class ProductCatalog {
  products: Product[];

  constructor() {
    this.products = [];
  }

  findProduct(sku: string): Product | undefined {
    return this.products.find(p => p.sku === sku);
  }

  browseProducts(): Product[] {
    return [...this.products];
  }

  filterByCategory(categoryName: string): Product[] {
    return this.products.filter(
      p => p.categories.some(c => c.categoryName === categoryName),
    );
  }

  filterByBrand(brand: string): Product[] {
    return this.products.filter(p => p.brand === brand);
  }

  search(keyword: string): Product[] {
    const lower = keyword.toLowerCase();
    return this.products.filter(
      p => p.name.toLowerCase().includes(lower)
        || p.description.toLowerCase().includes(lower)
        || p.brand.toLowerCase().includes(lower),
    );
  }

  computeAggregateRating(product: Product): void {
    if (product.customerReviews.length === 0) {
      product.aggregateStarRating = 0;
      return;
    }
    product.aggregateStarRating = product.customerReviews.reduce(
      (sum, r) => sum + r.starRating.value,
      0,
    ) / product.customerReviews.length;
  }
}
