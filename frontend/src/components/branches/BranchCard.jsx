import {Card, CardContent, Typography, Chip, Stack} from '@mui/material'


function ServiceCallCard({discrepancy}){

    const isCritical = discrepancy.priority == 'Critical'
    const isMedium = discrepancy.priority == 'Medium'

    return(
        <Card variant='outlined' sx={{minWidth: 240}}>
            <CardContent>
                <Typography variant='h6' component="div">
                    {discrepancy.id}:  {discrepancy.title}
                </Typography>
                <Typography color='text.secondary' gutterBottom>
                    ATM ID: {discrepancy.atmId}
                </Typography>
                <Stack direction="row" spacing={1} alignItems="center">
                    <Chip label={`${discrepancy.priority}`} color={isCritical ? 'error' : 'success' && isMedium ? 'warning' : 'success'}></Chip>
                    <Chip label={`${discrepancy.scStatus}`} variant='outlined' size='medium' color="primary"/>
                </Stack>
            </CardContent>
        </Card>
    )
};

export default ServiceCallCard;