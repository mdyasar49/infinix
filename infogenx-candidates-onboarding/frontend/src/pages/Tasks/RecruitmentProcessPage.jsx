import { useNavigate } from 'react-router-dom'
import ProgressSidebar from '../../components/ProgressSidebar'
import { useAuth } from '../../hooks/useAuth'
import { onboardingWorkflow } from '../../services/authService'
import './RecruitmentProcessPage.css'

function RecruitmentProcessPage() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const steps = onboardingWorkflow.map((step) => ({
    ...step,
    status: step.id === 2 ? 'current' : step.id < 2 ? 'complete' : 'locked',
  }))

  return (
    <div className="process-shell">
      <ProgressSidebar steps={steps} />

      <main className="process-main">
        <div className="process-card">
          <div className="process-header">
            <h2>Recruitment Process <span className="heading-accent">& Sourcing Overview</span></h2>
            <p>Multi-channel sourcing strategy, Boolean search filters, and candidate qualification workflow.</p>
          </div>

          <section>
            <h3>📍 Job Posting & Candidate Sourcing Matrix</h3>
            <div className="matrix-grid">
              <div className="matrix-card">
                <h4>💻 IT / Technical Roles</h4>
                <p>Full Stack Developers, Cloud Engineers, System Architects</p>
                <div className="channel-tags">
                  <span className="channel-tag">LinkedIn</span>
                  <span className="channel-tag">Naukri</span>
                  <span className="channel-tag">Indeed</span>
                  <span className="channel-tag">Upwork</span>
                  <span className="channel-tag">Internshala</span>
                </div>
              </div>

              <div className="matrix-card">
                <h4>💼 Non-IT / Business Roles</h4>
                <p>HR Executives, BDEs, Office Admins, Content Managers</p>
                <div className="channel-tags">
                  <span className="channel-tag">LinkedIn</span>
                  <span className="channel-tag">Indeed</span>
                  <span className="channel-tag">PlacementIndia</span>
                  <span className="channel-tag">Facebook Groups</span>
                </div>
              </div>

              <div className="matrix-card">
                <h4>🌏 Offshore / Remote Roles</h4>
                <p>Australian Time Zone Specialists, Product Support</p>
                <div className="channel-tags">
                  <span className="channel-tag">LinkedIn Recruiter</span>
                  <span className="channel-tag">Offshore Platforms</span>
                  <span className="channel-tag">Direct Outreach</span>
                </div>
              </div>
            </div>
          </section>

          <section className="boolean-panel">
            <h3>🔎 Recruiter Boolean Search Algorithms</h3>
            <p style={{ color: '#BDC8E2', marginBottom: '12px' }}>How Infogenx recruiters match your resume:</p>
            <div className="boolean-code">1. Skill Combination: React AND Node.js</div>
            <div className="boolean-code">2. Filter Exclusions: Developer NOT Manager</div>
            <div className="boolean-code">3. Exact Role Match: "Full Stack Developer" AND "Python"</div>
          </section>

          <section>
            <h3>📞 Candidate Screening to Interview Stage</h3>
            <div className="flow-steps">
              <div className="flow-step-card">
                <div className="step-num">1</div>
                <strong>Resume Review</strong>
                <p style={{ fontSize: '13px', color: '#5F6B7A', marginTop: '4px' }}>Skills & project verification</p>
              </div>

              <div className="flow-step-card">
                <div className="step-num">2</div>
                <strong>10-Min Phone Call</strong>
                <p style={{ fontSize: '13px', color: '#5F6B7A', marginTop: '4px' }}>Communication & availability check</p>
              </div>

              <div className="flow-step-card">
                <div className="step-num">3</div>
                <strong>Shortlisted</strong>
                <p style={{ fontSize: '13px', color: '#5F6B7A', marginTop: '4px' }}>Scheduled for Technical Round 1</p>
              </div>
            </div>
          </section>

          <div className="process-actions">
            <button
              type="button"
              className="secondary-button"
              onClick={() => navigate('/sop')}
            >
              ← Back to Overview
            </button>
            <button
              type="button"
              className="primary-button"
              onClick={() => navigate('/job-roles')}
            >
              Proceed to Job Roles →
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}

export default RecruitmentProcessPage
