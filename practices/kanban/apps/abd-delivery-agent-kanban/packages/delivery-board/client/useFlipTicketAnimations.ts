import { useLayoutEffect, useRef, type RefObject } from 'react';

const FLIP_DURATION_MS = 680;
const FLIP_EASING = 'cubic-bezier(0.16, 1, 0.3, 1)';
const MIN_DELTA_PX = 0.75;

function collectTicketRects(root: HTMLElement): Map<string, DOMRect> {
  const rects = new Map<string, DOMRect>();
  for (const el of root.querySelectorAll<HTMLElement>('[data-ticket]')) {
    const id = el.dataset.ticket;
    if (!id) continue;
    rects.set(id, el.getBoundingClientRect());
  }
  return rects;
}

function cleanupFlip(el: HTMLElement) {
  el.classList.remove('kb-ticket--flip', 'kb-ticket--flip-far');
  el.style.transition = '';
  el.style.transform = '';
  el.style.zIndex = '';
  el.style.willChange = '';
  el.style.boxShadow = '';
}

/**
 * FLIP animation for ticket cards when board layout changes between polls.
 * Moved tickets glide from their old slot; siblings shift up/down to make room.
 */
export function useFlipTicketAnimations(
  boardRef: RefObject<HTMLElement | null>,
  snapshotKey: string | undefined,
) {
  const prevRectsRef = useRef<Map<string, DOMRect>>(new Map());
  const seededRef = useRef(false);

  useLayoutEffect(() => {
    const root = boardRef.current;
    if (!root || !snapshotKey) return;

    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const nextRects = collectTicketRects(root);

    if (!seededRef.current) {
      seededRef.current = true;
      prevRectsRef.current = nextRects;
      return;
    }

    if (reducedMotion) {
      prevRectsRef.current = nextRects;
      return;
    }

    const prevRects = prevRectsRef.current;
    const animating: HTMLElement[] = [];

    for (const el of root.querySelectorAll<HTMLElement>('[data-ticket]')) {
      const id = el.dataset.ticket;
      if (!id) continue;

      const prev = prevRects.get(id);
      const next = nextRects.get(id);
      if (!prev || !next) continue;

      const dx = prev.left - next.left;
      const dy = prev.top - next.top;
      if (Math.abs(dx) < MIN_DELTA_PX && Math.abs(dy) < MIN_DELTA_PX) continue;

      const distance = Math.hypot(dx, dy);
      const farMove = distance > 120;

      cleanupFlip(el);
      el.classList.add('kb-ticket--flip');
      if (farMove) el.classList.add('kb-ticket--flip-far');

      el.style.willChange = 'transform';
      el.style.zIndex = farMove ? '20' : '5';
      el.style.transform = `translate3d(${dx}px, ${dy}px, 0)`;

      animating.push(el);
    }

    if (animating.length === 0) {
      prevRectsRef.current = nextRects;
      return;
    }

    const runToRest = () => {
      for (const el of animating) {
        el.style.transition = `transform ${FLIP_DURATION_MS}ms ${FLIP_EASING}`;
        el.style.transform = 'translate3d(0, 0, 0)';
      }
    };

    requestAnimationFrame(() => {
      requestAnimationFrame(runToRest);
    });

    const timers = animating.map((el) =>
      window.setTimeout(() => cleanupFlip(el), FLIP_DURATION_MS + 80),
    );

    for (const el of animating) {
      el.addEventListener(
        'transitionend',
        (ev) => {
          if (ev.propertyName !== 'transform') return;
          cleanupFlip(el);
        },
        { once: true },
      );
    }

    prevRectsRef.current = nextRects;

    return () => {
      for (const id of timers) window.clearTimeout(id);
      for (const el of animating) cleanupFlip(el);
    };
  }, [boardRef, snapshotKey]);
}
