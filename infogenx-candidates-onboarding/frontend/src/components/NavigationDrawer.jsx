import { useNavigate, useLocation } from 'react-router-dom'
import {
  Drawer,
  Box,
  Typography,
  IconButton,
  Avatar,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  ListSubheader,
  Divider,
  Chip,
  Button,
  Icon,
} from '@mui/material'
import { useAuth } from '../hooks/useAuth'
import logo from '../assets/logo.png'

function NavigationDrawer({ isOpen, onClose }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const handleNav = (path) => {
    navigate(path)
    onClose()
  }

  const handleLogout = () => {
    onClose()
    logout()
    navigate('/login')
  }

  const candidateName = user?.name || user?.email?.split('@')[0] || 'Candidate'
  const candidateInitial = candidateName.charAt(0).toUpperCase()
  const isAdmin = user?.role === 'admin'
  const isTestUser = user?.role === 'test_user' || user?.role === 'test'

  const roleLabel = isAdmin 
    ? '🛡️ System Administrator' 
    : (isTestUser ? '🧪 Test User (Unlimited)' : 'Candidate / Student')

  const candidateRole = user?.department
    ? `${user.department} Specialist`
    : roleLabel

  // Check assessment result
  let hasPassed = false
  if (user?.email) {
    try {
      const saved = sessionStorage.getItem(`infogenx_assessment_result_${user.email}`)
      if (saved) {
        const parsed = JSON.parse(saved)
        hasPassed = parsed.passed || parsed.score >= 40
      }
    } catch (e) {
      // ignore
    }
  }

  const menuSections = [
    ...(isAdmin ? [{
      title: 'Administrator Console (cPanel DB)',
      items: [
        { path: '/admin/offer-review', icon: 'admin_panel_settings', label: 'Monitor All & Edit Users', badge: 'Admin', badgeColor: 'error' },
      ],
    }] : []),
    {
      title: 'Core 6-Step Pipeline',
      items: [
        { path: '/pdf', icon: 'description', label: 'Step 1: SOP / PDF Guide', badge: 'Step 1', badgeColor: 'default' },
        { path: '/ppt', icon: 'co_present', label: 'Step 2: Company PPT', badge: 'Step 2', badgeColor: 'default' },
        { path: '/assessment', icon: 'quiz', label: 'Step 3: Assessment Exam', badge: 'Step 3', badgeColor: 'default' },
        {
          path: '/result',
          icon: 'assessment',
          label: 'Step 4: Exam Result',
          badge: hasPassed ? 'Passed ✓' : 'Step 4',
          badgeColor: hasPassed ? 'success' : 'default',
        },
        { path: '/offer-letter', icon: 'verified', label: 'Step 5: Official Offer Letter', badge: 'Sign', badgeColor: 'secondary' },
        { path: '/task', icon: 'assignment', label: 'Step 6: Recruitment Task', badge: 'Step 6', badgeColor: 'default' },
      ],
    },
    {
      title: 'HR & Careers',
      items: [
        { path: '/offer-letter', icon: 'verified', label: 'Offer Letter Acceptance', badge: 'Docx', badgeColor: 'secondary' },
        { path: '/hr-interview', icon: 'handshake', label: 'HR Interview Scheduling' },
        { path: '/job-roles', icon: 'work', label: 'Job Roles & Streams' },
        { path: '/signature', icon: 'draw', label: 'Digital E-Signature' },
      ],
    },
    {
      title: 'Learning & Orientation',
      items: [
        { path: '/materials', icon: 'menu_book', label: 'Learning Materials' },
        { path: '/training', icon: 'model_training', label: 'Training Modules' },
        { path: '/sop', icon: 'policy', label: 'Infogenx Recruitment SOP' },
        { path: '/recruitment-process', icon: 'format_list_numbered', label: 'Recruitment Flow Guide' },
      ],
    },
    {
      title: 'Portal & Policies',
      items: [
        { path: '/dashboard', icon: 'dashboard', label: 'Candidate Dashboard' },
        { path: '/onboarding', icon: 'rocket_launch', label: 'Onboarding Overview' },
        { path: '/terms', icon: 'gavel', label: 'Terms & Conditions' },
        { path: '/completion', icon: 'emoji_events', label: 'Completion Certificate' },
      ],
    },
  ]

  return (
    <Drawer
      anchor="left"
      open={isOpen}
      onClose={onClose}
      elevation={8}
      PaperProps={{
        sx: {
          width: { xs: 300, sm: 340 },
          backgroundColor: '#FFFFFF',
          display: 'flex',
          flexDirection: 'column',
        },
      }}
    >
      {/* Drawer Header */}
      <Box
        sx={{
          p: 2,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          borderBottom: '1px solid rgba(0, 18, 60, 0.08)',
          backgroundColor: '#FAFAFB',
        }}
      >
        <Box component="img" src={logo} alt="Infogenx" sx={{ height: 34, width: 'auto' }} />
        <IconButton onClick={onClose} size="small" sx={{ border: '1px solid #CBD5E1', borderRadius: 2 }}>
          <Icon sx={{ fontSize: 20 }}>close</Icon>
        </IconButton>
      </Box>

      {/* Candidate Profile Widget */}
      {user && (
        <Box
          sx={{
            p: 2,
            display: 'flex',
            alignItems: 'center',
            gap: 1.5,
            background: 'linear-gradient(135deg, rgba(0, 18, 60, 0.03) 0%, rgba(230, 85, 37, 0.06) 100%)',
            borderBottom: '1px solid rgba(0, 18, 60, 0.06)',
          }}
        >
          <Avatar
            sx={{
              width: 44,
              height: 44,
              background: 'linear-gradient(135deg, #00123C 0%, #E65525 100%)',
              fontWeight: 800,
              fontSize: 16,
              boxShadow: '0 2px 8px rgba(0, 18, 60, 0.2)',
            }}
          >
            {candidateInitial}
          </Avatar>
          <Box sx={{ overflow: 'hidden' }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 700, color: '#00123C' }} noWrap>
              {candidateName}
            </Typography>
            <Typography variant="caption" sx={{ color: '#5C6A86' }} noWrap display="block">
              {candidateRole}
            </Typography>
          </Box>
        </Box>
      )}

      {/* Navigation List */}
      <Box sx={{ flex: 1, overflowY: 'auto', py: 1 }}>
        {menuSections.map((section, sIdx) => (
          <List
            key={sIdx}
            dense
            disablePadding
            subheader={
              <ListSubheader
                disableSticky
                sx={{
                  backgroundColor: 'transparent',
                  fontWeight: 800,
                  fontSize: 11,
                  letterSpacing: '0.08em',
                  textTransform: 'uppercase',
                  color: '#8C99B2',
                  lineHeight: '28px',
                  pt: 1.5,
                  px: 2.5,
                }}
              >
                {section.title}
              </ListSubheader>
            }
          >
            {section.items.map((item, iIdx) => {
              const isActive = location.pathname === item.path
              return (
                <ListItem key={iIdx} disablePadding sx={{ px: 1.5, py: 0.3 }}>
                  <ListItemButton
                    selected={isActive}
                    onClick={() => handleNav(item.path)}
                    sx={{
                      borderRadius: 2.5,
                      py: 0.8,
                      px: 1.5,
                      '&.Mui-selected': {
                        background: 'linear-gradient(90deg, #00123C 0%, #E65525 100%)',
                        color: '#FFFFFF',
                        boxShadow: '0 4px 12px rgba(230, 85, 37, 0.25)',
                        '& .MuiListItemIcon-root .material-icons': { color: '#FFFFFF' },
                        '&:hover': {
                          background: 'linear-gradient(90deg, #00123C 0%, #E65525 100%)',
                        },
                      },
                      '&:hover': {
                        backgroundColor: '#FFF8F3',
                        color: '#E65525',
                        '& .MuiListItemIcon-root .material-icons': { color: '#E65525' },
                      },
                    }}
                  >
                    <ListItemIcon sx={{ minWidth: 36 }}>
                      <Icon
                        sx={{
                          fontSize: 20,
                          color: isActive ? '#FFFFFF' : '#00123C',
                          transition: 'color 0.2s',
                        }}
                      >
                        {item.icon}
                      </Icon>
                    </ListItemIcon>
                    <ListItemText
                      primary={item.label}
                      primaryTypographyProps={{
                        fontSize: 13,
                        fontWeight: isActive ? 700 : 600,
                      }}
                    />
                    {item.badge && (
                      <Chip
                        label={item.badge}
                        size="small"
                        color={item.badgeColor || 'default'}
                        sx={{
                          height: 20,
                          fontSize: 10,
                          fontWeight: 800,
                          borderRadius: 1.5,
                          backgroundColor: isActive ? '#FFFFFF' : undefined,
                          color: isActive ? '#E65525' : undefined,
                        }}
                      />
                    )}
                  </ListItemButton>
                </ListItem>
              )
            })}
          </List>
        ))}
      </Box>

      {/* Drawer Footer */}
      <Divider />
      <Box sx={{ p: 2, backgroundColor: '#FAFAFB', display: 'flex', flexDirection: 'column', gap: 1.5 }}>
        <Typography variant="caption" sx={{ color: '#64748B', lineHeight: 1.4 }}>
          Need assistance? <strong>HR Director:</strong><br />
          +91 97878 06366 • nithyanand.a@infogenx.com.au
        </Typography>

        <Button
          variant="outlined"
          fullWidth
          onClick={handleLogout}
          startIcon={<Icon>logout</Icon>}
          sx={{
            borderRadius: 2,
            borderColor: '#CBD5E1',
            color: '#00123C',
            fontWeight: 700,
            fontSize: 13,
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
    </Drawer>
  )
}

export default NavigationDrawer
