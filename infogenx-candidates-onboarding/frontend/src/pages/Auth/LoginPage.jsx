import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { login as authLogin } from '../../services/authService'
import logo from '../../assets/logo.png'
import './LoginPage.css'

function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login } = useAuth()
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    let animationFrameId
    let width = (canvas.width = window.innerWidth)
    let height = (canvas.height = window.innerHeight)

    const handleResize = () => {
      if (!canvas) return
      width = canvas.width = window.innerWidth
      height = canvas.height = window.innerHeight
    }
    window.addEventListener('resize', handleResize)

    const nodeCount = Math.min(Math.floor((width * height) / 22000), 40)
    const nodes = []
    const colors = ['#00123C', '#E65525']

    for (let i = 0; i < nodeCount; i++) {
      nodes.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.35,
        vy: (Math.random() - 0.5) * 0.35,
        radius: Math.random() * 2 + 1.2,
        color: colors[Math.random() > 0.35 ? 0 : 1],
      })
    }

    const render = () => {
      ctx.clearRect(0, 0, width, height)

      for (let i = 0; i < nodes.length; i++) {
        const node = nodes[i]
        node.x += node.vx
        node.y += node.vy

        if (node.x < 0 || node.x > width) node.vx *= -1
        if (node.y < 0 || node.y > height) node.vy *= -1

        ctx.beginPath()
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2)
        ctx.fillStyle = node.color === '#00123C' ? 'rgba(0, 18, 60, 0.25)' : 'rgba(230, 85, 37, 0.3)'
        ctx.fill()

        for (let j = i + 1; j < nodes.length; j++) {
          const other = nodes[j]
          const dx = other.x - node.x
          const dy = other.y - node.y
          const dist = Math.sqrt(dx * dx + dy * dy)

          if (dist < 140) {
            const alpha = (1 - dist / 140) * 0.12
            ctx.beginPath()
            ctx.moveTo(node.x, node.y)
            ctx.lineTo(other.x, other.y)
            ctx.strokeStyle = node.color === '#E65525' || other.color === '#E65525'
              ? `rgba(230, 85, 37, ${alpha})`
              : `rgba(0, 18, 60, ${alpha})`
            ctx.lineWidth = 1
            ctx.stroke()
          }
        }
      }

      animationFrameId = requestAnimationFrame(render)
    }

    render()

    return () => {
      window.removeEventListener('resize', handleResize)
      cancelAnimationFrame(animationFrameId)
    }
  }, [])

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setLoading(true)

    try {
      const result = await authLogin(email, password)

      if (result.success) {
        login(result.student)
        navigate('/pdf')
      } else {
        setError(result.error || 'Login failed. Please try again.')
      }
    } catch (error) {
      setError('Unable to connect to server.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-shell">
      <canvas ref={canvasRef} className="network-canvas" aria-hidden="true" />

      <main className="login-content">
        <div className="login-card">
          <img src={logo} alt="Infogenx Logo" className="hero-logo" />

          <div className="welcome-section">
            <h1><span className="text-navy">Candidate</span> <span className="text-orange">Login</span></h1>
            <p>Please login using the email ID and generated password provided after your application submission.</p>
          </div>

          {error && <div className="login-alert">{error}</div>}

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group login-field">
              <label className="input-label" htmlFor="email">Email ID</label>
              <div className="input-control">
                <svg className="input-icon" viewBox="0 0 24 24" aria-hidden="true">
                  <rect x="3" y="5" width="18" height="14" rx="2" />
                  <path d="m4 7 8 6 8-6" />
                </svg>
                <input
                  type="email"
                  id="email"
                  className="form-input"
                  placeholder="Enter your registered email ID"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  required
                  disabled={loading}
                />
              </div>
            </div>

            <div className="form-group login-field">
              <label className="input-label" htmlFor="password">Password</label>
              <div className="input-control">
                <svg className="input-icon" viewBox="0 0 24 24" aria-hidden="true">
                  <rect x="5" y="10" width="14" height="10" rx="2" />
                  <path d="M8 10V7a4 4 0 0 1 8 0v3" />
                </svg>
                <input
                  type="password"
                  id="password"
                  className="form-input"
                  placeholder="Enter your generated password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                  disabled={loading}
                />
              </div>
            </div>

            <button type="submit" className="login-button" disabled={loading}>
              {loading ? 'Signing In...' : 'Login'}
            </button>
          </form>
        </div>
      </main>

      <footer className="login-footer">
        <p>© 2026 Infogenx Pvt. Ltd. All Rights Reserved.</p>
      </footer>
    </div>
  )
}

export default LoginPage

