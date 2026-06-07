export function ChatbotIcon({ colorClass }: { colorClass: string }) {
  return (
    <svg
      className={'kb-skill-icon kb-skill-icon--bot ' + colorClass}
      viewBox="0 0 20 20"
      width="13"
      height="13"
      aria-label="In progress"
    >
      <rect x="2" y="4" width="16" height="11" rx="2.5" fill="currentColor" fillOpacity="0.2" stroke="currentColor" strokeWidth="1.5" />
      <path d="M5 15 L4 18 L8 15" fill="none" stroke="currentColor" strokeWidth="1.2" strokeLinejoin="round" />
      <line x1="10" y1="4" x2="10" y2="2" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
      <circle cx="10" cy="1.5" r="0.9" fill="currentColor" />
      <circle cx="7" cy="9" r="1.2" fill="currentColor" />
      <circle cx="13" cy="9" r="1.2" fill="currentColor" />
      <path d="M7.5 12 Q10 13.5 12.5 12" stroke="currentColor" strokeWidth="1" fill="none" strokeLinecap="round" />
    </svg>
  );
}

export function MagnifyIcon({ colorClass }: { colorClass: string }) {
  return (
    <svg
      className={'kb-skill-icon kb-skill-icon--review ' + colorClass}
      viewBox="0 0 20 20"
      width="13"
      height="13"
      aria-label="In review"
    >
      <circle cx="8" cy="8" r="5" fill="none" stroke="currentColor" strokeWidth="1.6" />
      <line x1="12" y1="12" x2="17" y2="17" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
  );
}

export function DoneIcon({ colorClass }: { colorClass: string }) {
  return (
    <svg
      className={'kb-skill-icon kb-skill-icon--done ' + colorClass}
      viewBox="0 0 14 14"
      width="11"
      height="11"
      aria-label="Done"
    >
      <polyline points="2,7 5.5,11 12,3" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function ReworkIcon({ colorClass }: { colorClass: string }) {
  return (
    <svg
      className={'kb-skill-icon kb-skill-icon--rework ' + colorClass}
      viewBox="0 0 16 16"
      width="14"
      height="14"
      aria-label="Rework needed"
    >
      <path d="M2 8a6 6 0 0 1 10.3-4.2l-1.8 1.8H15V1.1l-1.7 1.7A8 8 0 0 0 0 8h2zm12 0a6 6 0 0 1-10.3 4.2l1.8-1.8H1v4.5l1.7-1.7A8 8 0 0 0 16 8h-2z" fill="currentColor" />
    </svg>
  );
}

export function PendingIntentIcon({ colorClass }: { colorClass: string }) {
  return (
    <svg
      className={'kb-skill-icon kb-skill-icon--pending-intent ' + colorClass}
      viewBox="0 0 16 16"
      width="13"
      height="13"
      aria-label="Intent queued"
    >
      <path d="M8 14V4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
      <path d="M4 7l4-4 4 4" stroke="currentColor" strokeWidth="1.8" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <line x1="3" y1="2" x2="13" y2="2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}
