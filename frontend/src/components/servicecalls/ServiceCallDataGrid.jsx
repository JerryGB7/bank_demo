import {useEffect, useState} from "react"
import {DataGrid} from "@mui/x-data-grid"
import {Alert, Box, Chip, CircularProgress, Typography} from "@mui/material"
import apiClient from "../../api/client"    

// defining our data grid columns and map them to our backend API response data
const columns = [
    {field: 'id', headerName: 'ID', width: 70, type: 'number'},
    {field: 'title', headerName: 'Title', minWidth: 140, flex: 1},
    {
        field: 'priority',
        headerName: "Priority",
        width: 145,
        type: 'singleSelect',
        valueOptions: ['Low', 'Medium', 'Critical'],
        editable: true,
        renderCell: ({value}) => (
            <Chip
                label={value}
                size="small"
                color={value === 'Critical' ? 'error' : value === 'Medium' ? 'warning' : 'success'}
                variant="outlined"
            />
        ),
    },
    {
        field: 'status',
        headerName: "Call status",
        width: 145,
        type: 'singleSelect',
        valueOptions: ['Pending', 'In-Progress', 'Completed', 'Failed'],
        editable: true,
        renderCell: ({value}) => (
            <Chip
                label={value}
                size="small"
                color={value === 'Failed' ? 'error' : value === 'Completed' ? 'success' : 'info'}
                variant={value === 'In-Progress' ? 'filled' : 'outlined'}
            />
        ),
    },
    {field: 'atm_id', headerName: "ATM ID", width: 120, type: "number"},
    {field: 'technician_id', headerName: "Technician ID", width: 120, type: "number"},
];

//local state variables for tracking table rows, loading status, and network errors
// to track the lifecycle of the async API request so the UI can render appropriately

function ServiceCallDataGrid(){
    const [serviceCalls, setServiceCalls] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [updateError, setUpdateError] = useState(null)


    //react effect hood that runs our async fetch
    useEffect(() => {
        //track the component mount status to prevent memory leaks via network request delays
        let isMounted = true;

        //pull our atm data from the backend
        async function fetchServiceCalls(){
            try{
                const response = await apiClient.get('/service_calls')
                if(isMounted) setServiceCalls(response.data)
            } catch {
                if (isMounted) setError('error in this')
            } finally {
                if (isMounted) setLoading(false)
            }
        }
        fetchServiceCalls();
        return () => {
            isMounted = false
        }
    }, []);

    // using this function allows us to communicate the updated priority or status values through the matching backend endpoint.
    async function processRowUpdate(updatedRow, originalRow){
        setUpdateError(null)

        if (updatedRow.priority !== originalRow.priority){
            const response = await apiClient.patch(
                `/service_calls/${updatedRow.id}/priority`,
                null,
                {params: {new_priority: updatedRow.priority}}
            )
            return response.data
        }

        if (updatedRow.status !== originalRow.status){
            const response = await apiClient.patch(
                `/service_calls/${updatedRow.id}/status`,
                null,
                {params: {new_status: updatedRow.status}}
            )
            return response.data
        }

        return updatedRow
    }

    function handleProcessRowUpdateError(updateError){
        setUpdateError(updateError.response?.data?.detail || 'Unable to update service call')
    }

    // fun spinning progress indicator if loading data
    if (loading) {
        return (
            <Box sx={{display: 'flex', justifyContent: 'center', py: 8}}>
                <CircularProgress size={30} />
            </Box>
        )
    }

    if (error) return <Alert severity="error">{error}</Alert>

    return(
        <Box sx={{width: '100%'}}>
            {updateError && (
                <Alert severity="error" sx={{mb: 2}} onClose={() => setUpdateError(null)}>
                    {updateError}
                </Alert>
            )}
            <Box sx={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1.5}}>
                <Box>
                    <Typography variant="overline" sx={{color: 'primary.main', fontWeight: 700, letterSpacing: 1.2}}>
                        Operations queue
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Update priority or status directly from the table.
                    </Typography>
                </Box>
                <Typography variant="caption" color="text.secondary">
                    {serviceCalls.length} {serviceCalls.length === 1 ? 'call' : 'calls'}
                </Typography>
            </Box>
            <DataGrid
                rows={serviceCalls}
                columns={columns}
                getRowId={(row) => row.id}
                processRowUpdate={processRowUpdate}
                onProcessRowUpdateError={handleProcessRowUpdateError}
                disableRowSelectionOnClick
                pageSizeOptions={[5, 10, 25]}
                initialState={{
                    pagination: {paginationModel: {pageSize: 10, page: 0}},
                    sorting: {sortModel: [{field: 'id', sort: 'asc'}]},
                }}
                sx={{
                    minHeight: 390,
                    border: '1px solid',
                    borderColor: 'divider',
                    borderRadius: 2,
                    overflow: 'hidden',
                    backgroundColor: 'background.paper',
                    '& .MuiDataGrid-columnHeaders': {
                        backgroundColor: 'grey.50',
                        borderBottom: '1px solid',
                        borderColor: 'divider',
                    },
                    '& .MuiDataGrid-columnHeaderTitle': {fontWeight: 700},
                    '& .MuiDataGrid-cell': {borderColor: 'grey.100'},
                    '& .MuiDataGrid-row:hover': {backgroundColor: 'action.hover'},
                    '& .MuiDataGrid-footerContainer': {borderTop: '1px solid', borderColor: 'divider'},
                    '& .MuiDataGrid-virtualScroller': {overflowX: 'auto'},
                }}
            />
        </Box>

    )
}

export default ServiceCallDataGrid;