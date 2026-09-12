import { Navigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import TopHeader from './TopHeader'

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', background: '#F8FAFC' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '20px', fontWeight: '700', color: '#00123C', marginBottom: '8px' }}>
            Loading Infogenx Candidate Portal...
          </div>
          <div style={{ fontSize: '14px', color: '#5C6A86' }}>Please wait</div>
        </div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return (
    <div className="portal-app-layout" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: '#FFFFFF' }}>
      <div className="portal-header-container no-print" style={{ width: '100%', maxWidth: '1200px', margin: '0 auto', padding: '16px 20px 0 20px', boxSizing: 'border-box' }}>
        <TopHeader profile={user} />
      </div>
      <div className="portal-page-body" style={{ flex: 1, width: '100%' }}>
        {children}
      </div>
    </div>
  )
}
