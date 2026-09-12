import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  AppBar,
  Toolbar,
  Box,
  Button,
  Avatar,
  Typography,
  Icon,
} from '@mui/material'
import { useAuth } from '../hooks/useAuth'
import NavigationDrawer from './NavigationDrawer'
import logo from '../assets/logo.png'

function TopHeader({ profile }) {
  const { user: authUser, logout } = useAuth()
  const navigate = useNavigate()
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)
  const currentProfile = profile || authUser

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const candidateName = currentProfile?.name || currentProfile?.email?.split('@')[0] || 'Candidate'
  const candidateInitial = candidateName.charAt(0).toUpperCase()
  const candidateRole = currentProfile?.department
    ? `${currentProfile.department} Specialist`
    : (currentProfile?.role || 'Candidate')

  return (
    <>
      <NavigationDrawer isOpen={isDrawerOpen} onClose={() => setIsDrawerOpen(false)} />

      <AppBar
        position="static"
        elevation={0}
        className="no-print"
        sx={{
          backgroundColor: '#FFFFFF',
          borderRadius: 4,
          border: '1px solid rgba(0, 18, 60, 0.08)',
          boxShadow: '0 4px 20px rgba(0, 18, 60, 0.05)',
          maxWidth: '1200px',
          margin: '0 auto 20px auto',
          width: '100%',
          boxSizing: 'border-box',
          px: { xs: 1, sm: 2 },
          py: 0.5,
          color: 'text.primary',
        }}
      >
        <Toolbar disableGutters sx={{ justifyContent: 'space-between', minHeight: 64 }}>
          {/* Left: Drawer Toggle & Brand Logo */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: { xs: 1, sm: 2 } }}>
            <Button
              variant="outlined"
              onClick={() => setIsDrawerOpen(true)}
              startIcon={<Icon sx={{ color: '#E65525' }}>menu</Icon>}
              sx={{
                borderRadius: 2.5,
                borderColor: 'rgba(230, 85, 37, 0.3)',
                backgroundColor: '#FFF8F3',
                color: '#00123C',
                fontWeight: 700,
                fontSize: '14px',
                px: { xs: 1.5, sm: 2 },
                py: 0.8,
                '&:hover': {
                  backgroundColor: '#E65525',
                  borderColor: '#E65525',
                  color: '#FFFFFF',
                  '& .material-icons': { color: '#FFFFFF' },
                },
                transition: 'all 0.2s ease',
              }}
            >
              Menu
            </Button>

            <Box
              component="img"
              src={logo}
              alt="Infogenx"
              onClick={() => navigate('/pdf')}
              sx={{
                height: { xs: 32, sm: 40 },
                width: 'auto',
                cursor: 'pointer',
                transition: 'transform 0.2s',
                '&:hover': { transform: 'scale(1.02)' },
              }}
            />
          </Box>

          {/* Right: Candidate Profile & Logout */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: { xs: 1.5, sm: 2.5 } }}>
            {currentProfile && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                <Avatar
                  sx={{
                    width: 40,
                    height: 40,
                    background: 'linear-gradient(135deg, #00123C 0%, #E65525 100%)',
                    fontWeight: 800,
                    fontSize: 16,
                    boxShadow: '0 2px 8px rgba(0, 18, 60, 0.18)',
                  }}
                >
                  {candidateInitial}
                </Avatar>
                <Box sx={{ display: { xs: 'none', sm: 'block' }, textAlign: 'left' }}>
                  <Typography
                    variant="subtitle2"
                    sx={{
                      fontWeight: 700,
                      color: '#00123C',
                      lineHeight: 1.2,
                      maxWidth: 160,
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {candidateName}
                  </Typography>
                  <Typography
                    variant="caption"
                    sx={{
                      color: '#5C6A86',
                      lineHeight: 1,
                      maxWidth: 160,
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                      display: 'block',
                      mt: 0.3,
                    }}
                  >
                    {candidateRole}
                  </Typography>
                </Box>
              </Box>
            )}

            <Button
              variant="outlined"
              size="small"
              onClick={handleLogout}
              startIcon={<Icon sx={{ fontSize: 18 }}>logout</Icon>}
              sx={{
                borderRadius: 2,
                borderColor: '#CBD5E1',
                color: '#00123C',
                fontWeight: 600,
                fontSize: 13,
                px: 1.5,
                py: 0.6,
                '&:hover': {
                  borderColor: '#EF4444',
                  backgroundColor: '#FEE2E2',
                  color: '#DC2626',
                },
              }}
            >
              Logout
            </Button>
          </Box>
        </Toolbar>
      </AppBar>
    </>
  )
}

export default TopHeader
