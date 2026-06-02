import { useEffect, useState } from 'react';
import { Link, Route, Routes } from 'react-router-dom';
import {
  DeliveryKanbanBoard,
  fetchDefaultPlanningRoot,
  useDeliveryBoardPoll,
  updatePlanningRoot,
} from '@deliveryforge/delivery-board-client';
import { HomePage } from './pages/HomePage';
import {
  DEFAULT_PLANNING_ROOT,
  resolvePlanningRoot,
  savePlanningRootOverride,
} from './planningRoot';

function BoardPage() {
  const [planningRoot, setPlanningRoot] = useState(resolvePlanningRoot);
  const [inputRoot, setInputRoot] = useState(planningRoot);
  const [message, setMessage] = useState<string | null>(null);
  const [theme, setTheme] = useState<'engineering' | 'executive'>(() =>
    (localStorage.getItem('theme') as 'engineering' | 'executive') ?? 'engineering',
  );
  const { snapshot, error, loading, refresh, injectSnapshot } = useDeliveryBoardPoll(planningRoot);

  useEffect(() => {
    if (import.meta.env.VITE_PLANNING_ROOT) return;

    void fetchDefaultPlanningRoot()
      .then((serverRoot) => {
        if (!serverRoot || serverRoot === planningRoot) return;
        setPlanningRoot(serverRoot);
        setInputRoot(serverRoot);
      })
      .catch(() => {
        /* keep resolvePlanningRoot() fallback */
      });
  }, []);

  function toggleTheme(mode: 'engineering' | 'executive') {
    document.documentElement.setAttribute('data-theme', mode);
    localStorage.setItem('theme', mode);
    setTheme(mode);
  }

  async function applyPlanningRoot() {
    try {
      await updatePlanningRoot(inputRoot);
      savePlanningRootOverride(inputRoot);
      setPlanningRoot(inputRoot);
      setMessage('Planning folder connected.');
      await refresh();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Failed to connect');
    }
  }

  async function useDefaultFixture() {
    setInputRoot(DEFAULT_PLANNING_ROOT);
    try {
      await updatePlanningRoot(DEFAULT_PLANNING_ROOT);
      localStorage.removeItem('planningRootOverride');
      localStorage.removeItem('planningRoot');
      setPlanningRoot(DEFAULT_PLANNING_ROOT);
      setMessage('Connected to default fixture (pawplace-stubs).');
      await refresh();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Failed to connect');
    }
  }

  async function handleRefresh() {
    await refresh();
    setMessage('Re-read board.json from disk.');
  }

  return (
    <div className="app-shell">
      <header className="kb-header">
        <div>
          <div className="kicker">Agentic Agile Delivery</div>
          <h1>
            Kanban Board &mdash; <span className="accent">{snapshot?.boardTitle ?? '\u2026'}</span>
          </h1>
        </div>
        <div className="kb-header-right">
          <div className="abd-slide-mode-toggle" role="group" aria-label="Display mode">
            <button type="button" className={'abd-slide-mode-btn ' + (theme === 'executive' ? 'is-active' : '')} onClick={() => toggleTheme('executive')}>Executive</button>
            <button type="button" className={'abd-slide-mode-btn ' + (theme === 'engineering' ? 'is-active' : '')} onClick={() => toggleTheme('engineering')}>Engineering</button>
          </div>
          {snapshot?.syncedAt ? (
            <div className="kb-step muted">board.json {snapshot.syncedAt.slice(0, 19).replace('T', ' ')}Z</div>
          ) : null}
          <div className="kb-skill-links">
            <Link to="/" className="kb-skill-pill">home</Link>
          </div>
        </div>
      </header>

      <section className="config-bar">
        <label>
          Planning folder
          <input value={inputRoot} onChange={(e) => setInputRoot(e.target.value)} placeholder="C:/dev/.../docs/planning" />
        </label>
        <button type="button" onClick={() => void applyPlanningRoot()}>Connect</button>
        <button type="button" className="secondary" onClick={() => void useDefaultFixture()}>Use stubs</button>
        <button type="button" className="secondary" onClick={() => void handleRefresh()}>Refresh</button>
        <span className="poll-indicator">{loading ? 'Loading\u2026' : 'Polled ' + (snapshot?.polledAt?.slice(11, 19) ?? '')}</span>
      </section>

      {message ? <div className="status-banner">{message}</div> : null}
      {error ? <div className="status-banner error">{error}</div> : null}

      {snapshot ? (
        <DeliveryKanbanBoard
          snapshot={snapshot}
          onTeamUpdate={injectSnapshot}
          onModeToggle={injectSnapshot}
        />
      ) : null}
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/board" element={<BoardPage />} />
    </Routes>
  );
}
