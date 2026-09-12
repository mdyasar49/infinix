import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user session exists on mount
    const sessionData = sessionStorage.getItem('infogenx_session')
    if (sessionData) {
      setUser(JSON.parse(sessionData))
    }
    setLoading(false)
  }, [])

  const login = (userData) => {
    setUser(userData)
    sessionStorage.setItem('infogenx_session', JSON.stringify(userData))
  }

  const logout = () => {
    setUser(null)
    sessionStorage.removeItem('infogenx_session')
  }

  const updateProgress = (stepId, completed = true) => {
    if (user) {
      const updated = {
        ...user,
        onboardingProgress: {
          ...user.onboardingProgress,
          [stepId]: completed,
        },
      }
      setUser(updated)
      sessionStorage.setItem('infogenx_session', JSON.stringify(updated))
    }
  }

  const getCompletedSteps = () => {
    if (!user) return []
    return Object.keys(user.onboardingProgress || {})
      .filter((key) => user.onboardingProgress[key])
      .map(Number)
      .sort((a, b) => a - b)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, updateProgress, getCompletedSteps, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
