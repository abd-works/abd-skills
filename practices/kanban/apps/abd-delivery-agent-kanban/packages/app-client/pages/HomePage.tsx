import { Link } from 'react-router-dom';

export function HomePage() {
  return (
    <div className="app-shell home-page">
      <header className="kb-header">
        <div>
          <div className="kicker">abd.works</div>
          <h1>
            Delivery Agent <span className="accent">Kanban</span>
          </h1>
          <p className="lede">
            Read-only view of the kanban board. Polls <code>board.json</code> and <code>kanban.json</code>.
            The <strong>only</strong> write from this UI is team configuration when you +/&minus; agents.
          </p>
        </div>
      </header>
      <nav className="home-links">
        <Link to="/board" className="home-cta">Open live board</Link>
        <p className="hint">
          Default planning folder: <code>C:/dev/abd-pet-store-demo/docs/planning</code>
        </p>
      </nav>
    </div>
  );
}
