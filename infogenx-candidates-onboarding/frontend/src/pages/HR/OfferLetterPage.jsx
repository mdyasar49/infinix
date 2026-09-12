import { useNavigate } from 'react-router-dom'
import ProgressSidebar from '../../components/ProgressSidebar'
import { useAuth } from '../../hooks/useAuth'
import { onboardingWorkflow } from '../../services/authService'
import './OfferLetterPage.css'

function OfferLetterPage() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const steps = onboardingWorkflow.map((step) => ({
    ...step,
    status: step.id === 6 ? 'current' : step.id < 6 ? 'complete' : 'locked',
  }))

  return (
    <div className="offer-shell">
      <ProgressSidebar steps={steps} />

      <main className="offer-main">
        <div className="offer-card">
          <div className="offer-header">
            <h2>Selection, Offer <span className="heading-accent">& Compensation Framework</span></h2>
            <p>Commercial terms, stipend progression, hourly formulas, and post-internship conversion pay bands.</p>
          </div>

          <section className="formula-panel">
            <h3>🧮 Freelancer Hourly Rate Standard Formula</h3>
            <p style={{ fontSize: '14px', color: '#5F6B7A' }}>
              Base Divisor: 240 Standard Monthly Hours (30 Days × 8 Hours)
            </p>
            <div className="formula-box">
              Hourly Rate (INR) = Monthly Take-Home Salary ÷ 30 ÷ 8
            </div>
            <p style={{ fontSize: '13px', color: '#5F6B7A' }}>
              Example: Take-Home ₹25,000 ➔ ₹25,000 ÷ 30 ÷ 8 = ₹105/hr. 100-Hour contract = ₹10,500.
            </p>
          </section>

          <section>
            <h3>📈 Internship Stipend Progression Roadmap</h3>
            <div className="roadmap-grid">
              <div className="roadmap-card">
                <h4>MONTH 1 – 3</h4>
                <strong style={{ fontSize: '18px', color: '#081B5C' }}>Practical Training</strong>
                <p style={{ fontSize: '13px', color: '#5F6B7A', marginTop: '6px' }}>Orientation, mentorship & domain foundations.</p>
              </div>

              <div className="roadmap-card active">
                <h4>MONTH 4 – 5</h4>
                <strong style={{ fontSize: '18px', color: '#F25C1D' }}>₹3,000 – ₹5,000 / Mo</strong>
                <p style={{ fontSize: '13px', color: '#5F6B7A', marginTop: '6px' }}>Active project contribution & stipend.</p>
              </div>

              <div className="roadmap-card active">
                <h4>MONTH 6+</h4>
                <strong style={{ fontSize: '18px', color: '#F25C1D' }}>₹8,000 – ₹15,000+ / Mo</strong>
                <p style={{ fontSize: '13px', color: '#5F6B7A', marginTop: '6px' }}>Pre-conversion band & performance bonus.</p>
              </div>
            </div>
          </section>

          <section>
            <h3>🎓 Post-Internship Permanent Conversion Pay Bands</h3>
            <div className="pay-bands">
              <div className="pay-band-item">
                <span>Diploma Graduates</span>
                <strong style={{ color: '#F25C1D' }}>₹8,000 / Month</strong>
              </div>
              <div className="pay-band-item">
                <span>B.Sc. Graduates</span>
                <strong style={{ color: '#F25C1D' }}>₹10,000 / Month</strong>
              </div>
              <div className="pay-band-item">
                <span>B.E. / M.C.A. / M.Sc. Graduates</span>
                <strong style={{ color: '#F25C1D' }}>₹12,000 – ₹15,000+ / Month</strong>
              </div>
            </div>
          </section>

          <div className="offer-actions">
            <button
              type="button"
              className="secondary-button"
              onClick={() => navigate('/hr-interview')}
            >
              ← Back to HR Interview
            </button>
            <button
              type="button"
              className="primary-button"
              onClick={() => navigate('/onboarding')}
            >
              Proceed to Final Onboarding →
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}

export default OfferLetterPage
