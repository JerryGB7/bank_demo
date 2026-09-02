import { useState } from "react"
import { Container, Typography, Box, Button, Snackbar, Alert } from "@mui/material"

import AppHeader from "./components/layout/AppHeader"
import ATMDataGrid from "./components/atms/ATMDataGrid.jsx"
import ServiceCallDataGrid from "./components/servicecalls/ServiceCallDataGrid.jsx"
import BranchDataGrid from "./components/branches/BranchDataGrid.jsx"


import LoginForm from "./components/auth/LoginForm"
import { AuthProvider, useAuth } from "./context/AuthContext"



function Dashboard(){
  const {user, logout} = useAuth()
  const [showATMs, setShowATMs] = useState(false)
  const [notification, setNotification] = useState(null)

  return(
    <>
      <AppHeader username={user?.sub} role={user?.role} onLogout={logout} />
      <Container maxWidth="lg" sx={{mt: 4}}>
        <Typography variant="h3" component="h2" gutterBottom>
          Branch Operations Command Center
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom>
          All Branches
        </Typography>
        <Box sx={{mb: 4}}>
          <BranchDataGrid />
        </Box> 
        <Typography variant="h5" component="h2" gutterBottom>
          List of ATMS
        </Typography>
        <Button
          variant="contained"
          onClick={() => setShowATMs((visible) => !visible)}
          sx={{mb: 2}}
        >
          {showATMs ? "Hide ATMs" : "Show ATMs"}
        </Button>
        {showATMs && (
          <Box sx={{mb: 4}}>
            <ATMDataGrid />
          </Box>
        )}
        <Typography variant="h5" component="h2" gutterBottom>
          Current Service Calls
        </Typography>
        <Box sx={{mb: 4}}>
          <ServiceCallDataGrid />
        </Box>
      </Container>
      <Snackbar
        open={Boolean(notification)}
        autoHideDuration={6000}
        onClose={() => setNotification(null)}
      >
        <Alert severity="success" onClose={() => setNotification(null)}>
          {notification}
        </Alert>
      </Snackbar>
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