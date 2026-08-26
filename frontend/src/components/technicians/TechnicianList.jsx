import {Grid} from '@mui/material'
import TechnicianCard from './TechnicianCard'

function TechniciansList({technicians}){
    return (
        <Grid container spacing={2}>
            {technicians.map((technician)=>
                <Grid item key={technician.id}>
                    <TechnicianCard technician={technician}/>
                </Grid>)}
        </Grid>
    )
};

export default TechniciansList;