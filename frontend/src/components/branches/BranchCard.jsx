import {Card, CardContent, Typography, Chip, Stack} from '@mui/material'


function BranchCard({branch}){


    return(
        <Card variant='outlined' sx={{minWidth: 240}}>
            <CardContent>
                <Typography variant='h6' component="div">
                    {branch.id}:  {branch.bName}
                </Typography>
                <Typography color='text.secondary' gutterBottom>
                    Branch located in: {branch.locationRegion}
                </Typography>
            </CardContent>
        </Card>
    )
};

export default BranchCard;