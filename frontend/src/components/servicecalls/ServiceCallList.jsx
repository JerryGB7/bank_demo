import {Grid} from '@mui/material'
import ServiceCallCard from './ServiceCallCard'

function ServiceCallList({discrepancies}){
    return (
        <Grid container spacing={2}>
            {discrepancies.map((discrepancy)=>
                <Grid item key={discrepancy.id}>
                    <ServiceCallCard discrepancy={discrepancy}/>
                </Grid>)}
        </Grid>
    )
};

export default ServiceCallList;