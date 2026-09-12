import { useLocation } from 'react-router-dom'

export default function VisualTheme() {
  const { pathname } = useLocation()
  return pathname === '/login' ? <div className="visual-theme-root" aria-hidden="true" /> : null
}
