import { Link } from 'react-router-dom'
import './NotFoundPage.css'

function NotFoundPage() {
  return (
    <section className="notfound-shell">
      <div className="notfound-card">
        <h1>404</h1>
        <p>We couldn't find the page you're looking for. Return to the Infogenx portal home to continue your onboarding.</p>
        <Link to="/pdf-learning" className="primary-button">
          Return to Learning
        </Link>
      </div>
    </section>
  )
}

export default NotFoundPage
