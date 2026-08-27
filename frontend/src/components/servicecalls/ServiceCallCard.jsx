import {Card, CardContent, Typography, Chip, Stack} from '@mui/material'


function ServiceCallCard({serviceCall}){

    const isCritical = serviceCall.priority == 'Critical'
    const isMedium = serviceCall.priority == 'Medium'

    return(
        <Card variant='outlined' sx={{minWidth: 240}}>
            <CardContent>
                <Typography variant='h6' component="div">
                    {serviceCall.id}:  {serviceCall.title}
                </Typography>
                <Typography color='text.secondary' gutterBottom>
                    ATM ID: {serviceCall.atmId}
                </Typography>
                <Stack direction="row" spacing={1} alignItems="center">
                    <Chip label={`${serviceCall.priority}`} color={isCritical ? 'error' : 'success' && isMedium ? 'warning' : 'success'}></Chip>
                    <Chip label={`${serviceCall.scStatus}`} variant='outlined' size='medium' color="primary"/>
                </Stack>
            </CardContent>
        </Card>
    )
};

export default ServiceCallCard;