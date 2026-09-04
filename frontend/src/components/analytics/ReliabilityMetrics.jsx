import {useEffect, useState} from "react"
import {Alert, Box, Card, CardContent, CircularProgress, Divider, Stack, Typography} from "@mui/material"
import AssessmentOutlinedIcon from "@mui/icons-material/AssessmentOutlined"
import apiClient from "../../api/client"

function ReliabilityMetrics(){
	const [metrics, setMetrics] = useState([])
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState(null)

	useEffect(() => {
		let isMounted = true

		async function fetchReliabilityMetrics(){
			try {
				const response = await apiClient.get("/service_calls/reliability_metrics")
				if (isMounted) setMetrics(response.data)
			} catch {
				if (isMounted) setError("Unable to load reliability metrics.")
			} finally {
				if (isMounted) setLoading(false)
			}
		}

		fetchReliabilityMetrics()
		return () => {
			isMounted = false
		}
	}, [])

	if (loading) return <CircularProgress aria-label="Loading reliability metrics" />
	if (error) return <Alert severity="error">{error}</Alert>

	return (
		<Card variant="outlined" sx={{borderColor: "#d7dee8", textAlign: "left"}}>
			<CardContent sx={{p: {xs: 2, sm: 3}}}>
				<Stack direction="row" spacing={1} alignItems="center" mb={0.5}>
					
					<Typography variant="h6" component="h3" fontWeight={700}>
						Reliability Metrics
					</Typography>
				</Stack>
				<Typography variant="body2" color="text.secondary" mb={2}>
					Completed and failed service calls by ATM model
				</Typography>

				{metrics.length === 0 ? (
					<Alert severity="info" variant="outlined">No completed or failed service calls are available.</Alert>
				) : (
					<Stack divider={<Divider flexItem />}>
						{metrics.map((metric) => (
							<Box key={metric.model} sx={{py: 1.5, display: "grid", gridTemplateColumns: {xs: "1fr", sm: "minmax(0, 1fr) auto"}, gap: 1.5, alignItems: "center"}}>
								<Box>
									<Typography fontWeight={700}>{metric.model}</Typography>
									<Typography variant="body2" color="text.secondary">
										{metric.total_resolved} resolved service calls
									</Typography>
								</Box>
								<Stack direction="row" spacing={{xs: 1.5, sm: 2}} justifyContent="flex-end" flexWrap="wrap">
									<Typography variant="body2" color="success.main">Completed {metric.completion_ratio.toFixed(1)}%</Typography>
									<Typography variant="body2" color="error.main">Failed {metric.failure_ratio.toFixed(1)}%</Typography>
								</Stack>
							</Box>
						))}
					</Stack>
				)}
			</CardContent>
		</Card>
	)
}

export default ReliabilityMetrics
