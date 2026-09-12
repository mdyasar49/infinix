import { Link } from 'react-router-dom'
import logo from '../../assets/logo.png'
import './RegistrationPage.css'

function RegistrationPage() {
  return (
    <section className="register-shell">
      <div className="register-card">
        <div className="register-brand">
          <img src={logo} alt="Infogenx logo" />
          <span>Student Portal</span>
        </div>
        <h1>Create Your Student <span className="heading-accent">Account</span></h1>
        <p>Join Infogenx onboarding and access the full student journey with premium learning and assessment modules.</p>

        <form className="register-form">
          <div className="form-group">
            <label className="form-label" htmlFor="fullName">Full Name</label>
            <input className="form-input" id="fullName" type="text" placeholder="Enter your full name" />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="email">Email Address</label>
            <input className="form-input" id="email" type="email" placeholder="you@example.com" />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="password">Password</label>
            <input className="form-input" id="password" type="password" placeholder="Create a password" />
          </div>

          <div className="form-actions">
            <button type="button" className="primary-button">Create Account</button>
            <Link to="/login" className="secondary-button">Already have an account?</Link>
          </div>
        </form>

        <div className="register-footer">
          <p>By continuing, you agree to Infogenx onboarding terms and privacy guidelines.</p>
        </div>
      </div>
    </section>
  )
}

export default RegistrationPage
