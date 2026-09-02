import {useEffect, useState} from "react"
import {Alert, Box, Card, CardContent, CircularProgress, Divider, Stack, Typography} from "@mui/material"
import BuildCircleOutlinedIcon from "@mui/icons-material/BuildCircleOutlined"
import apiClient from "../../api/client"

const MAINTENANCE_THRESHOLD = 30

function MaintenanceFlags(){
	const [branches, setBranches] = useState([])
	const [atms, setAtms] = useState([])
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState(null)

	useEffect(() => {
		let isMounted = true

		async function fetchMaintenanceData(){
			try {
				const [branchResponse, atmResponse] = await Promise.all([
					apiClient.get("/branches"),
					apiClient.get("/atms"),
				])
				if (isMounted) {
					setBranches(branchResponse.data)
					setAtms(atmResponse.data)
				}
			} catch {
				if (isMounted) setError("Unable to load maintenance flags.")
			} finally {
				if (isMounted) setLoading(false)
			}
		}

		fetchMaintenanceData()
		return () => {
			isMounted = false
		}
	}, [])

	const flaggedBranches = branches.map((branch) => {
		const branchAtms = atms.filter((atm) => atm.branch_id === branch.id)
		const maintenanceCount = branchAtms.filter((atm) => atm.status === "Maintenance").length
		const percentage = branchAtms.length ? (maintenanceCount / branchAtms.length) * 100 : 0

		return {
			...branch,
			totalAtms: branchAtms.length,
			maintenanceCount,
			percentage,
		}
	}).filter((branch) => branch.percentage > MAINTENANCE_THRESHOLD)
		.sort((left, right) => right.percentage - left.percentage)

	if (loading) return <CircularProgress aria-label="Loading maintenance flags" />
	if (error) return <Alert severity="error">{error}</Alert>

	return (
		<Card variant="outlined" sx={{borderColor: "#d7dee8", textAlign: "left"}}>
			<CardContent sx={{p: {xs: 2, sm: 3}}}>
				<Stack direction={{xs: "column", sm: "row"}} justifyContent="space-between" gap={2} mb={2}>
					<Box>
						<Stack direction="row" spacing={1} alignItems="center">
							<BuildCircleOutlinedIcon color="warning" />
							<Typography variant="h6" component="h3" fontWeight={700}>
								Maintenance Flags
							</Typography>
						</Stack>
						<Typography variant="body2" color="text.secondary" mt={0.5}>
							Branches with more than {MAINTENANCE_THRESHOLD}% of active ATMs flagged for maintenance
						</Typography>
					</Box>
					<Box sx={{backgroundColor: "#fff4e5", color: "#8a4b08", px: 1.5, py: 1, borderRadius: 1, alignSelf: {xs: "flex-start", sm: "center"}}}>
						<Typography variant="subtitle2" fontWeight={700}>
							{flaggedBranches.length} {flaggedBranches.length === 1 ? "branch" : "branches"} flagged
						</Typography>
					</Box>
				</Stack>

				{flaggedBranches.length === 0 ? (
					<Alert severity="success" variant="outlined">
						No branches currently exceed the {MAINTENANCE_THRESHOLD}% maintenance threshold.
					</Alert>
				) : (
					<Stack divider={<Divider flexItem />}>
						{flaggedBranches.map((branch) => (
							<Box key={branch.id} sx={{py: 1.5, display: "grid", gridTemplateColumns: {xs: "1fr", sm: "minmax(0, 1fr) auto"}, gap: 1.5, alignItems: "center"}}>
								<Box>
									<Typography fontWeight={700}>{branch.name}</Typography>
									<Typography variant="body2" color="text.secondary">
										{branch.location_region || "Location not provided"}
									</Typography>
								</Box>
								<Stack direction="row" spacing={2} alignItems="center" justifyContent="flex-end">
									<Typography variant="body2" color="text.secondary">
										{branch.maintenanceCount} of {branch.totalAtms} ATMs
									</Typography>
									<Typography variant="h6" color="warning.main" fontWeight={800}>
										{branch.percentage.toFixed(0)}%
									</Typography>
								</Stack>
							</Box>
						))}
					</Stack>
				)}
			</CardContent>
		</Card>
	)
}

export default MaintenanceFlags
