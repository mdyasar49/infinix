import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { termsAgreement } from '../../services/mockData'
import './TermsConditionsPage.css'

function TermsConditionsPage() {
  const [accepted, setAccepted] = useState(false)
  const navigate = useNavigate()

  const handleContinue = () => {
    if (accepted) {
      navigate('/assessment')
    }
  }

  return (
    <section className="terms-shell">
      <div className="terms-panel">
        <div className="terms-header">
          <div>
            <h1>Infogenx Student Onboarding <span className="heading-accent">Terms &amp; Conditions</span></h1>
            <p>Please review the onboarding agreement and accept the terms to continue.</p>
          </div>
        </div>

        <div className="terms-card">
          <div className="terms-copy">
            {termsAgreement.sections.map((section) => (
              <div key={section.heading}>
                <h2>{section.heading.split(' ').slice(0, -1).join(' ')} <span className="heading-accent">{section.heading.split(' ').slice(-1)}</span></h2>
                <p>{section.body}</p>
              </div>
            ))}
          </div>

          <div className="terms-footer">
            <label className="checkbox-field">
              <input
                type="checkbox"
                checked={accepted}
                onChange={(event) => setAccepted(event.target.checked)}
              />
              <span>I have read and accept the terms and conditions.</span>
            </label>

            <div className="terms-actions">
              <button type="button" className="secondary-button" onClick={() => navigate('/materials')}>
                Back to Materials
              </button>
              <button type="button" className="primary-button" onClick={handleContinue} disabled={!accepted}>
                Continue to Assessment
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default TermsConditionsPage
