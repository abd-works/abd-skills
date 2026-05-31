/** Visual tokens — Increment 1 (interface-design.md § Visual direction) */
export const tokens = {
  display: { fontFamily: 'sans-serif', fontSize: 24, lineHeight: 32, fontWeight: 600, color: '#1A1A2E' },
  body: { fontFamily: 'sans-serif', fontSize: 16, lineHeight: 24, fontWeight: 400, color: '#2D2D2D' },
  label: { fontFamily: 'sans-serif', fontSize: 14, lineHeight: 20, fontWeight: 500, color: '#5C5C5C' },
  accent: '#B85C38',
  surface: '#FFFFFF',
  surfaceMuted: '#F5F5F0',
  staffSurface: '#EEF2F7',
  success: '#2D6A4F',
  danger: '#C0392B',
  focusRing: '2px solid #B85C38',
  focusOffset: 2,
  spacing: { xs: 4, sm: 8, md: 16, lg: 24, xl: 32 },
} as const;

/** Component-facing alias — spacing indexed 0–4 maps to 4 · 8 · 16 · 24 · 32 px scale */
export const layoutTokens = {
  display: tokens.display,
  body: tokens.body,
  label: tokens.label,
  accent: tokens.accent,
  surface: tokens.surface,
  surfaceMuted: tokens.surfaceMuted,
  staffSurface: tokens.staffSurface,
  success: tokens.success,
  danger: tokens.danger,
  focusRing: tokens.focusRing,
  focusOffset: tokens.focusOffset,
  spacing: [4, 8, 16, 24, 32] as const,
};
