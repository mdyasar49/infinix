import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import MaterialCard from '../../components/MaterialCard'
import { learningMaterials } from '../../services/mockData'
import './LearningMaterialsPage.css'

function LearningMaterialsPage() {
  const [materials, setMaterials] = useState(learningMaterials)
  const navigate = useNavigate()

  const isComplete = materials.every((item) => item.status === 'completed')

  const handleComplete = (id) => {
    setMaterials((previous) =>
      previous.map((item) => {
        if (item.id === id && item.status === 'current') {
          return { ...item, status: 'completed' }
        }
        if (item.id === id + 1 && item.status === 'locked') {
          return { ...item, status: 'current' }
        }
        return item
      }),
    )
  }

  const progressCount = useMemo(
    () => materials.filter((item) => item.status === 'completed').length,
    [materials],
  )

  return (
    <section className="materials-shell">
      <div className="materials-panel">
        <div className="flow-header">
          <div>
            <h1>Learning <span className="heading-accent">Materials</span></h1>
            <p>Complete each item in sequence to advance to the next onboarding stage.</p>
          </div>
          <p>{progressCount} of {materials.length} completed</p>
        </div>

        <div className="material-summary">
          <div className="summary-card">
            <strong>{progressCount}</strong>
            <p>Completed modules</p>
          </div>
          <div className="summary-card">
            <strong>{materials.filter((item) => item.status === 'current').length}</strong>
            <p>In progress</p>
          </div>
          <div className="summary-card">
            <strong>{materials.filter((item) => item.status === 'locked').length}</strong>
            <p>Locked modules</p>
          </div>
        </div>

        <div className="material-list">
          {materials.map((item, index) => {
            const disabled = item.status === 'locked'
            return (
              <MaterialCard
                key={item.id}
                index={index}
                item={item}
                disabled={disabled}
                onComplete={handleComplete}
              />
            )
          })}
        </div>

        <div className="continue-banner">
          <p>
            Once all learning materials are completed, you can move forward with the next onboarding step.
          </p>
          <button
            type="button"
            className="continue-button"
            disabled={!isComplete}
            onClick={() => isComplete && navigate('/terms')}
          >
            Continue to Terms
          </button>
        </div>
      </div>
    </section>
  )
}

export default LearningMaterialsPage
