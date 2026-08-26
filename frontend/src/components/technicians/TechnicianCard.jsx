import {Card, CardContent, Typography, Chip, Stack} from '@mui/material'


function TechnicianCard({technician}){

    return(
        <Card variant='outlined' sx={{minWidth: 240}}>
            <CardContent>
                <Typography variant='h6' component="div">
                    {technician.id}:  {technician.tName}
                </Typography>
                <Typography color='text.secondary' gutterBottom>
                    ATM ID: {technician.branchId}
                </Typography>
            </CardContent>
        </Card>
    )
};

export default TechnicianCard;