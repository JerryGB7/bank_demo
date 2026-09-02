// this section will be for grabbing the ATMS that are operating below 20 cash_level across all branches
import {useEffect, useState} from "react"
import {Alert, Box, Card, CardContent, CircularProgress, Divider, Stack, Typography} from "@mui/material"
import BuildCircleOutlinedIcon from "@mui/icons-material/BuildCircleOutlined"
import apiClient from "../../api/client"

// Define the cash percentage used to identify low-cash ATMs.
const LOW_CASH_THRESHOLD = 20

function LowCashAlert(){
	// Store ATM data, branch data, and request status.
	const [atms, setAtms] = useState([])
	const [branches, setBranches] = useState([])
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState(null)

	// Fetch low-cash ATMs and their branch information on mount.
	useEffect(() => {
		let isMounted = true

		// Load both API resources concurrently.
		async function fetchLowCashData(){
			try {
				const [atmResponse, branchResponse] = await Promise.all([
					apiClient.get(`/atms/low_cash?low_cash_threshold=${LOW_CASH_THRESHOLD}`),
					apiClient.get("/branches"),
				])
				if (isMounted) {
					setAtms(atmResponse.data)
					setBranches(branchResponse.data)
				}
			} catch {
				if (isMounted) setError("Unable to load maintenance flags.")
			} finally {
				if (isMounted) setLoading(false)
			}
		}

		fetchLowCashData()
		// Prevent state updates after the component unmounts.
		return () => {
			isMounted = false
		}
	}, [])

	// Exclude offline ATMs, attach branch names, and sort by cash level.
	const lowCash = atms
		.filter((atm) => atm.status !== "Offline")
		.map((atm) => ({
			...atm,
			branch: branches.find((branch) => branch.id === atm.branch_id),
		}))
		.sort((left, right) => left.cash_level - right.cash_level)

	if (loading) return <CircularProgress aria-label="Loading low cash flags" />
	if (error) return <Alert severity="error">{error}</Alert>

	// Render the alert card and the current low-cash ATM list.
	return (
		<Card variant="outlined" sx={{borderColor: "#d7dee8", textAlign: "left"}}>
			<CardContent sx={{p: {xs: 2, sm: 3}}}>
				<Stack direction={{xs: "column", sm: "row"}} justifyContent="space-between" gap={2} mb={2}>
					<Box>
						{/* Display the alert title and threshold description. */}
						<Stack direction="row" spacing={1} alignItems="center">
							<BuildCircleOutlinedIcon color="warning" />
							<Typography variant="h6" component="h3" fontWeight={700}>
								Low Cash Alert
							</Typography>
						</Stack>
						<Typography variant="body2" color="text.secondary" mt={0.5}>
							Branches with less than {LOW_CASH_THRESHOLD}% of active ATMs flagged for low-cash
						</Typography>
					</Box>
					{/* Show the number of flagged ATMs. */}
					<Box sx={{backgroundColor: "#fff4e5", color: "#8a4b08", px: 1.5, py: 1, borderRadius: 1, alignSelf: {xs: "flex-start", sm: "center"}}}>
								<Typography variant="subtitle2" fontWeight={700}>
									{lowCash.length} {lowCash.length === 1 ? "ATM" : "ATMs"} flagged
						</Typography>
					</Box>
				</Stack>

				{lowCash.length === 0 ? (
					// Show a success message when no active ATMs are below the threshold.
					<Alert severity="success" variant="outlined">
						No active ATMs currently operate below the {LOW_CASH_THRESHOLD}% cash reserve threshold.
					</Alert>
				) : (
					// List each flagged ATM with its branch, model, and cash level.
					<Stack divider={<Divider flexItem />}>
						{lowCash.map((atm) => (
							<Box key={atm.id} sx={{py: 1.5, display: "grid", gridTemplateColumns: {xs: "1fr", sm: "minmax(0, 1fr) auto"}, gap: 1.5, alignItems: "center"}}>
								<Box>
									<Typography fontWeight={700}>{atm.serial_number}</Typography>
									<Typography variant="body2" color="text.secondary">
										{atm.branch?.name || `Branch ${atm.branch_id}`}
									</Typography>
								</Box>
								<Stack direction="row" spacing={2} alignItems="center" justifyContent="flex-end">
									<Typography variant="body2" color="text.secondary">
										{atm.model || "ATM"}
									</Typography>
									<Typography variant="h6" color="warning.main" fontWeight={800}>
										{atm.cash_level}%
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

export default LowCashAlert