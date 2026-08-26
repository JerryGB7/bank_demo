import { Container, Typography, Box } from "@mui/material"
import AppHeader from "./components/layout/AppHeader"
import ATMList from "./components/atms/ATMList"
import { mockATMs } from "./mockData/atms"
import ServiceCallList from "./components/servicecalls/ServiceCallList"
import { mockServiceCalls } from "./mockData/discrepancies"

const atmsWithDiscrepancies = mockATMs.filter((atm) =>
  mockServiceCalls.some((discrepancy) => discrepancy.atmId === atm.id)
)

function App(){
  return(
    <>
      <AppHeader />
      <Container maxWidth='lg' sx={{mt: 4}}>
        <Typography variant="h5" component="h2" gutterBottom>
          Branch Overview
        </Typography>
        <Box sx={{mb:4}}>
          <h2 color="primary">All ATMS</h2>
          <ATMList atms={mockATMs}/>
        </Box>
        <Box sx={{mb:4}}>
          ATMS in need of maintenance
          <ATMList atms={atmsWithDiscrepancies}/>
        </Box>
        <Box sx={{mb:4}}>
          Service Calls In Progress
          <ServiceCallList discrepancies={mockServiceCalls}/>
        </Box>
      </Container>
    </>
  )
};

export default App;