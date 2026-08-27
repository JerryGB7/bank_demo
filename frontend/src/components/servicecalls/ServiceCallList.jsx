import {Grid} from '@mui/material'
import ServiceCallCard from './ServiceCallCard'

function ServiceCallList({serviceCalls}){
    return (
        <Grid container spacing={2}>
            {serviceCalls.map((serviceCall)=>
                <Grid item key={serviceCall.id}>
                    <ServiceCallCard serviceCall={serviceCall}/>
                </Grid>)}
        </Grid>
    )
};

export default ServiceCallList;