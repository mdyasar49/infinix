import { Link } from 'react-router-dom'
import { completionData } from '../../services/mockData'
import './CompletionPage.css'

function CompletionPage() {
  return (
    <section className="completion-shell">
      <div className="completion-card">
        <div className="completion-badge">Completed</div>
        <h1>Onboarding <span className="heading-accent">Completed</span></h1>
        <p>{completionData.message}</p>

        <div className="completion-summary">
          {completionData.summary.map((item) => (
            <div key={item} className="completion-item">
              <span>✓</span>
              <p>{item}</p>
            </div>
          ))}
        </div>

        <div className="completion-actions">
          <Link to="/dashboard" className="primary-button">
            Return to Dashboard
          </Link>
          <Link to="/materials" className="secondary-button">
            Review Your Learning Path
          </Link>
        </div>
      </div>
    </section>
  )
}

export default CompletionPage
