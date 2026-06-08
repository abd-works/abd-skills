import { useEffect, useRef, useState, type ReactElement } from 'react';

type LiveFx = 'spawn' | 'despawn' | null;

/** Ticket-row robot / magnify with grow, wiggle-while-live, shrink-on-done. */
export function LiveSkillIconView({
  visible,
  mode,
  BotIcon,
  MagnifyIcon,
  colorClass,
}: {
  visible: boolean;
  mode: 'bot' | 'magnify';
  BotIcon: (props: { colorClass: string }) => ReactElement;
  MagnifyIcon: (props: { colorClass: string }) => ReactElement;
  colorClass: string;
}) {
  const [mounted, setMounted] = useState(visible);
  const [fx, setFx] = useState<LiveFx>(null);
  const seededRef = useRef(false);

  useEffect(() => {
    if (!seededRef.current) {
      seededRef.current = true;
      if (visible) {
        setMounted(true);
        setFx('spawn');
      }
      return;
    }

    if (visible && !mounted) {
      setMounted(true);
      setFx('spawn');
      return;
    }

    if (!visible && mounted) {
      setFx('despawn');
      const id = window.setTimeout(() => {
        setMounted(false);
        setFx(null);
      }, 480);
      return () => window.clearTimeout(id);
    }
  }, [visible, mounted]);

  useEffect(() => {
    if (fx !== 'spawn') return;
    const id = window.setTimeout(() => setFx(null), 560);
    return () => window.clearTimeout(id);
  }, [fx]);

  if (!mounted) return null;

  const wrapClass =
    'kb-live-skill-icon' +
    (fx === 'spawn' ? ' kb-live-skill-icon--spawn' : '') +
    (fx === 'despawn' ? ' kb-live-skill-icon--despawn' : '') +
    (mode === 'bot' && !fx ? ' kb-live-skill-icon--working' : '');

  return (
    <span className={'kb-ticket-agent-icon ' + wrapClass}>
      {mode === 'magnify' ? (
        <MagnifyIcon colorClass={colorClass} />
      ) : (
        <BotIcon colorClass={colorClass} />
      )}
    </span>
  );
}
