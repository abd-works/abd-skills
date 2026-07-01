// =============================================================================
// Boundary class: GrowthBook
// Owned by: pml-my
// =============================================================================

// TODO: adjust imports — the CLI cannot resolve module paths automatically
// Referenced but not defined in this file:
//   FlagKey, FlagValue

export abstract class GrowthBook {
  abstract isOn(arg1: FlagKey): boolean
  abstract getValue(arg1: FlagKey): FlagValue
}
