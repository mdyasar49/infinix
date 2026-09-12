import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import ProgressSidebar from '../../components/ProgressSidebar'
import { useAuth } from '../../hooks/useAuth'
import { onboardingWorkflow } from '../../services/authService'
import './DashboardPage.css'

function DashboardPage() {
  const { user } = useAuth()
  const [steps, setSteps] = useState([])

  useEffect(() => {
    if (user) {
      // Build step statuses based on onboardingProgress
      const completedStepIds = Object.keys(user.onboardingProgress || {})
        .filter((key) => user.onboardingProgress[key])
        .map(Number)
        .sort((a, b) => a - b)

      const builtSteps = onboardingWorkflow.map((workflow) => {
        let status = 'locked'
        if (completedStepIds.includes(workflow.id)) {
          status = 'complete'
        } else if (workflow.id === (completedStepIds.length ? completedStepIds[completedStepIds.length - 1] + 1 : 2)) {
          status = 'current'
        }
        return {
          ...workflow,
          status,
        }
      })

      setSteps(builtSteps)
    }
  }, [user])

  const currentStep = steps.find((step) => step.status === 'current')
  const completedCount = steps.filter((step) => step.status === 'complete').length

  if (!user) {
    return null
  }

  return (
    <div className="dashboard-shell">
      <ProgressSidebar steps={steps} />

      <main className="dashboard-main">

        <section className="dashboard-welcome">
          <h2>Onboarding <span className="heading-accent">Progress</span></h2>
          <p>
            Your Infogenx onboarding journey is moving ahead smoothly. Complete the next module to unlock the
            following steps.
          </p>

          <div className="progress-card">
            <h3>Current Journey <span className="heading-accent">Status</span></h3>
            <div className="progress-line">
              {Array.from({ length: 10 }).map((_, index) => (
                <span key={index} className={index < completedCount ? 'active' : ''} />
              ))}
            </div>
            <div className="progress-values">
              <span>{Math.round((completedCount / 10) * 100)}% Completed</span>
              <span>{completedCount} of 10 steps done</span>
            </div>
          </div>
        </section>

        <section className="dashboard-grid">
          <article className="dashboard-panel">
            <h3>Next <span className="heading-accent">Milestone</span></h3>
            <div className="milestone-card">
              <strong>{currentStep?.title || 'All Steps Complete!'}</strong>
              <p>{currentStep?.description || 'You have completed all onboarding steps.'}</p>
              <div className="action-group">
                {currentStep && (
                  <>
                    <Link to={currentStep?.route || '/dashboard'} className="primary-button">
                      Continue to {currentStep?.title}
                    </Link>
                    <Link to="/materials" className="secondary-button">
                      Review Learning Materials
                    </Link>
                  </>
                )}
                {!currentStep && (
                  <Link to="/completion" className="primary-button">
                    View Completion Summary
                  </Link>
                )}
              </div>
            </div>
          </article>

          <article className="progress-card">
            <h3>Snapshot</h3>
            <div className="metrics-grid">
              <div className="metric-card">
                <strong>{user.batch}</strong>
                <p>Onboarding batch</p>
              </div>
              <div className="metric-card">
                <strong>{currentStep?.title || 'Complete'}</strong>
                <p>Next assigned activity</p>
              </div>
              <div className="metric-card">
                <strong>{user.location}</strong>
                <p>Student location</p>
              </div>
            </div>
          </article>
        </section>
      </main>
    </div>
  )
}

export default DashboardPage
