import { Container, Typography, Box } from "@mui/material"

import AppHeader from "./components/layout/AppHeader"
import ATMDataGrid from "./components/atms/ATMDataGrid.jsx"


import LoginForm from "./components/auth/LoginForm"
import { AuthProvider, useAuth } from "./context/AuthContext"


function Dashboard(){
  const {user, logout} = useAuth()

  return(
    <>
      <AppHeader username={user?.sub} role={user?.role} onLogout={logout} />
      <Container maxWidth="lg" sx={{mt: 4}}>
        <Typography variant="h5" component="h2" gutterBottom>
          Bank Overview
        </Typography>
        <Box sx={{mb: 4}}>
          <ATMDataGrid />
        </Box>
      </Container>
    </>
  )
};

//conditional layout switcher component that renders either the dashboard of the login form
// based on the users authentication status, that is tracked in the global Auth context
function AppContent() {
  const {isAuthenticated} = useAuth()
  return isAuthenticated ? <Dashboard /> : <LoginForm />
}


function App(){


  return(
    <>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </>
  )
};

export default App;