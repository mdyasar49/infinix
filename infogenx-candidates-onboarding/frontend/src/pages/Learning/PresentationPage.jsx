import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import './PresentationPage.css'

function PresentationPage() {
  const { user } = useAuth()
  const navigate = useNavigate()

  return (
    <div className="presentation-shell" style={{ background: '#FFFFFF', minHeight: 'calc(100vh - 100px)', padding: '0 20px 32px 20px' }}>
      <main className="presentation-main" style={{ maxWidth: '1000px', margin: '0 auto' }}>
        <div className="presentation-card" style={{
          background: '#FFFFFF',
          borderRadius: '20px',
          padding: '32px',
          border: '1.5px solid transparent',
          backgroundImage: 'linear-gradient(#ffffff, #ffffff), linear-gradient(135deg, #00123C 0%, #E65525 100%)',
          backgroundClip: 'padding-box, border-box',
          backgroundOrigin: 'padding-box, border-box',
          boxShadow: '0 20px 50px rgba(0, 18, 60, 0.06)'
        }}>
          <div className="presentation-header" style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h2 style={{
                fontSize: '26px',
                fontWeight: '800',
                margin: '0 0 6px',
                background: 'linear-gradient(135deg, #00123C 0%, #E65525 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent'
              }}>
                Infogenx Orientation Presentation
              </h2>
              <p style={{ margin: 0, color: '#5C6A86', fontSize: '14px' }}>
                Review the presentation learning material before continuing to the assessment.
              </p>
            </div>
            <div style={{
              background: '#FFF8F3',
              border: '1px solid rgba(230, 85, 37, 0.2)',
              color: '#E65525',
              padding: '6px 14px',
              borderRadius: '20px',
              fontSize: '13px',
              fontWeight: '700'
            }}>
              Step 2 of 2
            </div>
          </div>

          <div className="presentation-slide-container" style={{ width: '100%', height: '650px', borderRadius: '12px', overflow: 'hidden', border: '1px solid #CBD5E1', marginBottom: '24px' }}>
            <iframe
              src="/materials/Infogenx_Presentation.pdf#toolbar=0&navpanes=0&view=FitH"
              title="Infogenx Presentation PDF"
              className="presentation-slide-frame"
              style={{ width: '100%', height: '100%', border: 'none' }}
            />
          </div>

          <div className="presentation-actions" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <button
              type="button"
              onClick={() => navigate('/pdf')}
              style={{
                background: '#FFFFFF',
                color: '#00123C',
                border: '1px solid #CBD5E1',
                borderRadius: '10px',
                padding: '14px 32px',
                fontSize: '15px',
                fontWeight: '700',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              ← Previous
            </button>

            <button
              type="button"
              onClick={() => navigate('/assessment')}
              style={{
                background: 'linear-gradient(90deg, #00123C 0%, #E65525 100%)',
                color: '#FFFFFF',
                border: 'none',
                borderRadius: '10px',
                padding: '14px 36px',
                fontSize: '15px',
                fontWeight: '700',
                cursor: 'pointer',
                boxShadow: '0 8px 20px rgba(0, 18, 60, 0.15)',
                transition: 'all 0.2s ease'
              }}
            >
              Next →
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}

export default PresentationPage

