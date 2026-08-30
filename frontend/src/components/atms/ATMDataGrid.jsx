import {useEffect, useState} from "react"
import {DataGrid} from "@mui/x-data-grid"
import {Alert, Box, CircularProgress} from "@mui/material"
import apiClient from "../../api/client"

// The column definitions tell the DataGrid which fields from the API response should
// appear as columns and how to label them. This is important because the backend
// returns objects like { id, serial_number, model, ... }, and the grid needs a UI
// mapping between those response fields and readable headers/column widths.
const columns = [
    {field: 'id', headerName: 'ID', width: 70},
    {field: 'serial_number', headerName: 'Serial Number', width: 150},
    {field: 'model', headerName: "Model", width: 160},
    {field: 'status', headerName: "ATM status", width: 120},
    {field: 'cash_level', headerName: "Cash Level", width: 120, type: "number"},
    {field: 'branch_id', headerName: "Branch ID", width: 120, type: "number"},
    {field: 'technician_id', headerName: "Technician ID", width: 120, type: "number"},
];

// Local component state is used to manage the table's lifecycle and UI feedback:
// - atms: stores the ATM records returned from the backend
// - loading: tracks whether the API call is still in progress
// - error: stores any failed request message so we can show a useful alert
// This pattern is important because asynchronous data fetching does not complete
// instantly, and React needs state updates to re-render the component when data arrives.
function ATMDataGrid(){
    const [atms, setATMS] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    // useEffect is used here to fetch ATM data when the component mounts.
    // This is important because the data is not available immediately, so the component
    // must request it from the backend and update its UI once the response returns.
    useEffect(() => {
        // isMounted prevents a state update after the component is unmounted.
        // This matters because a delayed API request could finish after the user navigates
        // away, which would trigger React warnings or memory leaks.
        let isMounted = true;

        // The fetchAtms function is an asynchronous request to the backend API.
        // We call /atms to retrieve all ATM records and then store them in local state.
        async function fetchAtms(){
            try{
                const response = await apiClient.get('/atms')
                // Only update state if the component is still mounted.
                // This keeps the UI consistent and avoids setting state on an unmounted component.
                if(isMounted) setATMS(response.data)
            } catch {
                // A failed request is stored in error state so the component can display
                // a visible message instead of silently failing.
                if (isMounted) setError('error showing atms')
            } finally {
                // Finally runs whether the API call succeeds or fails, so we can stop the
                // loading indicator and let the user see either the data or the error state.
                if (isMounted) setLoading(false)
            }
        }

        fetchAtms();

        // Cleanup function runs when the component unmounts.
        // This is important for preventing stale async work from continuing after the page changes.
        return () => {
            isMounted = false
        }
    }, []);

    // The loading guard ensures the user sees a spinner while the request is in flight.
    // This is important for good UX because it shows the app is actively working instead of
    // appearing blank or frozen during network latency.
    if (loading) return <CircularProgress />

    // If the request fails, we display an error alert with a clear message.
    // This is important because users need immediate feedback about problems with the backend.
    if (error) return <Alert severity="error">{error}</Alert>

    // Once the data is loaded, render the Material UI DataGrid inside a container.
    // The Box gives the grid a fixed height and full width so the table has a consistent layout.
    return(
        <Box sx={{height: 400, width:'100%'}}>
            <DataGrid
                rows={atms}
                columns={columns}
                // getRowId ensures each row has a stable unique identifier.
                // This is important because the grid needs a way to track rows across re-renders,
                // sorting, and editing operations. Using the backend id field is the most reliable option.
                getRowId={(row) => row.id}
            />
        </Box>

    )
}

export default ATMDataGrid;