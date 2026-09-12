function MaterialCard({ item, index, onComplete, disabled }) {
  return (
    <article className={`material-card ${item.status}`}>
      <div className="material-header">
        <div className="material-tag">{item.type}</div>
        <span className={`material-status ${item.status}`}>{item.status}</span>
      </div>
      <h3>{item.title}</h3>
      <p>{item.description}</p>
      <div className="material-meta">
        <span>{item.duration}</span>
        <span>Step {index + 1}</span>
      </div>
      <button
        type="button"
        className="material-action"
        onClick={() => onComplete(item.id)}
        disabled={disabled || item.status === 'completed'}
      >
        {item.status === 'completed' ? 'Completed' : item.status === 'locked' ? 'Locked' : 'Mark as Completed'}
      </button>
    </article>
  )
}

export default MaterialCard
