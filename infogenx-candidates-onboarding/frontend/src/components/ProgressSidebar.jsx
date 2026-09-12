import { Link } from 'react-router-dom'

function ProgressSidebar({ steps }) {
  return (
    <aside className="portal-sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-logo">I</div>
        <div>
          <p className="sidebar-company">Infogenx</p>
          <p className="sidebar-tagline">Student Portal</p>
        </div>
      </div>

      <nav className="sidebar-steps">
        {steps.map((step) => (
          <Link
            key={step.id}
            to={step.route}
            className={`sidebar-step ${step.status}`}
          >
            <div className="step-index">
              {step.status === 'complete' ? '✓' : step.id}
            </div>
            <div className="step-copy">
              <p className="step-title">{step.title}</p>
              <p className="step-text">{step.description}</p>
            </div>
            <div className="step-badge">
              {step.status === 'locked' ? '🔒' : step.status === 'complete' ? 'Done' : 'Active'}
            </div>
          </Link>
        ))}
      </nav>
    </aside>
  )
}

export default ProgressSidebar
