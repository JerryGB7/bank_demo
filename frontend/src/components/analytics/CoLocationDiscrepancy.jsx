import {useEffect, useState} from "react"
import {Alert, Box, Card, CardContent, CircularProgress, Stack, Typography} from "@mui/material"
import apiClient from "../../api/client"

function getField(record, snakeCaseName, camelCaseName){
	return record?.[snakeCaseName] ?? record?.[camelCaseName]
}

export function countCoLocationDiscrepancies(atms = [], technicians = []){
	if (technicians.length === 0) {
		return atms.filter((atm) => (
			atm.ATM_branch_id != null &&
			atm.technician_branch_id != null &&
			atm.ATM_branch_id !== atm.technician_branch_id
		)).length
	}

	const technicianBranchById = new Map(
		technicians.map((technician) => [
			getField(technician, "id", "id"),
			getField(technician, "branch_id", "branchId"),
		]),
	)

	return atms.filter((atm) => {
		const technicianId = getField(atm, "technician_id", "technicianId")
		const atmBranchId = getField(atm, "branch_id", "branchId")
		const technicianBranchId = technicianBranchById.get(technicianId)

		return technicianId != null && technicianBranchId != null && atmBranchId !== technicianBranchId
	}).length
}

function CoLocationDiscrepancy(){
	const [discrepancies, setDiscrepancies] = useState([])
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState(null)

	useEffect(() => {
		let isMounted = true

		async function fetchDiscrepancyData(){
			try {
				const response = await apiClient.get("/atms/discrepency")
				if (isMounted) {
					setDiscrepancies(response.data)
				}
			} catch {
				if (isMounted) setError("Unable to load co-location discrepancies.")
			} finally {
				if (isMounted) setLoading(false)
			}
		}

		fetchDiscrepancyData()
		return () => {
			isMounted = false
		}
	}, [])

	if (loading) return <CircularProgress aria-label="Loading co-location discrepancies" />
	if (error) return <Alert severity="error">{error}</Alert>

	const discrepancyCount = countCoLocationDiscrepancies(discrepancies)

	return (
		<Card variant="outlined" sx={{borderColor: "#d7dee8", textAlign: "left"}}>
			<CardContent>
				<Stack direction="row" justifyContent="space-between" alignItems="center" gap={2}>
					<Box>
						<Typography variant="h6" component="h3" fontWeight={700}>
							Co-location Discrepancy
						</Typography>
						<Typography variant="body2" color="text.secondary">
							ATMs assigned to technicians based at another branch
						</Typography>
					</Box>
					<Typography variant="h4" color="warning.main" fontWeight={800}>
						{discrepancyCount}
					</Typography>
				</Stack>
			</CardContent>
		</Card>
	)
}

export default CoLocationDiscrepancy
