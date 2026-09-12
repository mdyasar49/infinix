import { createTheme } from '@mui/material/styles'

export const muiTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#00123C',
      light: '#1B2C59',
      dark: '#000A24',
      contrastText: '#FFFFFF',
    },
    secondary: {
      main: '#E65525',
      light: '#FF7347',
      dark: '#C23D10',
      contrastText: '#FFFFFF',
    },
    success: {
      main: '#22C55E',
      contrastText: '#FFFFFF',
    },
    background: {
      default: '#F8FAFC',
      paper: '#FFFFFF',
    },
    text: {
      primary: '#00123C',
      secondary: '#5C6A86',
    },
  },
  typography: {
    fontFamily: ['Roboto', '"Segoe UI"', 'sans-serif'].join(','),
    h1: { fontWeight: 800 },
    h2: { fontWeight: 800 },
    h3: { fontWeight: 700 },
    h4: { fontWeight: 700 },
    h5: { fontWeight: 700 },
    h6: { fontWeight: 700 },
    button: { textTransform: 'none', fontWeight: 600 },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 10,
          padding: '8px 18px',
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0 4px 14px rgba(0, 18, 60, 0.12)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderTopRightRadius: 20,
          borderBottomRightRadius: 20,
          boxShadow: '12px 0 36px rgba(0, 18, 60, 0.18)',
        },
      },
    },
  },
})
