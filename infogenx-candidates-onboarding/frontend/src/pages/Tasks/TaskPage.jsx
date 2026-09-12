import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import logo from '../../assets/logo.png'
import './TaskPage.css'

function TaskPage() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploaded, setUploaded] = useState(false)

  const steps = [
    { number: 1, title: 'Create Google Form', desc: 'Create a candidate/recruitment Google Form following the SOP structure.' },
    { number: 2, title: 'Add Required Fields', desc: 'Add required candidate application fields (Name, Contact, Qualification, Skills, Resume link).' },
    { number: 3, title: 'Design Recruitment Poster', desc: 'Create a professional recruitment poster using Infogenx brand guidelines.' },
    { number: 4, title: 'Add Form Link to Poster', desc: 'Embed or attach the Google Form link to your recruitment poster/post.' },
    { number: 5, title: 'Publish on Social Media', desc: 'Publish the recruitment post on LinkedIn or designated social channels.' },
    { number: 6, title: 'Take Screenshot', desc: 'Capture a clear screenshot of the published recruitment post.' },
    { number: 7, title: 'Upload Screenshot', desc: 'Upload the screenshot image below to complete your recruitment task.' },
  ]

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0])
    }
  }

  const handleUploadSubmit = (e) => {
    e.preventDefault()
    if (!selectedFile) {
      alert('Please select a screenshot file first.')
      return
    }
    setUploading(true)
    setTimeout(() => {
      setUploading(false)
      setUploaded(true)
    }, 1200)
  }

  return (
    <div className="task-shell" style={{ background: '#FFFFFF', minHeight: 'calc(100vh - 100px)', padding: '0 20px 32px 20px' }}>
      <main className="task-main" style={{ maxWidth: '1000px', margin: '0 auto' }}>
        <div className="task-card" style={{
          background: '#FFFFFF',
          borderRadius: '20px',
          padding: '40px 36px',
          border: '1.5px solid transparent',
          backgroundImage: 'linear-gradient(#ffffff, #ffffff), linear-gradient(135deg, #00123C 0%, #E65525 100%)',
          backgroundClip: 'padding-box, border-box',
          backgroundOrigin: 'padding-box, border-box',
          boxShadow: '0 20px 50px rgba(0, 18, 60, 0.06)'
        }}>

          {/* Centered Logo & Heading */}
          <div style={{ textAlign: 'center', marginBottom: '32px' }}>
            <img src={logo} alt="Infogenx Logo" style={{ height: '60px', width: 'auto', objectFit: 'contain', marginBottom: '20px' }} />
            <h1 style={{
              fontSize: '32px',
              fontWeight: '800',
              margin: '0 0 10px',
              background: 'linear-gradient(135deg, #00123C 0%, #E65525 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}>
              Recruitment Task
            </h1>
            <p style={{ margin: 0, color: '#5C6A86', fontSize: '15px' }}>
              TASK 1 — Practical Recruitment Execution & Verification
            </p>
          </div>

          {/* 7 Step Timeline List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginBottom: '36px' }}>
            <h3 style={{ fontSize: '18px', fontWeight: '800', color: '#00123C', margin: 0 }}>
              Task Execution Steps (1 to 7):
            </h3>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
              {steps.map((step) => (
                <div
                  key={step.number}
                  style={{
                    background: '#FFF8F3',
                    border: '1px solid rgba(0, 18, 60, 0.08)',
                    borderRadius: '14px',
                    padding: '20px',
                    display: 'flex',
                    gap: '16px',
                    alignItems: 'flex-start'
                  }}
                >
                  <span style={{
                    width: '32px',
                    height: '32px',
                    borderRadius: '50%',
                    background: 'linear-gradient(135deg, #00123C 0%, #E65525 100%)',
                    color: '#FFFFFF',
                    fontWeight: '800',
                    fontSize: '14px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0
                  }}>
                    {step.number}
                  </span>
                  <div>
                    <h4 style={{ margin: '0 0 4px', fontSize: '15px', fontWeight: '700', color: '#00123C' }}>
                      Step {step.number}: {step.title}
                    </h4>
                    <p style={{ margin: 0, fontSize: '13px', color: '#5C6A86', lineHeight: '1.5' }}>
                      {step.desc}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Upload Screenshot Card */}
          <div style={{
            background: '#F8FAFC',
            border: '2px dashed #CBD5E1',
            borderRadius: '16px',
            padding: '32px',
            textAlign: 'center'
          }}>
            <h3 style={{ fontSize: '20px', fontWeight: '800', color: '#00123C', margin: '0 0 8px' }}>
              Upload Task Screenshot
            </h3>
            <p style={{ fontSize: '14px', color: '#5C6A86', margin: '0 0 20px' }}>
              Select and upload the screenshot of your published recruitment post.
            </p>

            {uploaded ? (
              <div style={{
                background: '#F0FDF4',
                border: '1px solid #86EFAC',
                borderRadius: '12px',
                padding: '20px',
                color: '#15803D',
                fontWeight: '700',
                fontSize: '15px'
              }}>
                ✓ Screenshot Uploaded Successfully! Your task submission has been registered.
              </div>
            ) : (
              <form onSubmit={handleUploadSubmit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                  style={{ display: 'none' }}
                  id="screenshot-input"
                />

                <label
                  htmlFor="screenshot-input"
                  style={{
                    background: '#FFFFFF',
                    border: '1px solid #CBD5E1',
                    borderRadius: '10px',
                    padding: '12px 24px',
                    fontSize: '14px',
                    fontWeight: '700',
                    color: '#00123C',
                    cursor: 'pointer',
                    display: 'inline-block'
                  }}
                >
                  {selectedFile ? selectedFile.name : 'Choose Screenshot Image'}
                </label>

                {selectedFile && (
                  <p style={{ fontSize: '13px', color: '#00123C', margin: 0 }}>
                    Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
                  </p>
                )}

                <button
                  type="submit"
                  disabled={uploading || !selectedFile}
                  style={{
                    background: 'linear-gradient(90deg, #00123C 0%, #E65525 100%)',
                    color: '#FFFFFF',
                    border: 'none',
                    borderRadius: '10px',
                    padding: '14px 40px',
                    fontSize: '15px',
                    fontWeight: '700',
                    cursor: selectedFile ? 'pointer' : 'not-allowed',
                    opacity: selectedFile ? 1 : 0.6,
                    boxShadow: '0 8px 20px rgba(0, 18, 60, 0.15)'
                  }}
                >
                  {uploading ? 'Uploading...' : 'Upload Screenshot ✓'}
                </button>
              </form>
            )}
          </div>

        </div>
      </main>
    </div>
  )
}

export default TaskPage

