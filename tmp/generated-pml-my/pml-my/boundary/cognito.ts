// =============================================================================
// Boundary class: Cognito
// Owned by: pml-my
// =============================================================================

// TODO: adjust imports — the CLI cannot resolve module paths automatically
// Referenced but not defined in this file:
//   AccountToken, AuthHeaders, Email, OTPCode, Password, SessionTokens

export abstract class Cognito {
  abstract signUp(arg1: Email, arg2: Password): AccountToken
  abstract confirmSignUp(arg1: Email, arg2: OTPCode): void
  abstract signIn(arg1: Email, arg2: Password): SessionTokens
  abstract signOut(): void
  abstract resetPassword(arg1: Email): void
  abstract confirmResetPassword(arg1: Email, arg2: OTPCode, arg3: Password): void
  abstract getUser(): SessionTokens
  abstract getAuthorizationHeader(): AuthHeaders
  //region Invariants — names derived from legacy prose; rename to tight names (D24)
  // TODO: rename — original: force-refreshes session; returns idtoken + Bearer authorization
  /** @invariant */
  abstract forceRefreshesSessionReturnsIdtokenBearerAuthorization(): void

  //endregion

}
