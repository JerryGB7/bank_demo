import {useEffect, useState} from "react"
import {Alert, Box, Button, Card, CardContent, CircularProgress, Stack, TextField, Typography} from "@mui/material"
import AccountTreeOutlinedIcon from "@mui/icons-material/AccountTreeOutlined"
import apiClient from "../../api/client"

function ReportingLines({supervisorId: initialSupervisorId = ""}){
	const [supervisorId, setSupervisorId] = useState(String(initialSupervisorId))
	const [selectedSupervisorId, setSelectedSupervisorId] = useState(initialSupervisorId || null)
	const [technicianCount, setTechnicianCount] = useState(null)
	const [loading, setLoading] = useState(Boolean(initialSupervisorId))
	const [error, setError] = useState(null)

	useEffect(() => {
		if (!selectedSupervisorId) return undefined

		let isMounted = true

		apiClient.get("/service_calls/reporting_lines", {params: {supervisor_id: selectedSupervisorId}})
			.then((response) => {
				if (isMounted) setTechnicianCount(response.data.technicians_with_active_calls)
			})
			.catch(() => {
				if (isMounted) setError("Unable to load reporting-line data.")
			})
			.finally(() => {
				if (isMounted) setLoading(false)
			})

		return () => {
			isMounted = false
		}
	}, [selectedSupervisorId])

	function handleSubmit(event){
		event.preventDefault()
		const parsedSupervisorId = Number(supervisorId)
		if (Number.isInteger(parsedSupervisorId) && parsedSupervisorId > 0) {
			setError(null)
			setLoading(true)
			setSelectedSupervisorId(parsedSupervisorId)
			return
		}
		setError("Enter a valid supervisor ID.")
	}

	return (
		<Card variant="outlined" sx={{borderColor: "#d7dee8", textAlign: "left"}}>
			<CardContent sx={{p: {xs: 2, sm: 3}}}>
				<Stack direction="row" spacing={1} alignItems="center" mb={0.5}>
					
					<Typography variant="h6" component="h3" fontWeight={700}>
						Reporting Lines
					</Typography>
				</Stack>
				<Typography variant="body2" color="text.secondary" mb={2}>
					Technicians reporting to a supervisor with active service calls
				</Typography>

				<Box component="form" onSubmit={handleSubmit} sx={{display: "flex", gap: 1.5, flexWrap: "wrap", mb: 2}}>
					<TextField
						label="Supervisor ID"
						value={supervisorId}
						onChange={(event) => setSupervisorId(event.target.value)}
						 type="number"
						 size="small"
						 inputProps={{min: 1}}
					/>
					<Button type="submit" variant="contained">Check</Button>
				</Box>

				{loading && <CircularProgress size={28} aria-label="Loading reporting lines" />}
				{error && <Alert severity="error">{error}</Alert>}
				{!loading && !error && technicianCount !== null && (
					<Stack direction="row" justifyContent="space-between" alignItems="center" gap={2}>
						<Typography color="text.secondary">Technicians with active calls</Typography>
						<Typography variant="h4" color="primary" fontWeight={800}>{technicianCount}</Typography>
					</Stack>
				)}
			</CardContent>
		</Card>
	)
}

export default ReportingLines
