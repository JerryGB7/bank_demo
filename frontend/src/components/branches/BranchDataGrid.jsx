import {useEffect, useState} from "react"
import {DataGrid} from "@mui/x-data-grid"
import {Alert, Box, CircularProgress} from "@mui/material"
import apiClient from "../../api/client"    

// defining our data grid columns and map them to our backend API response data
const columns = [
    {field: 'id', headerName: 'ID', width: 70},
    {field: 'name', headerName: 'Serial Number', width: 150},
    {field: 'location_region', headerName: "Model", width: 160},
    {field: 'capacity', headerName: "Capacity", width: 120, type: "number"},
    {field: 'supervisor_id', headerName: "Supervisor ID", width: 120, type: "number"},
];

//local state variables for tracking table rows, loading status, and network errors
// to track the lifecycle of the async API request so the UI can render appropriately

function BranchDataGrid(){
    const [branches, setBranches] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    //react effect hood that runs our async fetch
    useEffect(() => {
        //track the component mount status to prevent memory leaks via network request delays
        let isMounted = true;

        //pull our atm data from the backend
        async function fetchBranches(){
            try{
                const response = await apiClient.get('/branches')
                if(isMounted) setBranches(response.data)
            } catch {
                if (isMounted) setError('error in this')
            } finally {
                if (isMounted) setLoading(false)
            }
        }
        fetchBranches();
        return () => {
            isMounted = false
        }
    }, []);

    // fun spinning progress indicator if loading data
    if (loading) return <CircularProgress />

    if (error) return <Alert severity="error">{error}</Alert>

    return(
        <Box sx={{height: 400, width:'100%'}}>
            <DataGrid rows={branches} columns={columns} getRowId={(row) => row.id}/>
        </Box>

    )
}

export default BranchDataGrid;