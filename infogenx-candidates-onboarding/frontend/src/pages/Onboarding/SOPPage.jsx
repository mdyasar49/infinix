import { useNavigate } from 'react-router-dom'
import ProgressSidebar from '../../components/ProgressSidebar'
import { useAuth } from '../../hooks/useAuth'
import { onboardingWorkflow } from '../../services/authService'
import './SOPPage.css'

function SOPPage() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const steps = onboardingWorkflow.map((step) => ({
    ...step,
    status: step.id === 1 ? 'current' : 'locked',
  }))

  return (
    <div className="sop-shell">
      <ProgressSidebar steps={steps} />

      <main className="sop-main">
        <section className="sop-welcome-banner">
          <p className="sop-tagline">Infogenx Pvt. Ltd. · Digital Transformation</p>
          <h2>Welcome to Infogenx <span className="heading-accent">Student Onboarding</span></h2>
          <p>
            10+ Years of Industry Experience delivering Smart Application Development, Intelligent Process Automation (IPA), Data Analytics, and AI & Cloud Solutions across India & Australia.
          </p>
          <div className="sop-tagline-pills">
            <span className="sop-pill">⚡ INNOVATE</span>
            <span className="sop-pill">🤖 AUTOMATE</span>
            <span className="sop-pill">🚀 SCALE</span>
          </div>
        </section>

        <section className="sop-grid">
          <article className="sop-info-card">
            <h3>🏢 Company Overview</h3>
            <ul className="sop-service-list">
              <li className="sop-service-item"><span className="sop-service-bullet">✓</span> 10+ Years of Global Industry Excellence</li>
              <li className="sop-service-item"><span className="sop-service-bullet">✓</span> Dual Operational Centers in India & Australia</li>
              <li className="sop-service-item"><span className="sop-service-bullet">✓</span> Enterprise Process Automation & Cloud Solutions</li>
            </ul>
          </article>

          <article className="sop-info-card">
            <h3>🛠 Core Capabilities</h3>
            <ul className="sop-service-list">
              <li className="sop-service-item"><span className="sop-service-bullet">✓</span> Smart Application Development (MERN, Python, Flutter)</li>
              <li className="sop-service-item"><span className="sop-service-bullet">✓</span> Intelligent Process Automation (IPA, n8n, UiPath)</li>
              <li className="sop-service-item"><span className="sop-service-bullet">✓</span> Cloud & BI Analytics (AWS, GCP, Power BI)</li>
            </ul>
          </article>

          <article className="sop-info-card">
            <h3>📋 Candidate SOP Objectives</h3>
            <ul className="sop-service-list">
              <li className="sop-service-item"><span className="sop-service-bullet">✓</span> Clear evaluation criteria for technical & non-IT tracks</li>
              <li className="sop-service-item"><span className="sop-service-bullet">✓</span> Transparent stipend & career progression roadmaps</li>
              <li className="sop-service-item"><span className="sop-service-bullet">✓</span> Structured onboarding, NDA & mentor alignment</li>
            </ul>
          </article>
        </section>

        <div className="sop-actions">
          <button
            type="button"
            className="primary-button sop-next-btn"
            onClick={() => navigate('/recruitment-process')}
          >
            Proceed to Recruitment Process →
          </button>
        </div>
      </main>
    </div>
  )
}

export default SOPPage
