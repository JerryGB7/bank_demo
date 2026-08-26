import {Card, CardContent, Typography, Chip, Stack} from '@mui/material'

const UNDER_CASH = 1
const OVER_CASH = 100
const LOW_CASH_WARNING = 20

function ATMCard({atm}){
    const cashOverUnder = atm.cashLevel < UNDER_CASH ||  atm.cashLevel > OVER_CASH
    const lowCashWarning = atm.cashLevel < LOW_CASH_WARNING && atm.cashLevel > UNDER_CASH
    const inMaintenance = atm.status == "Maintenance" || atm.status == "Offline"

    return(
        <Card variant='outlined' sx={{minWidth: 240}}>
            <CardContent>
                <Typography variant='h6' component="div">
                    {atm.serialNumber}
                </Typography>
                <Typography color='text.secondary' gutterBottom>
                   Model: '{atm.model}' ID: {atm.id}
                </Typography>
                <Stack direction="row" spacing={1} alignItems="center">
                    <Chip label={`${atm.cashLevel}%`} 
                        color={lowCashWarning ? 'warning' : 'success' && cashOverUnder ? 'error' : 'success'}>

                    </Chip>
                    <Chip label={atm.status} variant='outlined' size='medium' color={inMaintenance ? 'error' : 'success'}/>
                </Stack>
            </CardContent>
        </Card>
    )
};

export default ATMCard;