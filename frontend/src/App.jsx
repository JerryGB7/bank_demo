import { useState } from "react"
import { Container, Typography, Box, Snackbar, Alert } from "@mui/material"

import AppHeader from "./components/layout/AppHeader"
import ATMDataGrid from "./components/atms/ATMDataGrid.jsx"
import ServiceCallDataGrid from "./components/servicecalls/ServiceCallDataGrid.jsx"
import BranchDataGrid from "./components/branches/BranchDataGrid.jsx"
import MaintenanceFlags from "./components/analytics/MaintenanceFlags.jsx"
import LowCashAlert from "./components/analytics/LowCashAlert.jsx"
import CoLocationDiscrepancy from "./components/analytics/CoLocationDiscrepancy.jsx"
import ReliabilityMetrics from "./components/analytics/ReliabilityMetrics.jsx"
import ReportingLines from "./components/analytics/ReportingLines.jsx"


import LoginForm from "./components/auth/LoginForm"
import { AuthProvider, useAuth } from "./context/AuthContext"
import darkBlueBackground from "./assets/OIP.png"



function Dashboard(){
  const {user, logout} = useAuth()
  const [notification, setNotification] = useState(null)

  return(
    <Box sx={{
      minHeight: '100vh',
      backgroundImage: `linear-gradient(rgba(7, 22, 42, 0.3), rgba(7, 22, 42, 0.3)), url(${darkBlueBackground})`,
      backgroundPosition: 'center',
      backgroundSize: 'cover',
      backgroundAttachment: 'fixed',
      '& h1, & h2, & h3': {
        textShadow: '1px 0 #fff, -1px 0 #fff, 0 1px #fff, 0 -1px #fff',
      },
    }}>
      <AppHeader username={user?.sub} role={user?.role} onLogout={logout} />
      <Container maxWidth="lg" sx={{mt: 4}}>
        <Typography variant="h3" component="h2" gutterBottom>
          ATM Operations Command Center
        </Typography>
        <Box sx={{mb: 4}}>
          <MaintenanceFlags />
        </Box>
        <Box sx={{mb: 4}}>
          <LowCashAlert />
        </Box>
        <Box sx={{mb: 4}}>
          <CoLocationDiscrepancy />
        </Box>
        <Box sx={{mb: 4}}>
          <ReliabilityMetrics />
        </Box>
        <Box sx={{mb: 4}}>
          <ReportingLines />
        </Box>
        <Typography variant="h5" component="h2" gutterBottom>
          All Branches
        </Typography>
        <Box sx={{mb: 4}}>
          <BranchDataGrid />
        </Box> 
        <Typography variant="h5" component="h2" gutterBottom>
          List of ATMS
        </Typography>
          <Box sx={{mb: 4}}>
            <ATMDataGrid onNotification={setNotification} />
          </Box>
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
        <Alert severity={notification?.severity ?? "success"} onClose={() => setNotification(null)}>
          {notification?.message ?? notification}
        </Alert>
      </Snackbar>
    </Box>
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