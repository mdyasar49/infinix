import { useNavigate } from 'react-router-dom'
import ProgressSidebar from '../../components/ProgressSidebar'
import { useAuth } from '../../hooks/useAuth'
import { onboardingWorkflow } from '../../services/authService'
import './HRInterviewPage.css'

function HRInterviewPage() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const steps = onboardingWorkflow.map((step) => ({
    ...step,
    status: step.id === 5 ? 'current' : step.id < 5 ? 'complete' : 'locked',
  }))

  return (
    <div className="hr-shell">
      <ProgressSidebar steps={steps} />

      <main className="hr-main">
        <div className="hr-card">
          <div className="hr-header">
            <h2>HR & Leadership <span className="heading-accent">Interview (Round 2)</span></h2>
            <p>Round 2 assesses cultural fit, long-term aspirations, communication, and commercial expectations.</p>
          </div>

          <section>
            <h3>🤝 HR Evaluation Criteria</h3>
            <div className="criteria-grid">
              <div className="criteria-card">
                <h4>🎯 Company & Culture Fit</h4>
                <p>Alignment with Infogenx values: Innovate, Automate, Scale.</p>
              </div>

              <div className="criteria-card">
                <h4>📈 Career Goals (2-3 Yrs)</h4>
                <p>Growth mindset and long-term commitment to tech stack mastery.</p>
              </div>

              <div className="criteria-card">
                <h4>🗣 Stress Handling & Communication</h4>
                <p>Professional responsiveness, teamwork, and problem resolution.</p>
              </div>

              <div className="criteria-card">
                <h4>💰 Commercial & Offer Terms</h4>
                <p>Stipend progression, pay bands, and working hours agreement.</p>
              </div>
            </div>
          </section>

          <section className="questions-panel">
            <h3>❓ Core Interview Themes</h3>
            <div className="question-pills">
              <span className="q-pill">Career Goals & Aspirations</span>
              <span className="q-pill">Technical Skills Clarity</span>
              <span className="q-pill">Recruitment Knowledge</span>
              <span className="q-pill">Company Fit</span>
              <span className="q-pill">Stress Handling</span>
              <span className="q-pill">Learning Mindset</span>
            </div>
          </section>

          <div className="hr-actions">
            <button
              type="button"
              className="secondary-button"
              onClick={() => navigate('/assessment')}
            >
              ← Back to Technical Assessment
            </button>
            <button
              type="button"
              className="primary-button"
              onClick={() => navigate('/offer-letter')}
            >
              Proceed to Offer & Selection →
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}

export default HRInterviewPage
