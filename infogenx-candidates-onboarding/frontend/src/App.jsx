import AppRoutes from './routes/AppRoutes'
import { AuthProvider } from './hooks/useAuth'
import './brand-theme.css'

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  )
}

export default App
