/** << ValueObject >> — coordinates and address for map placement and distance. */
export class GeographicPlacement {
  constructor(
    readonly streetAddress: string,
    readonly latitude: number,
    readonly longitude: number,
  ) {}
}
