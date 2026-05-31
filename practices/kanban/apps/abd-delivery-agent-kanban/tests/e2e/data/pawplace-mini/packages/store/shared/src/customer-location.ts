import type { CustomerLocation as CustomerLocationDto } from '../types';

/** << ValueObject >> — geolocation input for distance ranking. */
export class CustomerLocation {
  constructor(
    readonly latitude: number | null,
    readonly longitude: number | null,
  ) {}

  static empty(): CustomerLocation {
    return new CustomerLocation(null, null);
  }

  static fromDto(dto: CustomerLocationDto): CustomerLocation {
    return new CustomerLocation(dto.latitude, dto.longitude);
  }

  toDto(): CustomerLocationDto | null {
    if (this.latitude === null || this.longitude === null) {
      return null;
    }
    return { latitude: this.latitude, longitude: this.longitude };
  }

  isEmpty(): boolean {
    return this.latitude === null || this.longitude === null;
  }
}
