import {useEffect, useState} from "react"
import {DataGrid} from "@mui/x-data-grid"
import {Alert, Box, Button, CircularProgress, Dialog, DialogActions, DialogContent, DialogTitle, MenuItem, TextField} from "@mui/material"
import apiClient from "../../api/client"
import {useAuth} from "../../context/AuthContext"

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
const emptyForm = {
    serial_number: "",
    model: "",
    status: "Operational",
    cash_level: "100",
    branch_id: "",
    technician_id: "",
}

function ATMDataGrid({onNotification}){
    const {user} = useAuth()
    const [atms, setATMS] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [createOpen, setCreateOpen] = useState(false)
    const [form, setForm] = useState(emptyForm)
    const [createError, setCreateError] = useState(null)
    const [creating, setCreating] = useState(false)

    const canCreate = user?.role === "Operation-Manager"

    function updateForm(event){
        setForm((current) => ({...current, [event.target.name]: event.target.value}))
    }

    function closeCreateDialog(){
        if (!creating) {
            setCreateOpen(false)
            setCreateError(null)
            setForm(emptyForm)
        }
    }

    async function handleCreate(event){
        event.preventDefault()
        setCreateError(null)

        const cashLevel = Number(form.cash_level)
        if (!form.serial_number || !form.model.trim() || !form.branch_id ||
            !Number.isInteger(cashLevel) || cashLevel < 0 || cashLevel > 100) {
            setCreateError("Enter a serial number, model, branch ID, and cash level from 0 to 100.")
            return
        }

        setCreating(true)
        try {
            const response = await apiClient.post("/atms", {
                serial_number: Number(form.serial_number),
                model: form.model.trim(),
                status: form.status,
                cash_level: cashLevel,
                branch_id: Number(form.branch_id),
                technician_id: form.technician_id ? Number(form.technician_id) : null,
            })
            setATMS((current) => [...current, response.data])
            closeCreateDialog()
            onNotification({severity: "success", message: "ATM created successfully."})
        } catch (requestError) {
            const detail = requestError.response?.data?.detail
            setCreateError(typeof detail === "string" ? detail : "The ATM could not be created.")
            onNotification({severity: "error", message: typeof detail === "string" ? detail : "The ATM could not be created."})
        } finally {
            setCreating(false)
        }
    }

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
        <>
        {canCreate && (
            <Button variant="contained" onClick={() => setCreateOpen(true)} sx={{mb: 2}}>
                Create ATM
            </Button>
        )}
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
        <Dialog open={createOpen} onClose={closeCreateDialog} fullWidth maxWidth="sm">
            <DialogTitle>Create ATM</DialogTitle>
            <Box component="form" onSubmit={handleCreate}>
                <DialogContent sx={{display: "grid", gap: 2}}>
                    <TextField name="serial_number" label="Serial number" type="number" value={form.serial_number} onChange={updateForm} required />
                    <TextField name="model" label="Model" value={form.model} onChange={updateForm} required />
                    <TextField name="status" label="Status" select value={form.status} onChange={updateForm}>
                        {['Operational', 'Low-Cash', 'Maintenance', 'Offline'].map((status) => <MenuItem key={status} value={status}>{status}</MenuItem>)}
                    </TextField>
                    <TextField name="cash_level" label="Cash level (%)" type="number" inputProps={{min: 0, max: 100}} value={form.cash_level} onChange={updateForm} required />
                    <TextField name="branch_id" label="Branch ID" type="number" value={form.branch_id} onChange={updateForm} required />
                    <TextField name="technician_id" label="Technician ID (optional)" type="number" value={form.technician_id} onChange={updateForm} />
                    {createError && <Alert severity="error">{createError}</Alert>}
                </DialogContent>
                <DialogActions>
                    <Button onClick={closeCreateDialog} disabled={creating}>Cancel</Button>
                    <Button type="submit" variant="contained" disabled={creating}>{creating ? "Creating..." : "Create ATM"}</Button>
                </DialogActions>
            </Box>
        </Dialog>
        </>
    )
}

export default ATMDataGrid;