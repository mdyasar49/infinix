import { useNavigate } from 'react-router-dom'
import useSignatureCanvas from '../../hooks/useSignatureCanvas'
import './SignaturePage.css'

function SignaturePage() {
  const { canvasRef, clearCanvas, isSigned } = useSignatureCanvas()
  const navigate = useNavigate()

  return (
    <section className="signature-shell">
      <div className="signature-panel">
        <div className="signature-header">
          <div>
            <h1>Digital <span className="heading-accent">Signature</span></h1>
            <p>Sign and accept your Infogenx offer to continue to the training phase.</p>
          </div>
          <span>Offer confirmation</span>
        </div>

        <div className="signature-card">
          <div className="signature-area">
            <canvas ref={canvasRef} className="signature-canvas" width="940" height="320" />
          </div>

          <div className="signature-note">
            <p>Use your mouse or touch input to sign above. Your acceptance will be captured instantly.</p>
            <button type="button" className="secondary-button" onClick={clearCanvas}>
              Clear Signature
            </button>
          </div>

          <div className="signature-actions">
            <button type="button" className="secondary-button" onClick={() => navigate('/offer-letter')}>
              Back to Offer
            </button>
            <button type="button" className="accept-button" onClick={() => navigate('/training')} disabled={!isSigned}>
              Accept Offer
            </button>
          </div>

          <div className="signature-footer">
            <p>Tip: Draw a smooth signature and use the Clear button if you want to retry.</p>
          </div>
        </div>
      </div>
    </section>
  )
}

export default SignaturePage
