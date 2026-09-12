import { Link } from 'react-router-dom'
import { trainingPlan } from '../../services/mockData'
import './TrainingPage.css'

function TrainingPage() {
  return (
    <section className="training-shell">
      <div className="training-panel">
        <div className="training-banner">
          <div>
            <p className="training-label">Day-1 Training</p>
            <h1>Infogenx Onboarding <span className="heading-accent">Instructions</span></h1>
          </div>
          <div className="training-status">
            <span>Ready for your first day</span>
          </div>
        </div>

        <div className="training-grid">
          <article className="training-card training-intro">
            <h2>Getting <span className="heading-accent">started</span></h2>
            <p>{trainingPlan.intro}</p>
          </article>

          <article className="training-card">
            <h2>Training <span className="heading-accent">Resources</span></h2>
            <ul>
              {trainingPlan.resources.map((resource) => (
                <li key={resource.title}>
                  <a href={resource.url} className="resource-link">
                    <span>{resource.title}</span>
                    <strong>{resource.type}</strong>
                  </a>
                </li>
              ))}
            </ul>
          </article>

          <article className="training-card">
            <h2>Day 1 <span className="heading-accent">Tasks</span></h2>
            <div className="task-list">
              {trainingPlan.tasks.map((task) => (
                <div key={task.title} className="task-item">
                  <div>
                    <p className="task-title">{task.title}</p>
                    <span className={`task-pill ${task.status.toLowerCase()}`}>{task.status}</span>
                  </div>
                </div>
              ))}
            </div>
          </article>
        </div>

        <div className="training-actions">
          <Link to="/completion" className="secondary-button">
            Proceed to Completion
          </Link>
          <Link to="/dashboard" className="primary-button">
            Back to Dashboard
          </Link>
        </div>
      </div>
    </section>
  )
}

export default TrainingPage
