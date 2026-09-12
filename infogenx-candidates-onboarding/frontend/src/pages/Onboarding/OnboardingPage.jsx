import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import ProgressSidebar from '../../components/ProgressSidebar'
import { useAuth } from '../../hooks/useAuth'
import { onboardingWorkflow } from '../../services/authService'
import './OnboardingPage.css'

function OnboardingPage() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [checklist, setChecklist] = useState({
    docs: true,
    nda: true,
    it: false,
    orientation: false,
  })

  const steps = onboardingWorkflow.map((step) => ({
    ...step,
    status: step.id === 7 ? 'complete' : 'complete',
  }))

  const toggleCheck = (key) => {
    setChecklist((prev) => ({ ...prev, [key]: !prev[key] }))
  }

  return (
    <div className="onboard-shell">
      <ProgressSidebar steps={steps} />

      <main className="onboard-main">
        <div className="onboard-card">
          <div className="onboard-header">
            <h2>Onboarding <span className="heading-accent">& Compliance Protocol</span></h2>
            <p>Verification checklist, NDA data security agreement, IT provisioning, and mentor assignment.</p>
          </div>

          <section>
            <h3>📋 Candidate Onboarding Checklist</h3>
            <div className="check-steps">
              <div
                className={`check-step-item ${checklist.docs ? 'done' : ''}`}
                onClick={() => toggleCheck('docs')}
                style={{ cursor: 'pointer' }}
              >
                <div className="check-badge">{checklist.docs ? '✓' : '1'}</div>
                <strong>1. Verify Docs</strong>
                <p style={{ fontSize: '13px', color: '#5F6B7A' }}>ID & Academic Degree Verification</p>
              </div>

              <div
                className={`check-step-item ${checklist.nda ? 'done' : ''}`}
                onClick={() => toggleCheck('nda')}
                style={{ cursor: 'pointer' }}
              >
                <div className="check-badge">{checklist.nda ? '✓' : '2'}</div>
                <strong>2. Sign NDA</strong>
                <p style={{ fontSize: '13px', color: '#5F6B7A' }}>Offer Acceptance & NDA Agreement</p>
              </div>

              <div
                className={`check-step-item ${checklist.it ? 'done' : ''}`}
                onClick={() => toggleCheck('it')}
                style={{ cursor: 'pointer' }}
              >
                <div className="check-badge">{checklist.it ? '✓' : '3'}</div>
                <strong>3. IT Setup</strong>
                <p style={{ fontSize: '13px', color: '#5F6B7A' }}>Email & Portal Credential Access</p>
              </div>

              <div
                className={`check-step-item ${checklist.orientation ? 'done' : ''}`}
                onClick={() => toggleCheck('orientation')}
                style={{ cursor: 'pointer' }}
              >
                <div className="check-badge">{checklist.orientation ? '✓' : '4'}</div>
                <strong>4. Orientation</strong>
                <p style={{ fontSize: '13px', color: '#5F6B7A' }}>Mentor Alignment & Project Handshake</p>
              </div>
            </div>
          </section>

          <section className="ready-banner">
            <h3>🚀 READY TO WORK!</h3>
            <p style={{ fontSize: '15px', opacity: 0.9 }}>
              Congratulations! Your candidate onboarding checklist is verified. You are clear for active project allocation at Infogenx.
            </p>
          </section>

          <section>
            <h3>📍 Infogenx Recruitment Desk Directory</h3>
            <div className="directory-grid">
              <div className="directory-box">
                <strong>Primary HR Contact</strong>
                <p>hr@infogenx.com</p>
              </div>
              <div className="directory-box">
                <strong>Drive & Off-Campus Desk</strong>
                <p>infogenx.jobs@gmail.com</p>
              </div>
              <div className="directory-box">
                <strong>Official Portal & Location</strong>
                <p>www.infogenx.com | HQ: Chennai, Tamil Nadu, India</p>
              </div>
            </div>
          </section>

          <div className="onboard-actions" style={{ display: 'flex', justifyContent: 'space-between' }}>
            <button
              type="button"
              className="secondary-button"
              onClick={() => navigate('/offer-letter')}
            >
              ← Back to Offer & Selection
            </button>
            <button
              type="button"
              className="primary-button"
              onClick={() => navigate('/sop')}
            >
              Return to Welcome Overview ↺
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}

export default OnboardingPage
