import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import './PdfLearningPage.css'

function PdfLearningPage() {
  const { user } = useAuth()
  const navigate = useNavigate()

  return (
    <div className="pdf-learning-shell" style={{ background: '#FFFFFF', minHeight: 'calc(100vh - 100px)', padding: '0 20px 32px 20px' }}>
      <main className="pdf-learning-main" style={{ maxWidth: '1000px', margin: '0 auto' }}>
        <section className="pdf-learning-card" style={{
          background: '#FFFFFF',
          borderRadius: '20px',
          padding: '32px',
          border: '1.5px solid transparent',
          backgroundImage: 'linear-gradient(#ffffff, #ffffff), linear-gradient(135deg, #00123C 0%, #E65525 100%)',
          backgroundClip: 'padding-box, border-box',
          backgroundOrigin: 'padding-box, border-box',
          boxShadow: '0 20px 50px rgba(0, 18, 60, 0.06)'
        }}>
          <div className="pdf-learning-header" style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h1 style={{
                fontSize: '26px',
                fontWeight: '800',
                margin: '0 0 6px',
                background: 'linear-gradient(135deg, #00123C 0%, #E65525 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent'
              }}>
                Infogenx SOP & Job Roles Guide
              </h1>
              <p style={{ margin: 0, color: '#5C6A86', fontSize: '14px' }}>
                Please review the document carefully before continuing to the orientation presentation.
              </p>
            </div>
            <span style={{
              background: '#FFF8F3',
              border: '1px solid rgba(230, 85, 37, 0.2)',
              color: '#E65525',
              padding: '6px 14px',
              borderRadius: '20px',
              fontSize: '13px',
              fontWeight: '700'
            }}>
              Step 1 of 2
            </span>
          </div>

          <div className="pdf-viewer" style={{ width: '100%', height: '650px', borderRadius: '12px', overflow: 'hidden', border: '1px solid #CBD5E1', marginBottom: '24px' }}>
            <iframe
              src="/materials/Infogenx_SOP.pdf#toolbar=0&navpanes=0&view=FitH"
              title="Infogenx SOP PDF"
              style={{ width: '100%', height: '100%', border: 'none' }}
            />
          </div>

          <div className="pdf-learning-actions" style={{ display: 'flex', justifyContent: 'flex-end' }}>
            <button
              type="button"
              onClick={() => navigate('/ppt')}
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
        </section>
      </main>
    </div>
  )
}

export default PdfLearningPage

